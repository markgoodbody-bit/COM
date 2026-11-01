'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict'),http=require('node:http');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {createSession,playerView}=require('../bridge/session'),{createServer}=require('../bridge/server');
const E=require('../src/engine'),Save=require('../src/save');
const act=(s,verb,...args)=>s.transact('/api/action',{revision:s.state().revision,verb,args});
test('public chart with unknown owner absent; only own agents/fleets and revealed power',()=>{
 const s=createSession(),v=s.state().view;
 assert.equal(v.systems.length,8);assert.deepEqual(v.systems.find(x=>x.id==='beacon'),{id:'beacon',x:10,y:0,known:false});
 assert.equal(v.systems.find(x=>x.id==='meridian').owner,null);
 assert.deepEqual(v.agents.map(x=>x.id),['orrin','ves']);assert.equal(v.agents[1].power,null);
 assert.deepEqual(v.fleets.map(x=>x.id),['iron']);assert.equal(v.fleets[0].capacity,16);
});
test('enemy treasury, missions, events, facilities and ships do not enter view',()=>{
 const g=E.createGame();g.events.push({faction:'league',type:'SENTINEL_ENEMY'});g.factions.league.treasury=987654321;
 g.fleets.wanderer.ships[0].secret='SECRET';
 const v=JSON.stringify(playerView(g,'directorate'));
 for(const secret of ['SENTINEL_ENEMY','987654321','wanderer','SECRET'])assert.ok(!v.includes(secret));
});
test('action journey matches engine; failed action leaves exact save and revision untouched',()=>{
 const s=createSession();act(s,'board','ves','iron');act(s,'move','iron','meridian');
 const before=s.transact('/api/save',{revision:2}).save;
 assert.throws(()=>act(s,'leave','ves'),/transit/);assert.equal(s.state().revision,2);
 assert.equal(s.transact('/api/save',{revision:2}).save,before);
 act(s,'tick','2');act(s,'leave','ves');act(s,'mission','ves','diplomacy','meridian');act(s,'tick','2');
 assert.equal(s.state().view.day,4);assert.ok(s.state().view.events.some(x=>x.includes('SUCCESS')));
});
test('save/load and deterministic next action preserve exact campaign',()=>{
 const a=createSession();act(a,'board','ves','iron');act(a,'move','iron','meridian');act(a,'tick','2');
 const save=a.transact('/api/save',{revision:3}).save,b=createSession();
 b.transact('/api/load',{revision:0,save});act(a,'tick','1');act(b,'tick','1');
 assert.deepEqual(a.state().view,b.state().view);
 assert.equal(a.transact('/api/save',{revision:4}).save,b.transact('/api/save',{revision:2}).save);
});
test('invalid imports, stale revisions and malformed verbs cannot change state',()=>{
 const s=createSession(),before=s.transact('/api/save',{revision:0}).save;
 for(const body of [{revision:0,verb:'save',args:['/tmp/a']},{revision:0,verb:'tick',args:['31']},{revision:0,verb:'tick',args:['1\nmove']},{revision:0,verb:'constructor',args:[]},{revision:0,verb:'tick',args:['1'],extra:true},{revision:9,verb:'tick',args:['1']}])assert.throws(()=>s.transact('/api/action',body));
 assert.throws(()=>s.transact('/api/load',{revision:0,save:'{}'}));
 assert.equal(s.transact('/api/save',{revision:0}).save,before);
});
test('new faction replaces session deliberately; export keeps CLI save compatibility',()=>{
 const s=createSession();s.transact('/api/new',{revision:0,seed:99,faction:'league'});
 assert.equal(s.state().view.faction,'league');assert.equal(s.state().view.fleets[0].id,'wanderer');
 const d=Save.decode(s.transact('/api/save',{revision:1}).save);assert.equal(d.faction,'league');assert.equal(d.game.rng,99);
});
async function fixture(t){
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'frontier-gui-'));
 fs.writeFileSync(path.join(dir,'index.html'),'<!doctype html><title>Fixture only</title>');
 fs.writeFileSync(path.join(dir,'app.js'),'// fixture');fs.writeFileSync(path.join(dir,'style.css'),'/* fixture */');
 const app=createServer({guiRoot:dir}),url=await app.listen();
 t.after(async()=>{app.server.closeAllConnections();await new Promise(r=>app.server.close(r));fs.rmSync(dir,{recursive:true,force:true});});
 const state=await (await fetch(url+'/api/state')).json();
 const post=(route,body,headers={})=>fetch(url+route,{method:'POST',headers:{Origin:url,'Content-Type':'application/json','X-Frontier-CSRF':state.csrf,...headers},body:JSON.stringify(body)});
 return {app,url,state,post};
}
test('HTTP loopback API actual journey, export/import and state revision conflict',async t=>{
 const {app,url,state,post}=await fixture(t);assert.equal(app.server.address().address,'127.0.0.1');assert.equal(state.csrf.length,64);
 let rev=0;
 for(const [verb,args] of [['board',['ves','iron']],['move',['iron','meridian']],['tick',['2']],['leave',['ves']],['mission',['ves','diplomacy','meridian']],['tick',['2']]]){
  const r=await post('/api/action',{revision:rev,verb,args});assert.equal(r.status,200);rev=(await r.json()).revision;
 }
 const saved=await (await post('/api/save',{revision:rev})).json();assert.equal(saved.filename,'frontier-day-4.json');
 assert.equal((await post('/api/new',{revision:rev,seed:7,faction:'league'})).status,200);
 const loaded=await post('/api/load',{revision:rev+1,save:saved.save});assert.equal(loaded.status,200);assert.equal((await loaded.json()).view.day,4);
 assert.equal((await post('/api/action',{revision:0,verb:'tick',args:['1']})).status,409);
 assert.equal((await (await fetch(url+'/api/state')).json()).view.day,4);
});
test('HTTP origin, CSRF, host, fetch-site and content-type gates',async t=>{
 const {url,post}=await fixture(t),b={revision:0,verb:'tick',args:['1']};
 for(const headers of [{Origin:'https://evil.test'},{Origin:'null'},{'X-Frontier-CSRF':'wrong'},{'Content-Type':'text/plain'},{'Sec-Fetch-Site':'cross-site'}])assert.ok((await post('/api/action',b,headers)).status>=400);
 const hostCode=await new Promise(resolve=>{http.get(url+'/api/state',{headers:{Host:'evil.test'}},r=>{r.resume();resolve(r.statusCode);});});assert.equal(hostCode,403);
 assert.equal((await fetch(url+'/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)})).status,403);
 assert.equal((await (await fetch(url+'/api/state')).json()).view.day,0);
});
test('HTTP no raw save GET/file traversal/unknown routes; headers and bounded bodies',async t=>{
 const {url,post}=await fixture(t);
 for(const route of ['/api/save','/src/engine.js','/%2e%2e/README.md','/app.js?file=secret'])assert.equal((await fetch(url+route)).status,404);
 const r=await fetch(url+'/');assert.equal(r.status,200);assert.match(r.headers.get('content-security-policy'),/frame-ancestors 'none'/);assert.equal(r.headers.get('cache-control'),'no-store');
 assert.equal((await post('/api/action',{revision:0,verb:'tick',args:['1'],extra:'x'.repeat(5000)})).status,413);
 const state=await(await fetch(url+'/api/state')).json();
 const invalid=await fetch(url+'/api/action',{method:'POST',headers:{Origin:url,'Content-Type':'application/json','X-Frontier-CSRF':state.csrf},body:'{'});assert.equal(invalid.status,400);
 assert.equal((await (await fetch(url+'/api/state')).json()).revision,0);
});

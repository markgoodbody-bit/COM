'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const E=require('../src/engine'),S=require('../src/save'),{playerView}=require('../bridge/session'),UI=require('../gui/app'),{createServer}=require('../bridge/server');
function recon(seed=1){const g=E.createGame(seed);E.mission(g,'directorate','ves','recon','cinder');E.tick(g,1);return g;}
test('successful recon records a dated defence snapshot',()=>{
 const g=recon(),e=g.events.find(e=>e.type==='mission_result');
 assert.equal(e.success,true);
 assert.deepEqual(e.recon,{garrison:12,fort:1,owner:'directorate'});
});
test('failure reveals nothing and cannot overwrite an older report',()=>{
 const failed=recon(42),e=failed.events.find(e=>e.type==='mission_result');
 assert.equal(e.success,false);assert.equal(e.recon,undefined);
 assert.equal(playerView(failed,'directorate').systems.find(s=>s.id==='cinder').recon,null);
 const g=recon();const report=playerView(g,'directorate').systems.find(s=>s.id==='cinder').recon;
 g.events.push({type:'mission_result',kind:'recon',faction:'directorate',target:'cinder',day:g.day,success:false});
 assert.deepEqual(playerView(g,'directorate').systems.find(s=>s.id==='cinder').recon,report);
});
test('private snapshot survives time, ownership changes and v1 save/load without live refresh',()=>{
 const g=recon(),before=playerView(g,'directorate').systems.find(s=>s.id==='cinder').recon;
 g.systems.cinder.garrison=99;g.systems.cinder.facilities.fort=4;g.systems.cinder.owner='league';E.tick(g,2);
 const v=playerView(g,'directorate'),s=v.systems.find(s=>s.id==='cinder');
 assert.deepEqual(s.recon,before);assert.equal(s.garrison,null);
 assert.match(UI.reconText(s.recon,s.owner),/day 1.*may now be stale.*ownership differs/);
 assert.deepEqual(playerView(S.decode(S.encode(g,'directorate')).game,'directorate'),v);
 const other=playerView(g,'league');assert.ok(!other.missionHistory.some(e=>e.recon));
 assert.ok(!other.systems.some(s=>s.recon));
 const old=E.createGame();assert.equal(S.decode(S.encode(old,'directorate')).game.events.length,old.events.length);
 const legacy=recon();delete legacy.events.find(e=>e.recon).recon;
 assert.equal(playerView(S.decode(S.encode(legacy,'directorate')).game,'directorate').systems.find(s=>s.id==='cinder').recon,null);
});
test('malformed or failed-event imported snapshots are refused',()=>{
 for(const mutate of [e=>e.recon.garrison=-1,e=>e.recon.fort='secret',e=>e.success=false,e=>e.recon.queue='hidden',e=>e.day=999]){
  const g=recon();mutate(g.events.find(e=>e.recon));assert.throws(()=>S.encode(g,'directorate'),/recon snapshot/);
 }
});
test('unseen enemy changes cannot alter normal player output',()=>{
 const g=recon(),before=playerView(g,'directorate');
 g.systems.beacon.garrison=777;g.systems.beacon.facilities.fort=999;
 g.factions.league.treasury=123456;E.queueBuild(g,'league','beacon','mine');
 assert.deepEqual(playerView(g,'directorate'),before);
 assert.deepEqual(Object.keys(before.systems.find(s=>s.id==='beacon')).sort(),['id','known','x','y']);
});
test('HTTP travel, recon, dated decision, invasion and save/load; other faction gets no report',async t=>{
 const app=createServer(),url=await app.listen();
 t.after(async()=>{app.server.closeAllConnections();await new Promise(r=>app.server.close(r));});
 const api=UI.createApi(url,fetch,{Origin:url});await api.state();
 const initial=E.createGame(1);initial.systems.meridian.owner='league';initial.systems.meridian.garrison=2;initial.systems.meridian.facilities.fort=0;
 await api.load(S.encode(initial,'directorate'));
 await api.action('loadtroops',['iron','8']);await api.action('board',['ves','iron']);
 await api.action('move',['iron','meridian']);await api.action('tick',['2']);let v=(await api.action('leave',['ves'])).view;
 assert.equal(v.systems.find(s=>s.id==='meridian').recon,null);
 let attempts=0;
 while(!v.systems.find(s=>s.id==='meridian').recon&&attempts++<10){
  await api.action('mission',['ves','recon','meridian']);v=(await api.action('tick',['1'])).view;
 }
 const report=v.systems.find(s=>s.id==='meridian').recon;assert.ok(report);
 assert.equal(report.garrison,2);assert.equal(report.fort,0);
 assert.ok(v.missionHistory.some(e=>e.recon&&e.recon.day===report.day));
 assert.ok(!v.events.some(e=>e.includes('agent tama')));
 // Finite player decision: invade only after an actual low-defence report.
 assert.ok(v.fleets.find(f=>f.id==='iron').troops>report.garrison+report.fort*3);
 v=(await api.action('invade',['iron','meridian'])).view;
 assert.equal(v.systems.find(s=>s.id==='meridian').owner,'directorate');
 assert.deepEqual(v.systems.find(s=>s.id==='meridian').recon,report);
 assert.match(UI.reconText(report,'directorate'),/ownership differs/);
 const saved=await api.save();await api.newGame(9,'league');v=(await api.load(saved.save)).view;
 assert.deepEqual(v.systems.find(s=>s.id==='meridian').recon,report);
 const decoded=S.decode(saved.save);v=(await api.load(S.encode(decoded.game,'league'))).view;
 assert.ok(!v.systems.some(s=>s.recon));assert.ok(!v.missionHistory.some(e=>e.recon));
 t.diagnostic('Actual loopback HTTP decision journey: travelled, recon observed day '+report.day+', invaded, retained dated report through capture/save/load.');
});

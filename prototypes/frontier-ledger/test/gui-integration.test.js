'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const E=require('../src/engine'),C=require('../src/commands'),S=require('../src/save');
const {createServer}=require('../bridge/server'),UI=require('../gui/app');
test('production retains event identity and item kind through queue, finish and save',()=>{
 const g=E.createGame(42);C.execute(g,'directorate','build cinder troops');C.execute(g,'directorate','tick 3');
 const events=g.events.filter(e=>e.faction==='directorate');
 assert.deepEqual(events.map(e=>[e.type,e.itemType,e.day]),[['build_start','troops',0],['build_finish','troops',3]]);
 assert.match(C.execute(g,'directorate','events'),/build_start troops @cinder \(queued; cost 6\)/);
 assert.match(C.execute(g,'directorate','events'),/build_finish troops @cinder \(completed\)/);
 assert.deepEqual(S.decode(S.encode(g,'directorate')).game.events,g.events);
 assert.equal(g.systems.cinder.garrison,15);
});
test('all production types retain distinct own notices without leaking enemy orders',()=>{
 const g=E.createGame(42);g.factions.directorate.treasury=100;
 for(const item of ['troops','mine','patrol'])E.queueBuild(g,'directorate','cinder',item);
 E.queueBuild(g,'league','beacon','troops');E.tick(g,4);
 for(const item of ['troops','mine','patrol'])for(const phase of ['build_start','build_finish'])assert.ok(g.events.some(e=>e.type===phase&&e.itemType===item&&e.faction==='directorate'));
 assert.doesNotMatch(C.execute(g,'directorate','events'),/beacon/);
});
test('integrated client/HTTP displays queued and completed production; old saves still import',async t=>{
 const app=createServer(),url=await app.listen();t.after(async()=>{app.server.closeAllConnections();await new Promise(r=>app.server.close(r));});
 const api=UI.createApi(url,fetch,{Origin:url});await api.state();
 let r=await api.action('build',['cinder','troops']);assert.match(r.view.events.at(-1),/queued; cost 6/);
 r=await api.action('tick',['3']);assert.match(r.view.events.at(-1),/completed/);
 // Historical ambiguous events cannot be reconstructed; retain them as historical text.
 const g=E.createGame(42);g.events.push({day:0,type:'troops',faction:'directorate',systemId:'cinder',cost:6});
 r=await api.load(S.encode(g,'directorate'));assert.equal(r.view.events[0],'Day 0: troops @cinder');
});
test('mission limitation copy does not promise intelligence or automatic ownership',()=>{
 assert.match(UI.MISSION_LIMITS,/several successful missions/);assert.match(UI.MISSION_LIMITS,/Support totals are not displayed/);assert.match(UI.MISSION_LIMITS,/does not reveal enemy/);
});

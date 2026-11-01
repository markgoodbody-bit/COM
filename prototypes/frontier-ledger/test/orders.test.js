'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const E=require('../src/engine'),{playerView}=require('../bridge/session'),{createServer}=require('../bridge/server'),UI=require('../gui/app');
test('only own missions and production on owned worlds reach the overview',()=>{
 const g=E.createGame();E.mission(g,'league','tama','recon','beacon');E.queueBuild(g,'league','beacon','troops');
 E.mission(g,'directorate','ves','diplomacy','cinder');E.queueBuild(g,'directorate','cinder','mine');
 let v=playerView(g,'directorate');assert.equal(v.missions.length,1);assert.equal(v.missions[0].agentId,'ves');
 assert.equal(v.systems.find(s=>s.id==='cinder').production[0].type,'mine');assert.ok(!Object.hasOwn(v.systems.find(s=>s.id==='beacon'),'production'));
 const text=JSON.stringify(UI.pendingOrders(v));assert.doesNotMatch(text,/beacon|tama|troops/i);
 g.systems.cinder.owner='league';v=playerView(g,'directorate');assert.ok(!Object.hasOwn(v.systems.find(s=>s.id==='cinder'),'production'));
});
test('ETA matches actual engine travel on every starting source/destination',()=>{
 for(const source of Object.keys(E.createGame().systems))for(const dest of Object.keys(E.createGame().systems)){
  const g=E.createGame();g.fleets.iron.at=source;const v=playerView(g,'directorate'),f=v.fleets[0];
  if(source===dest){assert.equal(UI.travelDays(v,f,dest),null);continue;}
  const estimate=UI.travelDays(v,f,dest);E.moveFleet(g,'directorate','iron',dest);assert.equal(g.fleets.iron.moving.daysLeft,estimate);
 }
});
test('pending rows select their actual subjects and count down to disappearance',()=>{
 const g=E.createGame();E.boardAgent(g,'directorate','ves','iron');E.moveFleet(g,'directorate','iron','meridian');E.queueBuild(g,'directorate','cinder','troops');
 let rows=UI.pendingOrders(playerView(g,'directorate'));assert.equal(rows.length,2);assert.equal(rows[0].days,2);assert.deepEqual(rows[0].selection,{fleet:'iron'});
 E.tick(g,1);rows=UI.pendingOrders(playerView(g,'directorate'));assert.equal(rows[0].days,1);assert.match(rows[0].label,/due day 2/);
 E.tick(g,2);assert.deepEqual(UI.pendingOrders(playerView(g,'directorate')),[]);
});
test('HTTP human loop: select action, see pending order, advance, see completion',async t=>{
 const app=createServer(),url=await app.listen();t.after(async()=>{app.server.closeAllConnections();await new Promise(r=>app.server.close(r));});
 const api=UI.createApi(url,fetch,{Origin:url});let v=(await api.state()).view;
 const order=UI.actionsFor(v,{system:'cinder'}).find(a=>a.verb==='build'&&a.args[1]==='troops');assert.equal(order.enabled,true);
 v=(await api.action(order.verb,order.args)).view;assert.equal(UI.pendingOrders(v)[0].days,3);assert.match(v.events.at(-1),/queued/);
 v=(await api.action('tick',['3'])).view;assert.equal(UI.pendingOrders(v).filter(o=>o.selection.system==='cinder').length,0);assert.match(v.events.at(-1),/completed/);
 assert.equal(v.systems.find(s=>s.id==='cinder').garrison,15);
});

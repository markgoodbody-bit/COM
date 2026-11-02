'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const E=require('../src/engine'),C=require('../src/commands'),AI=require('../src/ai'),S=require('../src/save'),{playerView}=require('../bridge/session'),UI=require('../gui/app'),{createServer}=require('../bridge/server');
function contact(){const g=E.createGame(1);E.boardAgent(g,'league','tama','wanderer');E.moveFleet(g,'directorate','iron','beacon');E.tick(g,4);return g;}
test('legal travel permits deliberate battle with real hull loss and intact survivors',()=>{
 const g=contact();assert.equal(typeof E.engage,'function');
 E.engage(g,'directorate','iron','wanderer');
 assert.equal(g.fleets.wanderer,undefined);assert.equal(g.agents.tama.at,'beacon');assert.equal(g.agents.tama.fleet,null);
 assert.equal(g.systems.beacon.garrison,16);S.validateGame(g);
});
test('ordinary legal loss at home permits paid replacement, save/replay and reuse',()=>{
 const g=contact();E.engage(g,'directorate','iron','wanderer');
 const money=g.factions.league.treasury;
 assert.equal(AI.orderFaction(g,'league').item,'patrol');
 assert.equal(g.factions.league.treasury,money-14);
 const job=g.systems.beacon.production.find(j=>j.type==='patrol');
 const copy=S.decode(S.encode(g,'league')).game;
 for(const state of [g,copy]){
  E.tick(state,4);
  assert.ok(state.fleets['fleet-'+job.id]);
  assert.equal(AI.orderFaction(state,'league').order,'BOARD');
  assert.equal(state.agents.tama.fleet,'fleet-'+job.id);
  assert.equal(AI.orderFaction(state,'league').order,'MOVE');
  S.validateGame(state);
 }
 assert.deepEqual(copy,g);
});
test('refused attacks leave state and RNG unchanged, contacts need physical fleet presence',()=>{
 const g=E.createGame(1),before=JSON.stringify(g);
 for(const [a,b] of [['iron','wanderer'],['iron','iron'],['wanderer','iron'],['iron','missing']]){
  assert.throws(()=>E.engage(g,'directorate',a,b));assert.equal(JSON.stringify(g),before);
 }
 assert.deepEqual(playerView(g,'directorate').contacts,[]);
 g.systems.beacon.garrison=999;g.fleets.wanderer.ships[0].power=99;
 assert.deepEqual(playerView(g,'directorate').contacts,[]);
});
test('losing agents strand at battle world; nonfriendly troops explicitly disband',()=>{
 // Search a fixed bounded seed range using only initial state and legal travel.
 let g;
 for(let seed=1;seed<=100;seed++){
  const trial=E.createGame(seed);E.boardAgent(trial,'directorate','ves','iron');
  E.moveFleet(trial,'directorate','iron','beacon');E.tick(trial,4);
  E.engage(trial,'directorate','iron','wanderer');
  if(!trial.fleets.iron){g=trial;break;}
 }
 assert.ok(g);assert.equal(g.agents.ves.at,'beacon');assert.equal(g.agents.ves.fleet,null);
 const e=g.events.find(e=>e.type==='fleet_encounter'&&e.faction==='directorate');
 assert.equal(e.troopDisposition,'disbanded');assert.equal(e.troops,6);
 assert.equal(g.systems.beacon.garrison,12);S.validateGame(g);
 assert.ok(C.execute(g,'directorate','events').includes('troops disbanded: 6'));
});
test('normal-seed HTTP mouse action can encounter and destroy an AI hull',async t=>{
 const app=createServer(),url=await app.listen();t.after(async()=>{app.server.closeAllConnections();await new Promise(r=>app.server.close(r));});
 const api=UI.createApi(url,fetch,{Origin:url});await api.state();await api.newGame(1,'directorate');
 await api.action('move',['iron','farpoint']);
 let v=(await api.action('tick',['3'])).view;
 const action=UI.actionsFor(v,{fleet:'iron',system:'farpoint'}).find(a=>a.verb==='engage');
 assert.ok(action&&action.enabled);assert.match(action.label,/loser loses ALL hulls/);
 assert.ok(v.contacts.some(e=>e.id==='wanderer'));
 v=(await api.action(action.verb,action.args)).view;
 assert.ok(v.events.some(e=>e.includes('wanderer lost 1 hull')));
 assert.ok(!v.contacts.some(e=>e.id==='wanderer'));
 const saved=await api.save(),g=S.decode(saved.save).game;S.validateGame(g);
 assert.equal(g.fleets.wanderer,undefined);
 
 // Normal HTTP advancement retains the actual opponent policy.
 v=(await api.action('tick',['3'])).view;
 const after=S.decode((await api.save()).save).game;
 assert.ok(after.systems.beacon.production.some(j=>j.type==='patrol')||Object.values(after.fleets).some(f=>f.faction==='league'));
 assert.ok(after.events.some(e=>e.type==='build_start'&&e.faction==='league'&&e.itemType==='patrol'));
 t.diagnostic('Normal seed1: move Iron to Farpoint; day3 visible contact; GUI action destroys Wanderer. AI legally queues replacement at Beacon. Remote pickup remains unresolved.');
});

test('guessed remote fleet IDs cannot disclose existence through refusal text',()=>{
 const g=E.createGame(1);
 const message=id=>{try{E.engage(g,'directorate','iron',id);}catch(e){return e.message;}};
 assert.equal(message('wanderer'),message('not-real'));
});

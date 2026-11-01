'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const E=require('../src/engine'),AI=require('../src/ai'),S=require('../src/save');
function stranded(){const g=E.createGame(1);delete g.fleets.iron;g.systems.cinder.facilities.mine=3;return g;}
test('lost transport gets one paid patrol, then boards and moves the diplomat',()=>{
 const g=stranded(),money=g.factions.directorate.treasury;
 const o=AI.orderFaction(g,'directorate');assert.equal(o.order,'BUILD');assert.equal(o.item,'patrol');
 assert.equal(g.factions.directorate.treasury,money-14);
 const id=g.systems.cinder.production[0].id,queued=JSON.stringify(g);
 AI.orderFaction(g,'directorate');assert.equal(JSON.stringify(g),queued);
 E.tick(g,3);assert.equal(g.fleets['fleet-'+id],undefined);
 E.tick(g,1);assert.equal(g.fleets['fleet-'+id].ships.length,1);
 assert.equal(AI.orderFaction(g,'directorate').order,'BOARD');
 assert.equal(g.agents.ves.fleet,'fleet-'+id);
 assert.equal(AI.orderFaction(g,'directorate').order,'MOVE');
 assert.ok(g.fleets['fleet-'+id].moving);
});
test('existing mobile passenger hull prevents replacement even in transit or occupied',()=>{
 for(const mode of ['ready','moving','occupied']){
  const g=E.createGame(1);g.systems.cinder.facilities.mine=3;
  if(mode==='moving'){E.boardAgent(g,'directorate','ves','iron');E.moveFleet(g,'directorate','iron','meridian');}
  if(mode==='occupied')E.boardAgent(g,'directorate','orrin','iron');
  AI.orderFaction(g,'directorate');
  assert.ok(!Object.values(g.systems).some(s=>s.production.some(j=>j.type==='patrol')));
 }
});
test('unaffordable, no yard or inherited queue cannot mutate otherwise idle state',()=>{
 for(const mode of ['money','yard','inherited','queued']){
  const g=stranded();
  if(mode==='money')g.factions.directorate.treasury=13;
  if(mode==='yard')g.systems.cinder.facilities.yard=0;
  if(mode==='inherited')g.systems.cinder.production.push({id:g.nextId++,faction:'league',type:'mine',remaining:3});
  if(mode==='queued')g.systems.beacon.production.push({id:g.nextId++,faction:'directorate',type:'patrol',remaining:4});
  const before=JSON.stringify(g);AI.orderFaction(g,'directorate');assert.equal(JSON.stringify(g),before,mode);
 }
});
test('replacement uses own state, ignores enemy fleets and money, and selects empty own yard',()=>{
 const a=stranded(),b=structuredClone(a);delete b.fleets.wanderer;b.factions.league.treasury=0;b.systems.beacon.facilities.yard=9;
 assert.deepEqual(AI.orderFaction(a,'directorate'),AI.orderFaction(b,'directorate'));
 assert.equal(a.systems.cinder.production.length,1);
});
test('legal diplomacy takes priority over replacement and queued save resumes exactly',()=>{
 const g=stranded();g.agents.ves.at='meridian';
 assert.equal(AI.orderFaction(g,'directorate').order,'DIPLOMACY');assert.equal(g.systems.cinder.production.length,0);
 const h=stranded();AI.orderFaction(h,'directorate');const copy=S.decode(S.encode(h,'directorate')).game;
 const a=AI.runCampaign(h,10,['directorate']),b=AI.runCampaign(copy,10,['directorate']);
 assert.deepEqual(a,b);assert.equal(JSON.stringify(h),JSON.stringify(copy));
 const types=new Set(['board','depart','disembark','mission_start','embark_troops','invasion','build_start']);
 for(let d=0;d<10;d++)assert.ok(h.events.filter(e=>e.faction==='directorate'&&e.day===d&&types.has(e.type)).length<=1);
});
test('zero passenger capacity is not a usable carrier; diplomat yard preferred over home',()=>{
 const g=E.createGame();g.fleets.iron.ships.forEach(h=>h.agentSlots=0);g.systems.meridian.owner='directorate';
 g.systems.meridian.facilities.yard=1;g.agents.ves.at='meridian';g.systems.cinder.facilities.mine=3;
 const o=AI.orderFaction(g,'directorate');assert.equal(o.item,'patrol');assert.equal(o.system,'meridian');
});

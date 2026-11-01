"use strict";
const test=require("node:test"), assert=require("node:assert/strict");
const E=require("../src/engine.js"), AI=require("../src/ai.js"), S=require("../src/save.js");
test("both original factions board their own ships",()=>{
 const g=E.createGame(11),d=AI.runAIDay(g);
 assert.equal(d.orders.length,2);assert.equal(d.orders[0].order,"BOARD");assert.equal(d.orders[1].order,"BOARD");
 assert.equal(g.agents.ves.fleet,"iron");assert.equal(g.agents.tama.fleet,"wanderer");assert.equal(g.day,1);
});
test("AI ship transit takes time before disembarkation",()=>{
 const g=E.createGame(11);AI.runAIDay(g);
 const d=AI.runAIDay(g);assert.equal(d.orders[0].order,"MOVE");assert.equal(d.orders[1].order,"MOVE");
 assert.equal(g.fleets.wanderer.at,"farpoint");assert.equal(g.fleets.iron.at,null);
 const p=AI.runAIDay(g);assert.equal(p.orders[0].order,"IN_TRANSIT");assert.equal(p.orders[1].order,"DISEMBARK");
 assert.equal(g.agents.tama.at,"farpoint");
});
test("target selection does not inspect hidden opponent ownership",()=>{
 const g=E.createGame(11);g.factions.league.known=["beacon"];g.systems.spire.owner="directorate";
 const a=AI.chooseTarget(g,"league","beacon");g.systems.spire.owner="league";
 assert.equal(a,AI.chooseTarget(g,"league","beacon"));
});
test("missions actually start where diplomat arrived",()=>{
 const g=E.createGame(21);AI.runCampaign(g,5);
 assert.ok(g.events.some(x=>x.type==="mission_start"&&x.kind==="diplomacy"));
 assert.ok(g.events.filter(x=>x.type==="mission_start").every(x=>g.agents[x.agentId].faction===x.faction));
});
test("both sides independently acquire new planets",()=>{
 const g=E.createGame(18);const days=AI.runCampaign(g,60);
 assert.ok(days.length<=60&&days.length>0);
 const claims=g.events.filter(e=>e.type==="acquire");
 assert.ok(claims.some(x=>x.faction==="league"));assert.ok(claims.some(x=>x.faction==="directorate"));
});
test("AI does not conjure troops or garrisons",()=>{
 const g=E.createGame(18);
 const count=()=>Object.values(g.fleets).reduce((n,f)=>n+f.troops,0)+
 Object.values(g.systems).reduce((n,s)=>n+s.garrison,0);
 const before=count();AI.runCampaign(g,10);assert.equal(count(),before);
});
test("same seed and orders yield same world and event log",()=>{
 const run=()=>{const g=E.createGame(7);AI.runCampaign(g,35);return JSON.stringify(g)};
 assert.equal(run(),run());
});
test("game over ends orders and ticks",()=>{
 const g=E.createGame();g.winner="league";const before=JSON.stringify(g);
 const d=AI.runAIDay(g);assert.equal(d.orders.length,0);assert.equal(JSON.stringify(g),before);
});
test("invalid faction list rejected without any effects",()=>{
 const g=E.createGame(),before=JSON.stringify(g);
 assert.throws(()=>AI.runAIDay(g,["league","invalid"]),/Unknown AI faction/);
 assert.throws(()=>AI.runAIDay(g,["league","league"]),/unique list/);
 assert.equal(JSON.stringify(g),before);
});
test("bounded campaign rejects invalid day budgets",()=>{
 const g=E.createGame();assert.throws(()=>AI.runCampaign(g,0),/1..365/);
 assert.throws(()=>AI.runCampaign(g,366),/1..365/);assert.equal(g.day,0);
});
test("no local ship is a transparent no-op",()=>{
 const g=E.createGame();g.fleets.wanderer.at="meridian";const before=JSON.stringify(g);
 const action=AI.orderFaction(g,"league");
 assert.equal(action.order,"NO_LOCAL_CARRIER");assert.equal(JSON.stringify(g),before);
});
// Meridian is on the Directorate's starting known list; here the League holds it. Ves rides aboard iron.
function warGame(){const g=E.createGame(5);g.systems.meridian.owner="league";E.boardAgent(g,"directorate","ves","iron");return g;}
const days=(g,n)=>{const o=[];for(let i=0;i<n;i++)o.push(AI.runAIDay(g,["directorate"]).orders[0]);return o;};
test("military loads at a friendly dock, advances and invades a visited enemy world",()=>{
 const g=warGame(),o=days(g,4);
 assert.deepEqual(o.map(x=>x.order),["LOAD_TROOPS","ADVANCE","IN_TRANSIT","INVADE"]);
 assert.equal(o[0].count,8);assert.equal(g.systems.cinder.garrison,4);
 assert.equal(o[3].troops,14);assert.equal(g.fleets.iron.troops,0);assert.equal(g.systems.meridian.owner,"directorate");
});
test("an under-strength fleet at its target goes back for troops first",()=>{
 const g=warGame();g.fleets.iron.at="meridian";
 const o=AI.orderFaction(g,"directorate");
 assert.equal(o.order,"RETURN_TO_DOCK");assert.equal(o.target,"cinder");assert.equal(g.systems.meridian.owner,"league");
});
test("a diplomat on the ground keeps its carrier while expansion has somewhere to go",()=>{
 const g=E.createGame(5);g.systems.meridian.owner="league";
 assert.equal(AI.orderFaction(g,"directorate").order,"BOARD");
 assert.equal(g.fleets.iron.troops,6);assert.equal(g.systems.cinder.garrison,12);
});
test("no visited enemy world, or no troops to send, leaves the diplomatic order",()=>{
 const fog=E.createGame(5);fog.systems.spire.owner="league";E.boardAgent(fog,"directorate","ves","iron");
 assert.equal(AI.orderFaction(fog,"directorate").order,"MOVE");assert.equal(fog.fleets.iron.troops,6);
 const dry=warGame();dry.fleets.iron.troops=0;dry.systems.cinder.garrison=4;
 assert.equal(AI.orderFaction(dry,"directorate").order,"MOVE");
 assert.equal(dry.fleets.iron.troops,0);assert.equal(dry.systems.cinder.garrison,4);assert.equal(dry.systems.meridian.owner,"league");
});
test("military orders ignore fogged ownership and hidden enemy strength",()=>{
 const seen=hide=>{const g=warGame();
   if(hide){g.systems.meridian.garrison=40;g.systems.meridian.facilities.fort=5;
     for(const id of ["spire","hollow","haven"])g.systems[id].owner="league";
     g.fleets.wanderer.at="farpoint";g.fleets.wanderer.troops=10;}
   return days(g,4);};
 assert.deepEqual(seen(true),seen(false));
});
test("only one fleet acts per faction per day",()=>{
 const g=warGame();g.fleets.spare={...structuredClone(g.fleets.iron),id:"spare",agents:[]};
 const spare=JSON.stringify(g.fleets.spare),events=g.events.length;
 assert.equal(AI.orderFaction(g,"directorate").fleet,"iron");
 assert.equal(JSON.stringify(g.fleets.spare),spare);assert.equal(g.events.length,events+1);
});
test("a campaign saved mid-attack resumes it identically",()=>{
 const g=warGame();days(g,2);assert.equal(g.fleets.iron.moving.destination,"meridian");
 const copy=S.decode(S.encode(g,"league")).game;
 const a=days(g,2),b=days(copy,2);
 assert.deepEqual(b,a);assert.deepEqual(a.map(x=>x.order),["IN_TRANSIT","INVADE"]);
 assert.equal(JSON.stringify(copy),JSON.stringify(g));
});
test("AI campaigns invade with legal orders, never add troops and replay exactly",()=>{
 const total=g=>Object.values(g.fleets).reduce((n,f)=>n+f.troops,0)+Object.values(g.systems).reduce((n,s)=>n+s.garrison,0);
 let invasions=0;
 for(let seed=0;seed<20;seed++){const g=E.createGame(seed);
   for(let d=0;d<120&&!g.winner;d++){const before=total(g);AI.runAIDay(g);assert.ok(total(g)<=before);}
   invasions+=g.events.filter(e=>e.type==="invasion").length;}
 assert.ok(invasions>0);
 const run=()=>{const g=E.createGame(3);AI.runCampaign(g,120);return JSON.stringify(g)};
 assert.equal(run(),run());
});

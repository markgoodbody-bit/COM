"use strict";
const test=require("node:test"), assert=require("node:assert/strict");
const E=require("../src/engine.js"), AI=require("../src/ai.js");
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

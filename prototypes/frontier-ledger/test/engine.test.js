"use strict";
const test=require("node:test");
const assert=require("node:assert/strict");
const E=require("../src/engine.js");

test("two original factions and distinct extraordinary paths",()=>{
  const g=E.createGame();
  assert.equal(E.FACTIONS.directorate.power,"cybernetic");
  assert.equal(E.FACTIONS.league.power,"psionic");
  assert.equal(g.factions.directorate.home,"cinder");
  assert.equal(g.factions.league.home,"beacon");
});
test("ships carry agents and physical travel consumes days",()=>{
  const g=E.createGame();
  E.boardAgent(g,"directorate","ves","iron");
  E.moveFleet(g,"directorate","iron","meridian");
  assert.equal(g.agents.ves.at,null);
  assert.throws(()=>E.disembarkAgent(g,"directorate","ves"),/transit/);
  E.tick(g,1); assert.equal(g.fleets.iron.at,null);
  E.tick(g,1); assert.equal(g.fleets.iron.at,"meridian");
  E.disembarkAgent(g,"directorate","ves");
  assert.equal(g.agents.ves.at,"meridian");
});
test("can't use enemy ship or remote teleport",()=>{
  const g=E.createGame();
  assert.throws(()=>E.boardAgent(g,"directorate","ves","wanderer"),/not controlled/);
  assert.throws(()=>E.mission(g,"directorate","ves","diplomacy","meridian"),/target world/);
});
test("missions cannot be started while agent aboard",()=>{
  const g=E.createGame();
  E.boardAgent(g,"directorate","ves","iron");
  assert.throws(()=>E.mission(g,"directorate","ves","diplomacy","cinder"),/not aboard/);
});
test("agent mission improves political support and can win a neutral system",()=>{
  const g=E.createGame(1);
  E.boardAgent(g,"directorate","ves","iron");
  E.moveFleet(g,"directorate","iron","meridian");
  E.tick(g,2); E.disembarkAgent(g,"directorate","ves");
  const before=g.systems.meridian.support.directorate;
  E.mission(g,"directorate","ves","diplomacy","meridian");
  E.tick(g,2);
  const result=g.events.find(e=>e.type==="mission_result");
  assert.equal(result.success,true);
  assert.equal(g.systems.meridian.support.directorate,before+25);
  assert.equal(g.systems.meridian.owner,null);
  E.mission(g,"directorate","ves","diplomacy","meridian");
  E.tick(g,2);
  assert.equal(g.systems.meridian.owner,"directorate");
});
test("a failed landing consumes committed troops without taking a base",()=>{
  const g=E.createGame();
  const f=g.fleets.iron;
  f.at="beacon";
  f.troops=2;
  const outcome=E.invade(g,"directorate","iron","beacon");
  assert.equal(outcome.success,false);
  assert.equal(g.winner,null);
  assert.equal(f.troops,0);
});
test("home base capture is victory but conquest is not loyalty",()=>{
  const g=E.createGame();
  g.fleets.iron.at="beacon";g.fleets.iron.troops=30;
  const outcome=E.invade(g,"directorate","iron","beacon");
  assert.equal(outcome.success,true);
  assert.equal(g.winner,"directorate");
  assert.equal(g.systems.beacon.support.directorate,45);
});
test("builds cost treasury and finish on their clock",()=>{
  const g=E.createGame();
  const before=g.factions.directorate.treasury;
  E.queueBuild(g,"directorate","cinder","patrol");
  assert.equal(g.factions.directorate.treasury,before-14);
  E.tick(g,3);assert.equal(g.fleets["fleet-1"],undefined);
  E.tick(g,1);assert.equal(g.fleets["fleet-1"].at,"cinder");
});
test("discover special potential locally without revealing everyone",()=>{
  const g=E.createGame();
  assert.equal(E.view(g,"directorate").agents.find(a=>a.id==="ves").power,null);
  E.discoverPower(g,"directorate","orrin","ves");
  assert.equal(E.view(g,"directorate").agents.find(a=>a.id==="ves").power.kind,"cybernetic");
  assert.throws(()=>E.discoverPower(g,"directorate","orrin","lyn"),/not controlled/);
});
test("fog conceals unfamiliar systems",()=>{
  const g=E.createGame();
  assert.equal(E.view(g,"directorate").systems.beacon,undefined);
  assert.equal(E.view(g,"league").systems.cinder,undefined);
});
test("same seeds and orders reproduce byte-identical outcomes",()=>{
  function run(){
    const g=E.createGame(18);
    E.boardAgent(g,"league","tama","wanderer");
    E.moveFleet(g,"league","wanderer","farpoint");
    E.tick(g,1); E.disembarkAgent(g,"league","tama");
    E.mission(g,"league","tama","diplomacy","farpoint");
    E.tick(g,2);
    return JSON.stringify(g);
  }
  assert.equal(run(),run());
});
test("invalid commands do not silently mutate state",()=>{
  const g=E.createGame();
  const snapshot=JSON.stringify(g);
  assert.throws(()=>E.queueBuild(g,"league","cinder","patrol"),/control/);
  assert.throws(()=>E.moveFleet(g,"league","wanderer","beacon"),/Already/);
  assert.equal(JSON.stringify(g),snapshot);
});

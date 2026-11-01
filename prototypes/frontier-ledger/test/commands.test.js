"use strict";
const test=require("node:test"), assert=require("node:assert/strict");
const E=require("../src/engine.js"), C=require("../src/commands.js"), S=require("../src/save.js");
test("human can read a constrained faction view",()=>{
 const g=E.createGame();
 assert.match(C.execute(g,"directorate","status"),/Aster Directorate/);
 assert.doesNotMatch(C.execute(g,"directorate","map"),/beacon/);
 assert.match(C.execute(g,"directorate","agents"),/ves/);
 assert.doesNotMatch(C.execute(g,"directorate","fleets"),/wanderer/);
});
test("human can board, move, unload an agent and start a mission",()=>{
 const g=E.createGame(1);
 C.execute(g,"directorate","board ves iron");
 C.execute(g,"directorate","move iron meridian");
 C.execute(g,"directorate","tick 2");
 C.execute(g,"directorate","leave ves");
 C.execute(g,"directorate","mission ves diplomacy meridian");
 assert.equal(g.agents.ves.busy,true);
 assert.equal(g.day,2);
});
test("human day advancement runs only the other faction AI",()=>{
 const g=E.createGame(1);
 C.execute(g,"directorate","tick 1");
 assert.equal(g.day,1);
 assert.equal(g.agents.tama.fleet,"wanderer");
 assert.equal(g.agents.ves.fleet,null);
});
test("explicit mission and troop commands refuse bad arguments atomically",()=>{
 const g=E.createGame(),before=JSON.stringify(g);
 assert.throws(()=>C.execute(g,"directorate","loadtroops iron 0"),/1..100000/);
 assert.throws(()=>C.execute(g,"directorate","mission ves diplomacy"),/requires/);
 assert.throws(()=>C.execute(g,"league","board ves wanderer"),/not controlled/);
 assert.equal(JSON.stringify(g),before);
});
test("defended home does not leak into limited map",()=>{
 const g=E.createGame();
 assert.equal(C.execute(g,"directorate","map").includes("beacon"),false);
});
test("gameover blocks any new action",()=>{
 const g=E.createGame();g.winner="directorate";const before=JSON.stringify(g);
 assert.throws(()=>C.execute(g,"league","tick 1"),/over/);
 assert.equal(JSON.stringify(g),before);
});
test("campaign round-trip retains RNG and in-flight ships, agents and missions",()=>{
 const g=E.createGame(29);
 C.execute(g,"directorate","board ves iron");
 C.execute(g,"directorate","move iron meridian");
 C.execute(g,"directorate","tick 1");
 const text=S.encode(g,"directorate"),out=S.decode(text);
 assert.equal(out.faction,"directorate");
 assert.deepEqual(out.game,g);
 assert.equal(S.encode(out.game,out.faction),text);
});
test("round-trip remains identical after mission and production are queued",()=>{
 const g=E.createGame();
 C.execute(g,"directorate","build cinder patrol");
 C.execute(g,"directorate","mission orrin recon cinder");
 const out=S.decode(S.encode(g,"directorate"));
 assert.deepEqual(out.game,g);
});
test("corrupted save must not be accepted",()=>{
 const g=E.createGame();
 const raw=S.encode(g,"directorate");
 const changed=raw.replace('"day":0','"day":3');
 assert.throws(()=>S.decode(changed),/checksum mismatch/);
});
test("unknown save version and wrong player faction are refused",()=>{
 const g=E.createGame();
 const envelope=JSON.parse(S.encode(g,"directorate"));
 envelope.payload.version=99;
 assert.throws(()=>S.decode(JSON.stringify(envelope)),/version/);
 assert.throws(()=>S.encode(g,"imaginary"),/faction/);
});
test("adversarial checksum-correct broken ship state is rejected",()=>{
 const g=E.createGame();
 g.agents.ves.at=null;g.agents.ves.fleet="unknown";
 assert.throws(()=>S.encode(g,"directorate"),/agent carrier/);
});
test("unsafe object keys in the state are refused",()=>{
 const g=E.createGame();
 g.events.push(JSON.parse('{"__proto__":{"bad":"yes"}}'));
 assert.throws(()=>S.encode(g,"directorate"),/unsafe key/);
});
test("saved state cannot invent troop capacity",()=>{
 const g=E.createGame();
 g.fleets.iron.troops=100;
 assert.throws(()=>S.encode(g,"directorate"),/fleet capacity/);
});
test("advancing 31 days is rejected before any change",()=>{
 const g=E.createGame(),before=JSON.stringify(g);
 assert.throws(()=>C.execute(g,"directorate","tick 31"),/1..30/);
 assert.equal(JSON.stringify(g),before);
});

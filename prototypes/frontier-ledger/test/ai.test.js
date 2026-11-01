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
 // Ves is still aboard while Iron travels; the Directorate spends that waiting day on a mine.
 const p=AI.runAIDay(g);assert.equal(p.orders[0].order,"BUILD");assert.equal(p.orders[0].item,"mine");
 assert.equal(g.agents.ves.fleet,"iron");assert.equal(p.orders[1].order,"DISEMBARK");
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
 // With nothing affordable, the waiting day cannot become a build either.
 const g=E.createGame();g.fleets.wanderer.at="meridian";g.factions.league.treasury=0;const before=JSON.stringify(g);
 const action=AI.orderFaction(g,"league");
 assert.equal(action.order,"NO_LOCAL_CARRIER");assert.equal(JSON.stringify(g),before);
});
// Meridian is on the Directorate's starting known list; here the League holds it. Ves rides aboard iron.
function warGame(){const g=E.createGame(5);g.systems.meridian.owner="league";E.boardAgent(g,"directorate","ves","iron");return g;}
const days=(g,n)=>{const o=[];for(let i=0;i<n;i++)o.push(AI.runAIDay(g,["directorate"]).orders[0]);return o;};
test("military loads at a friendly dock, advances and invades a visited enemy world",()=>{
 const g=warGame(),o=days(g,4);
 // The transit day now buys a mine; Cinder sits at the 4-troop floor, so it is not refilled above it.
 assert.deepEqual(o.map(x=>x.order),["LOAD_TROOPS","ADVANCE","BUILD","INVADE"]);
 assert.deepEqual([o[2].system,o[2].item],["cinder","mine"]);
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
 assert.deepEqual(b,a);assert.deepEqual(a.map(x=>x.order),["BUILD","INVADE"]);
 assert.equal(JSON.stringify(copy),JSON.stringify(g));
});
test("AI campaigns invade with legal orders, add troops only by paid builds, act once a day and replay exactly",()=>{
 const total=g=>Object.values(g.fleets).reduce((n,f)=>n+f.troops,0)+Object.values(g.systems).reduce((n,s)=>n+s.garrison,0);
 // Event types an AI order records on its own day; arrivals, results and completions come from the tick.
 const ORDER_EVENTS=new Set(["board","depart","disembark","mission_start","embark_troops","invasion","build_start"]);
 let invasions=0,builds=0;
 for(let seed=0;seed<20;seed++){const g=E.createGame(seed);
   for(let d=0;d<120&&!g.winner;d++){
    const before=total(g),day=g.day,from=g.events.length;AI.runAIDay(g);
    const fresh=g.events.slice(from),made=fresh.filter(e=>e.type==="build_finish"&&e.itemType==="troops").length;
    assert.ok(total(g)<=before+3*made,`seed ${seed} day ${day}: troops rose without a finished troop build`);
    for(const f of ["directorate","league"])
     assert.ok(fresh.filter(e=>e.day===day&&e.faction===f&&ORDER_EVENTS.has(e.type)).length<=1,`seed ${seed} day ${day}: ${f} acted twice`);
   }
   invasions+=g.events.filter(e=>e.type==="invasion").length;builds+=g.events.filter(e=>e.type==="build_start").length;}
 assert.ok(invasions>0&&builds>0,`invasions ${invasions}, builds ${builds}`);
 const run=()=>{const g=E.createGame(3);AI.runCampaign(g,120);return JSON.stringify(g)};
 assert.equal(run(),run());
});
// Ves on a mission makes the Directorate's diplomacy wait, and nothing hostile is known: an idle day.
function idleGame(){const g=E.createGame(42);E.mission(g,"directorate","ves","diplomacy","cinder");return g;}
test("an idle day reinforces a garrison below the 4-troop floor at the engine's price",()=>{
 const g=idleGame();g.systems.cinder.garrison=1;
 assert.deepEqual(AI.orderFaction(g,"directorate"),{faction:"directorate",order:"BUILD",system:"cinder",item:"troops"});
 assert.equal(g.factions.directorate.treasury,29);
 assert.deepEqual(g.systems.cinder.production.map(j=>j.type),["troops"]);
});
test("nothing is bought that cannot be paid for, and a refusal leaves no trace",()=>{
 const g=idleGame();g.systems.cinder.garrison=1;g.factions.directorate.treasury=5;const before=JSON.stringify(g);
 assert.equal(AI.orderFaction(g,"directorate").order,"MISSION_IN_PROGRESS");assert.equal(JSON.stringify(g),before);
});
test("one queued job per world, and mines stop at the cap",()=>{
 const g=idleGame();
 assert.deepEqual([AI.orderFaction(g,"directorate").item,g.systems.cinder.facilities.mine],["mine",2]);
 const queued=JSON.stringify(g);
 assert.equal(AI.orderFaction(g,"directorate").order,"MISSION_IN_PROGRESS");assert.equal(JSON.stringify(g),queued);
 const capped=idleGame();capped.systems.cinder.facilities.mine=3;const before=JSON.stringify(capped);
 assert.equal(AI.orderFaction(capped,"directorate").order,"MISSION_IN_PROGRESS");assert.equal(JSON.stringify(capped),before);
});
test("a world joined by diplomacy with no garrison gets troops, and the floor is never exceeded by choice",()=>{
 // 6 troops: above the floor, below the starting 12. Nothing is bought.
 const full=idleGame();full.systems.cinder.facilities.mine=3;full.systems.cinder.garrison=6;const before=JSON.stringify(full);
 assert.equal(AI.orderFaction(full,"directorate").order,"MISSION_IN_PROGRESS");assert.equal(JSON.stringify(full),before);
 const g=idleGame();g.systems.cinder.facilities.mine=3;g.systems.meridian.owner="directorate";
 assert.deepEqual([AI.orderFaction(g,"directorate").system,g.systems.meridian.production[0].type],["meridian","troops"]);
});
test("produced forces appear when the job is due",()=>{
 const g=idleGame();g.systems.cinder.garrison=1;AI.orderFaction(g,"directorate");
 E.tick(g,2);assert.equal(g.systems.cinder.garrison,1);
 E.tick(g,1);assert.equal(g.systems.cinder.garrison,4);
 assert.ok(g.events.some(e=>e.type==="build_finish"&&e.systemId==="cinder"&&e.itemType==="troops"));
});
test("production ignores the enemy's money, queues and hidden worlds",()=>{
 const play=hide=>{const g=E.createGame(42);
  if(hide){g.factions.league.treasury=987654;g.systems.beacon.production.push({id:900,faction:"league",type:"patrol",remaining:4});
   g.systems.spire.owner="league";g.systems.spire.garrison=40;}
  const o=[];for(let i=0;i<30;i++)o.push(AI.runAIDay(g,["directorate"]).orders[0]);return o;};
 const seen=play(false);
 assert.ok(seen.some(o=>o.order==="BUILD"));assert.deepEqual(play(true),seen);
});
test("a game saved with production queued replays identically",()=>{
 const g=idleGame();g.systems.cinder.garrison=1;AI.orderFaction(g,"directorate");
 const copy=S.decode(S.encode(g,"directorate")).game;
 const a=AI.runCampaign(g,12),b=AI.runCampaign(copy,12);
 assert.deepEqual(b,a);assert.equal(JSON.stringify(copy),JSON.stringify(g));
});
test("a captured world with a former-owner job cannot receive a second AI job",()=>{
 const g=idleGame();
 g.systems.cinder.facilities.mine=3;
 E.queueBuild(g,"league","beacon","troops");
 const inherited=JSON.parse(JSON.stringify(g.systems.beacon.production[0]));
 g.systems.beacon.owner="directorate";g.systems.beacon.garrison=0;
 const before=JSON.stringify(g);
 assert.equal(AI.orderFaction(g,"directorate").order,"MISSION_IN_PROGRESS");
 assert.equal(JSON.stringify(g),before);
 assert.deepEqual(g.systems.beacon.production,[inherited]);
 E.tick(g,3);
 assert.equal(g.systems.beacon.owner,"directorate");
 assert.equal(g.systems.beacon.garrison,3);
 assert.equal(g.systems.beacon.production.length,0);
 const event=g.events.find(e=>e.type==="build_finish"&&e.systemId==="beacon");
 assert.equal(event.faction,"league");
 assert.equal(event.itemType,"troops");
});

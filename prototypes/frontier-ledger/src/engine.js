"use strict";

/* Frontier Ledger: original headless space strategy simulation.
   No dependency on commercial game files, code, art, names or balance tables.
   One tick = one game-day; all state and probabilities are explicit. */

const FACTIONS = Object.freeze({
  directorate: { name: "Aster Directorate", power: "cybernetic" },
  league: { name: "Horizon League", power: "psionic" },
});

const SITES = [
  ["cinder", 0, 0, "directorate", 80, 12, 2, 1, 1],
  ["beacon", 10, 0, "league", 80, 12, 1, 1, 1],
  ["meridian", 4, 2, null, 45, 0, 1, 0, 0],
  ["farpoint", 7, 2, null, 45, 0, 1, 0, 0],
  ["gloam", 2, 6, null, 45, 0, 1, 0, 0],
  ["spire", 8, 6, null, 45, 0, 1, 0, 0],
  ["hollow", 5, 9, null, 45, 0, 1, 0, 0],
  ["haven", 0, 9, null, 45, 0, 1, 0, 0],
];

function insist(condition, message) {
  if (!condition) throw new Error(message);
}
function opposite(faction) {
  return faction === "directorate" ? "league" : "directorate";
}
function record(g, type, data) {
  const event = { ...data, day: g.day, type }; // reserved identity cannot be overwritten by payload
  g.events.push(event);
  return event;
}
function die(g) {
  // Stable reproducible unsigned LCG. This is our own balancing mechanism.
  g.rng = (Math.imul(g.rng, 1664525) + 1013904223) >>> 0;
  return g.rng % 100;
}
function createGame(seed = 42) {
  insist(Number.isSafeInteger(seed) && seed >= 0, "Seed must be a nonnegative integer");
  const systems = {};
  for (const [id, x, y, owner, support, garrison, mine, yard, fort] of SITES) {
    systems[id] = {
      id, x, y, owner, garrison,
      support: { directorate: owner === "directorate" ? support : 25,
                 league: owner === "league" ? support : 25 },
      facilities: { mine, yard, fort },
      production: [],
    };
  }
  const g = {
    day: 0, rng: seed >>> 0, winner: null, systems,
    factions: {
      directorate: { treasury: 35, home: "cinder", known: ["cinder", "meridian"] },
      league: { treasury: 25, home: "beacon", known: ["beacon", "farpoint"] },
    },
    agents: {
      orrin: { id:"orrin", faction:"directorate", at:"cinder", fleet:null,
        mentor:true, skills:{ diplomacy:2, espionage:2, command:6 },
        power:{ kind:"cybernetic", latent:false, level:1, revealed:true }, busy:false },
      ves: { id:"ves", faction:"directorate", at:"cinder", fleet:null,
        mentor:false, skills:{ diplomacy:6, espionage:4, command:2 },
        power:{ kind:"cybernetic", latent:true, level:0, revealed:false }, busy:false },
      lyn: { id:"lyn", faction:"league", at:"beacon", fleet:null,
        mentor:true, skills:{ diplomacy:5, espionage:5, command:3 },
        power:{ kind:"psionic", latent:false, level:1, revealed:true }, busy:false },
      tama: { id:"tama", faction:"league", at:"beacon", fleet:null,
        mentor:false, skills:{ diplomacy:7, espionage:3, command:3 },
        power:{ kind:"psionic", latent:true, level:0, revealed:false }, busy:false },
    },
    fleets: {
      iron: { id:"iron", faction:"directorate", at:"cinder", moving:null,
        ships:[{id:"iron-1", speed:3, troops:16, agentSlots:2, power:5}],
        troops:6, agents:[] },
      wanderer: { id:"wanderer", faction:"league", at:"beacon", moving:null,
        ships:[{id:"wanderer-1", speed:4, troops:10, agentSlots:2, power:3}],
        troops:4, agents:[] },
    },
    missions: [], events: [], nextId:1,
  };
  return g;
}
function getAgent(g, id, faction) {
  const a = g.agents[id];
  insist(a && a.faction === faction, "Agent not controlled by faction");
  return a;
}
function getFleet(g, id, faction) {
  const f = g.fleets[id];
  insist(f && f.faction === faction, "Fleet not controlled by faction");
  return f;
}
function getSite(g, id) {
  const s = g.systems[id];
  insist(s, "Unknown system");
  return s;
}
function boardAgent(g, faction, agentId, fleetId) {
  const a = getAgent(g, agentId, faction);
  const f = getFleet(g, fleetId, faction);
  insist(!a.busy && !a.fleet && a.at && !f.moving && f.at === a.at,
    "Boarding requires free agent and docked fleet at same system");
  insist(f.agents.length < f.ships.reduce((n, s) => n + s.agentSlots, 0),
    "No free passenger berths");
  a.at = null; a.fleet = f.id; f.agents.push(a.id);
  return record(g, "board", { faction, agentId, fleetId });
}
function disembarkAgent(g, faction, agentId) {
  const a = getAgent(g, agentId, faction);
  insist(a.fleet, "Agent is not aboard a fleet");
  const f = getFleet(g, a.fleet, faction);
  insist(!f.moving && f.at, "Cannot disembark during transit");
  f.agents.splice(f.agents.indexOf(agentId), 1);
  a.fleet = null; a.at = f.at;
  return record(g, "disembark", { faction, agentId, systemId:a.at });
}
function moveFleet(g, faction, fleetId, destination) {
  const f = getFleet(g, fleetId, faction);
  insist(!f.moving && f.at, "Fleet already in transit");
  const a = getSite(g, f.at), b = getSite(g, destination);
  insist(a.id !== b.id, "Already at destination");
  // Without these, Math.min() of no ships is Infinity (a one-day jump anywhere)
  // and a zero speed gives an arrival that never comes.
  insist(f.ships.length > 0, "Fleet has no ships to move");
  insist(f.ships.every(s => Number.isFinite(s.speed) && s.speed > 0),
    "Every ship needs a positive speed");
  const speed = Math.min(...f.ships.map(s => s.speed));
  const days = Math.max(1, Math.ceil(Math.hypot(b.x-a.x,b.y-a.y)/speed));
  f.moving = { destination, daysLeft:days };
  f.at = null;
  return record(g, "depart", { faction, fleetId, destination, eta:g.day+days });
}
// Deliberate local encounter. All losing hulls are lost; agents escape to the
// same world. Troops land at a friendly world or disband (explicitly recorded).
function engage(g,faction,fleetId,targetId) {
  insist(!g.winner,"Campaign is over");
  const a=getFleet(g,fleetId,faction),b=g.fleets[targetId];
  insist(b&&b.faction!==faction&&a.at&&a.at===b.at&&!a.moving&&!b.moving,
    "No hostile contact at this system");
  for(const v of [a,b]){
    insist(v.ships.length>0&&v.ships.every(h=>Number.isSafeInteger(h.power)&&h.power>=0),"Invalid combat hulls");
    insist(v.agents.every(id=>g.agents[id]&&g.agents[id].fleet===v.id&&!g.agents[id].busy),"Invalid passenger state");
  }
  const site=getSite(g,a.at);
  const power=v=>v.ships.reduce((n,h)=>n+h.power,0);
  const ap=power(a),bp=power(b),ar=die(g),br=die(g);
  const loser=ap*20+ar>bp*20+br?b:a; // ties favour defender
  const loss=loser.ships.length,passengers=[...loser.agents],troops=loser.troops;
  const landed=site.owner===loser.faction;
  for(const id of passengers){g.agents[id].fleet=null;g.agents[id].at=site.id;}
  if(landed)site.garrison+=troops;
  delete g.fleets[loser.id];
  let own;
  for(const v of [a,b]){
    const e=record(g,"fleet_encounter",{faction:v.faction,systemId:site.id,
      attacker:a.id,defender:b.id,lostFleet:loser.id,lostHulls:loss,
      attackPower:ap,defencePower:bp,attackRoll:ar,defenceRoll:br,
      outcome:v===loser?"lost":"won",
      ...(v===loser?{survivors:passengers,troops,troopDisposition:landed?"landed":"disbanded"}:{})});
    if(v.faction===faction)own=e;
  }
  return own;
}
function troopCapacity(f) {
  return f.ships.reduce((n, s) => n + s.troops, 0);
}
function dockedAtFriendly(g, faction, fleetId) {
  const f = getFleet(g, fleetId, faction);
  insist(!f.moving && f.at, "Cannot transfer troops during transit");
  const s = getSite(g, f.at);
  insist(s.owner === faction, "Troops transfer only at a friendly system");
  return [f, s];
}
// Every check runs before any change, so a refused transfer creates or loses no troops.
function embarkTroops(g, faction, fleetId, count) {
  insist(Number.isInteger(count) && count >= 1, "Troop count must be a positive integer");
  const [f, s] = dockedAtFriendly(g, faction, fleetId);
  insist(s.garrison >= count, "Not enough garrison troops to embark");
  insist(f.troops + count <= troopCapacity(f), "Exceeds the fleet's troop capacity");
  s.garrison -= count;
  f.troops += count;
  return record(g, "embark_troops", { faction, fleetId, systemId:s.id, count });
}
function disembarkTroops(g, faction, fleetId, count) {
  insist(Number.isInteger(count) && count >= 1, "Troop count must be a positive integer");
  const [f, s] = dockedAtFriendly(g, faction, fleetId);
  insist(f.troops >= count, "Not enough troops aboard");
  f.troops -= count;
  s.garrison += count;
  return record(g, "disembark_troops", { faction, fleetId, systemId:s.id, count });
}
function discoverPower(g, faction, mentorId, candidateId) {
  const mentor=getAgent(g, mentorId, faction), candidate=getAgent(g, candidateId, faction);
  insist(mentor.mentor && mentor.at && mentor.at === candidate.at &&
         !mentor.busy && !candidate.busy && !candidate.fleet,
    "Mentor and candidate must be free and physically colocated");
  insist(candidate.power.kind === FACTIONS[faction].power, "Incompatible potential");
  insist(candidate.power.latent && !candidate.power.revealed, "No undiscovered potential");
  candidate.power.revealed = true;
  candidate.power.level = 1;
  return record(g, "awakening", { faction, candidateId, kind:candidate.power.kind });
}
function mission(g, faction, agentId, kind, target) {
  insist(kind === "diplomacy" || kind === "recon" || kind === "sabotage",
    "Unknown mission kind");
  const a=getAgent(g,agentId,faction), s=getSite(g,target);
  insist(!a.busy && !a.fleet && a.at === s.id,
    "Agent must be free on target world (not aboard a ship)");
  if (kind==="sabotage") insist(s.owner && s.owner !== faction, "No hostile facility to sabotage");
  a.busy=true;
  const m={id:g.nextId++,faction,agentId,kind,target,daysLeft:kind==="recon"?1:2};
  g.missions.push(m);
  record(g, "mission_start", { ...m });
  return m.id;
}
function resolution(g, m) {
  const a=g.agents[m.agentId],s=g.systems[m.target],skill=
    m.kind==="diplomacy"?a.skills.diplomacy:a.skills.espionage;
  const bonus=a.power.revealed?a.power.level*6:0;
  const resistance=m.kind==="sabotage"?s.facilities.fort*12:0;
  const chance=Math.max(5,Math.min(95,20+skill*9+bonus-resistance));
  const roll=die(g),success=roll<chance;
  if(success) {
    if(m.kind==="diplomacy") {
      s.support[m.faction]=Math.min(100,s.support[m.faction]+25);
      if(!s.owner && s.support[m.faction]>=65) {
        s.owner=m.faction;
        record(g, "acquire", { faction:m.faction, systemId:s.id, method:"diplomacy" });
      }
    } else if(m.kind==="recon") {
      const known=g.factions[m.faction].known;
      if(!known.includes(s.id)) known.push(s.id);
    } else if(m.kind==="sabotage" && s.facilities.mine>0) {
      s.facilities.mine--;
    }
  }
  a.busy=false;
  record(g,"mission_result",{id:m.id,kind:m.kind,faction:m.faction,target:m.target,
    chance,roll,success,...(success&&m.kind==="recon"?{recon:{garrison:s.garrison,fort:s.facilities.fort,owner:s.owner}}:{})});
}
function queueBuild(g,faction,systemId,type) {
  const s=getSite(g,systemId);
  insist(s.owner===faction,"Must control system to build");
  insist(type==="patrol"||type==="troops"||type==="mine","Unknown build");
  insist(type!=="patrol"||s.facilities.yard>0,"Patrol requires shipyard");
  const cost=type==="patrol"?14:type==="troops"?6:10;
  const wallet=g.factions[faction];
  insist(wallet.treasury>=cost,"Insufficient treasury");
  wallet.treasury-=cost;
  const item={id:g.nextId++,faction,type,remaining:type==="patrol"?4:3};
  s.production.push(item);
  record(g,"build_start",{faction,systemId,itemType:type,cost});
  return item.id;
}
function finishBuild(g,s,item) {
  if(item.type==="mine") s.facilities.mine++;
  else if(item.type==="troops") s.garrison+=3;
  else {
    const id="fleet-"+item.id;
    g.fleets[id]={id,faction:item.faction,at:s.id,moving:null,
      ships:[{id:"hull-"+item.id,speed:4,troops:5,agentSlots:1,power:2}],
      troops:0,agents:[]};
  }
  record(g,"build_finish",{systemId:s.id,faction:item.faction,itemType:item.type});
}
function invade(g,faction,fleetId,systemId,commanderId=null) {
  const f=getFleet(g,fleetId,faction),s=getSite(g,systemId);
  const defender=s.owner;
  insist(!f.moving && f.at===s.id,"Fleet must be present to invade");
  insist(s.owner!==faction,"Already owned");
  insist(f.troops>0,"No landing force");
  let leader=0;
  if(commanderId!==null) {
    const a=getAgent(g,commanderId,faction);
    insist(a.fleet===f.id,"Commander must be aboard invasion fleet");
    leader=a.skills.command;
  }
  const assault=f.troops*3+leader;
  const defence=s.garrison*2+s.facilities.fort*5;
  const success=assault>defence;
  f.troops=0; // landing force committed, successful or not
  if(success) {
    s.owner=faction;
    s.garrison=Math.max(1,Math.floor((assault-defence)/3));
    s.support[faction]=45; // conquest is not popular approval
    const enemy=opposite(faction);
    if(s.id===g.factions[enemy].home) g.winner=faction;
  }
  // Notify the owner at the time of attack, even if ownership has just changed.
  // This separate audience record carries no attacking fleet or strength data.
  if(defender!==null)record(g,"defence_notice",{faction:defender,systemId,
    outcome:success?"WORLD_LOST":"ATTACK_REPELLED"});
  return record(g,"invasion",{faction,fleetId,systemId,assault,defence,success});
}
function tick(g,days=1) {
  insist(Number.isInteger(days)&&days>=1&&days<=365,"Ticks must be 1..365");
  for(let i=0;i<days;i++) {
    if(g.winner) break;
    g.day++;
    for(const f of Object.values(g.fleets)) if(f.moving) {
      f.moving.daysLeft--;
      if(f.moving.daysLeft===0) {
        const at=f.moving.destination;
        f.at=at; f.moving=null;
        const known=g.factions[f.faction].known;
        if(!known.includes(at)) known.push(at);
        record(g,"arrival",{faction:f.faction,fleetId:f.id,systemId:at});
      }
    }
    for(const s of Object.values(g.systems)) {
      if(s.owner) g.factions[s.owner].treasury+=s.facilities.mine;
      const finished=[];
      for(const job of s.production) {
        job.remaining--;
        if(job.remaining<=0) finished.push(job);
      }
      s.production=s.production.filter(j=>j.remaining>0);
      for(const item of finished) finishBuild(g,s,item);
    }
    const completed=[];
    for(const m of g.missions) {
      m.daysLeft--;
      if(m.daysLeft<=0) completed.push(m);
    }
    g.missions=g.missions.filter(m=>m.daysLeft>0);
    for(const m of completed) resolution(g,m);
  }
  return g;
}
function view(g,faction) {
  insist(FACTIONS[faction],"Unknown faction");
  const known=new Set(g.factions[faction].known);
  return {
    day:g.day, victory:g.winner,
    treasury:g.factions[faction].treasury,
    systems:Object.fromEntries(Object.entries(g.systems)
      .filter(([id,s])=>known.has(id)||s.owner===faction)
      .map(([id,s])=>[id,{id,x:s.x,y:s.y,owner:s.owner,
        garrison:s.owner===faction?s.garrison:null,
        facilities:s.owner===faction?{...s.facilities}:null}])),
    agents:Object.values(g.agents).filter(a=>a.faction===faction).map(a=>({
      id:a.id,at:a.at,fleet:a.fleet,busy:a.busy,skills:{...a.skills},
      power:a.power.revealed?{kind:a.power.kind,level:a.power.level}:null,
    })),
  };
}
module.exports={engage,FACTIONS,createGame,boardAgent,disembarkAgent,moveFleet,
  embarkTroops,disembarkTroops,discoverPower,mission,queueBuild,invade,tick,view};

"use strict";
/* Frontier Ledger: original deterministic opponent policy.
 * Chart coordinates are public; owner/support only observed on visited systems.
 * Military: load troops at a friendly dock, advance on a visited enemy world, invade.
 * One order per faction per day. No networking, model calls or schedulers.
 */
const E=require("./engine.js");
const DEFAULT_FACTIONS=Object.freeze(["directorate","league"]);
function factionData(g,f) {
  if(!Object.prototype.hasOwnProperty.call(E.FACTIONS,f)) throw Error("Unknown AI faction");
  return g.factions[f];
}
function dist(a,b){return Math.hypot(a.x-b.x,a.y-b.y);}
function chooseDiplomat(g,f) {
  factionData(g,f);
  return Object.values(g.agents).filter(a=>a.faction===f)
    .sort((a,b)=>b.skills.diplomacy-a.skills.diplomacy||a.id.localeCompare(b.id))[0]||null;
}
function chooseTarget(g,f,origin) {
  const known=new Set(factionData(g,f).known),at=g.systems[origin];
  if(!at) return null;
  const neutrals=Object.values(g.systems).filter(s=>known.has(s.id)&&s.owner===null);
  // Never inspect owner on unknown worlds. Only public chart positions.
  const available=neutrals.length?neutrals:Object.values(g.systems).filter(s=>!known.has(s.id));
  available.sort((a,b)=>dist(at,a)-dist(at,b)||a.id.localeCompare(b.id));
  return available[0]?.id||null;
}
function chooseCarrier(g,f,at) {
  return Object.values(g.fleets).filter(v=>
    v.faction===f&&v.at===at&&!v.moving&&v.ships.length>0&&
    v.agents.length<v.ships.reduce((n,s)=>n+s.agentSlots,0))
    .sort((a,b)=>a.id.localeCompare(b.id))[0]||null;
}
// Troops the policy leaves in any friendly garrison it loads from.
const RESERVE=4;
function capacity(v){return v.ships.reduce((n,s)=>n+s.troops,0);}
function hostileTargets(g,f,origin) {
  // Owner is read only on systems this faction has visited; enemy garrisons, forts and fleets are never read.
  const known=new Set(factionData(g,f).known),at=g.systems[origin];
  return Object.values(g.systems).filter(s=>known.has(s.id)&&s.owner!==null&&s.owner!==f)
    .sort((a,b)=>dist(at,a)-dist(at,b)||a.id.localeCompare(b.id));
}
function reloadDocks(g,f,origin) {
  const at=g.systems[origin];
  return Object.values(g.systems).filter(s=>s.owner===f&&s.id!==origin&&s.garrison>RESERVE)
    .sort((a,b)=>dist(at,a)-dist(at,b)||a.id.localeCompare(b.id));
}
function fleetOrder(g,f,v) {
  const targets=hostileTargets(g,f,v.at);
  if(!targets.length)return null;
  const here=g.systems[v.at],room=capacity(v)-v.troops;
  if(here.owner===f) {
    const count=Math.min(room,here.garrison-RESERVE);
    if(count>=1) {
      E.embarkTroops(g,f,v.id,count);
      return {faction:f,order:"LOAD_TROOPS",fleet:v.id,at:here.id,count};
    }
  }
  // Enemy strength is hidden, so a fleet attacks only when full or when no friendly dock can add troops.
  const docks=room>0?reloadDocks(g,f,v.at):[];
  if(v.troops>0&&!docks.length) {
    const troops=v.troops;
    if(targets[0].id===here.id) {
      // No commander: the engine turns a commander's skill into extra garrison on an undefended world.
      E.invade(g,f,v.id,here.id);
      return {faction:f,order:"INVADE",fleet:v.id,target:here.id,troops};
    }
    E.moveFleet(g,f,v.id,targets[0].id);
    return {faction:f,order:"ADVANCE",fleet:v.id,target:targets[0].id,troops};
  }
  if(!docks.length)return null;
  E.moveFleet(g,f,v.id,docks[0].id);
  return {faction:f,order:"RETURN_TO_DOCK",fleet:v.id,target:docks[0].id};
}
function militaryOrder(g,f,diplomat) {
  // A fleet stays with a diplomat on the ground beside it while expansion still has somewhere to go,
  // so the diplomat is never stranded; a diplomat aboard rides along.
  const held=diplomat&&diplomat.at&&chooseTarget(g,f,diplomat.at)!==null?diplomat.at:null;
  const fleets=Object.values(g.fleets).filter(v=>
    v.faction===f&&!v.moving&&v.at&&v.ships.length>0&&v.at!==held)
    .sort((a,b)=>a.id.localeCompare(b.id));
  for(const v of fleets){const o=fleetOrder(g,f,v);if(o)return o;}
  return null;
}
// Economy: every own world is kept at the military's RESERVE floor, never refilled above it, and gets
// mines up to a cap. A first version refilled home to 12; that re-armed the military without end and its
// reload trips kept the diplomat's ship, cutting diplomatic acquisitions from 119 to 40 (20 seeds, 60 days).
// Costs, times and legality stay the engine's.
const MINE_CAP=3;
// Diplomacy orders that change the game; any other diplomacy result is a waiting day.
const DIPLOMACY_ACTS=new Set(["DISEMBARK","MOVE","DIPLOMACY","BOARD"]);
// A mobile hull with passenger capacity counts even when travelling or occupied:
// temporary unavailability must not trigger ship proliferation.
function replacementCarrier(g,f) {
  const own=Object.values(g.fleets).filter(v=>v.faction===f);
  if(own.some(v=>v.ships.length>0&&v.ships.every(h=>h.speed>0)&&
      v.ships.reduce((n,h)=>n+h.agentSlots,0)>0))return null;
  const worlds=Object.values(g.systems);
  // Own prepaid patrols remain ours under existing engine semantics, even after a capture.
  if(worlds.some(s=>s.production.some(j=>j.faction===f&&j.type==="patrol")))return null;
  if(factionData(g,f).treasury<14)return null;
  const diplomat=chooseDiplomat(g,f),home=factionData(g,f).home;
  const yards=worlds.filter(s=>s.owner===f&&s.facilities.yard>0&&s.production.length===0)
    .sort((a,b)=>(b.id===diplomat?.at)-(a.id===diplomat?.at)||
      (b.id===home)-(a.id===home)||a.id.localeCompare(b.id));
  if(!yards.length)return null;
  E.queueBuild(g,f,yards[0].id,"patrol");
  return {faction:f,order:"BUILD",system:yards[0].id,item:"patrol"};
}
function economyOrder(g,f) {
  // Own worlds only: owner, garrison, mines and all queued jobs on those worlds. One queued job per world at a time.
  const home=factionData(g,f).home;
  const worlds=Object.values(g.systems).filter(s=>s.owner===f&&s.production.length===0)
    .sort((a,b)=>(b.id===home)-(a.id===home)||a.garrison-b.garrison||a.id.localeCompare(b.id));
  const wants=[];
  for(const s of worlds)if(s.garrison<RESERVE)wants.push([s.id,"troops"]);
  for(const s of worlds.slice().sort((a,b)=>a.facilities.mine-b.facilities.mine||a.id.localeCompare(b.id)))
    if(s.facilities.mine<MINE_CAP)wants.push([s.id,"mine"]);
  for(const [system,item] of wants){
    // queueBuild checks owner, item, shipyard and treasury before any change, so a refusal leaves no trace.
    try{E.queueBuild(g,f,system,item);}catch{continue;}
    return {faction:f,order:"BUILD",system,item};
  }
  return null;
}
function orderFaction(g,f) {
  factionData(g,f);
  if(g.winner) return {faction:f,order:"GAME_OVER"};
  const a=chooseDiplomat(g,f);
  const war=militaryOrder(g,f,a);
  if(war)return war;
  // Production only takes a day that diplomacy would otherwise spend waiting.
  const talk=diplomacyOrder(g,f,a);
  if(DIPLOMACY_ACTS.has(talk.order))return talk;
  return replacementCarrier(g,f)||economyOrder(g,f)||talk;
}
function diplomacyOrder(g,f,a) {
  if(!a)return {faction:f,order:"NO_AGENT"};
  if(a.busy)return {faction:f,order:"MISSION_IN_PROGRESS",agent:a.id};
  if(a.fleet) {
    const ship=g.fleets[a.fleet];
    if(!ship||ship.faction!==f)return {faction:f,order:"CARRIER_UNAVAILABLE",agent:a.id};
    if(ship.moving)return {faction:f,order:"IN_TRANSIT",agent:a.id};
    if(!ship.at)return {faction:f,order:"CARRIER_LOCATION_UNKNOWN",agent:a.id};
    const known=g.factions[f].known.includes(ship.at);
    if(known&&g.systems[ship.at].owner===null){
      E.disembarkAgent(g,f,a.id);
      return {faction:f,order:"DISEMBARK",agent:a.id,at:ship.at};
    }
    const target=chooseTarget(g,f,ship.at);
    if(target&&target!==ship.at){
      E.moveFleet(g,f,ship.id,target);
      return {faction:f,order:"MOVE",agent:a.id,fleet:ship.id,target};
    }
    E.disembarkAgent(g,f,a.id);
    return {faction:f,order:"DISEMBARK",agent:a.id,at:ship.at};
  }
  if(!a.at)return {faction:f,order:"AGENT_LOCATION_UNKNOWN",agent:a.id};
  const site=g.systems[a.at],known=g.factions[f].known.includes(a.at);
  if(!site)return {faction:f,order:"AGENT_SITE_UNKNOWN",agent:a.id};
  if(known&&site.owner===null) {
    E.mission(g,f,a.id,"diplomacy",a.at);
    return {faction:f,order:"DIPLOMACY",agent:a.id,at:a.at};
  }
  const target=chooseTarget(g,f,a.at);
  if(!target)return {faction:f,order:"NO_UNCLAIMED_DESTINATION"};
  const ship=chooseCarrier(g,f,a.at);
  if(!ship)return {faction:f,order:"NO_LOCAL_CARRIER",agent:a.id,at:a.at};
  E.boardAgent(g,f,a.id,ship.id);
  return {faction:f,order:"BOARD",agent:a.id,fleet:ship.id,target};
}
function runAIDay(g,factions=DEFAULT_FACTIONS) {
  if(!Array.isArray(factions)||new Set(factions).size!==factions.length||
    factions.some(f=>typeof f!=="string"))throw Error("AI factions must be a unique list");
  factions.forEach(f=>factionData(g,f));
  if(g.winner)return {day:g.day,orders:[],winner:g.winner};
  const orders=factions.map(f=>orderFaction(g,f));
  E.tick(g,1);
  return {day:g.day,orders,winner:g.winner};
}
function runCampaign(g,days=20,factions=DEFAULT_FACTIONS) {
  if(!Number.isSafeInteger(days)||days<1||days>365)throw Error("Campaign days must be 1..365");
  const history=[];
  for(let i=0;i<days&&!g.winner;i++)history.push(runAIDay(g,factions));
  return history;
}
module.exports={chooseDiplomat,chooseTarget,orderFaction,runAIDay,runCampaign};

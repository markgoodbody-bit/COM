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
function orderFaction(g,f) {
  factionData(g,f);
  if(g.winner) return {faction:f,order:"GAME_OVER"};
  const a=chooseDiplomat(g,f);
  const war=militaryOrder(g,f,a);
  if(war)return war;
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

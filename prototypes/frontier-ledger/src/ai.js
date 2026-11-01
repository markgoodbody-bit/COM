"use strict";
/* Frontier Ledger: original deterministic opponent policy.
 * Chart coordinates are public; owner/support only observed on visited systems.
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
function orderFaction(g,f) {
  factionData(g,f);
  if(g.winner) return {faction:f,order:"GAME_OVER"};
  const a=chooseDiplomat(g,f);
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

"use strict";
// Frontier Ledger save v1: JSON with accidental-corruption detection (NOT authentication).
const E=require("./engine.js");
const FORMAT="frontier-ledger",VERSION=1,MAX_CHARS=2_000_000;
const has=(obj,k)=>Object.prototype.hasOwnProperty.call(obj,k);
function fail(msg){throw Error("Invalid campaign save: "+msg)}
function obj(x){return x!==null&&typeof x==="object"&&!Array.isArray(x)}
function boundedInt(x,min=0,max=1e9){return Number.isSafeInteger(x)&&x>=min&&x<=max}
function keySet(objMap,max) {
 if(!obj(objMap))fail("expected object map");
 const keys=Object.keys(objMap);
 if(keys.length>max)fail("oversized object map");
 if(keys.some(k=>k==="__proto__"||k==="constructor"||k==="prototype"))fail("unsafe object key");
 return keys;
}
function safeTree(x) {
 let nodes=0;
 const walk=(v,depth)=>{
   if(++nodes>100000||depth>32)fail("oversized or nested state");
   if(Array.isArray(v)){
     if(v.length>60000)fail("oversized array");
     for(const val of v)walk(val,depth+1);
   }else if(obj(v)){
     for(const k of Object.keys(v)){
       if(["__proto__","constructor","prototype"].includes(k))fail("unsafe key");
       walk(v[k],depth+1);
     }
   }else if(typeof v==="number"&&!Number.isFinite(v))fail("non-finite numeric value");
 };
 walk(x,0);
}
function requireMapKeys(map,expect){
 const actual=keySet(map,expect.length);
 if(actual.length!==expect.length||expect.some(k=>!has(map,k)))fail("wrong faction keys");
}
function validateGame(g) {
 safeTree(g);
 if(!obj(g)||!boundedInt(g.day,0,10000000)||!boundedInt(g.rng,0,4294967295)||
    !boundedInt(g.nextId,1,1000000000))fail("game header");
 if(g.winner!==null&&!has(E.FACTIONS,g.winner))fail("winner");
 const factions=Object.keys(E.FACTIONS);requireMapKeys(g.factions,factions);
 const siteIds=keySet(g.systems,2048);
 if(siteIds.length<2)fail("missing systems");
 for(const id of siteIds){
   const s=g.systems[id];
   if(!obj(s)||s.id!==id||!Number.isFinite(s.x)||!Number.isFinite(s.y)||
     (s.owner!==null&&!factions.includes(s.owner))||
     !boundedInt(s.garrison,0,1000000)||!obj(s.support)||!obj(s.facilities)||
     !Array.isArray(s.production)||s.production.length>2048)fail("system "+id);
   for(const f of factions){if(!boundedInt(s.support[f],0,100))fail("support "+id)}
   for(const k of ["mine","yard","fort"])if(!boundedInt(s.facilities[k],0,10000))fail("facility "+id);
   for(const job of s.production){
     if(!obj(job)||!boundedInt(job.id,1)||!factions.includes(job.faction)||
       !["patrol","troops","mine"].includes(job.type)||
       !boundedInt(job.remaining,1,100000))fail("production "+id);
   }
 }
 for(const f of factions) {
   const data=g.factions[f];
   if(!obj(data)||!has(g.systems,data.home)||!boundedInt(data.treasury,0,1e12)||
     !Array.isArray(data.known)||data.known.length>siteIds.length||
     new Set(data.known).size!==data.known.length||
     data.known.some(id=>!has(g.systems,id)))fail("faction "+f);
 }
 const fleetIds=keySet(g.fleets,3000),agentIds=keySet(g.agents,3000);
 for(const id of fleetIds){
   const v=g.fleets[id];
   if(!obj(v)||v.id!==id||!factions.includes(v.faction)||
      !Array.isArray(v.ships)||v.ships.length>100||
      !Array.isArray(v.agents)||v.agents.length>500||
      new Set(v.agents).size!==v.agents.length||!boundedInt(v.troops,0,100000))fail("fleet "+id);
   if(v.moving!==null){
     if(v.at!==null||!obj(v.moving)||!has(g.systems,v.moving.destination)||
       !boundedInt(v.moving.daysLeft,1,100000))fail("fleet transit "+id);
   }else if(!has(g.systems,v.at))fail("fleet position "+id);
   let berths=0,capacity=0;
   for(const ship of v.ships){
     if(!obj(ship)||typeof ship.id!=="string"||!Number.isFinite(ship.speed)||
       ship.speed<=0||!boundedInt(ship.troops,0,100000)||
       !boundedInt(ship.agentSlots,0,100000))fail("ship "+id);
     berths+=ship.agentSlots;capacity+=ship.troops;
   }
   if(v.troops>capacity||v.agents.length>berths)fail("fleet capacity "+id);
 }
 for(const id of agentIds){
   const a=g.agents[id];
   if(!obj(a)||a.id!==id||!factions.includes(a.faction)||typeof a.busy!=="boolean"||
      typeof a.mentor!=="boolean"||!obj(a.skills)||!obj(a.power)||
      !["cybernetic","psionic"].includes(a.power.kind)||
      a.power.kind!==E.FACTIONS[a.faction].power||
      typeof a.power.revealed!=="boolean"||typeof a.power.latent!=="boolean"||
      !boundedInt(a.power.level,0,1000))fail("agent "+id);
   for(const k of ["diplomacy","espionage","command"])if(!boundedInt(a.skills[k],0,1000))fail("agent skill "+id);
   if(a.fleet===null){
      if(!has(g.systems,a.at))fail("agent location "+id);
   }else{
      if(a.at!==null||!has(g.fleets,a.fleet)||
        g.fleets[a.fleet].faction!==a.faction||
        !g.fleets[a.fleet].agents.includes(id)||a.busy)fail("agent carrier "+id);
   }
 }
 for(const id of fleetIds){
   for(const passenger of g.fleets[id].agents){
     if(!has(g.agents,passenger)||g.agents[passenger].fleet!==id)fail("passenger "+id);
   }
 }
 if(!Array.isArray(g.missions)||!Array.isArray(g.events)||g.missions.length>3000||g.events.length>60000)fail("timeline");
 // Optional additive event payload: old v1 saves need no migration.
 for(const e of g.events)if(obj(e)&&has(e,"recon")){
   const r=e.recon;
   if(e.type!=="mission_result"||e.kind!=="recon"||e.success!==true||
      !factions.includes(e.faction)||!has(g.systems,e.target)||!boundedInt(e.day,0,g.day)||
      !obj(r)||Object.keys(r).sort().join(",")!=="fort,garrison,owner"||
      !boundedInt(r.garrison,0,1000000)||!boundedInt(r.fort,0,10000)||
      !(r.owner===null||factions.includes(r.owner)))fail("recon snapshot");
 }
 for(const m of g.missions){
   if(!obj(m)||!factions.includes(m.faction)||!has(g.agents,m.agentId)||
     !has(g.systems,m.target)||!boundedInt(m.daysLeft,1,100000)||
     !g.agents[m.agentId].busy||g.agents[m.agentId].fleet!==null||
     g.agents[m.agentId].at!==m.target)fail("mission");
 }
 return true;
}
function checksum(content) {
 let x=2166136261;
 for(let i=0;i<content.length;i++){
   x^=content.charCodeAt(i);
   x=Math.imul(x,16777619)>>>0;
 }
 return x.toString(16).padStart(8,"0");
}
function encode(g,faction) {
 if(!has(E.FACTIONS,faction))fail("faction");
 validateGame(g);
 const payload={version:VERSION,faction,game:g};
 const raw=JSON.stringify(payload);
 if(raw.length>MAX_CHARS)fail("game too large");
 return JSON.stringify({format:FORMAT,payload,checksum:checksum(raw)})+"\n";
}
function decode(serialized) {
 if(typeof serialized!=="string"||serialized.length>MAX_CHARS+256)fail("save too large");
 let envelope;
 try{envelope=JSON.parse(serialized)}catch{fail("malformed JSON")}
 if(!obj(envelope)||envelope.format!==FORMAT||!obj(envelope.payload)||
    envelope.payload.version!==VERSION||typeof envelope.checksum!=="string"||
    !/^[0-9a-f]{8}$/.test(envelope.checksum))fail("format or version");
 const p=envelope.payload;
 if(!has(E.FACTIONS,p.faction))fail("faction");
 if(checksum(JSON.stringify(p))!==envelope.checksum)fail("checksum mismatch");
 validateGame(p.game);
 return {game:p.game,faction:p.faction};
}
module.exports={encode,decode,validateGame};

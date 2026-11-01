"use strict";
// Frontier Ledger: original headless campaign commands. No filesystem or provider access.
const E=require("./engine.js"), AI=require("./ai.js");
const HELP=[
 "status | map | chart | agents | fleets | events | help",
 "board AGENT FLEET | leave AGENT | move FLEET SYSTEM",
 "mission AGENT diplomacy|recon|sabotage SYSTEM",
 "loadtroops FLEET COUNT | unloadtroops FLEET COUNT",
 "build SYSTEM patrol|troops|mine | invade FLEET SYSTEM [COMMANDER]",
 "awaken MENTOR CANDIDATE | tick [DAYS] (1..30)",
 "save FILE | load FILE | quit (in the interactive shell)"
].join("\n");
function requireSide(f) {
 if(!Object.prototype.hasOwnProperty.call(E.FACTIONS,f))throw Error("Unknown player faction");
}
function integer(s,label,max) {
 if(typeof s!=="string"||!/^(0|[1-9][0-9]*)$/.test(s))throw Error(label+" must be an integer");
 const n=Number(s);
 if(!Number.isSafeInteger(n)||n<1||n>max)throw Error(label+" must be within 1.."+max);
 return n;
}
function formatView(g,f) {
 const v=E.view(g,f);
 const holdings=Object.values(g.systems).filter(s=>s.owner===f).length;
 return "Day "+v.day+" | "+E.FACTIONS[f].name+" | treasury "+v.treasury+
   " | controlled "+holdings+" | winner "+(v.victory??"none");
}
function mapView(g,f) {
 const sites=Object.values(E.view(g,f).systems);
 return sites.map(s=>s.id+" ("+s.x+","+s.y+") "+(s.owner??"neutral")+
  " | garrison "+(s.garrison??"?")+
  " | facilities "+(s.facilities?JSON.stringify(s.facilities):"?")).join("\n")||
  "No known systems";
}
// The public chart the opponent policy already reads: ids and coordinates only.
// Without it the shell names only known systems, and exploring needs a name to move to.
function chartView(g) {
 return Object.values(g.systems).map(s=>s.id+" ("+s.x+","+s.y+")").join("\n");
}
function agentsView(g,f) {
 return E.view(g,f).agents.map(a=>a.id+" "+(a.fleet?"aboard "+a.fleet:(a.at??"unknown"))+
  (a.busy?" [mission]":"")+" | "+JSON.stringify(a.skills)+
  " | power "+(a.power?JSON.stringify(a.power):"hidden")).join("\n");
}
function fleetsView(g,f) {
 return Object.values(g.fleets).filter(v=>v.faction===f).map(v=>
   v.id+" "+(v.moving?"in transit to "+v.moving.destination+" ("+v.moving.daysLeft+"d)":(v.at??"unknown"))+
   " | ships "+v.ships.length+" | troops "+v.troops+" | agents "+
   (v.agents.join(",")||"none")).join("\n");
}
// An event belongs to a faction; do not expose opponent actions, targets or rolls.
// Show at most the last 20 own events, including mission and invasion outcomes.
function eventView(g,f,start=0) {
 const own=g.events.slice(start).filter(e=>e.faction===f);
 if(!own.length)return "No faction events recorded.";
 const recent=own.slice(-20).map(e=>{
   if(e.type==="defence_notice")
     return "Day "+e.day+": Invasion @"+e.systemId+" "+e.outcome;
   if(e.type==="build_start" || e.type==="build_finish")
     return "Day "+e.day+": "+e.type+" "+e.itemType+" @"+e.systemId+
       (e.type==="build_start"?" (queued; cost "+e.cost+")":
        " (completed)"+(g.systems[e.systemId]?.owner!==f?"; world is not currently yours: availability to you is not confirmed":""));
   const parts=["Day "+e.day+": "+e.type];
   // Results carry a mission ID, not an agent ID. Join only to our own start.
   const missionStart=e.type==="mission_result" && e.id!==undefined
     ?g.events.find(s=>s.type==="mission_start"&&s.faction===f&&s.id===e.id):null;
   const agentId=e.agentId??missionStart?.agentId;
   if(agentId)parts.push("agent "+agentId);
   if(e.fleetId)parts.push("fleet "+e.fleetId);
   if(e.systemId||e.target)parts.push("@"+(e.systemId??e.target));
   if(e.type==="mission_result")
     parts.push(e.success?"SUCCESS":"FAILED","chance "+e.chance+"%","roll "+e.roll);
   if(e.type==="invasion")parts.push(e.success?"SUCCESS":"FAILED");
   return parts.join(" ");
 });
 if(own.length>20)recent.unshift("("+ (own.length-20) +" earlier faction events omitted)");
 return recent.join("\n");
}
// ONE command only. Mutations happen inside independently validating engine calls.
function execute(g,f,line) {
 requireSide(f);
 if(typeof line!=="string"||line.length>240)throw Error("Command must be a short text line");
 const args=line.trim().split(/\s+/).filter(Boolean),verb=(args.shift()??"").toLowerCase();
 const exact=(n)=>{if(args.length!==n)throw Error(verb+" requires "+n+" argument(s)")};
 const mutating=new Set(["board","leave","move","mission","loadtroops","unloadtroops","build","invade","awaken","tick"]);
 if(g.winner&&mutating.has(verb))throw Error("Campaign is over");
 let result;
 switch(verb){
 case "":case "help":exact(0);return HELP;
 case "status":exact(0);return formatView(g,f);
 case "map":exact(0);return mapView(g,f);
 case "chart":exact(0);return chartView(g);
 case "agents":exact(0);return agentsView(g,f);
 case "fleets":exact(0);return fleetsView(g,f);
 case "events":exact(0);return eventView(g,f);
 case "board":exact(2);result=E.boardAgent(g,f,args[0],args[1]);break;
 case "leave":exact(1);result=E.disembarkAgent(g,f,args[0]);break;
 case "move":exact(2);result=E.moveFleet(g,f,args[0],args[1]);break;
 case "mission":exact(3);result=E.mission(g,f,args[0],args[1],args[2]);break;
 case "loadtroops":exact(2);result=E.embarkTroops(g,f,args[0],integer(args[1],"Troop count",100000));break;
 case "unloadtroops":exact(2);result=E.disembarkTroops(g,f,args[0],integer(args[1],"Troop count",100000));break;
 case "build":exact(2);result=E.queueBuild(g,f,args[0],args[1]);break;
 case "invade":if(args.length<2||args.length>3)throw Error("invade needs FLEET SYSTEM [COMMANDER]");
   result=E.invade(g,f,args[0],args[1],args[2]??null);break;
 case "awaken":exact(2);result=E.discoverPower(g,f,args[0],args[1]);break;
 case "tick":if(args.length>1)throw Error("tick takes zero or one day count");
   const days=args.length?integer(args[0],"Days",30):1;
   const other=Object.keys(E.FACTIONS).find(x=>x!==f);
   const eventStart=g.events.length;
   AI.runCampaign(g,days,[other]);
   return "Advanced to day "+g.day+"; "+formatView(g,f)+"\n"+
     "Your events during advancement:\n"+eventView(g,f,eventStart);
 default:throw Error("Unknown command: "+verb+" (use help)");
 }
 return "Accepted: "+(typeof result==="object"?JSON.stringify(result):String(result));
}
module.exports={execute,HELP,formatView};

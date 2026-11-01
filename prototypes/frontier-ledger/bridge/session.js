'use strict';
const E=require('../src/engine'), Commands=require('../src/commands'), Save=require('../src/save');
const COUNTS={board:[2],leave:[1],move:[2],mission:[3],loadtroops:[2],unloadtroops:[2],build:[2],invade:[2,3],awaken:[2],tick:[1]};
function fail(message,status=400){throw Object.assign(new Error(message),{status});}
function object(x){return x!==null&&typeof x==='object'&&!Array.isArray(x);}
function keys(x,expected){if(!object(x)||Object.keys(x).length!==expected.length||expected.some(k=>!Object.hasOwn(x,k)))fail('Unexpected request fields');}
function playerView(g,f){
 const v=E.view(g,f);
 return {day:v.day,faction:f,factionName:E.FACTIONS[f].name,treasury:v.treasury,
  controlled:Object.values(g.systems).filter(s=>s.owner===f).length,winner:v.victory,
  systems:Object.values(g.systems).map(s=>v.systems[s.id]?{...v.systems[s.id],known:true}:{id:s.id,x:s.x,y:s.y,known:false}),
  agents:v.agents,
  fleets:Object.values(g.fleets).filter(s=>s.faction===f).map(s=>({id:s.id,at:s.at,moving:s.moving?{destination:s.moving.destination,daysLeft:s.moving.daysLeft}:null,
   ships:s.ships.length,troops:s.troops,capacity:s.ships.reduce((n,h)=>n+h.troops,0),agentSlots:s.ships.reduce((n,h)=>n+h.agentSlots,0),agents:[...s.agents]})),
  events:Commands.execute(g,f,'events').split('\n')};
}
function createSession(){
 let game=E.createGame(42),faction='directorate',revision=0;
 function state(){return {view:playerView(game,faction),revision};}
 function transact(route,body){
  if(!object(body)||body.revision!==revision)fail('Campaign changed. Refresh before acting.',409);
  if(route==='/api/save') {keys(body,['revision']);return {save:Save.encode(game,faction),filename:`frontier-day-${game.day}.json`};}
  let candidate,nextFaction=faction,message;
  if(route==='/api/new'){
   keys(body,['revision','seed','faction']);
   if(!Number.isSafeInteger(body.seed)||body.seed<0||body.seed>4294967295||!Object.hasOwn(E.FACTIONS,body.faction))fail('Choose a seed from 0 to 4294967295 and a known faction');
   candidate=E.createGame(body.seed);nextFaction=body.faction;message='New campaign started';
  }else if(route==='/api/load'){
   keys(body,['revision','save']);
   const decoded=Save.decode(body.save);candidate=decoded.game;nextFaction=decoded.faction;message='Campaign loaded';
  }else if(route==='/api/action'){
   keys(body,['revision','verb','args']);
   if(typeof body.verb!=='string'||!Object.hasOwn(COUNTS,body.verb)||!Array.isArray(body.args)||!COUNTS[body.verb].includes(body.args.length)||body.args.some(a=>typeof a!=='string'||!/^[a-z0-9-]{1,64}$/.test(a)))fail('Invalid action or arguments');
   // Transactional copy: even future engine throws after mutation cannot partially commit.
   candidate=structuredClone(game);
   message=Commands.execute(candidate,faction,[body.verb,...body.args].join(' '));
  }else fail('Not found',404);
  Save.validateGame(candidate);
  // Projection must also succeed before commit (including imported state).
  playerView(candidate,nextFaction);
  game=candidate;faction=nextFaction;revision++;
  return {...state(),message};
 }
 return {state,transact};
}
module.exports={createSession,playerView};

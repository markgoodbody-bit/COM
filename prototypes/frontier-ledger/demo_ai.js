"use strict";
/* Deterministic, headless, original-IP opponent-vs-opponent example. */
const E=require("./src/engine.js"), AI=require("./src/ai.js");
const seed=Number(process.argv[2]??18), days=Number(process.argv[3]??35);
if(!Number.isSafeInteger(seed)||seed<0||!Number.isSafeInteger(days)||days<1||days>365) {
  console.error("Usage: node demo_ai.js [nonnegative-seed] [days:1..365]");
  process.exitCode=2;
} else {
  const game=E.createGame(seed);
  const history=AI.runCampaign(game,days);
  const captures=game.events.filter(e=>e.type==="acquire")
    .map(e=>({day:e.day,faction:e.faction,system:e.systemId}));
  const missions=game.events.filter(e=>e.type==="mission_result")
    .reduce((stats,e)=>{
      stats.attempts++;if(e.success)stats.successes++;return stats;
    },{attempts:0,successes:0});
  console.log(JSON.stringify({
    seed,daysPlayed:game.day,territory:Object.fromEntries(
      Object.keys(E.FACTIONS).map(f=>[f,
        Object.values(game.systems).filter(s=>s.owner===f).length])),
    missions,captures,
    firstOrders:history.slice(0,6).map(h=>({day:h.day,orders:h.orders.map(o=>o.order)})),
    winner:game.winner
  },null,2));
}

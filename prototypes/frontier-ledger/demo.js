"use strict";
const E=require("./src/engine.js");
const g=E.createGame(19);
E.boardAgent(g,"directorate","ves","iron");
E.moveFleet(g,"directorate","iron","meridian");
E.tick(g,2);
E.disembarkAgent(g,"directorate","ves");
E.mission(g,"directorate","ves","diplomacy","meridian");
E.tick(g,2);
console.log(JSON.stringify({day:g.day,treasury:g.factions.directorate.treasury,
  sector:g.systems.meridian,events:g.events,winner:g.winner},null,2));

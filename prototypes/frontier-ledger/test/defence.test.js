"use strict";
const test=require('node:test'),assert=require('node:assert/strict');
const E=require('../src/engine.js'),C=require('../src/commands.js');

for(const success of [true,false])test(`defender receives a minimal ${success?'lost-world':'repelled-attack'} report`,()=>{
 const g=E.createGame();
 g.fleets.wanderer.at='cinder';
 if(success)g.systems.cinder.garrison=0,g.systems.cinder.facilities.fort=0;
 E.invade(g,'league','wanderer','cinder');
 const notice=g.events.find(e=>e.type==='defence_notice');
 assert.deepEqual(Object.keys(notice).sort(),['day','type','faction','systemId','outcome'].sort());
 assert.equal(notice.faction,'directorate');
 assert.equal(notice.outcome,success?'WORLD_LOST':'ATTACK_REPELLED');
 const before=JSON.stringify(g),report=C.execute(g,'directorate','events');
 assert.match(report,new RegExp('Invasion @cinder '+notice.outcome));
 assert.doesNotMatch(report,/\b(wanderer|assault|defence|beacon|chance|roll)\b/);
 assert.equal(JSON.stringify(g),before);
 assert.doesNotMatch(C.execute(g,'league','events'),/WORLD_LOST|ATTACK_REPELLED/);
});
test('neutral invasion does not invent a defender or report other locations',()=>{
 const g=E.createGame();g.fleets.iron.at='meridian';
 E.invade(g,'directorate','iron','meridian');
 assert.equal(g.events.filter(e=>e.type==='defence_notice').length,0);
 assert.equal(C.execute(g,'league','events'),'No faction events recorded.');
});
test('human tick reports an AI attack on a world owned before capture',()=>{
 const g=E.createGame();
 g.factions.league.known.push('cinder');
 g.fleets.wanderer.troops=10;
 E.boardAgent(g,'league','tama','wanderer');
 g.fleets.wanderer.at='cinder';
 g.systems.cinder.garrison=0;g.systems.cinder.facilities.fort=0;
 const report=C.execute(g,'directorate','tick 1');
 assert.equal(g.systems.cinder.owner,'league');
 assert.match(report,/Invasion @cinder WORLD_LOST/);
 assert.doesNotMatch(report,/\b(wanderer|assault|defence|beacon|chance|roll)\b/);
});

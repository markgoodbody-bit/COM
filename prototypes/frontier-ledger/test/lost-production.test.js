'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const E=require('../src/engine'),C=require('../src/commands');
test('own completion on a lost world does not promise usable reinforcements or expose its strength',()=>{
 const g=E.createGame();E.queueBuild(g,'directorate','cinder','troops');g.systems.cinder.owner='league';g.systems.cinder.garrison=987;
 E.tick(g,3);const before=JSON.stringify(g),text=C.execute(g,'directorate','events');
 assert.match(text,/build_finish troops @cinder \(completed\); world is not currently yours: availability to you is not confirmed/);
 assert.doesNotMatch(text,/987|990|league/);assert.equal(JSON.stringify(g),before);
});
test('current-control qualification changes truthfully after recapture without rewriting old events',()=>{
 const g=E.createGame();E.queueBuild(g,'directorate','cinder','troops');E.tick(g,3);
 assert.doesNotMatch(C.execute(g,'directorate','events'),/not currently yours/);
 g.systems.cinder.owner='league';assert.match(C.execute(g,'directorate','events'),/not currently yours/);
 g.systems.cinder.owner='directorate';assert.doesNotMatch(C.execute(g,'directorate','events'),/not currently yours/);
});

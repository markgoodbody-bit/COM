'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const E=require('../src/engine'),{playerView,createSession}=require('../bridge/session'),UI=require('../gui/app'),{createServer}=require('../bridge/server');
test('economy and political support expose own values only; fog remains absent',()=>{
 const g=E.createGame();g.systems.meridian.support.league=99;E.queueBuild(g,'league','beacon','mine');
 const v=playerView(g,'directorate');assert.equal(v.dailyIncome,2);assert.equal(v.systems.find(s=>s.id==='cinder').dailyIncome,2);
 assert.equal(v.systems.find(s=>s.id==='meridian').ownSupport,25);
 const hidden=v.systems.find(s=>s.id==='beacon');assert.deepEqual(Object.keys(hidden).sort(),['id','known','x','y']);
 assert.ok(v.systems.every(s=>!Object.hasOwn(s,'support')));
});
test('income and build descriptions agree with real mine and troop completion',()=>{
 const g=E.createGame(),v=playerView(g,'directorate');
 const choices=UI.actionsFor(v,{system:'cinder'});assert.match(choices.find(x=>x.args[1]==='mine').label,/\+1\/day, 3 days/);
 E.queueBuild(g,'directorate','cinder','mine');const before=g.factions.directorate.treasury;E.tick(g,3);
 assert.equal(g.factions.directorate.treasury-before,6);assert.equal(playerView(g,'directorate').dailyIncome,3);
 E.tick(g,1);assert.equal(g.factions.directorate.treasury-before,9);
});
test('result history joins only own starts and never invents an agent',()=>{
 const g=E.createGame();g.events.push({day:0,type:'mission_start',faction:'league',id:9,agentId:'tama'});
 g.events.push({day:1,type:'mission_result',faction:'directorate',id:9,target:'cinder',kind:'recon',success:true,chance:50,roll:1});
 g.events.push({day:1,type:'mission_result',faction:'league',id:7,target:'beacon',kind:'sabotage',success:true});
 const h=playerView(g,'directorate').missionHistory;assert.equal(h.length,1);assert.equal(h[0].agentId,null);
});
test('mentor action uses actual mentor flag, not guessed revealed power',()=>{
 const g=E.createGame();g.agents.orrin.mentor=false;
 assert.ok(!UI.actionsFor(playerView(g,'directorate'),{agent:'orrin',system:'cinder'}).some(a=>a.verb==='awaken'));
});
test('actual HTTP campaign segment gives partial diplomacy then acquisition; save/reload preserves own history',async t=>{
 const app=createServer(),url=await app.listen();t.after(async()=>{app.server.closeAllConnections();await new Promise(r=>app.server.close(r));});
 const api=UI.createApi(url,fetch,{Origin:url});await api.state();
 await api.action('board',['ves','iron']);await api.action('move',['iron','meridian']);await api.action('tick',['2']);await api.action('leave',['ves']);
 await api.action('mission',['ves','diplomacy','meridian']);let v=(await api.action('tick',['2'])).view;
 assert.equal(v.systems.find(s=>s.id==='meridian').ownSupport,50);assert.equal(v.systems.find(s=>s.id==='meridian').owner,null);
 assert.equal(v.missionHistory[0].agentId,'ves');assert.equal(v.missionHistory[0].success,true);
 let attempts=1;
 while(v.systems.find(s=>s.id==='meridian').owner===null&&attempts<10){await api.action('mission',['ves','diplomacy','meridian']);v=(await api.action('tick',['2'])).view;attempts++;}
 assert.equal(v.systems.find(s=>s.id==='meridian').owner,'directorate');assert.equal(v.dailyIncome,3);
 const saved=await api.save(),history=v.missionHistory;await api.newGame(7,'league');v=(await api.load(saved.save)).view;assert.deepEqual(v.missionHistory,history);
 t.diagnostic(`Seed42: first success day4 gives50 support/neutral; acquired by day${v.day} after${attempts} diplomacy attempts; income${v.dailyIncome}/day; save/reload exact own history.`);
});

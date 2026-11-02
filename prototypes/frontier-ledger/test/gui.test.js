"use strict";
// The visual client in gui/: its choices agree with the engine, it never shows an unknown owner,
// it talks to the real bridge, and its source keeps the bridge's CSP and textContent rules.
const test=require("node:test"), assert=require("node:assert/strict");
const fs=require("node:fs"), path=require("node:path");
const {createSession}=require("../bridge/session"), {createServer}=require("../bridge/server");
const E=require("../src/engine.js"), Save=require("../src/save.js");
const UI=require("../gui/app.js");
const GUI=path.join(__dirname,"..","gui");

// A fresh session holding exactly s's campaign, so a trial action cannot touch s.
function fork(s){
 const save=s.transact("/api/save",{revision:s.state().revision}).save,copy=createSession();
 copy.transact("/api/load",{revision:0,save});
 return copy;
}
function selections(v){
 const out=v.systems.map(s=>({system:s.id}));
 for(const f of v.fleets){
  out.push({system:f.at,fleet:f.id});
  for(const s of v.systems)if(s.id!==f.at)out.push({system:s.id,fleet:f.id});
 }
 for(const a of v.agents)out.push({system:a.at,agent:a.id});
 return out;
}
// Every argument list a player could send from one entry: its default, plus each option of a select.
function argLists(a){
 if(a.input&&a.input.kind==="select")return a.input.options.map(o=>a.argsFor(o.value));
 return [a.args];
}
function accepted(s,verb,args){
 try{fork(s).transact("/api/action",{revision:1,verb,args});return true;}catch{return false;}
}

test("the chart shows all eight public stars and no owner for an unvisited one",()=>{
 const v=createSession().state().view,pos=UI.layout(v.systems);
 assert.equal(Object.keys(pos).length,8);
 for(const p of Object.values(pos))assert.ok(p.x>=0&&p.x<=600&&p.y>=0&&p.y<=520);
 const beacon=v.systems.find(s=>s.id==="beacon");
 assert.equal(UI.ownerClass(beacon,v.faction),"unknown");assert.equal(UI.ownerText(beacon,v.faction),"Unknown");
 // Even a forged unknown entry that carries an owner is drawn as unknown.
 assert.equal(UI.ownerText({id:"x",x:0,y:0,known:false,owner:"league"},"directorate"),"Unknown");
 assert.equal(UI.ownerText(v.systems.find(s=>s.id==="cinder"),v.faction),"Yours");
 assert.equal(UI.ownerText(v.systems.find(s=>s.id==="meridian"),v.faction),"Neutral");
});

// Check every choice the client shows at s's current state against the engine; return the playable ones.
function agree(s,label,count){
 const v=s.state().view,playable=[];
 for(const sel of selections(v))for(const a of UI.actionsFor(v,sel)){
  if(!a.args.length)continue;            // a status line such as "on a mission", not a request
  for(const args of argLists(a)){
   const ok=accepted(s,a.verb,args);
   assert.equal(ok,a.enabled,`${label} day ${v.day}: ${a.verb} ${args.join(" ")} offered=${a.enabled} engine=${ok} (${a.reason})`);
   if(a.enabled){count.offered++;playable.push([a.verb,args]);}else count.refused++;
  }
 }
 return playable;
}
function sessionAt(g,faction){
 const s=createSession();s.transact("/api/load",{revision:0,save:Save.encode(g,faction)});return s;
}
// States a random walk rarely reaches, built directly with the engine.
const CRAFTED={
 "an agent aboard a travelling fleet":g=>{E.boardAgent(g,"directorate","ves","iron");E.moveFleet(g,"directorate","iron","meridian");},
 "a full one-berth fleet beside a free agent":g=>{
  g.fleets.skiff={id:"skiff",faction:"directorate",at:"cinder",moving:null,
   ships:[{id:"skiff-1",speed:4,troops:5,agentSlots:1,power:2}],troops:0,agents:[]};
  E.boardAgent(g,"directorate","ves","skiff");},
 "a garrison smaller than the fleet's free room":g=>{g.systems.cinder.garrison=3;},
 "a loaded fleet at an enemy world, with a possible commander":g=>{
  E.boardAgent(g,"directorate","ves","iron");g.systems.meridian.owner="league";g.fleets.iron.at="meridian";},
 "an empty fleet at an enemy world":g=>{g.systems.meridian.owner="league";g.fleets.iron.at="meridian";g.fleets.iron.troops=0;},
 "an agent on a mission":g=>{E.mission(g,"directorate","ves","diplomacy","cinder");},
 "an empty treasury":g=>{g.factions.directorate.treasury=5;},
 "a finished campaign":g=>{g.winner="league";},
};
test("every offered action is accepted by the engine and every refused one is refused",t=>{
 const count={offered:0,refused:0};let rng=7;
 const next=n=>{rng=(Math.imul(rng,1103515245)+12345)>>>0;return rng%n;};
 for(const [label,make] of Object.entries(CRAFTED)){const g=E.createGame(42);make(g);agree(sessionAt(g,"directorate"),label,count);}
 for(const [seed,faction] of [[42,"directorate"],[42,"league"],[7,"directorate"],[18,"league"]]){
  const s=createSession();s.transact("/api/new",{revision:0,seed,faction});
  for(let step=0;step<40&&!s.state().view.winner;step++){
   const playable=agree(s,seed+"/"+faction,count);
   const [verb,args]=next(3)===0||!playable.length?["tick",[String(1+next(3))]]:playable[next(playable.length)];
   s.transact("/api/action",{revision:s.state().revision,verb,args});
  }
 }
 t.diagnostic(`checked against the engine: ${count.offered} offered, ${count.refused} refused`);
 assert.ok(count.offered>200&&count.refused>20,`offered ${count.offered}, refused ${count.refused}`);
});

test("the client completes a real journey against the loopback bridge, including save and load",async t=>{
 const app=createServer(),url=await app.listen();
 t.after(async()=>{app.server.closeAllConnections();await new Promise(r=>app.server.close(r));});
 for(const [route,type,marker] of [["/","text/html",'<svg id="chart"'],["/style.css","text/css",".star"],["/app.js","text/javascript","actionsFor"]]){
  const r=await fetch(url+route),body=await r.text();
  assert.equal(r.status,200);assert.match(r.headers.get("content-type"),new RegExp(type));
  assert.match(r.headers.get("content-security-policy"),/script-src 'self'/);assert.ok(body.includes(marker));
 }
 const api=UI.createApi(url,fetch,{Origin:url});
 let v=(await api.state()).view;
 const pick=(sel,verb,label)=>{
  const a=UI.actionsFor(v,sel).find(x=>x.verb===verb&&(!label||x.label.includes(label)));
  assert.ok(a&&a.enabled,`${verb} ${label||""} should be offered`);return a;
 };
 const play=async(a,value)=>{v=(await api.action(a.verb,value===undefined?a.args:a.argsFor(value))).view;};
 await play(pick({system:"cinder",agent:"ves"},"board","Iron"));
 await play(pick({system:"meridian",fleet:"iron"},"move"),"meridian");
 assert.equal(v.fleets[0].moving.destination,"meridian");
 v=(await api.action("tick",["2"])).view;
 await play(pick({system:"meridian",fleet:"iron"},"leave","Ves"));
 await play(pick({system:"meridian",agent:"ves"},"mission","Diplomacy"));
 v=(await api.action("tick",["2"])).view;
 assert.equal(v.day,4);assert.ok(v.events.some(e=>/mission_result/.test(e)));
 const saved=await api.save();assert.match(saved.filename,/^frontier-day-4\.json$/);
 v=(await api.newGame(5,"league")).view;assert.equal(v.faction,"league");assert.equal(v.day,0);
 v=(await api.load(saved.save)).view;assert.equal(v.faction,"directorate");assert.equal(v.day,4);
 await assert.rejects(api.action("tick",["31"]),e=>e.status===400&&/1..30|Invalid/.test(e.message));
});

test("after days pass, the lines shown as new are exactly the ones added",()=>{
 assert.deepEqual(UI.newEvents(["No faction events recorded."],["Day 1: a","Day 1: b"]),["Day 1: a","Day 1: b"]);
 const full=Array.from({length:20},(_,i)=>"Day "+i+": x");
 assert.deepEqual(UI.newEvents(full,full.slice(2).concat(["Day 20: y","Day 20: z"])),["Day 20: y","Day 20: z"]);
 assert.deepEqual(UI.newEvents(full,full),[]);
});

test("a known world that changes hands is named; an unknown one is not compared",()=>{
 const v=createSession().state().view,after=structuredClone(v);
 after.systems.find(s=>s.id==="meridian").owner="league";
 after.systems.find(s=>s.id==="beacon").owner="league";   // unknown to this side: never compared
 assert.deepEqual(UI.ownershipChanges(v,after),["Meridian changed hands: neutral → enemy."]);
 assert.deepEqual(UI.ownershipChanges(v,v),[]);
});

test("a download that is only requested does not mark the campaign saved",()=>{
 // Campfire #942 review: if the browser blocks the download, New and Load must still warn.
 const js=fs.readFileSync(path.join(GUI,"app.js"),"utf8");
 const handler=js.slice(js.indexOf('$("save-game")'),js.indexOf('$("load-game")'));
 assert.ok(handler.includes("api.save()"));
 assert.doesNotMatch(handler,/unsaved\s*=\s*false/);
});

test("a newly seen hostile fleet is announced once, and an engagement names itself",()=>{
 const before={contacts:[]},after={contacts:[{id:"wanderer",at:"farpoint",ships:1,power:3}]};
 assert.deepEqual(UI.newContacts(before,after),
  ["Hostile fleet Wanderer at Farpoint (1 hull(s), power 3). Select your fleet there to see the Engage choice."]);
 assert.deepEqual(UI.newContacts(after,after),[]);
 assert.equal(UI.describe("engage",["iron","wanderer"],{}),"Iron engaged Wanderer.");
});

test("gui source keeps the bridge's rules: no HTML injection, inline code or remote resources",()=>{
 const html=fs.readFileSync(path.join(GUI,"index.html"),"utf8");
 const js=fs.readFileSync(path.join(GUI,"app.js"),"utf8"),css=fs.readFileSync(path.join(GUI,"style.css"),"utf8");
 for(const bad of [/innerHTML/,/outerHTML/,/insertAdjacentHTML/,/document\.write/,/\beval\s*\(/,/new Function/,/\.style\./])
  assert.doesNotMatch(js,bad);
 assert.doesNotMatch(html,/<script(?![^>]*\bsrc=)[^>]*>/);     // every script is an external file
 assert.doesNotMatch(html,/\son[a-z]+\s*=/i);                   // no inline event handlers
 assert.doesNotMatch(html,/\sstyle\s*=/i);                      // no inline style attributes
 for(const [name,src] of [["index.html",html],["app.js",js],["style.css",css]]){
  const urls=(src.match(/\b(?:https?:)?\/\/[a-z0-9.-]+/gi)||[]).filter(u=>u!=="http://www.w3.org");
  assert.deepEqual(urls,[],name+" names a remote resource");
  assert.doesNotMatch(src,/@import|url\(/,name+" loads another resource");
 }
});

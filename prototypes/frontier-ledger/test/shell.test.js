"use strict";
const test=require("node:test"), assert=require("node:assert/strict");
const fs=require("node:fs"), os=require("node:os"), path=require("node:path");
const {spawnSync}=require("node:child_process");
const E=require("../src/engine.js"), C=require("../src/commands.js");
const PLAY=path.join(__dirname,"..","play.js");
// Runs play.js on scripted stdin inside a fresh temp folder, where any save lands.
function shell(dir,input) {
 return spawnSync(process.execPath,[PLAY,"42","directorate"],{cwd:dir,input,encoding:"utf8",timeout:20000});
}
function tempDir(t) {
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),"frontier-shell-"));
 t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
 return dir;
}
test("the public chart names every system without owner, garrison or facilities",()=>{
 const g=E.createGame(),before=JSON.stringify(g);
 const out=C.execute(g,"directorate","chart");
 for(const s of Object.values(g.systems))assert.match(out,new RegExp("^"+s.id+" \\("+s.x+","+s.y+"\\)$","m"));
 assert.doesNotMatch(out,/directorate|league|neutral|garrison|facilities/);
 assert.equal(JSON.stringify(g),before);
});
test("a charted but fogged system can be reached and then appears on the map",()=>{
 const g=E.createGame();
 assert.match(C.execute(g,"directorate","chart"),/^farpoint /m);
 assert.doesNotMatch(C.execute(g,"directorate","map"),/farpoint/);
 C.execute(g,"directorate","move iron farpoint");
 C.execute(g,"directorate","tick 3");
 assert.match(C.execute(g,"directorate","map"),/^farpoint /m);
});
test("nothing runs after quit, and the shell exits cleanly",(t)=>{
 const dir=tempDir(t);
 const r=shell(dir,"quit\nsave late.json\ntick 5\n");
 assert.equal(fs.existsSync(path.join(dir,"late.json")),false);
 assert.doesNotMatch(r.stdout,/Saved|Advanced/);
 assert.equal(r.stderr,"");
 assert.equal(r.status,0);
});
test("end of input closes the shell without an error",(t)=>{
 const r=shell(tempDir(t),"status\n");
 assert.equal(r.stderr,"");
 assert.equal(r.status,0);
 assert.match(r.stdout,/Campaign closed/);
});
test("save, quit and load in a new process continue byte-identically",(t)=>{
 const dir=tempDir(t),orders="board ves iron\nmove iron meridian\ntick 2\n";
 shell(dir,orders+"save mid.json\nquit\n");
 shell(dir,"load mid.json\ntick 5\nsave resumed.json\nquit\n");
 shell(dir,orders+"tick 5\nsave straight.json\nquit\n");
 const resumed=fs.readFileSync(path.join(dir,"resumed.json"));
 assert.deepEqual(resumed,fs.readFileSync(path.join(dir,"straight.json")));
});

test("uppercase SAVE/LOAD/QUIT work, and buffered commands after QUIT do not run",(t)=>{
 const dir=tempDir(t);
 const first=shell(dir,"SAVE UpperCase.json\nQUIT\nsave late.json\ntick 5\n");
 assert.equal(first.status,0);
 assert.equal(first.stderr,"");
 assert.equal(fs.existsSync(path.join(dir,"UpperCase.json")),true);
 assert.equal(fs.existsSync(path.join(dir,"late.json")),false);
 assert.doesNotMatch(first.stdout,/Advanced/);
 const second=shell(dir,"LOAD UpperCase.json\nstatus\nQUIT\n");
 assert.equal(second.status,0);
 assert.match(second.stdout,/Loaded directorate campaign at day 0/);
});

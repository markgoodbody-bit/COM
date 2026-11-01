"use strict";
// The Windows launcher, run through cmd.exe. Skipped elsewhere: play.cmd is Windows-only.
const test=require("node:test"), assert=require("node:assert/strict");
const {spawn,spawnSync}=require("node:child_process");
const fs=require("node:fs"), os=require("node:os"), path=require("node:path");
const LAUNCHER=path.join(__dirname,"..","play.cmd");
const SYS=path.join(process.env.SystemRoot||"C:\\Windows","System32");
const CMD=path.join(SYS,"cmd.exe");
const windows={skip:process.platform!=="win32"&&"play.cmd runs only on Windows"};
function folder(t){
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),"fl-launch-"));
 t.after(()=>fs.rmSync(dir,{recursive:true,force:true}));
 return dir;
}
// A stand-in node.cmd that logs every call and reports VERSION, so the launcher's checks can be driven.
function fakeNode(dir,version,playExit=0){
 fs.writeFileSync(path.join(dir,"node.cmd"),["@echo off",'echo %*>>"%~dp0calls.txt"',
   'if "%~1"=="--version" (echo '+version+"& exit /b 0)","exit /b "+playExit,""].join("\r\n"));
 return ()=>fs.existsSync(path.join(dir,"calls.txt"))?
   fs.readFileSync(path.join(dir,"calls.txt"),"utf8").split(/\r?\n/).filter(Boolean):[];
}
// cmd /s /c "..." keeps a launcher path with spaces intact.
function command(pathDirs,args=[]){
 const line='""'+LAUNCHER+'"'+args.map(a=>" "+a).join("")+'"';
 return [CMD,["/d","/s","/c",line],{windowsVerbatimArguments:true,
   env:{SystemRoot:process.env.SystemRoot,ComSpec:CMD,PATHEXT:".COM;.EXE;.BAT;.CMD",PATH:[...pathDirs,SYS].join(";")}}];
}
function launch(cwd,pathDirs,input,args){
 const [exe,argv,opts]=command(pathDirs,args);
 return spawnSync(exe,argv,{...opts,cwd,input,encoding:"utf8",timeout:20000});
}
// An error must stay on screen: after 1.5 s the window is still open, and one key closes it.
async function stopsAndWaits(cwd,pathDirs){
 const [exe,argv,opts]=command(pathDirs);
 const child=spawn(exe,argv,{...opts,cwd});
 let out="";child.stdout.on("data",d=>out+=d);
 const exited=new Promise(done=>child.on("exit",code=>done(code)));
 await new Promise(done=>setTimeout(done,1500));
 assert.equal(child.exitCode,null,"closed without waiting: "+out);
 child.stdin.end("x");
 return {status:await exited,out};
}
test("play.cmd starts the game from another folder and passes the seed and side",windows,t=>{
 const dir=folder(t),r=launch(dir,[path.dirname(process.execPath)],"status\nsave t.json\nquit\n",["7","league"]);
 assert.equal(r.status,0,r.stdout+r.stderr);
 assert.match(r.stdout,/Horizon League/);assert.match(r.stdout,/Campaign closed/);
 assert.ok(fs.existsSync(path.join(dir,"t.json")));assert.equal(r.stderr,"");
});
test("without Node.js it says so and waits for a key before closing",windows,async t=>{
 const r=await stopsAndWaits(folder(t),[]);
 assert.equal(r.status,1);
 assert.match(r.out,/Node\.js was not found/);assert.match(r.out,/Press a key to close/);
});
test("Node.js older than 20 is refused before the game starts",windows,async t=>{
 const dir=folder(t),calls=fakeNode(dir,"v18.20.0"),r=await stopsAndWaits(dir,[dir]);
 assert.equal(r.status,1,r.out);
 assert.match(r.out,/needs Node\.js 20 or later/);assert.match(r.out,/v18\.20\.0/);
 assert.ok(calls().length>0&&calls().every(c=>c==="--version"),calls().join(" | "));
});
test("Node.js 20 is accepted and runs this folder's play.js",windows,t=>{
 const dir=folder(t),calls=fakeNode(dir,"v20.0.0"),r=launch(dir,[dir],"");
 assert.equal(r.status,0,r.stdout+r.stderr);
 const play=path.join(path.dirname(LAUNCHER),"play.js").toLowerCase();
 assert.ok(calls().some(c=>c.toLowerCase().includes(play)),calls().join(" | "));
});
test("a game that stops with an error keeps the window open and reports the code",windows,async t=>{
 const dir=folder(t);fakeNode(dir,"v24.0.0",3);
 const r=await stopsAndWaits(dir,[dir]);
 assert.equal(r.status,3,r.out);
 assert.match(r.out,/stopped with exit code 3/);assert.match(r.out,/Press a key to close/);
});

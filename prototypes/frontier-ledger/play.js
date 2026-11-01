"use strict";
// Interactive text-only player. Run: node play.js [SEED] [directorate|league]
const readline=require("node:readline");
const fs=require("node:fs");
const path=require("node:path");
const crypto=require("node:crypto");
const E=require("./src/engine.js"), Commands=require("./src/commands.js"), Save=require("./src/save.js");
let seed=42,side=process.argv[3]??"directorate";
if(process.argv[2]!==undefined) {
 seed=Number(process.argv[2]);
 if(!Number.isSafeInteger(seed)||seed<0||seed>4294967295)throw Error("Seed must be 0..4294967295");
}
if(!Object.prototype.hasOwnProperty.call(E.FACTIONS,side))throw Error("Unknown starting faction");
let game=E.createGame(seed);
const rl=readline.createInterface({input:process.stdin,output:process.stdout,terminal:process.stdin.isTTY});
const MAX_BYTES=2_000_256;
function writeSave(filename) {
 if(!filename||filename.length>200)throw Error("save requires a short FILE path");
 const target=path.resolve(filename);
 const tmp=path.join(path.dirname(target),"."+path.basename(target)+"."+process.pid+"."+crypto.randomBytes(6).toString("hex")+".tmp");
 const text=Save.encode(game,side);
 const fd=fs.openSync(tmp,"wx",0o600);
 try{
   fs.writeFileSync(fd,text,"utf8");
   fs.fsyncSync(fd);
 }catch(err){fs.closeSync(fd);try{fs.unlinkSync(tmp)}catch{}throw err}
 fs.closeSync(fd);
 try{fs.renameSync(tmp,target)}catch(err){try{fs.unlinkSync(tmp)}catch{}throw err}
 return "Saved day "+game.day+" to "+target+" (atomic replacement; not a crash-durability guarantee)";
}
function readSave(filename) {
 if(!filename||filename.length>200)throw Error("load requires a short FILE path");
 const target=path.resolve(filename);
 const info=fs.statSync(target);
 if(!info.isFile()||info.size>MAX_BYTES)throw Error("Save path must be a bounded regular file");
 const loaded=Save.decode(fs.readFileSync(target,"utf8"));
 // Swap only after successful parse, checksum and model validation.
 game=loaded.game;side=loaded.faction;
 return "Loaded "+side+" campaign at day "+game.day;
}
console.log("Frontier Ledger — original text-only prototype. "+Commands.formatView(game,side));
console.log("Type 'help' for commands, 'save FILE' to persist, 'quit' to leave.");
function prompt(){rl.setPrompt("day "+game.day+" "+side+"> ");rl.prompt()}
let closed=false;
rl.on("line",(line)=>{
 // readline still delivers lines it buffered before close(); a closed shell runs none of them.
 if(closed)return;
 const raw=line.trim();
 if(raw==="quit"||raw==="exit"){rl.close();return}
 try{
   if(raw.startsWith("save ")){console.log(writeSave(raw.slice(5).trim()))}
   else if(raw.startsWith("load ")){console.log(readSave(raw.slice(5).trim()))}
   else console.log(Commands.execute(game,side,raw));
 }catch(err){console.error("Rejected: "+err.message)}
 prompt();
});
rl.on("close",()=>{closed=true;console.log("Campaign closed. Unsaved progress is not retained.");});
prompt();

'use strict';
const {createServer}=require('./bridge/server');
const fs=require('node:fs'),path=require('node:path');
async function main(){
 for(const file of ['index.html','style.css','app.js'])if(!fs.existsSync(path.join(__dirname,'gui',file)))throw Error('Visual frontend not yet present. Use the completed visual integration branch.');
 const app=createServer();const url=await app.listen();
 console.log('Frontier Ledger local game: '+url);
 console.log('Open this address in your browser. Keep this window open while playing. Save before closing.');
 // No shell or automatic browser activation. URL remains visible in a double-click launcher.
 process.on('SIGINT',()=>app.server.close(()=>process.exit(0)));
}
if(require.main===module)main().catch(e=>{console.error(e.message);process.exitCode=1;});
module.exports={main};

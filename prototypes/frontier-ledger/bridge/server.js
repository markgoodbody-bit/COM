'use strict';
const http=require('node:http'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {createSession}=require('./session');
const STATIC={'/':['index.html','text/html; charset=utf-8'],'/style.css':['style.css','text/css; charset=utf-8'],'/app.js':['app.js','text/javascript; charset=utf-8']};
function createServer({guiRoot=path.join(__dirname,'../gui')}={}){
 const session=createSession(),csrf=crypto.randomBytes(32).toString('hex');
 let origin;
 const server=http.createServer(async(req,res)=>{
  const headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer',
   'Content-Security-Policy':"default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",'Cross-Origin-Resource-Policy':'same-origin'};
  const reply=(status,data,type='application/json; charset=utf-8')=>{res.writeHead(status,{...headers,'Content-Type':type});res.end(type.startsWith('application/json')?JSON.stringify(data):data);};
  try{
   if(req.headers.host!==new URL(origin).host) return reply(403,{error:'Host refused'});
   if(req.headers.origin!==undefined&&req.headers.origin!==origin)return reply(403,{error:'Origin refused'});
   if(req.headers['sec-fetch-site']==='cross-site')return reply(403,{error:'Cross-site request refused'});
   if(req.method==='GET'&&req.url==='/api/state')return reply(200,{...session.state(),csrf});
   if(req.method==='GET'&&Object.hasOwn(STATIC,req.url)){
    const [file,type]=STATIC[req.url];
    // Fixed allowlist only. Never resolve caller paths or serve the save/engine files.
    let data;try{data=fs.readFileSync(path.join(guiRoot,file));}catch{return reply(503,{error:'Visual frontend is not installed in this source checkout yet'});}
    return reply(200,data,type);
   }
   const routes=['/api/action','/api/new','/api/save','/api/load'];
   if(req.method!=='POST'||!routes.includes(req.url))return reply(404,{error:'Not found'});
   if(req.headers.origin!==origin||req.headers['x-frontier-csrf']!==csrf)return reply(403,{error:'Origin or session token refused'});
   if(req.headers['content-type']!=='application/json')return reply(415,{error:'Use application/json'});
   const cap=req.url==='/api/load'?2100000:4096;
   let size=0,chunks=[];
   for await(const chunk of req){size+=chunk.length;if(size>cap){reply(413,{error:'Request too large'});req.resume();return;}chunks.push(chunk);}
   let body;try{body=JSON.parse(Buffer.concat(chunks).toString('utf8'));}catch{return reply(400,{error:'Malformed JSON'});}
   let result;
   try{result=session.transact(req.url,body);}catch(e){return reply(e.status||400,{error:e.message});}
   reply(200,{...result,csrf});
  }catch{if(!res.headersSent)reply(500,{error:'Local game request failed; no result claimed'});else res.end();}
 });
 server.requestTimeout=10000;server.headersTimeout=10000;server.maxHeadersCount=32;
 return {server,async listen(port=0){await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(port,'127.0.0.1',resolve);});origin=`http://127.0.0.1:${server.address().port}`;return origin;}};
}
module.exports={createServer};

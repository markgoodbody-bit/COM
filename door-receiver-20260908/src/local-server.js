/** Loopback only. No request-body or access logs. Synthetic testing, not public deployment. */
import {createServer} from 'node:http';
import {SqliteAdapter} from './sqlite-adapter.js';
import {handle} from './handler.js';
import {resolve} from 'node:path';
const token=process.env.PSFH_ADMIN_TOKEN,rate=process.env.PSFH_RATE_SECRET;
if(!token||token.length<32||!rate||rate.length<32){
  console.error('Set PSFH_ADMIN_TOKEN and PSFH_RATE_SECRET to separate random secrets (at least 32 characters). No default credentials.');process.exit(2);
}
const db=new SqliteAdapter(resolve(process.env.PSFH_DB??'synthetic-receiver.sqlite'));
const env={DB:db,ADMIN_TOKEN:token,RATE_SECRET:rate,SYNTHETIC_ONLY:'true',APP_ORIGIN:''};
const server=createServer(async(req,res)=>{
  try {
    const body=req.method==='GET'||req.method==='HEAD'?undefined:req;
    const request=new Request(env.APP_ORIGIN+req.url,{method:req.method,headers:req.headers,...(body?{body,duplex:'half'}:{})});
    const response=await handle(request,env);
    res.writeHead(response.status,Object.fromEntries(response.headers));res.end(Buffer.from(await response.arrayBuffer()));
  }catch{res.writeHead(503,{'Cache-Control':'no-store'});res.end('LOCAL_SERVICE_FAILURE');}
});
server.requestTimeout=10000;server.headersTimeout=10000;
server.listen(Number(process.env.PORT??8788),'127.0.0.1',()=>{
  env.APP_ORIGIN=`http://127.0.0.1:${server.address().port}`;
  console.log('LOCAL_SYNTHETIC_READY '+env.APP_ORIGIN);
  process.send?.({origin:env.APP_ORIGIN});
});
for(const signal of ['SIGTERM','SIGINT'])process.on(signal,()=>server.close(()=>{db.close();process.exit(0);}));

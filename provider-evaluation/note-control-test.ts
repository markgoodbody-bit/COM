import {Store,newKey} from '../door-receiver-20260908/src/store.js';
import {CorrectionStore} from '../door-receiver-20260908/src/correction-store.js';
import {handle} from '../door-receiver-20260908/src/router.js';

function check(value:unknown,label:string):asserts value{if(!value)throw Error(label);}
function object(value:unknown):Record<string,unknown>{
  check(value!==null&&typeof value==='object'&&!Array.isArray(value),'expected JSON object');
  return Object.fromEntries(Object.entries(value));
}

// Synthetic-only follow-up. Reuses an existing withdrawn synthetic target.
// No input content, credentials or externally chosen action is accepted.
export async function noteControlEvaluation(env:Env):Promise<Response>{
  const store=new Store(env.DB),corrections=new CorrectionStore(env.DB);
  const settings={DB:env.DB,SYNTHETIC_ONLY:'true',APP_ORIGIN:'http://127.0.0.1:8791',ADMIN_TOKEN:newKey(),RATE_SECRET:newKey()};
  const targetId='e08910e1-92a2-4480-b5fc-f8dbf5cc2351';
  const input={target_id:targetId,kind:'privacy',note:'SYNTHETIC post-resolution note control',retry_key:newKey(),management_key:newKey()};
  let reportId:string|undefined;
  const passed:string[]=[];
  const call=async(path:string,body?:Record<string,unknown>,admin=false)=>{
    const r=await handle(new Request(settings.APP_ORIGIN+path,{method:body?'POST':'GET',headers:{'Content-Type':'application/json',...(admin?{Authorization:'Bearer '+settings.ADMIN_TOKEN}:{})},...(body?{body:JSON.stringify(body)}:{})}),settings);
    return {status:r.status,body:object(await r.json())};
  };
  try{
    const service=await store.first('SELECT enabled,ready_until FROM service WHERE id=1');
    check(service.enabled===0&&service.ready_until===0,'evaluation must begin paused');
    const targetBefore=await store.first('SELECT * FROM contributions WHERE id=?',targetId);
    check(targetBefore?.state==='withdrawn'&&targetBefore.body===null,'expected prior synthetic target');
    const publicBefore=JSON.stringify((await call('/api/posts')).body);
    const receipt=await call('/api/correction',input);
    check(receipt.status===200&&typeof receipt.body.id==='string','new correction receipt');
    reportId=receipt.body.id;
    const command={action:'clear_note',id:reportId,management_key:input.management_key};
    const pending=await call('/api/correction-manage',command);
    check(pending.status===409&&pending.body.error==='CORRECTION_NOT_RESOLVED','pending clearing must refuse');
    const resolved=await call('/api/admin',{action:'resolve-correction',id:reportId,outcome:'no_change',reason:'SYNTHETIC review; no target action'},true);
    check(resolved.status===200&&resolved.body.state==='resolved','resolution');
    const before=object(await corrections.receipt(reportId,input.management_key));
    check(before.note===input.note,'nonempty note before clear');
    const wrong=await call('/api/correction-manage',{...command,management_key:newKey()});
    check(wrong.status===404,'wrong key must refuse');
    check((await corrections.receipt(reportId,input.management_key)).note===input.note,'wrong key changed note');
    passed.push('pending clearing and wrong management key refused');
    const cleared=await call('/api/correction-manage',command);
    check(cleared.status===200&&cleared.body.note==='','owner clearing');
    for(const field of ['id','target_id','kind','state','operator_outcome','operator_reason','created_at','closed_at'])
      check(cleared.body[field]===before[field],'disposition changed: '+field);
    passed.push('owner clears only note while review disposition remains');
    check((await call('/api/correction-manage',command)).status===200,'repeat clearing');
    const retry=await call('/api/correction',input);
    check(retry.status===200&&retry.body.id===reportId&&retry.body.note==='','original retry restored cleared note');
    const events=await store.rows('SELECT action FROM correction_events WHERE correction_id=? ORDER BY id',reportId);
    check(JSON.stringify(events.map((r:{action:string})=>r.action))===JSON.stringify(['received','resolved','reporter_note_cleared']),'exact audit or duplicate clearing');
    passed.push('repeat clearing and original retry retain one clear event and empty note');
    check(JSON.stringify(await store.first('SELECT * FROM contributions WHERE id=?',targetId))===JSON.stringify(targetBefore),'target changed');
    check(JSON.stringify((await call('/api/posts')).body)===publicBefore,'public view changed');
    check(JSON.stringify(await store.first('SELECT enabled,ready_until FROM service WHERE id=1'))===JSON.stringify(service),'intake changed');
    passed.push('target/public view unchanged; ordinary intake remained paused');
    return Response.json({status:'PASS',reportId,targetId,passed,limits:'Local workerd invokes real router with existing remote D1. Live note clearing only; no backup/log/physical-erasure claim or public endpoint.'});
  }catch(error){return Response.json({status:'FAIL',reportId,passed,error:String(error)},{status:500});}
  finally{
    if(reportId){const r=await corrections.receipt(reportId,input.management_key);if(r.state==='pending')await corrections.withdraw(reportId,input.management_key);else if(r.state==='resolved'&&r.note!=='')await corrections.clearNote(reportId,input.management_key);}
  }
}

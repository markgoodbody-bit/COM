import {Store,newKey} from '../door-receiver-20260908/src/store.js';
import {CorrectionStore} from '../door-receiver-20260908/src/correction-store.js';
import {handle} from '../door-receiver-20260908/src/router.js';

function check(value: unknown, label: string): asserts value {if(!value)throw Error(label);}
function object(value: unknown): Record<string,unknown> {
  if(!value||typeof value!=='object'||Array.isArray(value))throw Error('expected object');
  return Object.fromEntries(Object.entries(value));
}

// Bounded, synthetic recipe only. No incoming content, credentials or actions.
export async function correctionEvaluation(env: Env): Promise<Response> {
  const settings={DB:env.DB,SYNTHETIC_ONLY:'true',APP_ORIGIN:'http://127.0.0.1:8791',RATE_SECRET:newKey(),ADMIN_TOKEN:newKey()};
  const store=new Store(env.DB), corrections=new CorrectionStore(env.DB),passed:string[]=[];
  const owner=newKey(),reportKeys={retry_key:newKey(),management_key:newKey()};
  let targetId:string|undefined,reportId:string|undefined;
  const call=async(path:string,input?:Record<string,unknown>,auth=false)=>{
    const response=await handle(new Request(settings.APP_ORIGIN+path,{
      method:input?'POST':'GET',headers:{'Content-Type':'application/json',...(auth?{Authorization:'Bearer '+settings.ADMIN_TOKEN}:{})},
      ...(input?{body:JSON.stringify(input)}:{})
    }),settings);
    return {status:response.status,body:object(await response.json())};
  };
  try {
    await store.readiness(true);
    const target=await store.submit({body:'SYNTHETIC correction target',display_name:'',retry_key:newKey(),management_key:owner},'synthetic-correction-'+crypto.randomUUID());
    targetId=target.id;
    await store.readiness(false);
    const before=await store.first('SELECT * FROM contributions WHERE id=?',targetId);
    const publicBefore=JSON.stringify((await call('/api/posts')).body);
    const ordinary=await call('/api/submit',{body:'SYNTHETIC paused refusal',display_name:'',retry_key:newKey(),management_key:newKey()});
    check(ordinary.status===503&&ordinary.body.error==='INTAKE_PAUSED','ordinary intake not paused');
    const input={target_id:targetId,kind:'misattribution',note:'SYNTHETIC private note',...reportKeys};
    const received=await call('/api/correction',input);
    check(received.status===200&&received.body.state==='pending'&&typeof received.body.id==='string','correction receipt');
    reportId=received.body.id;
    passed.push('ordinary intake refused while correction accepted');
    const retry=await call('/api/correction',input);
    const changed=await call('/api/correction',{...input,note:'SYNTHETIC changed retry'});
    check(retry.status===200&&retry.body.id===reportId,'same retry identity');
    check(changed.status===409&&changed.body.error==='CORRECTION_RETRY_CONFLICT','changed retry refusal');
    check((await store.first('SELECT COUNT(*) AS n FROM correction_requests WHERE id=?',reportId)).n===1,'duplicate correction');
    passed.push('same retry returns one record; changed retry conflicts');
    check((await call('/api/admin',{action:'corrections'})).status===401,'unauthorised queue');
    check((await call('/api/correction-manage',{action:'receipt',id:reportId,management_key:newKey()})).status===404,'wrong reporter key');
    const queue=await call('/api/admin',{action:'corrections'},true);
    check(queue.status===200&&Array.isArray(queue.body.corrections)&&queue.body.corrections.some(row=>object(row).id===reportId),'private operator queue');
    const receipt=await call('/api/correction-manage',{action:'receipt',id:reportId,management_key:reportKeys.management_key});
    check(receipt.status===200&&receipt.body.note===input.note,'reporter receipt');
    check(JSON.stringify((await call('/api/posts')).body)===publicBefore,'public view changed on report');
    passed.push('private operator and reporter access; no public report leakage');
    const resolve={action:'resolve-correction',id:reportId,outcome:'no_change',reason:'SYNTHETIC disposition, no target action'};
    check((await call('/api/admin',resolve)).status===401,'unauthorised resolution');
    const resolved=await call('/api/admin',resolve,true);
    check(resolved.status===200&&resolved.body.state==='resolved','resolution receipt');
    check(JSON.stringify(await store.first('SELECT * FROM contributions WHERE id=?',targetId))===JSON.stringify(before),'report or resolution mutated target');
    check(JSON.stringify((await call('/api/posts')).body)===publicBefore,'resolution changed public view');
    passed.push('explicit resolution does not mutate target or public state');
    const otherKeys={retry_key:newKey(),management_key:newKey()};
    const other=await call('/api/correction',{target_id:targetId,kind:'other',note:'SYNTHETIC withdrawable note',...otherKeys});
    check(other.status===200&&typeof other.body.id==='string','second receipt');
    const withdrawn=await call('/api/correction-manage',{action:'withdraw',id:other.body.id,management_key:otherKeys.management_key});
    check(withdrawn.status===200&&withdrawn.body.state==='withdrawn'&&withdrawn.body.note==='','reporter withdrawal');
    passed.push('pending reporter withdrawal clears note while intake paused');
    const blocked=await handle(new Request('https://example.invalid/report'),{...settings,APP_ORIGIN:'https://example.invalid'});
    check(blocked.status===503,'non-loopback guard');
    passed.push('hard non-loopback guard retained');
    return Response.json({status:'PASS',targetId,reportId,withdrawnReportId:other.body.id,passed,limits:'Local workerd invokes real router with remote D1. Not deployed HTTP or standalone CLI integration. Resolved synthetic note retained; no erasure claim.'});
  } catch(error) {
    return Response.json({status:'FAIL',targetId,reportId,passed,error:String(error)},{status:500});
  } finally {
    await store.readiness(false);
    if(targetId)await store.withdraw(targetId,owner);
    if(reportId){const r=await corrections.receipt(reportId,reportKeys.management_key);if(r.state==='pending')await corrections.withdraw(reportId,reportKeys.management_key);}
  }
}

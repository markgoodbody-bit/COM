import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {fork} from 'node:child_process';
import {once} from 'node:events';
import {Worker} from 'node:worker_threads';
import {SqliteAdapter} from '../src/sqlite-adapter.js';
import {Store,Problem,newKey,DAY} from '../src/store.js';
import {handle} from '../src/handler.js';
const fixed=Date.parse('2026-09-08T15:00:00Z');
function draft(body='A synthetic objection.'){return {body,display_name:'Invented reader',retry_key:newKey(),management_key:newKey()};}
function fixture(t){
  const dir=mkdtempSync(join(tmpdir(),'psfh-test-')),path=join(dir,'test.sqlite');
  const db=new SqliteAdapter(path);let now=fixed;
  const store=new Store(db,()=>now);
  t.after(()=>{db.close();rmSync(dir,{recursive:true,force:true});});
  const env={DB:db,ADMIN_TOKEN:newKey(),RATE_SECRET:newKey(),SYNTHETIC_ONLY:'true',APP_ORIGIN:'http://127.0.0.1:8788'};
  const call=(path,input,auth=false)=>handle(new Request(env.APP_ORIGIN+path,{method:input?'POST':'GET',
    headers:{'Content-Type':'application/json',...(auth?{Authorization:'Bearer '+env.ADMIN_TOKEN}:{})},
    ...(input?{body:JSON.stringify(input)}:{})}),env,()=>now);
  return {db,store,path,env,call,advance:ms=>{now+=ms;},now:()=>now};
}
async function expectProblem(promise,code){await assert.rejects(promise,e=>e instanceof Problem&&e.code===code);}

test('default closed; authenticated readiness opens only a bounded intake window',async t=>{
  const f=fixture(t),input=draft();
  assert.equal((await f.call('/api/submit',input)).status,503);
  assert.equal((await f.call('/api/admin',{action:'ready'})).status,401);
  assert.equal((await f.call('/api/admin',{action:'ready'},true)).status,200);
  assert.equal((await f.call('/api/submit',input)).status,200);
  f.advance(DAY+1);assert.equal((await f.call('/api/submit',draft())).status,503);
});
test('lost database acknowledgement recovers one committed record even while paused',async t=>{
  const f=fixture(t);await f.store.readiness(true);const input=draft();
  const base=f.env.DB;let fail=true;
  f.env.DB={batch:s=>base.batch(s),prepare(sql){
    const p=base.prepare(sql);if(!sql.startsWith('INSERT INTO contributions'))return p;
    return {bind(...values){const statement=p.bind(...values);return {...statement,async run(){const r=await statement.run();if(fail){fail=false;throw new Error('simulated post-commit acknowledgement loss');}return r;}};}};
  }};
  const failed=await f.call('/api/submit',input);
  assert.equal(failed.status,503);assert.equal((await failed.json()).error,'STORAGE_OR_SERVICE_FAILURE');
  assert.equal(f.db.sql.prepare('SELECT COUNT(*) AS n FROM contributions').get().n,1);
  f.env.DB=base;await f.store.readiness(false);
  const recovered=await f.call('/api/submit',input);assert.equal(recovered.status,200);
  const receipt=await recovered.json();assert.equal(receipt.state,'pending');
  assert.equal(f.db.sql.prepare('SELECT COUNT(*) AS n FROM contributions').get().n,1);
  await expectProblem(f.store.submit({...input,body:'Different content'},'client'),'RETRY_CONTENT_CONFLICT');
  await expectProblem(f.store.receipt(receipt.id,newKey()),'RECEIPT_UNAVAILABLE');
});
test('private pending text, keys and rejection reasons do not appear in public reads',async t=>{
  const f=fixture(t);await f.store.readiness(true);const input=draft('PRIVATE-PENDING-TEXT');
  const r=await f.store.submit(input,'client');
  await f.store.moderate(r.id,{action:'decline',revision:1,reason:'PRIVATE-MODERATION-REASON'},'operator');
  for(const path of ['/','/api/posts']){
    const result=await f.call(path),raw=await result.text();
    for(const value of [input.body,input.management_key,input.retry_key,'PRIVATE-MODERATION-REASON'])assert.ok(!raw.includes(value));
    assert.equal(result.headers.get('cache-control'),'no-store');
  }
  assert.equal((await f.call('/api/admin',{action:'queue'})).status,401);
});
test('stale approval cannot publish a replaced or withdrawn contribution',async t=>{
  const f=fixture(t);await f.store.readiness(true);const input=draft('revision A');
  const r=await f.store.submit(input,'client');
  await f.store.moderate(r.id,{action:'publish',revision:1,reason:'Safe synthetic text'},'operator');
  await f.store.respond(r.id,{revision:1,body:'A separate project response'},'operator');
  assert.equal((await f.store.publicItems())[0].responses.length,1);
  const revised=await f.store.revise(r.id,input.management_key,{body:'revision B',display_name:'same unverified name',revision:1});
  assert.equal(revised.revision,2);assert.deepEqual(await f.store.publicItems(),[]);
  await expectProblem(f.store.moderate(r.id,{action:'publish',revision:1,reason:'old review'},'operator'),'MODERATION_STATE_CONFLICT');
  await f.store.moderate(r.id,{action:'publish',revision:2,reason:'reviewed B'},'operator');
  await f.store.withdraw(r.id,input.management_key);
  await expectProblem(f.store.moderate(r.id,{action:'publish',revision:2,reason:'stale'},'operator'),'MODERATION_STATE_CONFLICT');
  assert.deepEqual(await f.store.publicItems(),[]);
  assert.equal((await f.store.receipt(r.id,input.management_key)).body,null);
});
test('paused/full intake still permits revision, withdrawal and reconsideration',async t=>{
  const f=fixture(t);await f.store.readiness(true);const a=draft(),b=draft();
  const ra=await f.store.submit(a,'a'),rb=await f.store.submit(b,'b');
  await f.store.moderate(rb.id,{action:'decline',revision:1,reason:'A reconsiderable moderation reason'},'operator');
  f.db.sql.exec('UPDATE service SET pending_limit=1');
  await expectProblem(f.store.submit(draft(),'new'),'QUEUE_FULL');
  await f.store.readiness(false);
  await f.store.reconsider(rb.id,b.management_key,'Please reconsider');
  assert.equal((await f.store.receipt(rb.id,b.management_key)).reconsideration,true);
  await f.store.revise(ra.id,a.management_key,{body:'replacement',revision:1});
  await f.store.withdraw(ra.id,a.management_key);
  await expectProblem(f.store.submit(draft(),'c'),'INTAKE_PAUSED');
});
test('expiry is visible as not reviewed; cleanup is explicitly request-driven',async t=>{
  const f=fixture(t);await f.store.readiness(true);const a=draft();const r=await f.store.submit(a,'a');
  f.advance(14*DAY+1);
  // No timer/process is running: demonstrate, rather than hide, the physical-retention limit.
  assert.equal(f.db.sql.prepare('SELECT body FROM contributions').get().body,a.body);
  await f.store.sweep();const closed=await f.store.receipt(r.id,a.management_key);
  assert.equal(closed.state,'expired');assert.equal(closed.body,null);
  assert.equal(closed.moderation_reason,null);
  await expectProblem(f.store.reconsider(r.id,a.management_key,'Late reconsideration'),'NOT_RECONSIDERABLE');
});
test('moderation event and state change roll back together on storage failure',async t=>{
  const f=fixture(t);await f.store.readiness(true);const r=await f.store.submit(draft(),'a');
  f.db.sql.exec(`CREATE TRIGGER fail_publish_event BEFORE INSERT ON events WHEN NEW.action='publish'
    BEGIN SELECT RAISE(ABORT,'injected event failure'); END;`);
  await assert.rejects(f.store.moderate(r.id,{action:'publish',revision:1,reason:'test'},'operator'));
  assert.equal((await f.store.first('SELECT state FROM contributions WHERE id=?',r.id)).state,'pending');
  assert.deepEqual(await f.store.publicItems(),[]);
});
test('rate limit is enforced in storage; accepted retries do not consume a new slot',async t=>{
  const f=fixture(t);await f.store.readiness(true);let first;
  for(let i=0;i<6;i++){const d=draft('item '+i);await f.store.submit(d,'same-client');first??=d;}
  await expectProblem(f.store.submit(draft(),'same-client'),'RATE_LIMITED');
  assert.equal((await f.store.submit(first,'same-client')).state,'pending');
  assert.equal(f.db.sql.prepare('SELECT COUNT(*) AS n FROM contributions').get().n,6);
});
test('total body cap also blocks intake when the pending queue is empty',async t=>{
  const f=fixture(t);await f.store.readiness(true);f.db.sql.exec('UPDATE service SET body_limit=1');
  const a=draft(),r=await f.store.submit(a,'a');
  await f.store.moderate(r.id,{action:'publish',revision:1,reason:'synthetic'},'operator');
  await expectProblem(f.store.submit(draft(),'b'),'BODY_CAPACITY');
  await f.store.withdraw(r.id,a.management_key);
  assert.equal((await f.store.submit(draft(),'b')).state,'pending');
});
test('exact Unicode and markup survive as inert text; invalid/oversized requests fail',async t=>{
  const f=fixture(t);await f.store.readiness(true);
  const original='😀 e\u0301 <script>alert(1)</script> & "quoted"';
  const input=draft(original),r=await f.store.submit(input,'client');
  assert.equal((await f.store.receipt(r.id,input.management_key)).body,original);
  await f.store.moderate(r.id,{action:'publish',revision:1,reason:'inert synthetic markup'},'operator');
  const html=await (await f.call('/')).text();
  assert.ok(html.includes('&lt;script&gt;'));assert.ok(!html.includes('<script>'));
  await expectProblem(f.store.submit(draft('😀'.repeat(4001)),'client'),'INVALID_TEXT');
  await expectProblem(f.store.submit(draft('bad\0text'),'client'),'INVALID_TEXT');
  const oversized=await f.call('/api/submit',{...draft(),body:'x'.repeat(70000)});assert.equal(oversized.status,413);
  const valid=await f.store.submit(draft('😀'.repeat(4000)),'other');assert.equal([...valid.body].length,4000);
});
test('failed HTML send preserves unsent text and the original retry keys',async t=>{
  const f=fixture(t),input=draft('Keep this synthetic unsent text');
  const req=new Request(f.env.APP_ORIGIN+'/submit',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded',Origin:f.env.APP_ORIGIN},body:new URLSearchParams(input)});
  const result=await handle(req,f.env),html=await result.text();assert.equal(result.status,503);
  for(const value of [input.body,input.retry_key,input.management_key])assert.ok(html.includes(value));
});
test('public hosting, cross-origin posting and credentials in query strings are refused',async t=>{
  const f=fixture(t);
  const remote=await handle(new Request('https://discuss.pleasestartfromhere.com/'),f.env);assert.equal(remote.status,503);
  const cross=await handle(new Request(f.env.APP_ORIGIN+'/api/submit',{method:'POST',headers:{'Content-Type':'application/json',Origin:'https://example.com'},body:JSON.stringify(draft())}),f.env);assert.equal(cross.status,403);
  assert.equal((await handle(new Request(f.env.APP_ORIGIN+'/api/manage?key=secret'),f.env)).status,400);
});
async function compete(path,inputs){
  const gate=new SharedArrayBuffer(4),view=new Int32Array(gate),workers=[];
  for(let i=0;i<inputs.length;i++){
    const w=new Worker(new URL('./contender.js',import.meta.url),{workerData:{path,gate,now:fixed,input:inputs[i],client:'worker'+i},execArgv:[]});
    const ready=once(w,'message');
    const result=new Promise((resolve,reject)=>{w.on('message',m=>{if(!m.ready)resolve(m);});w.on('error',reject);});
    workers.push({w,ready,result});
  }
  await Promise.all(workers.map(w=>w.ready));Atomics.store(view,0,1);Atomics.notify(view,0);
  const results=await Promise.all(workers.map(w=>w.result));await Promise.all(workers.map(({w})=>w.terminate()));return results;
}
test('five simultaneous connections compete for one queue slot: exactly one is admitted',async t=>{
  const f=fixture(t);await f.store.readiness(true);f.db.sql.exec('UPDATE service SET pending_limit=1');
  const results=await compete(f.path,Array.from({length:5},()=>draft()));
  assert.equal(results.filter(r=>r.ok).length,1);assert.equal(results.filter(r=>r.code==='QUEUE_FULL').length,4);
  assert.equal(f.db.sql.prepare('SELECT COUNT(*) AS n FROM contributions').get().n,1);
});
test('simultaneous retries recover the same record despite a one-slot queue',async t=>{
  const f=fixture(t);await f.store.readiness(true);f.db.sql.exec('UPDATE service SET pending_limit=1');
  const input=draft(),results=await compete(f.path,Array.from({length:5},()=>input));
  assert.equal(results.filter(r=>r.ok).length,5);assert.equal(new Set(results.map(r=>r.id)).size,1);
  assert.equal(f.db.sql.prepare('SELECT COUNT(*) AS n FROM contributions').get().n,1);
});

test('HTTP lifecycle across SIGKILL and restart uses the same disk receipt',async t=>{
  const dir=mkdtempSync(join(tmpdir(),'psfh-http-')),path=join(dir,'durable.sqlite');
  const adminToken=newKey(),rateSecret=newKey();let child;let logs='';
  t.after(async()=>{if(child&&child.exitCode===null){const end=once(child,'exit');child.kill('SIGTERM');await end;}rmSync(dir,{recursive:true,force:true});});
  async function start(){
    child=fork(new URL('../src/local-server.js',import.meta.url),[],{silent:true,execArgv:[],env:{...process.env,PORT:'0',PSFH_DB:path,PSFH_ADMIN_TOKEN:adminToken,PSFH_RATE_SECRET:rateSecret}});
    child.stdout.on('data',b=>{logs+=b;});child.stderr.on('data',b=>{logs+=b;});
    const timeout=setTimeout(()=>child.kill('SIGKILL'),10000);
    const [msg]=await once(child,'message');clearTimeout(timeout);return msg.origin;
  }
  let origin=await start();
  const send=async(path,input,admin=false)=>fetch(origin+path,{method:'POST',headers:{'Content-Type':'application/json',...(admin?{Authorization:'Bearer '+adminToken}:{})},body:JSON.stringify(input)});
  assert.equal((await send('/api/admin',{action:'ready'},true)).status,200);
  const root=await (await fetch(origin+'/')).text();
  const input={body:'Synthetic lifecycle objection',display_name:'Invented contributor',
    retry_key:root.match(/name="retry_key" value="([^"]+)"/)[1],
    management_key:root.match(/name="management_key" value="([^"]+)"/)[1]};
  const first=await fetch(origin+'/submit',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded',Origin:origin},body:new URLSearchParams(input)});
  assert.equal(first.status,200);await first.body.cancel(); // Application never consumes the receipt.
  const dead=once(child,'exit');child.kill('SIGKILL');await dead;origin=await start();
  await send('/api/admin',{action:'pause'},true);
  const recovered=await send('/api/submit',input),r=await recovered.json();assert.equal(recovered.status,200);assert.equal(r.state,'pending');
  const queue=await (await send('/api/admin',{action:'queue'},true)).json();assert.equal(queue.queue.length,1);
  assert.deepEqual((await (await fetch(origin+'/api/posts')).json()).posts,[]);
  assert.equal((await send('/api/admin',{action:'publish',id:r.id,revision:r.revision,reason:'Reviewed invented text'},true)).status,200);
  assert.equal((await send('/api/admin',{action:'respond',id:r.id,revision:r.revision,body:'This is a separately attributed project reply.'},true)).status,200);
  const published=(await (await fetch(origin+'/api/posts')).json()).posts;assert.equal(published.length,1);assert.equal(published[0].responses.length,1);
  assert.equal((await send('/api/manage',{action:'withdraw',id:r.id,management_key:input.management_key})).status,200);
  assert.deepEqual((await (await fetch(origin+'/api/posts')).json()).posts,[]);
  for(const secret of [adminToken,rateSecret,input.management_key,input.retry_key])assert.ok(!logs.includes(secret));
});

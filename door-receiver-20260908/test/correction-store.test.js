import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync,readFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {SqliteAdapter} from '../src/sqlite-adapter.js';
import {newKey,Problem} from '../src/store.js';
import {CorrectionStore} from '../src/correction-store.js';

const fixed=Date.parse('2026-09-08T17:00:00Z');
function fixture(t){
  const dir=mkdtempSync(join(tmpdir(),'psfh-correction-')),db=new SqliteAdapter(join(dir,'test.sqlite'));
  db.sql.exec(readFileSync(new URL('../migrations/0002_correction_requests.sql',import.meta.url),'utf8'));
  const store=new CorrectionStore(db,()=>fixed);
  t.after(()=>{db.close();rmSync(dir,{recursive:true,force:true});});
  return {db,store};
}
function draft(target='00000000-0000-4000-8000-000000000001'){
  return {target_id:target,kind:'privacy',note:'Please review material that appears to concern me.',retry_key:newKey(),management_key:newKey()};
}
async function expectProblem(promise,code){await assert.rejects(promise,e=>e instanceof Problem&&e.code===code);}

test('correction request remains available while ordinary intake is paused',async t=>{
  const f=fixture(t);f.db.sql.exec('UPDATE service SET enabled=0,pending_limit=1,body_limit=1');
  const input=draft(),r=await f.store.submit(input,'client-a');
  assert.equal(r.state,'pending');
  assert.equal(r.target_id,input.target_id);
  assert.equal(f.db.sql.prepare('SELECT COUNT(*) AS n FROM correction_events').get().n,1);
});

test('correction requests have reserved capacity separate from contribution queue',async t=>{
  const f=fixture(t);f.db.sql.exec('UPDATE service SET correction_limit=1');
  await f.store.submit(draft(),'a');
  await expectProblem(f.store.submit(draft('00000000-0000-4000-8000-000000000002'),'b'),'CORRECTION_QUEUE_FULL');
});

test('retry identity recovers one request and rejects changed content',async t=>{
  const f=fixture(t),input=draft();
  const first=await f.store.submit(input,'client');
  const retry=await f.store.submit(input,'client');
  assert.equal(retry.id,first.id);
  assert.equal(f.db.sql.prepare('SELECT COUNT(*) AS n FROM correction_requests').get().n,1);
  await expectProblem(f.store.submit({...input,note:'Different note'},'client'),'CORRECTION_RETRY_CONFLICT');
});

test('reporter can privately inspect then withdraw while ordinary intake remains paused',async t=>{
  const f=fixture(t),input=draft(),r=await f.store.submit(input,'client');
  assert.equal((await f.store.receipt(r.id,input.management_key)).note,input.note);
  const closed=await f.store.withdraw(r.id,input.management_key);
  assert.equal(closed.state,'withdrawn');assert.equal(closed.note,'');
  assert.equal((await f.store.queue()).length,0);
  await expectProblem(f.store.receipt(r.id,newKey()),'CORRECTION_RECEIPT_UNAVAILABLE');
});

test('operator resolution is explicit and does not itself mutate the target contribution',async t=>{
  const f=fixture(t),input=draft(),r=await f.store.submit(input,'client');
  const result=await f.store.resolve(r.id,{outcome:'content_removed',reason:'Synthetic operator disposition only'},'operator');
  assert.equal(result.state,'resolved');assert.equal(result.operator_outcome,'content_removed');
  assert.equal(f.db.sql.prepare('SELECT COUNT(*) AS n FROM contributions').get().n,0);
  const actions=f.db.sql.prepare('SELECT action FROM correction_events ORDER BY id').all().map(x=>x.action);
  assert.deepEqual(actions,['received','resolved']);
  await expectProblem(f.store.resolve(r.id,{outcome:'no_change',reason:'stale'},'operator'),'CORRECTION_STATE_CONFLICT');
});

test('unauthenticated report never auto-hides or publishes anything',async t=>{
  const f=fixture(t),input=draft();await f.store.submit(input,'client');
  assert.equal(f.db.sql.prepare("SELECT COUNT(*) AS n FROM contributions WHERE state='published'").get().n,0);
  assert.equal((await f.store.queue()).length,1);
});

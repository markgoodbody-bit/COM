import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {SqliteAdapter} from '../src/sqlite-adapter.js';
import {Store,Problem,newKey,ATTENDED_LEASE_MS} from '../src/store.js';

const fixed=Date.parse('2026-09-08T18:00:00Z');
function fixture(t){
  const dir=mkdtempSync(join(tmpdir(),'psfh-attended-')),db=new SqliteAdapter(join(dir,'test.sqlite'));let now=fixed;
  const store=new Store(db,()=>now);
  t.after(()=>{db.close();rmSync(dir,{recursive:true,force:true});});
  return {store,advance:ms=>{now+=ms;},now:()=>now};
}
function draft(body='Synthetic attended-window message'){
  return {body,display_name:'Invented reader',retry_key:newKey(),management_key:newKey()};
}
async function expectProblem(promise,code){await assert.rejects(promise,e=>e instanceof Problem&&e.code===code);}

test('ready opens exactly one one-hour attended lease then closes new intake',async t=>{
  const f=fixture(t),start=f.now();
  const lease=await f.store.readiness(true);
  assert.equal(lease.enabled,true);
  assert.equal(lease.ready_until,start+ATTENDED_LEASE_MS);
  assert.equal((await f.store.submit(draft('within lease'),'client-a')).state,'pending');
  f.advance(ATTENDED_LEASE_MS+1);
  await expectProblem(f.store.submit(draft('after lease'),'client-b'),'INTAKE_PAUSED');
});

test('authorised renewal extends from current time and pause closes immediately',async t=>{
  const f=fixture(t);await f.store.readiness(true);
  f.advance(30*60*1000);
  const renewed=await f.store.readiness(true);
  assert.equal(renewed.ready_until,f.now()+ATTENDED_LEASE_MS);
  assert.equal((await f.store.submit(draft('after renewal'),'client-a')).state,'pending');
  const paused=await f.store.readiness(false);
  assert.deepEqual(paused,{enabled:false,ready_until:0});
  await expectProblem(f.store.submit(draft('after pause'),'client-b'),'INTAKE_PAUSED');
});

test('lease expiry blocks only new intake; existing owner can still inspect and withdraw',async t=>{
  const f=fixture(t);await f.store.readiness(true);const input=draft(),receipt=await f.store.submit(input,'client-a');
  f.advance(ATTENDED_LEASE_MS+1);
  await expectProblem(f.store.submit(draft('new'),'client-b'),'INTAKE_PAUSED');
  assert.equal((await f.store.receipt(receipt.id,input.management_key)).state,'pending');
  const withdrawn=await f.store.withdraw(receipt.id,input.management_key);
  assert.equal(withdrawn.state,'withdrawn');
  assert.equal(withdrawn.body,null);
});

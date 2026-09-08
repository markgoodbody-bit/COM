import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {SqliteAdapter} from '../src/sqlite-adapter.js';
import {newKey,Problem} from '../src/store.js';
import {edgeAdmission} from '../src/edge-admission.js';
import {handle} from '../src/router.js';

const fixed=Date.parse('2026-09-08T18:30:00Z');
function fixture(t){
  const dir=mkdtempSync(join(tmpdir(),'psfh-edge-admission-')),db=new SqliteAdapter(join(dir,'test.sqlite'));
  t.after(()=>{db.close();rmSync(dir,{recursive:true,force:true});});
  const env={DB:db,ADMIN_TOKEN:newKey(),RATE_SECRET:newKey(),SYNTHETIC_ONLY:'true',APP_ORIGIN:'http://127.0.0.1:8788'};
  return {db,env};
}
function endlessJsonStream(){
  const state={pulls:0};
  const body=new ReadableStream({pull(controller){state.pulls++;controller.enqueue(new Uint8Array(1024).fill(32));if(state.pulls===1000)controller.close();}});
  return {body,state};
}
function post(env,path,body,headers={}){
  return handle(new Request(env.APP_ORIGIN+path,{method:'POST',headers:{'Content-Type':'application/json',...headers},body,duplex:'half'}),env,()=>fixed);
}

test('contribution edge denial happens before request body is consumed',async t=>{
  const {env}=fixture(t),keys=[];
  env.CONTRIBUTION_RATE_LIMITER={limit:async({key})=>{keys.push(key);return {success:false};}};
  const stream=endlessJsonStream();
  const response=await post(env,'/api/submit',stream.body);
  assert.equal(response.status,429);
  assert.equal((await response.json()).error,'CONTRIBUTION_EDGE_RATE_LIMITED');
  assert.ok(stream.state.pulls<10,`body was pulled ${stream.state.pulls} times before edge refusal`);
  assert.deepEqual(keys,['psfh:contribution']);
});

test('correction has a distinct reserved edge budget and also refuses before body read',async t=>{
  const {env}=fixture(t),contributionKeys=[],correctionKeys=[];
  env.CONTRIBUTION_RATE_LIMITER={limit:async({key})=>{contributionKeys.push(key);return {success:true};}};
  env.CORRECTION_RATE_LIMITER={limit:async({key})=>{correctionKeys.push(key);return {success:false};}};
  const stream=endlessJsonStream();
  const response=await post(env,'/api/correction',stream.body);
  assert.equal(response.status,429);
  assert.equal((await response.json()).error,'CORRECTION_EDGE_RATE_LIMITED');
  assert.ok(stream.state.pulls<10);
  assert.deepEqual(correctionKeys,['psfh:correction']);
  assert.deepEqual(contributionKeys,[],'ordinary budget must not be consumed by correction traffic');
});

test('local synthetic receiver remains runnable without provider rate-limit bindings',async t=>{
  const {env}=fixture(t);
  const body=JSON.stringify({body:'synthetic',display_name:'x',retry_key:newKey(),management_key:newKey()});
  const response=await post(env,'/api/submit',body);
  assert.equal(response.status,503);
  assert.equal((await response.json()).error,'INTAKE_PAUSED');
});

test('future non-synthetic mode fails closed if edge binding is absent',async()=>{
  await assert.rejects(()=>edgeAdmission({SYNTHETIC_ONLY:'false'},'contribution'),
    error=>error instanceof Problem&&error.status===503&&error.code==='EDGE_RATE_LIMIT_NOT_CONFIGURED');
});

test('edge keys are class based rather than visitor supplied identifiers',async()=>{
  const seen=[];
  const env={SYNTHETIC_ONLY:'false',
    CONTRIBUTION_RATE_LIMITER:{limit:async input=>{seen.push(input);return {success:true};}},
    CORRECTION_RATE_LIMITER:{limit:async input=>{seen.push(input);return {success:true};}}};
  assert.deepEqual(await edgeAdmission(env,'contribution'),{enforced:true});
  assert.deepEqual(await edgeAdmission(env,'correction'),{enforced:true});
  assert.deepEqual(seen,[{key:'psfh:contribution'},{key:'psfh:correction'}]);
});

import test from 'node:test';
import assert from 'node:assert/strict';
import {fork,spawnSync} from 'node:child_process';
import {once} from 'node:events';
import {mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,resolve,relative} from 'node:path';
import {fileURLToPath} from 'node:url';
import {newKey} from '../src/store.js';

test('actual operator CLI can review and answer; contributor reads answer via own receipt',async t=>{
  const dir=mkdtempSync(join(tmpdir(),'psfh-operator-flow-'));
  const token=newKey(),rate=newKey();let logs='';
  const server=fork(new URL('../src/local-server.js',import.meta.url),[],{
    silent:true,execArgv:[],env:{...process.env,PORT:'0',PSFH_DB:join(dir,'synthetic.sqlite'),PSFH_ADMIN_TOKEN:token,PSFH_RATE_SECRET:rate}
  });
  server.stdout.on('data',b=>{logs+=b;});server.stderr.on('data',b=>{logs+=b;});
  t.after(async()=>{
    if(server.exitCode===null&&server.signalCode===null){const end=once(server,'exit');server.kill('SIGTERM');await end;}
    const rel=relative(resolve(tmpdir()),resolve(dir));
    assert.ok(rel&&!rel.startsWith('..')&&!rel.includes(':'),'cleanup stays in synthetic temp directory');
    rmSync(dir,{recursive:true,force:true});
  });
  const ready=once(server,'message');
  const deadline=setTimeout(()=>server.kill('SIGKILL'),10000);
  let origin;
  try{
    const result=await Promise.race([ready,once(server,'exit').then(()=>{throw Error('synthetic server exited before ready');})]);
    origin=result[0].origin;
  }finally{clearTimeout(deadline);}
  const cli=(action,input,credential=token)=>{
    const result=spawnSync(process.execPath,[fileURLToPath(new URL('../src/operator-cli.js',import.meta.url)),action],{
      env:{...process.env,PSFH_OPERATOR_URL:origin,PSFH_ADMIN_TOKEN:credential},
      input:input?JSON.stringify(input):'',encoding:'utf8',timeout:5000,windowsHide:true
    });
    assert.ifError(result.error);
    logs+=result.stdout+result.stderr;
    return {status:result.status,stdout:result.stdout,stderr:result.stderr};
  };
  const ok=(action,input)=>{const r=cli(action,input);assert.equal(r.status,0,`${action} failed`);return JSON.parse(r.stdout);};
  const send=(path,input)=>fetch(origin+path,{method:'POST',headers:{'Content-Type':'application/json',Origin:origin},body:JSON.stringify(input)});
  const bad=cli('queue',undefined,newKey());assert.equal(bad.status,1);assert.match(bad.stderr,/401_MODERATOR_AUTH_REQUIRED/);
  assert.equal(ok('ready').enabled,true);
  const form=await (await fetch(origin+'/')).text();
  const draft={body:'SYNTHETIC: I disagree with this example.',display_name:'Invented reader',
    retry_key:form.match(/name="retry_key" value="([^"]+)"/)[1],management_key:form.match(/name="management_key" value="([^"]+)"/)[1]};
  const sent=await fetch(origin+'/submit',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded',Origin:origin},body:new URLSearchParams(draft)});
  assert.equal(sent.status,200);await sent.body.cancel();
  const receipt=await (await send('/api/submit',draft)).json();
  assert.equal(receipt.state,'pending');
  const queued=ok('queue').queue;assert.equal(queued.length,1);assert.equal(queued[0].body,draft.body);
  assert.equal(queued[0].id,receipt.id);assert.equal(ok('pause').enabled,false);
  const reason='SYNTHETIC review: relevant disagreement; no private details.';
  assert.equal(ok('publish',{id:receipt.id,revision:receipt.revision,reason}).state,'published');
  const responseText='SYNTHETIC answer: the example needs a clearer limit. <not executable>';
  assert.equal(ok('respond',{id:receipt.id,revision:receipt.revision,body:responseText}).responded,true);
  const managed={action:'receipt',id:receipt.id,management_key:draft.management_key};
  const wrong=await send('/api/manage',{...managed,management_key:newKey()});assert.equal(wrong.status,404);
  const ownerReceipt=await (await send('/api/manage',managed)).json();
  assert.equal(ownerReceipt.state,'published');assert.equal(ownerReceipt.moderation_reason,reason);
  assert.equal(ownerReceipt.responses?.length,1,'private receipt must carry the project answer');
  assert.equal(ownerReceipt.responses[0].body,responseText);
  assert.equal(ownerReceipt.responses[0].actor,'authorised-local-operator');
  const html=await (await fetch(origin+'/manage',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded',Origin:origin},body:new URLSearchParams(managed)})).text();
  assert.ok(html.includes('&lt;not executable&gt;'));assert.ok(!html.includes('<not executable>'));
  const withdrawn=await (await send('/api/manage',{...managed,action:'withdraw'})).json();
  assert.equal(withdrawn.state,'withdrawn');assert.equal(withdrawn.body,null);
  const after=await (await send('/api/manage',managed)).json();assert.deepEqual(after.responses,[]);
  assert.deepEqual((await (await fetch(origin+'/api/posts')).json()).posts,[]);
  for(const secret of [token,rate,draft.retry_key,draft.management_key])assert.ok(!logs.includes(secret),'private key absent from captured process output');
});

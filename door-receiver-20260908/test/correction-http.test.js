import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {SqliteAdapter} from '../src/sqlite-adapter.js';
import {newKey} from '../src/store.js';
import {handle} from '../src/router.js';

const fixed=Date.parse('2026-09-08T17:10:00Z');
function fixture(t){
  const dir=mkdtempSync(join(tmpdir(),'psfh-correction-http-')),db=new SqliteAdapter(join(dir,'test.sqlite'));
  t.after(()=>{db.close();rmSync(dir,{recursive:true,force:true});});
  const env={DB:db,ADMIN_TOKEN:newKey(),RATE_SECRET:newKey(),SYNTHETIC_ONLY:'true',APP_ORIGIN:'http://127.0.0.1:8788'};
  const call=(path,input,auth=false)=>handle(new Request(env.APP_ORIGIN+path,{method:input?'POST':'GET',headers:{'Content-Type':'application/json',...(auth?{Authorization:'Bearer '+env.ADMIN_TOKEN}:{})},...(input?{body:JSON.stringify(input)}:{})}),env,()=>fixed);
  return {db,env,call};
}
function report(){return {target_id:'00000000-0000-4000-8000-000000000001',kind:'privacy',note:'Please review this synthetic item.',retry_key:newKey(),management_key:newKey()};}

test('HTTP correction route works while contribution intake stays paused',async t=>{
  const f=fixture(t),input=report();
  assert.equal((await f.call('/api/submit',{body:'ordinary',display_name:'x',retry_key:newKey(),management_key:newKey()})).status,503);
  const stored=await f.call('/api/correction',input);assert.equal(stored.status,200);
  const receipt=await stored.json();assert.equal(receipt.state,'pending');
  assert.equal((await f.call('/api/admin',{action:'corrections'})).status,401);
  const queue=await (await f.call('/api/admin',{action:'corrections'},true)).json();
  assert.equal(queue.corrections.length,1);assert.equal(queue.corrections[0].id,receipt.id);
});

test('reporter can inspect and withdraw through HTTP without opening contribution intake',async t=>{
  const f=fixture(t),input=report(),receipt=await (await f.call('/api/correction',input)).json();
  let r=await f.call('/api/correction-manage',{action:'receipt',id:receipt.id,management_key:input.management_key});
  assert.equal(r.status,200);assert.equal((await r.json()).note,input.note);
  r=await f.call('/api/correction-manage',{action:'withdraw',id:receipt.id,management_key:input.management_key});
  assert.equal((await r.json()).state,'withdrawn');
  const q=await (await f.call('/api/admin',{action:'corrections'},true)).json();assert.equal(q.corrections.length,0);
});

test('operator resolution records an outcome but does not automatically mutate target content',async t=>{
  const f=fixture(t),input=report(),receipt=await (await f.call('/api/correction',input)).json();
  const resolved=await f.call('/api/admin',{action:'resolve-correction',id:receipt.id,outcome:'no_change',reason:'Synthetic review found no target content to change.'},true);
  assert.equal(resolved.status,200);assert.equal((await resolved.json()).operator_outcome,'no_change');
  assert.equal(f.db.sql.prepare('SELECT COUNT(*) AS n FROM contributions').get().n,0);
});

test('browser correction form exists but remains inside the hard local-only receiver guard',async t=>{
  const f=fixture(t),page=await f.call('/report');assert.equal(page.status,200);
  const text=await page.text();assert.match(text,/not an automatic takedown/i);assert.match(text,/Save both private keys/i);
  const remote={...f.env,APP_ORIGIN:'https://discussion.example.test'};
  const blocked=await handle(new Request(remote.APP_ORIGIN+'/report'),remote,()=>fixed);assert.equal(blocked.status,503);
});

test('oversized unlabelled streams stop early on correction and admin routing',async t=>{
  const f=fixture(t);
  for(const path of ['/api/correction','/api/admin']){
    let pulls=0;
    const body=new ReadableStream({pull(controller){
      pulls++;controller.enqueue(new Uint8Array(1024).fill(32));
      if(pulls===1000)controller.close();
    }});
    const response=await handle(new Request(f.env.APP_ORIGIN+path,{method:'POST',headers:{'Content-Type':'application/json'},body,duplex:'half'}),f.env,()=>fixed);
    assert.equal(response.status,413);
    assert.ok(pulls<100,`${path} consumed ${pulls} chunks before refusing`);
  }
});

test('failed browser report preserves selected reason with original retry keys',async t=>{
  const f=fixture(t),input={...report(),target_id:'',kind:'misattribution'};
  const response=await handle(new Request(f.env.APP_ORIGIN+'/report',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(input)}),f.env,()=>fixed);
  assert.equal(response.status,400);
  const html=await response.text();
  assert.match(html,/<option value="misattribution" selected>/);
  assert.ok(html.includes(input.retry_key));assert.ok(html.includes(input.management_key));
});

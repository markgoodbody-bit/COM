import test from 'node:test';
import assert from 'node:assert/strict';
import {reconcile} from './reconcile.mjs';
const epoch='a'.repeat(32),url='https://github.com/markgoodbody-bit/COM/issues/760';
function fixture() {
  const messages=[{epoch,sender:'framework',request_key:'one',recipient:'shared',kind:'message',body:'same',github_anchor:null,seq:1},
    {epoch,sender:'framework',request_key:'two',recipient:'shared',kind:'message',body:'same',github_anchor:null,seq:2},
    {epoch,sender:'claude',request_key:'three',recipient:'codex',kind:'decision',body:'decision',github_anchor:url,seq:3}];
  const collection={started_at:100,ended_at:100,page_count:1,last_page_complete:true,last_next:null,head_seq_at_start:3,head_seq_at_end:3};
  return {aperture:'codex',github:{epoch,scope:'synthetic-run',complete:true,collection,messages:messages.map(m=>({...m,witness_url:url+'#issuecomment-'+m.seq}))},
    bus:{epoch,scope:'synthetic-run',complete:true,head_seq:3,retained_after:0,checkpoint_version:0,consumed:0,
      aperture:'codex',window:{from_seq:0,to_seq:3,row_count:3},collection,
      server_time:100,head_bounds:{max_age_seconds:60,max_lag:50},
      comhead:{basis_seq:3,updated_at:100,freshness:'CURRENT',github_anchor:url},messages}};
}
test('reconciler matches explicit identities, reports repeats, never mutates inputs',()=>{
  const input=fixture(),before=JSON.stringify(input),r=reconcile(input);
  assert.equal(r.status,'SUPPLIED_SNAPSHOTS_MATCH'); assert.equal(r.sync_complete,false);
  assert.equal(JSON.stringify(input),before); assert.equal(r.repeated_shared[0].count,2);
  assert.deepEqual(r.messages.map(m=>m.routing),['shared','shared','direct']);
});
test('same body cannot replace stable identity; absence fails closed',()=>{
  const f=fixture();f.github.messages[0].request_key='unrelated';const r=reconcile(f);
  assert.equal(r.status,'UNKNOWN');assert.ok(r.issues.some(i=>i.code==='BUS_ONLY'));
  assert.ok(r.issues.some(i=>i.code==='GITHUB_ONLY'));assert.equal(r.authority_winner,null);
});
test('routing, decision anchor and body disagreements stay explicit',()=>{
  for(const [field,value] of [['recipient','claude'],['body','different'],['github_anchor',null]]) {
    const f=fixture();f.bus.messages[2][field]=value;const r=reconcile(f);
    assert.equal(r.status,'UNKNOWN');assert.ok(r.issues.some(i=>i.code==='MESSAGE_DIFFERENCE'));
    if(field==='github_anchor') assert.ok(r.issues.some(i=>i.code==='DECISION_ANCHOR_MISSING'));
  }
});
test('incomplete scope, epoch, checkpoint, gap and head cannot manufacture agreement',()=>{
  for(const change of [f=>f.github.complete=false,f=>f.github.epoch='b'.repeat(32),f=>f.bus.retained_after=1,
    f=>f.bus.checkpoint_version=1,f=>f.bus.comhead.freshness='STALE',f=>f.bus.comhead=null]) {
    const f=fixture();change(f);assert.equal(reconcile(f).status,'UNKNOWN');
  }
});
test('duplicate identity/sequence, missing witness and bounds refuse',()=>{
  for(const change of [f=>f.bus.messages.push({...f.bus.messages[0]}),f=>f.bus.messages[1].seq=1,
    f=>delete f.github.messages[0].witness_url,f=>f.bus.messages=Array(1001).fill(f.bus.messages[0])]) {
    const f=fixture();change(f);assert.equal(reconcile(f).status,'UNKNOWN');
  }
  assert.equal(reconcile().status,'UNKNOWN');
});
test('ack evidence is explicit; history disposition and malformed accounting refuse',()=>{
  const f=fixture();f.bus.messages[2].my_disposition=JSON.stringify({seq:3,no_answer_owed:'observed reason'});
  assert.equal(reconcile(f).status,'SUPPLIED_SNAPSHOTS_MATCH');
  f.aperture='other';assert.ok(reconcile(f).issues.some(i=>i.code==='OTHER_RECIPIENT_DISPOSITION'));
  f.bus.messages[2].my_disposition='broken';assert.ok(reconcile(f).issues.some(i=>i.code==='INVALID_OBSERVED_DISPOSITION'));
});
test('claimed CURRENT cannot conceal expired COMHEAD or absent freshness evidence',()=>{
  const f=fixture();f.bus.server_time=200;
  assert.ok(reconcile(f).issues.some(i=>i.code==='COMHEAD_FRESHNESS_DIFFERENCE'));
  assert.equal(reconcile(f).state.comhead.freshness,'STALE');
  delete f.bus.head_bounds;
  assert.ok(reconcile(f).issues.some(i=>i.code==='COMHEAD_FRESHNESS_UNVERIFIED'));
});
test('CC R1-R6: coverage, witness uniqueness, aperture and collection markers required',()=>{
  for(const change of [f=>{f.bus.messages=f.bus.messages.slice(0,1);f.github.messages=f.github.messages.slice(0,1);},
    f=>{f.bus.messages=[];f.github.messages=[];},f=>f.github.messages.forEach(m=>m.witness_url=url),
    f=>f.github.messages[1].witness_url=f.github.messages[0].witness_url,
    f=>f.aperture='claude',f=>{delete f.bus.collection;delete f.github.collection;}]) {
    const f=fixture();change(f);assert.equal(reconcile(f).status,'UNKNOWN');
  }
});

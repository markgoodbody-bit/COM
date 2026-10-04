import test from 'node:test';
import assert from 'node:assert/strict';
import {collect,readOnlyReader} from './collect.mjs';
const epoch='a'.repeat(32),url='https://github.com/markgoodbody-bit/COM/issues/760';
const marker={aperture:'codex',epoch,head_seq:101,retained_after:0,checkpoint_version:0,consumed:0,server_time:100};
function fixture() {
  const calls=[];
  const rows=Array.from({length:101},(_,i)=>({epoch,seq:i+1,sender:'codex',request_key:'trial.'+(i+1),recipient:'shared',kind:'message',body:'synthetic '+i,github_anchor:null}));
  const comments=rows.map((row,i)=>({id:i+1,html_url:url+'#issuecomment-'+(i+1),updated_at:'fixed',user:{login:'markgoodbody-bit'},body:'COM_SHADOW_V1\n'+JSON.stringify({scope:'trial',message:row})}));
  const json=data=>({status:200,raw:JSON.stringify(data),link:null});
  const readGithub=async path=>{
    calls.push(['github',path]);
    if(path.includes('/comments?')) {const page=Number(new URL('https://api.github.com'+path).searchParams.get('page'));return {...json(comments.slice((page-1)*100,page*100)),link:page===1?'<https://api.github.com/repos/markgoodbody-bit/COM/issues/760/comments?per_page=100&page=2>; rel="next"':null};}
    return json({number:760,comments:comments.length,html_url:url,updated_at:'fixed'});
  };
  const readBus=async path=>{
    calls.push(['bus',path]);
    if(path.includes('/history?')) {const after=Number(new URL('https://bus.invalid'+path).searchParams.get('after'));return json({...marker,window_row_count:101,history_only:true,messages:rows.filter(r=>r.seq>after).slice(0,100),has_more:rows.filter(r=>r.seq>after).length>100});}
    if(path==='/v1/head') return json({...marker,snapshot:{version:1,basis_seq:101,updated_at:100,github_anchor:url},freshness:'CURRENT'});
    if(path==='/v1/recovery') return json({...marker,checkpoint:null});
    return json(marker);
  };
  return {calls,rows,comments,readGithub,readBus,json,args:{readGithub,readBus,issue:760,scope:'trial',aperture:'codex',epoch,
    head_bounds:{max_age_seconds:60,max_lag:50},trusted_authors:{codex:['markgoodbody-bit']}}};
}
test('independent twice-paginated sources match with reproducible private receipts',async()=>{
  const f=fixture(),before=JSON.stringify([f.rows,f.comments]),r=await collect(f.args);
  assert.equal(r.status,'SUPPLIED_SNAPSHOTS_MATCH');assert.equal(r.messages.length,101);
  assert.equal(r.sync_complete,false);assert.equal(JSON.stringify([f.rows,f.comments]),before);
  assert.equal(f.calls.filter(([s,p])=>s==='github'&&p.includes('page=2')).length,2);
  assert.equal(f.calls.filter(([s,p])=>s==='bus'&&p.includes('after=100')).length,2);
  assert.ok(r.source_receipts.every(r=>r.sha256.length===64&&r.raw));
  assert.ok(f.calls.every(([,p])=>!p.includes('/ack')&&!p.includes('/messages')));
});
test('pagination omission, failed page and stalled/repeated bus rows stay UNKNOWN',async()=>{
  for(const mutate of [
    f=>({...f.args,readGithub:async p=>p.includes('page=2')?f.json([]):f.readGithub(p)}),
    f=>({...f.args,readGithub:async p=>p.includes('page=2')?{status:503,raw:'{}'}:f.readGithub(p)}),
    f=>({...f.args,readBus:async p=>p.includes('after=100')?f.json({...marker,history_only:true,messages:[],has_more:true}):f.readBus(p)}),
    f=>({...f.args,readBus:async p=>p.includes('after=100')?f.json({...marker,history_only:true,messages:[f.rows[0]],has_more:false}):f.readBus(p)})]) {
    const f=fixture();assert.equal((await collect(mutate(f))).status,'UNKNOWN');
  }
});
test('body edit without GitHub marker change is caught across complete scans',async()=>{
  const f=fixture();let firstPages=0;
  const readGithub=async p=>{if(p.includes('page=1')&&++firstPages===2) f.comments[0].body+=' ';return f.readGithub(p);};
  const r=await collect({...f.args,readGithub});assert.equal(r.status,'UNKNOWN');
  assert.equal(r.issues[0].code,'SOURCE_CHANGED_ACROSS_COLLECTION');
});
test('bus head/ack changes, epoch changes and unaccounted retained floor refuse',async()=>{
  for(const change of [{head_seq:102},{epoch:'b'.repeat(32)},{retained_after:1}]) {
    const f=fixture();const readBus=async p=>p==='/v1/state'?f.json({...marker,...change}):f.readBus(p);
    assert.equal((await collect({...f.args,readBus})).status,'UNKNOWN');
  }
  const f=fixture();let pages=0;
  const readBus=async p=>{if(p.includes('after=0')&&++pages===2) f.rows[0].my_disposition={seq:1,no_answer_owed:'changed'};return f.readBus(p);};
  assert.equal((await collect({...f.args,readBus})).issues[0].code,'SOURCE_CHANGED_ACROSS_COLLECTION');
});
test('source author, witness URL and anchor existence are independently checked',async()=>{
  for(const change of [f=>f.comments[0].user.login='stranger',f=>f.comments[0].html_url=url+'#issuecomment-999']) {
    const f=fixture();change(f);assert.equal((await collect(f.args)).status,'UNKNOWN');
  }
  const f=fixture();const readGithub=async p=>p.endsWith('/issues/760')?f.json({number:760,comments:101,html_url:url,updated_at:'changing '+f.calls.length}):f.readGithub(p);
  assert.equal((await collect({...f.args,readGithub})).status,'UNKNOWN');
  const g=fixture();g.rows[0].github_anchor=url+'#issuecomment-999';
  assert.equal((await collect(g.args)).status,'UNKNOWN');
});
test('reader is GET-only, epoch-bound, refuses redirect/path escape, excludes bearer from receipts',async()=>{
  const seen=[];const reader=readOnlyReader({origin:'https://bus.invalid',service:'bus',epoch,token:'private',fetchImpl:async(u,options)=>{seen.push({u,options});return new Response('{}');}});
  const r=await reader('/v1/history?after=0&limit=100');
  assert.equal(seen[0].options.method,'GET');assert.equal(seen[0].options.redirect,'error');
  assert.equal(seen[0].options.headers['X-COM-Epoch'],epoch);assert.ok(!JSON.stringify(r).includes('private'));
  await assert.rejects(reader('/v1/ack'));assert.throws(()=>readOnlyReader({origin:'http://bus.invalid',service:'bus',epoch}));
  const gh=readOnlyReader({origin:'https://api.github.com',service:'github',fetchImpl:async()=>new Response('{}')});
  await assert.rejects(gh('/repos/markgoodbody-bit/COM/issues/../../other'));
});
test('missing Link receipt, duplicate source JSON keys and truncated bus count refuse',async()=>{
  const f=fixture();
  for(const readGithub of [async p=>{const r=await f.readGithub(p);delete r.link;return r;},
    async p=>p.includes('/comments?')?{status:200,link:null,raw:'[{"id":1,"id":2}]'}:f.readGithub(p)])
    assert.equal((await collect({...f.args,readGithub})).status,'UNKNOWN');
  const readBus=async p=>p.includes('/history?')?f.json({...marker,window_row_count:500,history_only:true,messages:[f.rows.at(-1)],has_more:false}):f.readBus(p);
  assert.equal((await collect({...f.args,readBus})).issues[0].code,'BUS_HEAD_OR_COUNT_NOT_REACHED');
});

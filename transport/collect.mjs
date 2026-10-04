import {reconcile} from './reconcile.mjs';
import {parsePayloadJson} from './worker.mjs';
const repository='/repos/markgoodbody-bit/COM';
const anchor=/^https:\/\/github\.com\/markgoodbody-bit\/COM\/(issues|pull)\/([1-9][0-9]*)(?:#issuecomment-([0-9]+))?$/;
const stable=value=>JSON.stringify(value);
const sha=async text=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text))),b=>b.toString(16).padStart(2,'0')).join('');
class Unknown extends Error {}

// Only GET, no redirect following and no credential in returned receipts.
// Reader origin/credential is configured by the caller, never source content.
export function readOnlyReader({origin,token,service,epoch,fetchImpl=fetch}) {
  const url=new URL(origin);
  if(url.protocol!=='https:'||url.username||url.password||url.pathname!=='/'||url.search||url.hash||
    !['github','bus'].includes(service)||(service==='github'&&url.origin!=='https://api.github.com')||
    (service==='bus'&&!/^[a-f0-9]{32}$/.test(epoch??''))) throw Error('INVALID_READER_ORIGIN');
  return async path=>{
    if(typeof path!=='string'||(service==='github'?!/^\/repos\/markgoodbody-bit\/COM\/issues\/(?:comments\/[1-9][0-9]*|[1-9][0-9]*(?:\/comments\?per_page=100&page=[1-9][0-9]*)?)$/.test(path):
      !/^\/v1\/(state|head|recovery|history)(?:\?|$)/.test(path))) throw Error('READ_PATH_NOT_ALLOWED');
    const response=await fetchImpl(url.origin+path,{method:'GET',redirect:'error',
      headers:{Accept:'application/json',...(token?{Authorization:'Bearer '+token}:{}),...(service==='bus'?{'X-COM-Epoch':epoch}:{})}});
    const raw=await response.text();
    if(new TextEncoder().encode(raw).length>524288) throw Error('READ_BODY_BOUND');
    return {status:response.status,raw,link:response.headers.get('link')};
  };
}

// Whole retained-window scans twice; never calls inbox (which issues receipts).
// Private evidence is separate from the shareable result by construction.
export async function collect({readGithub,readBus,issue=764,scope,aperture,epoch,head_bounds,trusted_authors}={}) {
  const receipts=[];
  const fail=reason=>({result:{status:'UNKNOWN',input_provenance:'COLLECTED',observation_only:true,sync_complete:false,authority_winner:null,
    issues:[{code:reason}]},private_receipts:receipts});
  if(typeof readGithub!=='function'||typeof readBus!=='function'||issue!==764||
    !/^[a-z0-9-]{1,64}$/.test(scope??'')||!/^[a-f0-9]{32}$/.test(epoch??'')||
    typeof aperture!=='string'||!trusted_authors||!head_bounds) return fail('INVALID_COLLECTION_CONFIG');
  let totalBytes=0;
  async function read(source,path,pass) {
    let response;
    try {response=await (source==='github'?readGithub:readBus)(path);} catch {
      receipts.push({source,path,pass,status:null,error:'READER_FAILURE'});throw new Unknown('SOURCE_READ_FAILED');
    }
    if(!response||typeof response.raw!=='string') throw new Unknown('SOURCE_READ_FAILED');
    const size=new TextEncoder().encode(response.raw).length;totalBytes+=size;
    if(size>524288||totalBytes>4194304) throw new Unknown('COLLECTION_BYTES_BOUND');
    const hash=await sha(response.raw);
    receipts.push({source,path,pass,status:response.status,sha256:hash,raw:response.raw,link:response.link??null});
    if(response.status!==200) throw new Unknown('SOURCE_READ_FAILED');
    if(source==='github'&&path.includes('/comments?')) {
      if(!Object.hasOwn(response,'link')||response.link!==null&&typeof response.link!=='string') throw new Unknown('GITHUB_LAST_PAGE_MARKER_MISSING');
    }
    // The request decoder requires an object root; wrap GitHub array responses
    // without parsing first, so duplicate keys cannot disappear in JSON.parse.
    return parsePayloadJson('{"source":'+response.raw+'}').source;
  }
  async function githubScan(pass) {
    const started_at=Date.now();let page_count=0;
    const before=await read('github',`${repository}/issues/${issue}`,pass);
    if(before.number!==issue||before.html_url!==`https://github.com/markgoodbody-bit/COM/issues/${issue}`||
      !Number.isSafeInteger(before.comments)||before.comments<0) throw new Unknown('GITHUB_IDENTITY_INVALID');
    const comments=[];
    for(let page=1;;page++) {
      if(page>11) throw new Unknown('GITHUB_PAGINATION_BOUND');
      const rows=await read('github',`${repository}/issues/${issue}/comments?per_page=100&page=${page}`,pass);
      page_count++;
      if(!Array.isArray(rows)||rows.length>100) throw new Unknown('GITHUB_PAGE_INVALID');
      comments.push(...rows);
      if(comments.length>1000) throw new Unknown('GITHUB_ROWS_BOUND');
      const link=receipts.at(-1).link;
      const next=link?.match(/<([^>]+)>;\s*rel="next"/);
      if(!next) break;
      if(next[1]!==`https://api.github.com${repository}/issues/${issue}/comments?per_page=100&page=${page+1}`||rows.length!==100) throw new Unknown('GITHUB_NEXT_PAGE_INVALID');
    }
    const after=await read('github',`${repository}/issues/${issue}`,pass);
    if(stable(before)!==stable(after)||comments.length!==after.comments) throw new Unknown('GITHUB_CHANGED_OR_INCOMPLETE');
    const ids=new Set(),messages=[];
    for(const comment of comments) {
      if(!Number.isSafeInteger(comment.id)||comment.id<1||ids.has(comment.id)||
        comment.html_url!==before.html_url+'#issuecomment-'+comment.id||typeof comment.body!=='string') throw new Unknown('GITHUB_COMMENT_INVALID');
      ids.add(comment.id);
      if(!comment.body.startsWith('COM_SHADOW_V1\n')) continue;
      const envelope=parsePayloadJson(comment.body.slice('COM_SHADOW_V1\n'.length));
      if(envelope.scope!==scope) continue;
      if(typeof comment.created_at!=='string'||!Number.isFinite(Date.parse(comment.created_at))||
        comment.updated_at!==comment.created_at) throw new Unknown('GITHUB_WITNESS_EDITED');
      const message=envelope.message;
      if(!message||message.epoch!==epoch||typeof message.request_key!=='string'||
        !Array.isArray(trusted_authors[message.sender])||!trusted_authors[message.sender].includes(comment.user?.login)) throw new Unknown('GITHUB_WITNESS_UNBOUND');
      // Source cannot substitute another witness URL.
      messages.push({...message,witness_url:comment.html_url});
    }
    return {marker:before,comments,messages,collection:{started_at,ended_at:Date.now(),page_count,last_page_complete:true,last_next:null}};
  }
  const stateKey=state=>stable([state.aperture,state.epoch,state.head_seq,state.consumed,state.retained_after,state.checkpoint_version]);
  async function busScan(pass) {
    const before=await read('bus','/v1/state',pass);
    if(before.aperture!==aperture||before.epoch!==epoch||!Number.isSafeInteger(before.retained_after)||before.retained_after!==0||
      !Number.isSafeInteger(before.head_seq)||before.head_seq<0) throw new Unknown('BUS_EPOCH_OR_GAP_UNBOUND');
    const head=await read('bus','/v1/head',pass),recovery=await read('bus','/v1/recovery',pass);
    if(stateKey(head)!==stateKey(before)||stateKey(recovery)!==stateKey(before)) throw new Unknown('BUS_MARKERS_CHANGED');
    const rows=[];let after=0,rowCount=null,page_count=0;
    for(let page=0;;page++) {
      if(page>=11) throw new Unknown('BUS_PAGINATION_BOUND');
      const history=await read('bus',`/v1/history?after=${after}&limit=100`,pass);
      page_count++;
      if(stateKey(history)!==stateKey(before)||history.history_only!==true||!Array.isArray(history.messages)||
        typeof history.has_more!=='boolean'||history.messages.length>100) throw new Unknown('BUS_PAGE_INVALID_OR_CHANGED');
      if(!Number.isSafeInteger(history.window_row_count)||history.window_row_count<0||rowCount!==null&&rowCount!==history.window_row_count) throw new Unknown('BUS_ROW_COUNT_UNPROVED');
      rowCount=history.window_row_count;
      for(const row of history.messages) {
        if(!Number.isSafeInteger(row.seq)||row.seq<=after||row.seq>before.head_seq) throw new Unknown('BUS_PAGE_SEQUENCE_INVALID');
        after=row.seq;rows.push({...row,epoch});
      }
      if(rows.length>1000) throw new Unknown('BUS_ROWS_BOUND');
      if(!history.has_more) break;
      if(!history.messages.length) throw new Unknown('BUS_PAGINATION_STALLED');
    }
    if(after!==before.head_seq||rows.length!==rowCount) throw new Unknown('BUS_HEAD_OR_COUNT_NOT_REACHED');
    const end=await read('bus','/v1/state',pass),endHead=await read('bus','/v1/head',pass),endRecovery=await read('bus','/v1/recovery',pass);
    if([end,endHead,endRecovery].some(s=>stateKey(s)!==stateKey(before))||
      stable(head.snapshot)!==stable(endHead.snapshot)||stable(recovery.checkpoint)!==stable(endRecovery.checkpoint)) throw new Unknown('BUS_CHANGED');
    return {marker:end,head:endHead,recovery:endRecovery,rows,window:{from_seq:0,to_seq:before.head_seq,row_count:rowCount},
      collection:{started_at:before.server_time,ended_at:end.server_time,page_count,last_page_complete:true,
        head_seq_at_start:before.head_seq,head_seq_at_end:end.head_seq}};
  }
  try {
    // Independent full reads, not one source copied into the other.
    const g1=await githubScan(1),b1=await busScan(1),g2=await githubScan(2),b2=await busScan(2);
    if(stable([g1.marker,g1.comments,g1.messages])!==stable([g2.marker,g2.comments,g2.messages])||stateKey(b1.marker)!==stateKey(b2.marker)||stable(b1.rows)!==stable(b2.rows)||
      stable(b1.head.snapshot)!==stable(b2.head.snapshot)||stable(b1.recovery.checkpoint)!==stable(b2.recovery.checkpoint)) throw new Unknown('SOURCE_CHANGED_ACROSS_COLLECTION');
    const messages=b2.rows;
    if(!messages.length&&!g2.messages.length) throw new Unknown('EMPTY_SHADOW_SCOPE');
    // Verify referenced GitHub objects by read, never infer their authority.
    const anchors=new Set([...messages,...g2.messages].map(m=>m.github_anchor).filter(Boolean));
    if(b2.head.snapshot?.github_anchor) anchors.add(b2.head.snapshot.github_anchor);
    if(b2.recovery.checkpoint?.github_anchor) anchors.add(b2.recovery.checkpoint.github_anchor);
    if(anchors.size>100) throw new Unknown('ANCHOR_READ_BOUND');
    for(const url of anchors) {
      const match=anchor.exec(url);if(!match) throw new Unknown('ANCHOR_INVALID');
      const path=match[3]?`${repository}/issues/comments/${match[3]}`:`${repository}/issues/${match[2]}`;
      const first=await read('github',path,'anchor-1'),second=await read('github',path,'anchor-2');
      if(first.html_url!==url||stable(first)!==stable(second)) throw new Unknown('ANCHOR_MISSING_OR_CHANGED');
    }
    const bus={...b2.marker,scope,complete:true,messages,window:b2.window,collection:b2.collection,checkpoint:b2.recovery.checkpoint,
      comhead:b2.head.snapshot?{...b2.head.snapshot,freshness:b2.head.freshness}:null,head_bounds};
    const result=reconcile({aperture,github:{scope,epoch,complete:true,collection:g2.collection,messages:g2.messages},bus});
    return {result:{...result,input_provenance:'COLLECTED',collection:'DOUBLE_READ_LOCAL_CONTRACT_NOT_GLOBAL_ATOMICITY'},private_receipts:receipts};
  } catch(error) {return fail(error instanceof Unknown?error.message:'SOURCE_DECODE_OR_READER_FAILURE');}
}

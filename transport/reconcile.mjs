// Pure observation over explicitly supplied shadow snapshots. No I/O or writes.
// Caller must acquire complete, independently witnessed inputs; this function
// does not authenticate GitHub observations or turn a claimed decision into authority.
const anchor=/^https:\/\/github\.com\/markgoodbody-bit\/COM\/(issues|pull)\/[1-9][0-9]*(#issuecomment-[0-9]+)?$/;
const epoch=value=>/^[a-f0-9]{32}$/.test(value??'');
const integer=value=>Number.isSafeInteger(value)&&value>=0;
const identity=row=>JSON.stringify([row.epoch,row.sender,row.request_key]);
const content=row=>JSON.stringify([row.recipient,row.kind,row.body,row.github_anchor??null]);
export function reconcile({github,bus,aperture}={}) {
  const result={status:'UNKNOWN',observation_only:true,sync_complete:false,
    authority_winner:null,issues:[],messages:[],repeated_shared:[],state:null};
  const issue=(code,details={})=>result.issues.push({code,...details});
  if (!github||!bus||typeof aperture!=='string'||!aperture||!Array.isArray(github.messages)||!Array.isArray(bus.messages)) {
    issue('INVALID_SNAPSHOT'); return result;
  }
  if (github.messages.length>1000||bus.messages.length>1000||
      new TextEncoder().encode(JSON.stringify({github,bus})).length>2097152) {
    issue('SNAPSHOT_BOUND_EXCEEDED'); return result;
  }
  if (!epoch(bus.epoch)||!epoch(github.epoch)||bus.epoch!==github.epoch||
      !integer(bus.head_seq)||!integer(bus.retained_after)||!integer(bus.checkpoint_version)||
      !integer(bus.consumed)||bus.retained_after>bus.head_seq||bus.consumed>bus.head_seq) {
    issue('INVALID_OR_DIFFERENT_EPOCH_STATE'); return result;
  }
  // Scope is a caller-defined shadow run, not all GitHub discussion. Both sides
  // must attest completion of that same run. Row count alone proves nothing.
  if (typeof bus.scope!=='string'||!bus.scope||github.scope!==bus.scope||
      github.complete!==true||bus.complete!==true) issue('INCOMPLETE_OR_DIFFERENT_SCOPE');
  if (bus.consumed<bus.retained_after) issue('GAP_OPEN');
  if (bus.checkpoint_version>0 && (!bus.checkpoint||bus.checkpoint.version!==bus.checkpoint_version||
      bus.checkpoint.new_epoch!==bus.epoch||bus.checkpoint.retained_after!==bus.retained_after||
      !/^[a-f0-9]{64}$/.test(bus.checkpoint.archive_sha256??'')||
      !anchor.test(bus.checkpoint.github_anchor??''))) issue('CHECKPOINT_UNVERIFIED');
  const head=bus.comhead;
  result.state={epoch:bus.epoch,checkpoint_version:bus.checkpoint_version,
    retained_after:bus.retained_after,consumed:bus.consumed,head_seq:bus.head_seq,
    gap:bus.consumed<bus.retained_after,comhead:head??null};
  if (!head||!['CURRENT','STALE','UNKNOWN'].includes(head.freshness)||!integer(head.basis_seq)||
      head.basis_seq>bus.head_seq||!anchor.test(head.github_anchor??'')) issue('COMHEAD_UNKNOWN_OR_INVALID');
  else {
    const bounds=bus.head_bounds;
    if (!integer(bus.server_time)||!integer(head.updated_at)||!bounds||!integer(bounds.max_age_seconds)||!integer(bounds.max_lag)||
        head.updated_at>bus.server_time) issue('COMHEAD_FRESHNESS_UNVERIFIED');
    else {
      const computed=bus.server_time-head.updated_at>bounds.max_age_seconds||bus.head_seq-head.basis_seq>bounds.max_lag?'STALE':'CURRENT';
      if (head.freshness!==computed) issue('COMHEAD_FRESHNESS_DIFFERENCE');
      if (computed!=='CURRENT') issue('COMHEAD_NOT_CURRENT',{freshness:computed});
    }
  }
  const maps=[];
  for (const [source,snapshot] of [['github',github],['bus',bus]]) {
    const map=new Map(),seqs=new Set();
    for (const row of snapshot.messages) {
      if (!row||row.epoch!==bus.epoch||typeof row.sender!=='string'||!row.sender||
          typeof row.request_key!=='string'||!row.request_key||typeof row.recipient!=='string'||!row.recipient||
          typeof row.kind!=='string'||typeof row.body!=='string') {issue('INVALID_MESSAGE',{source}); continue;}
      const key=identity(row);
      if (map.has(key)) issue('DUPLICATE_IDENTITY',{source,identity:JSON.parse(key)});
      map.set(key,row);
      if (source==='bus') {
        if (!integer(row.seq)||row.seq===0||row.seq>bus.head_seq||seqs.has(row.seq)) issue('INVALID_OR_DUPLICATE_SEQUENCE',{identity:JSON.parse(key)});
        seqs.add(row.seq);
      } else if (!anchor.test(row.witness_url??'')) issue('GITHUB_WITNESS_MISSING',{identity:JSON.parse(key)});
      if (row.kind==='decision'&&!anchor.test(row.github_anchor??'')) issue('DECISION_ANCHOR_MISSING',{source,identity:JSON.parse(key)});
    }
    maps.push(map);
  }
  const [gm,bm]=maps;
  for (const key of new Set([...gm.keys(),...bm.keys()])) {
    const g=gm.get(key),b=bm.get(key),presence=g&&b?'BOTH':g?'GITHUB_ONLY':'BUS_ONLY';
    const row=b??g;
    const routing=row.recipient==='shared'?'shared':row.recipient===aperture?'direct':'history';
    const entry={identity:JSON.parse(key),presence,seq:b?.seq??null,routing,
      github_recipient:g?.recipient??null,bus_recipient:b?.recipient??null,
      github_anchor:g?.github_anchor??null,bus_anchor:b?.github_anchor??null,
      ack:b?.my_disposition??null};
    result.messages.push(entry);
    if (presence!=='BOTH') issue(presence,{identity:entry.identity,consequential:row.kind==='decision'});
    else if (content(g)!==content(b)) issue('MESSAGE_DIFFERENCE',{identity:entry.identity});
    // A disposition is observed, never inferred from cursor position or reading.
    if (b?.my_disposition!=null) {
      let disposition=b.my_disposition;
      try {if(typeof disposition==='string') disposition=JSON.parse(disposition);} catch {disposition=null;}
      if (!disposition||disposition.seq!==b.seq||
          !((integer(disposition.answered_by)&&disposition.answered_by>0&&disposition.no_answer_owed===undefined)||
          (disposition.answered_by===undefined&&typeof disposition.no_answer_owed==='string'&&disposition.no_answer_owed.trim())))
        issue('INVALID_OBSERVED_DISPOSITION',{identity:entry.identity});
      if (routing==='history') issue('OTHER_RECIPIENT_DISPOSITION',{identity:entry.identity});
    }
  }
  const repeats=new Map();
  for (const row of bm.values()) if(row.recipient==='shared') {
    const key=JSON.stringify([row.sender,row.body]);
    if (!repeats.has(key)) repeats.set(key,[]);
    repeats.get(key).push(row.seq);
  }
  for (const [key,sequences] of repeats) if(sequences.length>1)
    result.repeated_shared.push({sender:JSON.parse(key)[0],count:sequences.length,sequences,observation_only:true});
  if (!result.issues.length) result.status='SUPPLIED_SNAPSHOTS_MATCH';
  return result;
}

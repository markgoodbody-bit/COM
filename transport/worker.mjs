// Candidate D1 adapter. No provisioning endpoint, retries, logging or YAC imports.
const enc = new TextEncoder();
export class Refusal extends Error {
  constructor(code, status = 400) { super(code); this.status = status; }
}
const anchorPattern = /^https:\/\/github\.com\/markgoodbody-bit\/COM\/(issues|pull)\/[1-9][0-9]*(#issuecomment-[0-9]+)?$/;
export async function digest(value) {
  return [...new Uint8Array(await crypto.subtle.digest('SHA-256', enc.encode(value)))].map(x => x.toString(16).padStart(2, '0')).join('');
}
function response(data, status = 200) {
  return new Response(JSON.stringify(data), {status, headers: {
    'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff', 'Content-Security-Policy': "default-src 'none'; frame-ancestors 'none'"
  }});
}
// JSON.parse alone silently accepts duplicate keys. Scan the already valid JSON
// with decoded property names, including escaped aliases and nested objects.
export function parsePayloadJson(source) {
  const data = JSON.parse(source);
  let at = 0;
  const whitespace = () => { while (/\s/.test(source[at] ?? '') && at < source.length) at++; };
  function string() {
    const start = at++;
    while (at < source.length) {
      if (source[at] === '\\') { at += 2; continue; }
      if (source[at++] === '"') return JSON.parse(source.slice(start, at));
    }
    throw new Refusal('JSON_INVALID');
  }
  function value(depth) {
    if (depth > 32) throw new Refusal('JSON_DEPTH_BOUND');
    whitespace();
    const type = source[at];
    if (type === '"') { string(); return; }
    if (type === '{' || type === '[') {
      const object = type === '{', close = object ? '}' : ']';
      const names = new Set(); at++; whitespace();
      if (source[at] === close) { at++; return; }
      while (true) {
        whitespace();
        if (object) {
          const name = string();
          if (names.has(name)) throw new Refusal('JSON_DUPLICATE_KEY');
          names.add(name); whitespace(); at++; // colon, checked by JSON.parse
        }
        value(depth + 1); whitespace();
        if (source[at++] === close) return;
      }
    }
    while (at < source.length && !/[\s,}\]]/.test(source[at])) at++;
  }
  value(0);
  if (!data || typeof data !== 'object' || Array.isArray(data)) throw new Refusal('JSON_INVALID');
  return data;
}
async function payload(request) {
  if (request.headers.get('Content-Type')?.split(';')[0].trim() !== 'application/json') throw new Refusal('JSON_REQUIRED', 415);
  if (!request.body) throw new Refusal('JSON_INVALID');
  const reader = request.body.getReader();
  const chunks = []; let count = 0;
  try {
    while (true) {
      const {done, value} = await reader.read(); if (done) break;
      count += value.byteLength;
      if (count > 20000) { await reader.cancel(); throw new Refusal('PAYLOAD_BOUND', 413); }
      chunks.push(value);
    }
  } finally { reader.releaseLock(); }
  const bytes = new Uint8Array(count); let offset = 0;
  for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.length; }
  try {
    return parsePayloadJson(new TextDecoder('utf-8', {fatal: true}).decode(bytes));
  } catch (error) { if (error instanceof Refusal) throw error; throw new Refusal('JSON_INVALID'); }
}
const safeInt = n => Number.isSafeInteger(n) && n >= 0;
const s = (db, sql, ...args) => db.prepare(sql).bind(...args);
// A failing CHECK aborts the D1 batch: no silent zero-effect mutation.
const guard = (db, condition, ...args) => s(db,
  `INSERT INTO mutation_guard(id,ok) VALUES(1,CASE WHEN ${condition} THEN 1 ELSE 0 END)
   ON CONFLICT(id) DO UPDATE SET ok=excluded.ok`, ...args);
const active = 'EXISTS(SELECT 1 FROM apertures WHERE id=? AND credential_hash=? AND revoked=0)';
const headActive = `EXISTS(SELECT 1 FROM head_capabilities c JOIN apertures a ON a.id=c.aperture
  WHERE c.capability='comhead_writer' AND c.aperture=? AND c.credential_hash=? AND c.revoked=0 AND a.revoked=0)
  AND NOT EXISTS(SELECT 1 FROM apertures WHERE credential_hash=?)`;

export class Bus {
  constructor(db, env = {}) { this.db = db; this.env = env; }
  async actor(token) {
    if (typeof token !== 'string' || !/^[A-Za-z0-9_-]{43}$/.test(token)) throw new Refusal('UNAUTHORIZED', 401);
    const hash = await digest(token);
    const actor = await s(this.db, 'SELECT id,consumed FROM apertures WHERE credential_hash=? AND revoked=0', hash).first();
    if (!actor) throw new Refusal('UNAUTHORIZED', 401);
    return {...actor, hash};
  }
  async headWriter(token) {
    if (typeof token!=='string' || !/^[A-Za-z0-9_-]{43}$/.test(token)) throw new Refusal('UNAUTHORIZED',401);
    const hash=await digest(token);
    const writer=await s(this.db,`SELECT c.aperture AS id FROM head_capabilities c
      JOIN apertures a ON a.id=c.aperture WHERE c.capability='comhead_writer'
      AND c.credential_hash=? AND c.revoked=0 AND a.revoked=0
      AND NOT EXISTS(SELECT 1 FROM apertures WHERE credential_hash=?)`,hash,hash).first();
    if (!writer) throw new Refusal('UNAUTHORIZED',401);
    return {...writer,hash};
  }
  async writeHead(writer,data) {
    const {expected_version:version,basis_seq:basis,body,github_anchor:anchor}=data;
    if (Object.keys(data).some(key=>!['expected_version','basis_seq','body','github_anchor'].includes(key))) throw new Refusal('HEAD_FIELDS_ONLY');
    if (!safeInt(version) || version===Number.MAX_SAFE_INTEGER || !safeInt(basis)) throw new Refusal('INVALID_HEAD');
    if (typeof body!=='string' || !body.trim() || enc.encode(body).length>8192) throw new Refusal('INVALID_HEAD_BODY');
    if (typeof anchor!=='string' || !anchorPattern.test(anchor)) throw new Refusal('HEAD_ANCHOR_REQUIRED');
    const db=this.db;
    const prior=await s(db,'SELECT version,basis_seq FROM comhead WHERE id=1').first();
    if ((prior?.version??0)!==version) throw new Refusal('HEAD_VERSION_CONFLICT',409);
    const head=await s(db,'SELECT COALESCE(MAX(seq),0) AS seq FROM messages').first();
    if (basis>head.seq || basis<(prior?.basis_seq??0)) throw new Refusal('INVALID_HEAD_BASIS');
    let result;
    try { result=await db.batch([
      guard(db,headActive,writer.id,writer.hash,writer.hash),
      guard(db,'COALESCE((SELECT version FROM comhead WHERE id=1),0)=?',version),
      guard(db,'?<=COALESCE((SELECT MAX(seq) FROM messages),0) AND ?>=COALESCE((SELECT basis_seq FROM comhead WHERE id=1),0)',basis,basis),
      s(db,`INSERT INTO head_audit(version,aperture,capability,server_time,prior_basis_seq,new_basis_seq,github_anchor)
        VALUES(?,?,'comhead_writer',unixepoch(),(SELECT basis_seq FROM comhead WHERE id=1),?,?)`,version+1,writer.id,basis,anchor),
      s(db,`INSERT INTO comhead(id,version,basis_seq,updated_at,body,github_anchor) VALUES(1,?,?,unixepoch(),?,?)
        ON CONFLICT(id) DO UPDATE SET version=excluded.version,basis_seq=excluded.basis_seq,
        updated_at=excluded.updated_at,body=excluded.body,github_anchor=excluded.github_anchor`,version+1,basis,body,anchor),
      s(db,'SELECT version,basis_seq,updated_at,github_anchor FROM comhead WHERE id=1')
    ]); } catch (error) {
      const current=await s(db,'SELECT version FROM comhead WHERE id=1').first();
      if ((current?.version??0)!==version) throw new Refusal('HEAD_VERSION_CONFLICT',409);
      throw error;
    }
    return {...result[5].results[0],sync_complete:false};
  }
  async state(actor) {
    const row = await s(this.db, `SELECT consumed,
      (SELECT COALESCE(MAX(seq),0) FROM messages) AS head_seq,
      unixepoch() AS server_time FROM apertures WHERE id=? AND credential_hash=? AND revoked=0`, actor.id, actor.hash).first();
    if (!row) throw new Refusal('UNAUTHORIZED', 401);
    return row;
  }
  async send(actor, data) {
    const {request_key: key, body, to: recipient, kind = 'message', github_anchor: anchor = null} = data;
    if (typeof key !== 'string' || !/^[A-Za-z0-9_-]{1,64}$/.test(key)) throw new Refusal('INVALID_REQUEST_KEY');
    if (typeof body !== 'string' || enc.encode(body).length < 1 || enc.encode(body).length > 16384) throw new Refusal('INVALID_BODY');
    if (typeof recipient !== 'string' || !['message', 'decision'].includes(kind)) throw new Refusal('INVALID_ROUTING');
    if (anchor !== null && (typeof anchor !== 'string' || !anchorPattern.test(anchor))) throw new Refusal('INVALID_ANCHOR');
    if (kind === 'decision' && anchor === null) throw new Refusal('DECISION_ANCHOR_REQUIRED');
    const db = this.db;
    const limits = ['SEND_WINDOW_SECONDS','SEND_MAX_ALL','SEND_MAX_SHARED'].map(name => {
      const raw=this.env[name], number=Number(raw);
      if (!/^[1-9][0-9]*$/.test(raw??'') || !safeInt(number)) throw new Refusal('RATE_BOUNDS_UNSET',503);
      return number;
    });
    const [window,allLimit,sharedLimit]=limits;
    if (!await s(db,"SELECT id FROM apertures WHERE id=? AND (revoked=0 OR id='shared')",recipient).first()) throw new Refusal('UNKNOWN_RECIPIENT');
    let results;
    try { results = await db.batch([
      guard(db, `${active} AND EXISTS(SELECT 1 FROM apertures WHERE id=? AND (revoked=0 OR id='shared'))`, actor.id, actor.hash, recipient),
      s(db, `INSERT INTO messages(sender,recipient,kind,github_anchor,request_key,body,received_at)
        SELECT ?,?,?,?,?,?,unixepoch() WHERE
        EXISTS(SELECT 1 FROM messages WHERE sender=? AND request_key=?) OR
        ((SELECT COUNT(*) FROM messages WHERE sender=? AND received_at>unixepoch()-?)<? AND
         (?!='shared' OR (SELECT COUNT(*) FROM messages WHERE sender=? AND recipient='shared' AND received_at>unixepoch()-?)<?))
        ON CONFLICT(sender,request_key) DO NOTHING`, actor.id, recipient, kind, anchor, key, body,
          actor.id,key,actor.id,window,allLimit,recipient,actor.id,window,sharedLimit),
      guard(db, `NOT EXISTS(SELECT 1 FROM messages WHERE sender=? AND request_key=?) OR
        EXISTS(SELECT 1 FROM messages WHERE sender=? AND request_key=? AND body=? AND recipient=? AND kind=? AND github_anchor IS ?)`, actor.id,key,actor.id, key, body, recipient, kind, anchor),
      s(db, `SELECT (SELECT seq FROM messages WHERE sender=? AND request_key=?) AS seq,
        unixepoch() AS server_time,(SELECT COALESCE(MAX(seq),0) FROM messages) AS head_seq,
        MAX(1,COALESCE((SELECT received_at FROM messages WHERE sender=? AND received_at>unixepoch()-?
          ORDER BY received_at DESC LIMIT 1 OFFSET ?)+?-unixepoch(),0),
          CASE WHEN ?='shared' THEN COALESCE((SELECT received_at FROM messages WHERE sender=? AND recipient='shared' AND received_at>unixepoch()-?
          ORDER BY received_at DESC LIMIT 1 OFFSET ?)+?-unixepoch(),0) ELSE 0 END) AS retry_after_seconds`,
        actor.id,key,actor.id,window,allLimit-1,window,recipient,actor.id,window,sharedLimit-1,window)
    ]); } catch (error) {
      const prior=await s(db,'SELECT * FROM messages WHERE sender=? AND request_key=?',actor.id,key).first();
      if (prior && (prior.body!==body || prior.recipient!==recipient || prior.kind!==kind || prior.github_anchor!==anchor)) throw new Refusal('REQUEST_KEY_CONFLICT',409);
      throw error;
    }
    const result=results[3].results[0];
    if (result.seq===null) {
      const refusal=new Refusal('RATE_LIMITED',429);
      refusal.retryAfter=Math.min(window,result.retry_after_seconds);
      throw refusal;
    }
    const {retry_after_seconds,...accepted}=result;
    return accepted;
  }
  async fetch(actor, after, limit) {
    if (!safeInt(after) || !safeInt(limit) || limit < 1 || limit > 100) throw new Refusal('INVALID_PAGE');
    const db = this.db; const receipt = crypto.randomUUID();
    const results = await db.batch([
      guard(db, `${active} AND EXISTS(SELECT 1 FROM apertures WHERE id=? AND consumed=?)`, actor.id, actor.hash, actor.id, after),
      s(db, 'DELETE FROM deliveries WHERE aperture=? AND disposition IS NULL', actor.id),
      s(db, `INSERT INTO deliveries(receipt,aperture,start_seq,end_seq)
        SELECT ?,?,?,MAX(seq) FROM (SELECT seq FROM messages WHERE seq>? AND recipient IN (?,'shared') ORDER BY seq LIMIT ?) HAVING MAX(seq) IS NOT NULL`, receipt, actor.id, after, after, actor.id, limit),
      s(db, "SELECT *,recipient=? AS to_me,CASE WHEN recipient='shared' THEN 'shared' ELSE 'direct' END AS delivery FROM messages WHERE seq>? AND recipient IN (?,'shared') ORDER BY seq LIMIT ?",actor.id, after, actor.id, limit),
      s(db, `SELECT (SELECT COALESCE(MAX(seq),0) FROM messages) AS head_seq,
        (SELECT COUNT(*) FROM messages WHERE seq>? AND recipient IN (?,'shared')) AS unread_count, unixepoch() AS server_time`, after,actor.id)
    ]);
    const messages = results[3].results;
    return {...results[4].results[0], messages, receipt: messages.length ? receipt : null,
      consumed: after, through: messages.length ? messages.at(-1).seq : after,
      page_count: messages.length, has_more: results[4].results[0].unread_count > messages.length};
  }
  async acknowledge(actor, data) {
    const {receipt, through, dispositions} = data;
    if (!safeInt(through) || typeof receipt !== 'string' || receipt.length > 128) throw new Refusal('INVALID_ACK');
    if (!Array.isArray(dispositions) || dispositions.length<1 || dispositions.length>100) throw new Refusal('ACK_DISPOSITION_REQUIRED');
    const canonical=dispositions.map(row=>{
      if (!row || !safeInt(row.seq) || row.seq===0 || (row.no_answer_owed===undefined)===(row.answered_by===undefined)) throw new Refusal('INVALID_DISPOSITION');
      if (row.no_answer_owed!==undefined) {
        if (typeof row.no_answer_owed!=='string' || !row.no_answer_owed.trim() || enc.encode(row.no_answer_owed).length>1024) throw new Refusal('INVALID_DISPOSITION');
        return {seq:row.seq,no_answer_owed:row.no_answer_owed};
      }
      if (!safeInt(row.answered_by) || !row.answered_by) throw new Refusal('INVALID_ANSWER');
      return {seq:row.seq,answered_by:row.answered_by};
    });
    if (canonical.some((row,i)=>i>0 && row.seq<=canonical[i-1].seq)) throw new Refusal('INVALID_DISPOSITION');
    const disposition=JSON.stringify(canonical);
    const db = this.db;
    const conditions=canonical.flatMap(row=>[
      guard(db, `EXISTS(SELECT 1 FROM messages m JOIN deliveries d ON m.seq>d.start_seq AND m.seq<=d.end_seq WHERE d.receipt=? AND m.seq=? AND m.recipient IN (?,'shared'))`,receipt,row.seq,actor.id),
      guard(db, '? IS NULL OR EXISTS(SELECT 1 FROM messages WHERE seq=? AND sender=?)',row.answered_by??null,row.answered_by??null,actor.id)
    ]);
    await db.batch([
      guard(db, active, actor.id, actor.hash),
      guard(db, `EXISTS(SELECT 1 FROM deliveries d JOIN apertures a ON a.id=d.aperture
        WHERE d.receipt=? AND d.aperture=? AND d.end_seq=? AND a.consumed IN(d.start_seq,d.end_seq)
        AND (d.disposition IS NULL OR d.disposition=?))`, receipt, actor.id, through, disposition),
      guard(db, "(SELECT COUNT(*) FROM messages m JOIN deliveries d ON m.seq>d.start_seq AND m.seq<=d.end_seq WHERE d.receipt=? AND m.recipient IN (?,'shared'))=?",receipt,actor.id,canonical.length),
      ...conditions,
      ...canonical.map(row=>s(db,'INSERT INTO acknowledgements(receipt,aperture,seq,disposition) VALUES (?,?,?,?) ON CONFLICT(receipt,seq) DO NOTHING',receipt,actor.id,row.seq,JSON.stringify(row))),
      s(db, 'UPDATE apertures SET consumed=? WHERE id=?', through, actor.id),
      s(db, 'UPDATE deliveries SET disposition=? WHERE receipt=?', disposition, receipt)
    ]);
    return this.state(actor);
  }
  async history(actor, after, limit) {
    if (!safeInt(after)||!safeInt(limit)||limit<1||limit>100) throw new Refusal('INVALID_PAGE');
    const state=await this.state(actor);
    const messages=(await this.db.batch([s(this.db,`SELECT m.*,
      (SELECT disposition FROM acknowledgements WHERE aperture=? AND seq=m.seq LIMIT 1) AS my_disposition
      FROM messages m WHERE seq>? ORDER BY seq LIMIT ?`,actor.id,after,limit+1)]))[0].results;
    const more=messages.length>limit;
    return {...state,messages:messages.slice(0,limit),has_more:more,history_only:true};
  }
  async head(actor, env) {
    const reads=await this.db.batch([
      s(this.db,`SELECT consumed,(SELECT COALESCE(MAX(seq),0) FROM messages) AS head_seq,
        unixepoch() AS server_time FROM apertures WHERE id=? AND credential_hash=? AND revoked=0`,actor.id,actor.hash),
      s(this.db,'SELECT version,basis_seq,updated_at,body,github_anchor FROM comhead WHERE id=1')
    ]);
    const state=reads[0].results[0],snapshot=reads[1].results[0]??null;
    if (!state) throw new Refusal('UNAUTHORIZED',401);
    const ageBound=Number(env.HEAD_MAX_AGE_SECONDS),lagBound=Number(env.HEAD_MAX_LAG);
    let freshness='UNKNOWN',reason='HEAD_MISSING';
    if (snapshot) {
      reason='FRESHNESS_BOUNDS_UNSET';
      if (/^(0|[1-9][0-9]*)$/.test(env.HEAD_MAX_AGE_SECONDS??'') && /^(0|[1-9][0-9]*)$/.test(env.HEAD_MAX_LAG??'') && safeInt(ageBound) && safeInt(lagBound)) {
        const age=state.server_time-snapshot.updated_at, lag=state.head_seq-snapshot.basis_seq;
        if (age<0 || lag<0 || !anchorPattern.test(snapshot.github_anchor)) reason='HEAD_BASIS_INVALID';
        else if (age>ageBound || lag>lagBound) {freshness='STALE';reason='HEAD_BOUND_EXCEEDED';}
        else {freshness='CURRENT';reason='WITHIN_CONFIGURED_BOUNDS';}
      }
    }
    return {...state,snapshot,freshness,reason,sync_complete:false};
  }
}

export default {
  async fetch(request, env) {
    try {
      if (!env.DB) throw new Refusal('STORAGE_UNAVAILABLE', 503);
      const bus = new Bus(env.DB,env);
      const auth = request.headers.get('Authorization') || '';
      const token=auth.startsWith('Bearer ') ? auth.slice(7) : '';
      const url = new URL(request.url);
      if (request.method==='POST' && url.pathname==='/v1/head') {
        const writer=await bus.headWriter(token);
        if (env.WRITES_ENABLED!=='true' || env.HEAD_WRITES_ENABLED!=='true') throw new Refusal('HEAD_WRITES_CLOSED',503);
        return response(await bus.writeHead(writer,await payload(request)));
      }
      const actor = await bus.actor(token);
      if (request.method === 'GET' && url.pathname === '/v1/state') return response(await bus.state(actor));
      if (request.method === 'GET' && ['/v1/head','/v1/health'].includes(url.pathname)) return response(await bus.head(actor,env));
      if (request.method === 'GET' && url.pathname === '/v1/history') {
        const after=url.searchParams.get('after')??'0',limit=url.searchParams.get('limit')??'20';
        if (!/^\d+$/.test(after)||!/^\d+$/.test(limit)) throw new Refusal('INVALID_PAGE');
        return response(await bus.history(actor,Number(after),Number(limit)));
      }
      if (request.method === 'GET' && url.pathname === '/v1/messages') {
        const after = url.searchParams.get('after'); const limit = url.searchParams.get('limit') ?? '20';
        if (!after || !/^\d+$/.test(after) || !/^\d+$/.test(limit)) throw new Refusal('INVALID_PAGE');
        return response(await bus.fetch(actor, Number(after), Number(limit)));
      }
      if (request.method === 'POST' && ['/v1/messages', '/v1/ack'].includes(url.pathname)) {
        if (env.WRITES_ENABLED !== 'true') throw new Refusal('WRITES_CLOSED', 503);
        const data = await payload(request);
        return response(url.pathname === '/v1/ack' ? await bus.acknowledge(actor, data) : await bus.send(actor, data));
      }
      throw new Refusal('NOT_FOUND', 404);
    } catch (error) {
      // No raw exceptions, SQL, credentials or message bodies returned/logged.
      return response({status: error instanceof Refusal ? error.message : 'STORAGE_OR_ATOMIC_REFUSAL',
        ...(error instanceof Refusal && error.retryAfter!==undefined ? {retry_after_seconds:error.retryAfter}:{}),
        sync_complete: false, server_time: Math.floor(Date.now()/1000)}, error instanceof Refusal ? error.status : 503);
    }
  }
};

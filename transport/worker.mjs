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
    const data = JSON.parse(new TextDecoder('utf-8', {fatal: true}).decode(bytes));
    if (!data || typeof data !== 'object' || Array.isArray(data)) throw new Error();
    return data;
  } catch { throw new Refusal('JSON_INVALID'); }
}
const safeInt = n => Number.isSafeInteger(n) && n >= 0;
const s = (db, sql, ...args) => db.prepare(sql).bind(...args);
// A failing CHECK aborts the D1 batch: no silent zero-effect mutation.
const guard = (db, condition, ...args) => s(db,
  `INSERT INTO mutation_guard(id,ok) VALUES(1,CASE WHEN ${condition} THEN 1 ELSE 0 END)
   ON CONFLICT(id) DO UPDATE SET ok=excluded.ok`, ...args);
const active = 'EXISTS(SELECT 1 FROM apertures WHERE id=? AND credential_hash=? AND revoked=0)';

export class Bus {
  constructor(db) { this.db = db; }
  async actor(token) {
    if (typeof token !== 'string' || !/^[A-Za-z0-9_-]{43}$/.test(token)) throw new Refusal('UNAUTHORIZED', 401);
    const hash = await digest(token);
    const actor = await s(this.db, 'SELECT id,consumed FROM apertures WHERE credential_hash=? AND revoked=0', hash).first();
    if (!actor) throw new Refusal('UNAUTHORIZED', 401);
    return {...actor, hash};
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
    const results = await db.batch([
      guard(db, `${active} AND EXISTS(SELECT 1 FROM apertures WHERE id=? AND revoked=0)`, actor.id, actor.hash, recipient),
      s(db, `INSERT INTO messages(sender,recipient,kind,github_anchor,request_key,body,received_at)
        VALUES(?,?,?,?,?,?,unixepoch()) ON CONFLICT(sender,request_key) DO NOTHING`, actor.id, recipient, kind, anchor, key, body),
      guard(db, 'EXISTS(SELECT 1 FROM messages WHERE sender=? AND request_key=? AND body=? AND recipient=? AND kind=? AND github_anchor IS ?)', actor.id, key, body, recipient, kind, anchor),
      s(db, 'SELECT seq,unixepoch() AS server_time,(SELECT MAX(seq) FROM messages) AS head_seq FROM messages WHERE sender=? AND request_key=?', actor.id, key)
    ]);
    return results[3].results[0];
  }
  async fetch(actor, after, limit) {
    if (!safeInt(after) || !safeInt(limit) || limit < 1 || limit > 100) throw new Refusal('INVALID_PAGE');
    const db = this.db; const receipt = crypto.randomUUID();
    const results = await db.batch([
      guard(db, `${active} AND EXISTS(SELECT 1 FROM apertures WHERE id=? AND consumed=?)`, actor.id, actor.hash, actor.id, after),
      s(db, 'DELETE FROM deliveries WHERE aperture=?', actor.id),
      s(db, `INSERT INTO deliveries(receipt,aperture,start_seq,end_seq)
        SELECT ?,?,?,MAX(seq) FROM (SELECT seq FROM messages WHERE seq>? ORDER BY seq LIMIT ?) HAVING MAX(seq) IS NOT NULL`, receipt, actor.id, after, after, limit),
      s(db, 'SELECT * FROM messages WHERE seq>? ORDER BY seq LIMIT ?', after, limit),
      s(db, `SELECT (SELECT COALESCE(MAX(seq),0) FROM messages) AS head_seq,
        (SELECT COUNT(*) FROM messages WHERE seq>?) AS unread_count, unixepoch() AS server_time`, after)
    ]);
    const messages = results[3].results;
    return {...results[4].results[0], messages, receipt: messages.length ? receipt : null,
      consumed: after, through: messages.length ? messages.at(-1).seq : after,
      page_count: messages.length, has_more: results[4].results[0].unread_count > messages.length};
  }
  async acknowledge(actor, data) {
    const {receipt, through, no_answer_owed: reason, answered_by: answer} = data;
    if (!safeInt(through) || typeof receipt !== 'string' || receipt.length > 128) throw new Refusal('INVALID_ACK');
    if ((reason === undefined) === (answer === undefined)) throw new Refusal('ACK_DISPOSITION_REQUIRED');
    let disposition;
    if (reason !== undefined) {
      if (typeof reason !== 'string' || !reason.trim() || enc.encode(reason).length > 1024) throw new Refusal('INVALID_DISPOSITION');
      disposition = 'no_answer_owed:' + reason;
    } else {
      if (!safeInt(answer) || answer === 0) throw new Refusal('INVALID_ANSWER');
      disposition = 'answered_by:' + answer;
    }
    const db = this.db;
    await db.batch([
      guard(db, active, actor.id, actor.hash),
      guard(db, `EXISTS(SELECT 1 FROM deliveries d JOIN apertures a ON a.id=d.aperture
        WHERE d.receipt=? AND d.aperture=? AND d.end_seq=? AND a.consumed IN(d.start_seq,d.end_seq)
        AND (d.disposition IS NULL OR d.disposition=?))`, receipt, actor.id, through, disposition),
      guard(db, '? IS NULL OR EXISTS(SELECT 1 FROM messages WHERE seq=? AND sender=?)', answer ?? null, answer ?? null, actor.id),
      s(db, 'UPDATE apertures SET consumed=? WHERE id=?', through, actor.id),
      s(db, 'UPDATE deliveries SET disposition=? WHERE receipt=?', disposition, receipt)
    ]);
    return this.state(actor);
  }
}

export default {
  async fetch(request, env) {
    try {
      if (!env.DB) throw new Refusal('STORAGE_UNAVAILABLE', 503);
      const bus = new Bus(env.DB);
      const auth = request.headers.get('Authorization') || '';
      const actor = await bus.actor(auth.startsWith('Bearer ') ? auth.slice(7) : '');
      const url = new URL(request.url);
      if (request.method === 'GET' && url.pathname === '/v1/state') return response(await bus.state(actor));
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
        sync_complete: false, server_time: Math.floor(Date.now()/1000)}, error instanceof Refusal ? error.status : 503);
    }
  }
};

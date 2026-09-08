/** A deliberately isolated receiving core; D1-shaped calls, no network or tool execution. */
export const DAY = 86400000;
const encoder = new TextEncoder();
export class Problem extends Error {
  constructor(status, code) { super(code); this.status=status; this.code=code; }
}
export function text(value, max, allowEmpty=false) {
  if (typeof value !== 'string' || (!allowEmpty && !value.trim()) ||
      [...value].length > max || /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/u.test(value) ||
      /[\uD800-\uDFFF]/u.test(value)) throw new Problem(400,'INVALID_TEXT');
  return value;
}
export function key(value) {
  if (typeof value !== 'string' || !/^[A-Za-z0-9_-]{43}$/.test(value))
    throw new Problem(400,'INVALID_PRIVATE_KEY');
  return value;
}
export function newKey() {
  const bytes=crypto.getRandomValues(new Uint8Array(32));
  return btoa(String.fromCharCode(...bytes)).replaceAll('+','-').replaceAll('/','_').replace(/=+$/,'');
}
export async function sha(value) {
  return [...new Uint8Array(await crypto.subtle.digest('SHA-256',encoder.encode(value)))]
    .map(n=>n.toString(16).padStart(2,'0')).join('');
}
export class Store {
  constructor(db, clock=()=>Date.now()) { this.db=db; this.clock=clock; }
  statement(sql,...args) { return this.db.prepare(sql).bind(...args); }
  async first(sql,...args) { return this.statement(sql,...args).first(); }
  async rows(sql,...args) { return (await this.statement(sql,...args).all()).results; }
  async readiness(enabled) {
    const until=enabled?this.clock()+DAY:0;
    await this.statement('UPDATE service SET enabled=?,ready_until=? WHERE id=1',enabled?1:0,until).run();
    return {enabled,ready_until:until};
  }
  async sweep() {
    const now=this.clock();
    // Expired pending work is not a merit rejection. Closed bodies are not retained as history.
    await this.db.batch([
      this.statement(`DELETE FROM responses WHERE contribution_id IN
        (SELECT id FROM contributions WHERE state IN ('pending','declined')
          AND body IS NOT NULL AND body_expires_at <= ?)`,now),
      this.statement(`UPDATE contributions SET
          state=CASE WHEN state='pending' THEN 'expired' ELSE state END,
          body=NULL,display_name='',moderation_reason=NULL,reconsideration=0,
          closed_at=?,updated_at=?,revision=revision+1
        WHERE state IN ('pending','declined') AND body IS NOT NULL AND body_expires_at<=?`,now,now,now)
    ]);
  }
  async submit(input, clientHash) {
    const body=text(input.body,4000), display=text(input.display_name??'',80,true);
    const manageHash=await sha(key(input.management_key));
    const retryHash=await sha(key(input.retry_key));
    const requestHash=await sha(JSON.stringify([body,display,manageHash]));
    let row=await this.first('SELECT * FROM contributions WHERE retry_hash=?',retryHash);
    if (!row) {
      const now=this.clock(), id=crypto.randomUUID();
      try {
        await this.statement(`INSERT INTO contributions
          (id,retry_hash,request_hash,manage_hash,display_name,body,state,created_at,updated_at,body_expires_at,client_hash)
          SELECT ?,?,?,?,?,?,'pending',?,?,?,?
          WHERE NOT EXISTS(SELECT 1 FROM contributions WHERE retry_hash=?)`,
          id,retryHash,requestHash,manageHash,display,body,now,now,now+14*DAY,clientHash,retryHash).run();
      } catch(e) {
        for (const code of ['INTAKE_PAUSED','QUEUE_FULL','BODY_CAPACITY','RATE_LIMITED']) {
          if (String(e.message).includes(code)) throw new Problem(code==='RATE_LIMITED'?429:503,code);
        }
        throw e;
      }
      row=await this.first('SELECT * FROM contributions WHERE retry_hash=?',retryHash);
    }
    if (!row) throw new Problem(503,'STORAGE_RESULT_UNKNOWN');
    if (row.request_hash!==requestHash) throw new Problem(409,'RETRY_CONTENT_CONFLICT');
    return this.privateView(row);
  }
  privateView(row) {
    return {id:row.id,state:row.state,revision:row.revision,body:row.body,
      display_name:row.display_name,body_expires_at:row.body_expires_at,
      moderation_reason:row.moderation_reason,reconsideration:!!row.reconsideration,
      closed_at:row.closed_at,updated_at:row.updated_at};
  }
  async owner(id,managementKey) {
    const hash=await sha(key(managementKey));
    const row=await this.first('SELECT * FROM contributions WHERE id=? AND manage_hash=?',id,hash);
    if (!row) throw new Problem(404,'RECEIPT_UNAVAILABLE');
    return row;
  }
  async receipt(id,managementKey) { return this.privateView(await this.owner(id,managementKey)); }
  async revise(id,managementKey,input) {
    const row=await this.owner(id,managementKey);
    const body=text(input.body,4000), display=text(input.display_name??'',80,true);
    if (!['pending','published','declined'].includes(row.state)||row.body===null)
      throw new Problem(409,'CLOSED_CONTRIBUTION');
    if (!Number.isSafeInteger(input.revision)||input.revision!==row.revision)
      throw new Problem(409,'REVISION_CONFLICT');
    const now=this.clock(), marker=crypto.randomUUID();
    const result=await this.db.batch([
      this.statement(`UPDATE contributions SET body=?,display_name=?,state='pending',
        revision=revision+1,updated_at=?,body_expires_at=?,moderation_reason=NULL,reconsideration=0
        WHERE id=? AND revision=? AND body IS NOT NULL
        AND state IN ('pending','published','declined')`,body,display,now,now+14*DAY,id,row.revision),
      this.statement(`INSERT INTO events(contribution_id,revision,action,actor,reason,created_at)
        SELECT id,revision,'revised','contributor',?,? FROM contributions WHERE id=? AND changes()=1`,marker,now,id),
      this.statement(`DELETE FROM responses WHERE contribution_id=? AND EXISTS
        (SELECT 1 FROM events WHERE contribution_id=? AND reason=?)`,id,id,marker)
    ]);
    if (result[0].meta.changes!==1) throw new Problem(409,'REVISION_CONFLICT');
    return this.receipt(id,managementKey);
  }
  async withdraw(id,managementKey) {
    const row=await this.owner(id,managementKey);
    if (row.state==='withdrawn') return this.privateView(row);
    const now=this.clock();
    await this.db.batch([
      this.statement(`UPDATE contributions SET state='withdrawn',body=NULL,display_name='',
        moderation_reason=NULL,reconsideration=0,closed_at=?,updated_at=?,revision=revision+1
        WHERE id=? AND state!='withdrawn'`,now,now,id),
      this.statement(`INSERT INTO events(contribution_id,revision,action,actor,created_at)
        SELECT id,revision,'withdrawn','contributor',? FROM contributions WHERE id=? AND changes()=1`,now,id),
      this.statement('DELETE FROM responses WHERE contribution_id=?',id)
    ]);
    return this.receipt(id,managementKey);
  }
  async reconsider(id,managementKey,reason) {
    text(reason,1000);
    const row=await this.owner(id,managementKey);
    if (row.state!=='declined'||row.body===null) throw new Problem(409,'NOT_RECONSIDERABLE');
    const now=this.clock();
    await this.db.batch([
      this.statement(`UPDATE contributions SET reconsideration=1,updated_at=?
        WHERE id=? AND state='declined' AND body IS NOT NULL`,now,id),
      this.statement(`INSERT INTO events(contribution_id,revision,action,actor,reason,created_at)
        SELECT id,revision,'reconsideration','contributor',?,? FROM contributions
        WHERE id=? AND changes()=1`,reason,now,id)
    ]);
    return this.receipt(id,managementKey);
  }
  async moderate(id,input,actor) {
    const action=input.action, reason=text(input.reason,1000);
    if (!['publish','decline'].includes(action)||!Number.isSafeInteger(input.revision))
      throw new Problem(400,'INVALID_MODERATION');
    const now=this.clock(), state=action==='publish'?'published':'declined';
    const result=await this.db.batch([
      this.statement(`UPDATE contributions SET state=?,moderation_reason=?,updated_at=?,
        body_expires_at=?,reconsideration=0
        WHERE id=? AND revision=? AND body IS NOT NULL
        AND (state='pending' OR (state='declined' AND reconsideration=1))`,
        state,reason,now,state==='declined'?now+14*DAY:null,id,input.revision),
      this.statement(`INSERT INTO events(contribution_id,revision,action,actor,reason,created_at)
        SELECT id,revision,?,?,?,? FROM contributions WHERE id=? AND changes()=1`,action,actor,reason,now,id)
    ]);
    if(result[0].meta.changes!==1) throw new Problem(409,'MODERATION_STATE_CONFLICT');
    return {id,state,revision:input.revision};
  }
  async respond(id,input,actor) {
    const body=text(input.body,4000);
    if(!Number.isSafeInteger(input.revision)) throw new Problem(400,'INVALID_REVISION');
    const result=await this.statement(`INSERT INTO responses(contribution_id,revision,actor,body,created_at)
      SELECT id,revision,?,?,? FROM contributions WHERE id=? AND revision=? AND state='published'`,
      actor,body,this.clock(),id,input.revision).run();
    if(result.meta.changes!==1) throw new Problem(409,'RESPONSE_STATE_CONFLICT');
    return {id,responded:true};
  }
  async publicItems() {
    const rows=await this.rows(`SELECT id,body,display_name,revision,created_at,updated_at
      FROM contributions WHERE state='published' AND body IS NOT NULL ORDER BY created_at DESC LIMIT 100`);
    for(const row of rows) row.responses=await this.rows(`SELECT actor,body,created_at FROM responses
      WHERE contribution_id=? AND revision=? ORDER BY id`,row.id,row.revision);
    return rows;
  }
  async queue() {
    return this.rows(`SELECT id,body,display_name,state,revision,moderation_reason,reconsideration,created_at
      FROM contributions WHERE body IS NOT NULL AND (state='pending' OR reconsideration=1)
      ORDER BY created_at LIMIT 100`);
  }
}

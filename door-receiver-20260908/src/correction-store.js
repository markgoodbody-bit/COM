import {Problem,text,key,sha} from './store.js';

const KINDS=new Set(['privacy','safety','misattribution','other']);
const OUTCOMES=new Set(['no_change','content_changed','content_removed','other']);

function target(value){
  if(typeof value!=='string'||!value.trim()||[...value].length>80||/[\u0000-\u001f\u007f]/u.test(value))
    throw new Problem(400,'INVALID_TARGET_ID');
  return value.trim();
}
function kind(value){if(!KINDS.has(value))throw new Problem(400,'INVALID_CORRECTION_KIND');return value;}

export class CorrectionStore {
  constructor(db,clock=()=>Date.now()){this.db=db;this.clock=clock;}
  statement(sql,...args){return this.db.prepare(sql).bind(...args);}
  async first(sql,...args){return this.statement(sql,...args).first();}
  async rows(sql,...args){return (await this.statement(sql,...args).all()).results;}
  privateView(row){return {id:row.id,target_id:row.target_id,kind:row.kind,note:row.note,state:row.state,
    operator_outcome:row.operator_outcome,operator_reason:row.operator_reason,created_at:row.created_at,
    updated_at:row.updated_at,closed_at:row.closed_at};}
  async submit(input,clientHash){
    const targetId=target(input.target_id), reportKind=kind(input.kind);
    const note=text(input.note??'',1000,true);
    const manageHash=await sha(key(input.management_key));
    const retryHash=await sha(key(input.retry_key));
    const requestHash=await sha(JSON.stringify([targetId,reportKind,note,manageHash]));
    let row=await this.first('SELECT * FROM correction_requests WHERE retry_hash=?',retryHash);
    if(!row){
      const now=this.clock(),id=crypto.randomUUID();
      try{
        await this.statement(`INSERT INTO correction_requests
          (id,retry_hash,request_hash,manage_hash,target_id,kind,note,state,created_at,updated_at,client_hash)
          SELECT ?,?,?,?,?,?,?,'pending',?,?,? WHERE NOT EXISTS
          (SELECT 1 FROM correction_requests WHERE retry_hash=?)`,
          id,retryHash,requestHash,manageHash,targetId,reportKind,note,now,now,clientHash,retryHash).run();
      }catch(e){
        const msg=String(e.message);
        if(msg.includes('CORRECTION_QUEUE_FULL'))throw new Problem(503,'CORRECTION_QUEUE_FULL');
        if(msg.includes('CORRECTION_RATE_LIMITED'))throw new Problem(429,'CORRECTION_RATE_LIMITED');
        throw e;
      }
      row=await this.first('SELECT * FROM correction_requests WHERE retry_hash=?',retryHash);
    }
    if(!row)throw new Problem(503,'CORRECTION_STORAGE_RESULT_UNKNOWN');
    if(row.request_hash!==requestHash)throw new Problem(409,'CORRECTION_RETRY_CONFLICT');
    return this.privateView(row);
  }
  async owner(id,managementKey){
    const manageHash=await sha(key(managementKey));
    const row=await this.first('SELECT * FROM correction_requests WHERE id=? AND manage_hash=?',id,manageHash);
    if(!row)throw new Problem(404,'CORRECTION_RECEIPT_UNAVAILABLE');
    return row;
  }
  async receipt(id,managementKey){return this.privateView(await this.owner(id,managementKey));}
  async withdraw(id,managementKey){
    const row=await this.owner(id,managementKey);
    if(row.state==='withdrawn')return this.privateView(row);
    if(row.state==='resolved')throw new Problem(409,'CORRECTION_ALREADY_RESOLVED');
    const now=this.clock(),token=crypto.randomUUID();
    const result=await this.db.batch([
      this.statement(`UPDATE correction_requests SET state='withdrawn',note='',closed_at=?,updated_at=?,mutation_token=?
        WHERE id=? AND state='pending'`,now,now,token,id),
      this.statement(`INSERT INTO correction_events(correction_id,action,actor,created_at)
        SELECT id,'withdrawn','reporter',? FROM correction_requests WHERE id=? AND mutation_token=?`,now,id,token)
    ]);
    if(result[0].meta.changes!==1)throw new Problem(409,'CORRECTION_STATE_CONFLICT');
    return this.receipt(id,managementKey);
  }
  async clearNote(id,managementKey){
    const row=await this.owner(id,managementKey);
    if(row.state!=='resolved')throw new Problem(409,'CORRECTION_NOT_RESOLVED');
    if(row.note==='')return this.privateView(row);
    const now=this.clock(),token=crypto.randomUUID();
    const result=await this.db.batch([
      this.statement(`UPDATE correction_requests SET note='',updated_at=?,mutation_token=?
        WHERE id=? AND state='resolved' AND note!=''`,now,token,id),
      this.statement(`INSERT INTO correction_events(correction_id,action,actor,created_at)
        SELECT id,'reporter_note_cleared','reporter',? FROM correction_requests
        WHERE id=? AND mutation_token=?`,now,id,token)
    ]);
    if(result[0].meta.changes!==1){
      const current=await this.owner(id,managementKey);
      if(current.state==='resolved'&&current.note==='')return this.privateView(current);
      throw new Problem(409,'CORRECTION_STATE_CONFLICT');
    }
    return this.receipt(id,managementKey);
  }
  async queue(){return this.rows(`SELECT id,target_id,kind,note,state,created_at,updated_at
    FROM correction_requests WHERE state='pending' ORDER BY created_at LIMIT 100`);}
  async resolve(id,input,actor){
    if(typeof id!=='string'||!id.trim())throw new Problem(400,'CORRECTION_ID_REQUIRED');
    if(!OUTCOMES.has(input.outcome))throw new Problem(400,'INVALID_CORRECTION_OUTCOME');
    const reason=text(input.reason,1000),now=this.clock(),token=crypto.randomUUID();
    const result=await this.db.batch([
      this.statement(`UPDATE correction_requests SET state='resolved',operator_outcome=?,operator_reason=?,closed_at=?,updated_at=?,mutation_token=?
        WHERE id=? AND state='pending'`,input.outcome,reason,now,now,token,id),
      this.statement(`INSERT INTO correction_events(correction_id,action,actor,reason,created_at)
        SELECT id,'resolved',?,?,? FROM correction_requests WHERE id=? AND mutation_token=?`,actor,reason,now,id,token)
    ]);
    if(result[0].meta.changes!==1)throw new Problem(409,'CORRECTION_STATE_CONFLICT');
    return this.first('SELECT id,target_id,kind,state,operator_outcome,operator_reason,closed_at FROM correction_requests WHERE id=?',id);
  }
}

// Bounded operator-only logical archive. No HTTP route or automatic restore.
import {digest,parsePayloadJson} from './worker.mjs';
const tables={
  transport_meta:['id','epoch','retained_after','checkpoint_version'],
  apertures:['id','credential_hash','revoked','consumed'],
  messages:['seq','sender','recipient','kind','github_anchor','request_key','body','received_at'],
  comhead:['id','version','basis_seq','updated_at','body','github_anchor'],
  head_capabilities:['capability','aperture','credential_hash','revoked'],
  head_audit:['version','aperture','capability','server_time','prior_basis_seq','new_basis_seq','github_anchor'],
  deliveries:['receipt','aperture','start_seq','end_seq','disposition'],
  acknowledgements:['receipt','aperture','seq','disposition'],
  recovery_checkpoints:['version','prior_epoch','new_epoch','retained_after','head_seq','server_time','archive_sha256','github_anchor','prior_head_anchor']
};
const names=Object.keys(tables),maxRows=1000,maxBytes=1048576;
const verifiedPackets=new WeakSet();
const anchor=/^https:\/\/github\.com\/markgoodbody-bit\/COM\/(issues|pull)\/[1-9][0-9]*(#issuecomment-[0-9]+)?$/;
const sql=(db,text,...args)=>db.prepare(text).bind(...args);
const guard=(db,condition,...args)=>sql(db,`INSERT INTO mutation_guard(id,ok) VALUES(1,CASE WHEN ${condition} THEN 1 ELSE 0 END)
  ON CONFLICT(id) DO UPDATE SET ok=excluded.ok`,...args);
function shape(packet,schemaHash) {
  if (JSON.stringify(Object.keys(packet))!==JSON.stringify(['format','schema_sha256','github_anchor','tables','sequence']) ||
      packet.format!=='COM_LOGICAL_ARCHIVE_V1' || packet.schema_sha256!==schemaHash ||
      !/^[a-f0-9]{64}$/.test(schemaHash??'') || !anchor.test(packet.github_anchor??'') ||
      !Number.isSafeInteger(packet.sequence) || packet.sequence<0 ||
      JSON.stringify(Object.keys(packet.tables??{}))!==JSON.stringify(names)) throw Error('ARCHIVE_INVALID');
  let count=0;
  for (const name of names) {
    const rows=packet.tables[name];
    if (!Array.isArray(rows) || (count+=rows.length)>maxRows) throw Error('ARCHIVE_BOUND');
    for (const row of rows) if (!row || JSON.stringify(Object.keys(row))!==JSON.stringify(tables[name]) ||
      Object.values(row).some(v=>v!==null && typeof v!=='string' && (typeof v!=='number' || !Number.isSafeInteger(v)))) throw Error('ARCHIVE_INVALID');
  }
  const meta=packet.tables.transport_meta;
  const shared=packet.tables.apertures.filter(row=>row.id==='shared');
  if (meta.length!==1 || meta[0].id!==1 || !/^[a-f0-9]{32}$/.test(meta[0].epoch) ||
      shared.length!==1 || shared[0].credential_hash!=='NO_CREDENTIAL:shared' || shared[0].revoked!==1 || shared[0].consumed!==0 ||
      packet.tables.messages.some(row=>row.seq>packet.sequence)) throw Error('ARCHIVE_INVALID');
  return count;
}
export async function exportArchive(db,{epoch,schema_sha256,github_anchor}) {
  if (!/^[a-f0-9]{32}$/.test(epoch??'') || !/^[a-f0-9]{64}$/.test(schema_sha256??'') || !anchor.test(github_anchor??'')) throw Error('ARCHIVE_INVALID');
  const reads=await db.batch([
    guard(db,'EXISTS(SELECT 1 FROM transport_meta WHERE id=1 AND epoch=?)',epoch),
    ...names.map(name=>sql(db,`SELECT ${tables[name].join(',')} FROM ${name} ORDER BY ${tables[name].join(',')} LIMIT ?`,maxRows+1)),
    sql(db,"SELECT COALESCE((SELECT seq FROM sqlite_sequence WHERE name='messages'),0) AS seq")
  ]);
  const packet={format:'COM_LOGICAL_ARCHIVE_V1',schema_sha256,github_anchor,
    tables:Object.fromEntries(names.map((name,i)=>[name,reads[i+1].results])),sequence:reads.at(-1).results[0].seq};
  const rowCount=shape(packet,schema_sha256),text=JSON.stringify(packet);
  if (new TextEncoder().encode(text).length>maxBytes) throw Error('ARCHIVE_BOUND');
  return {text,sha256:await digest(text),row_count:rowCount};
}
export async function verifyArchive(text,expectedSha256,schemaHash) {
  if (typeof text!=='string' || new TextEncoder().encode(text).length>maxBytes) throw Error('ARCHIVE_BOUND');
  if (!/^[a-f0-9]{64}$/.test(expectedSha256??'') || await digest(text)!==expectedSha256) throw Error('ARCHIVE_HASH_MISMATCH');
  const packet=parsePayloadJson(text); shape(packet,schemaHash);
  for (const rows of Object.values(packet.tables)) { for (const row of rows) Object.freeze(row); Object.freeze(rows); }
  Object.freeze(packet.tables); Object.freeze(packet);
  verifiedPackets.add(packet); return packet;
}
export async function restoreArchive(db,text,expectedSha256,schemaHash) {
  const packet=await verifyArchive(text,expectedSha256,schemaHash);
  const inserts=names.flatMap(name=>packet.tables[name].filter(row=>!(name==='apertures' && row.id==='shared')).map(row=>
    sql(db,`INSERT INTO ${name}(${tables[name].join(',')}) VALUES(${tables[name].map(()=>'?').join(',')})`,...tables[name].map(key=>row[key]))));
  await db.batch([
    guard(db,names.map(name=>`(SELECT COUNT(*) FROM ${name})=${name==='apertures'?1:0}`).join(' AND ')+
      " AND EXISTS(SELECT 1 FROM apertures WHERE id='shared' AND credential_hash='NO_CREDENTIAL:shared' AND revoked=1 AND consumed=0)"),
    ...inserts,
    sql(db,"DELETE FROM sqlite_sequence WHERE name='messages'"),
    sql(db,"INSERT INTO sqlite_sequence(name,seq) VALUES('messages',?)",packet.sequence)
  ]);
  return {epoch:packet.tables.transport_meta[0].epoch,restored:true,hosted_restore:false};
}
export function archiveHistory(verifiedPacket,aperture,after,limit=20) {
  if (!verifiedPackets.has(verifiedPacket)) throw Error('ARCHIVE_NOT_VERIFIED');
  if (!verifiedPacket.tables.apertures.some(row=>row.id===aperture && row.revoked===0) ||
      !Number.isSafeInteger(after) || after<0 || !Number.isSafeInteger(limit) || limit<1 || limit>100) throw Error('ARCHIVE_READ_INVALID');
  const rows=verifiedPacket.tables.messages.filter(row=>row.seq>after).slice(0,limit+1);
  return {messages:rows.slice(0,limit),has_more:rows.length>limit,
    epoch:verifiedPacket.tables.transport_meta[0].epoch,history_only:true,archive_observation_only:true,sync_complete:false};
}

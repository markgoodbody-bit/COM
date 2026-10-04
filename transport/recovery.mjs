import {verifyArchive} from './archive.mjs';
// Operator-only database routine. Not exposed to ordinary/head-writer HTTP auth.
// This binds an externally retained archive receipt; it does not create a backup
// or prove that the referenced archive exists/is restorable.
export async function advanceCheckpoint(db, input) {
  const {expected_epoch,expected_checkpoint,new_epoch,retained_after,archive_sha256,github_anchor}=input;
  if (!/^[a-f0-9]{32}$/.test(expected_epoch??'') || !/^[a-f0-9]{32}$/.test(new_epoch??'') ||
      !Number.isSafeInteger(expected_checkpoint) || expected_checkpoint<0 || expected_checkpoint===Number.MAX_SAFE_INTEGER ||
      !Number.isSafeInteger(retained_after) || retained_after<0 || !/^[a-f0-9]{64}$/.test(archive_sha256??'') ||
      !/^https:\/\/github\.com\/markgoodbody-bit\/COM\/(issues|pull)\/[1-9][0-9]*(#issuecomment-[0-9]+)?$/.test(github_anchor??'')) {
    throw new Error('INVALID_CHECKPOINT');
  }
  const sql=(text,...args)=>db.prepare(text).bind(...args);
  const result=await db.batch([
    sql(`INSERT INTO mutation_guard(id,ok) VALUES(1,CASE WHEN EXISTS(
      SELECT 1 FROM transport_meta WHERE id=1 AND epoch=? AND checkpoint_version=? AND retained_after<=?
      AND ?<=COALESCE((SELECT MAX(seq) FROM messages),0)) THEN 1 ELSE 0 END)
      ON CONFLICT(id) DO UPDATE SET ok=excluded.ok`,expected_epoch,expected_checkpoint,retained_after,retained_after),
    sql(`INSERT INTO recovery_checkpoints VALUES(?,?,?,?,(SELECT COALESCE(MAX(seq),0) FROM messages),unixepoch(),?,?,
      (SELECT github_anchor FROM comhead WHERE id=1))`,expected_checkpoint+1,expected_epoch,new_epoch,retained_after,archive_sha256,github_anchor),
    sql('UPDATE transport_meta SET epoch=?,retained_after=?,checkpoint_version=? WHERE id=1',new_epoch,retained_after,expected_checkpoint+1),
    // Preserve body/version and prior anchor in the audit, but do not present an
    // old orientation snapshot as CURRENT following a checkpoint/restore.
    sql("UPDATE comhead SET github_anchor='RECOVERY_REAUTHOR_REQUIRED' WHERE id=1"),
    sql('SELECT * FROM recovery_checkpoints WHERE version=?',expected_checkpoint+1)
  ]);
  return result[4].results[0];
}

export async function resolveGap(db,{archive_text,archive_sha256,schema_sha256,aperture,current_epoch,
  checkpoint_version,expected_consumed,dispositions,github_anchor}) {
  const packet=await verifyArchive(archive_text,archive_sha256,schema_sha256);
  const oldEpoch=packet.tables.transport_meta[0].epoch;
  if (!/^[a-f0-9]{32}$/.test(current_epoch??'') || !Number.isSafeInteger(checkpoint_version) || checkpoint_version<1 ||
      !Number.isSafeInteger(expected_consumed) || expected_consumed<0 || typeof aperture!=='string' ||
      !/^https:\/\/github\.com\/markgoodbody-bit\/COM\/(issues|pull)\/[1-9][0-9]*(#issuecomment-[0-9]+)?$/.test(github_anchor??'')) throw Error('INVALID_GAP_RESOLUTION');
  const sql=(text,...args)=>db.prepare(text).bind(...args);
  const guard=(condition,...args)=>sql(`INSERT INTO mutation_guard(id,ok) VALUES(1,CASE WHEN ${condition} THEN 1 ELSE 0 END)
    ON CONFLICT(id) DO UPDATE SET ok=excluded.ok`,...args);
  const meta=await sql('SELECT * FROM transport_meta WHERE id=1').first();
  if (!meta || meta.epoch!==current_epoch || meta.checkpoint_version!==checkpoint_version || expected_consumed>=meta.retained_after ||
      meta.retained_after>packet.sequence || !packet.tables.apertures.some(a=>a.id===aperture && a.revoked===0)) throw Error('GAP_CONTEXT_MISMATCH');
  const boundary=meta.retained_after;
  const expected=packet.tables.messages.filter(m=>m.seq>expected_consumed && m.seq<=boundary &&
    (m.recipient===aperture || m.recipient==='shared')).map(m=>m.seq).sort((a,b)=>a-b);
  if (!Array.isArray(dispositions) || dispositions.length!==expected.length) throw Error('GAP_NOT_ACCOUNTED_FOR');
  const canonical=dispositions.map(row=> {
    if (!row || Object.keys(row).some(k=>!['seq','answered_by','no_answer_owed'].includes(k)) ||
        !Number.isSafeInteger(row.seq) || row.seq<=0 || (row.answered_by===undefined)===(row.no_answer_owed===undefined)) throw Error('INVALID_RECOVERY_DISPOSITION');
    if (row.answered_by!==undefined) {
      if (!Number.isSafeInteger(row.answered_by) || row.answered_by<=0) throw Error('INVALID_RECOVERY_DISPOSITION');
      return {seq:row.seq,answered_by:row.answered_by};
    }
    if (typeof row.no_answer_owed!=='string' || !row.no_answer_owed.trim() || new TextEncoder().encode(row.no_answer_owed).length>1024) throw Error('INVALID_RECOVERY_DISPOSITION');
    return {seq:row.seq,no_answer_owed:row.no_answer_owed};
  });
  if (JSON.stringify(canonical.map(row=>row.seq))!==JSON.stringify(expected)) throw Error('GAP_NOT_ACCOUNTED_FOR');
  const writes=canonical.flatMap(row=>[
    guard('? IS NULL OR EXISTS(SELECT 1 FROM messages WHERE seq=? AND sender=?)',row.answered_by??null,row.answered_by??null,aperture),
    sql(`INSERT INTO recovery_dispositions VALUES(?,?,?,?,?) ON CONFLICT DO NOTHING`,aperture,oldEpoch,archive_sha256,row.seq,JSON.stringify(row)),
    guard(`EXISTS(SELECT 1 FROM recovery_dispositions WHERE aperture=? AND old_epoch=? AND archive_sha256=? AND original_seq=? AND disposition=?)`,
      aperture,oldEpoch,archive_sha256,row.seq,JSON.stringify(row))
  ]);
  const result=await db.batch([
    guard(`EXISTS(SELECT 1 FROM transport_meta WHERE id=1 AND epoch=? AND checkpoint_version=? AND retained_after=?)
      AND EXISTS(SELECT 1 FROM apertures WHERE id=? AND revoked=0 AND consumed IN (?,?))
      AND EXISTS(SELECT 1 FROM recovery_checkpoints WHERE version=? AND new_epoch=? AND prior_epoch=? AND archive_sha256=?)`,
      current_epoch,checkpoint_version,boundary,aperture,expected_consumed,boundary,checkpoint_version,current_epoch,oldEpoch,archive_sha256),
    ...writes,
    guard(`(SELECT COUNT(*) FROM recovery_dispositions WHERE aperture=? AND old_epoch=? AND archive_sha256=? AND original_seq>? AND original_seq<=?)=?`,
      aperture,oldEpoch,archive_sha256,expected_consumed,boundary,expected.length),
    sql(`INSERT INTO gap_resolutions VALUES(?,?,?,?,?,?,?,?,unixepoch()) ON CONFLICT DO NOTHING`,
      aperture,current_epoch,checkpoint_version,oldEpoch,archive_sha256,expected_consumed,boundary,github_anchor),
    guard(`EXISTS(SELECT 1 FROM gap_resolutions WHERE aperture=? AND current_epoch=? AND checkpoint_version=? AND old_epoch=?
      AND archive_sha256=? AND prior_consumed=? AND retained_boundary=? AND github_anchor=?)`,
      aperture,current_epoch,checkpoint_version,oldEpoch,archive_sha256,expected_consumed,boundary,github_anchor),
    sql('UPDATE apertures SET consumed=? WHERE id=? AND consumed=?',boundary,aperture,expected_consumed),
    sql('SELECT * FROM gap_resolutions WHERE aperture=? AND current_epoch=? AND checkpoint_version=?',aperture,current_epoch,checkpoint_version)
  ]);
  return result.at(-1).results[0];
}

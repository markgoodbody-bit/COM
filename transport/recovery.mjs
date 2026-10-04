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

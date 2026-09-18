# PSFH / Remark42 restore-guard probe — 18 September 2026

Status: **SYNTHETIC LOOPBACK / NO PUBLIC INTAKE / NO REAL PERSON DATA / NO DEPLOYMENT**

## Question

Can PSFH prevent a retained pre-deletion Remark42 backup from silently republishing text that the project has already accepted for removal, without replacing Remark42 storage?

## Proposed smallest mechanism

Keep a separate removal receipt containing only:
- site id;
- thread URL;
- Remark42 comment id;
- accepted removal timestamp;
- bounded reason / operator receipt id.

Do **not** retain the removed guest text in the receipt.

Restore procedure:

1. take the public route out of service;
2. restore the selected Remark42 backup;
3. replay accepted removal receipts against restored state;
4. verify removed text is absent;
5. only then reopen the public route.

This is an operational guard, not backup erasure.

## Expected ceilings

`RESTORE_GUARD != BACKUP_PURGE`

`REPLAYED_DELETE != LEGAL_ERASURE`

`REMOVAL_RECEIPT != IDENTITY_PROOF`

`LOOPBACK_QUIESCE != PRODUCTION_PROXY_GATE`

If comment IDs do not survive restore, or admin replay cannot reliably re-delete the restored object, this route fails.

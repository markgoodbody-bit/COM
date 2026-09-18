# PSFH / Remark42 backup-erasure probe — 18 September 2026

Status: **SYNTHETIC LOOPBACK PROBE / NO PUBLIC INTAKE / NO REAL PERSON DATA / NO DEPLOYMENT**

## Question

> If a visitor mark is deleted from the current Remark42 store, can a retained pre-deletion Remark42 backup restore that text?

This is a narrow #118 custody/removal gate. It is not a general Remark42 security review.

## Why this matters

Current owner documentation says Remark42:
- automatically backs up content;
- keeps up to 10 backup files by default (`MAX_BACKUP_FILES=10`);
- can restore a native backup, replacing current comments with the backup contents.

Owner:
https://github.com/umputun/remark42

The earlier PSFH loopback probe established that a deleted comment disappears from the **current owner readback**. That did not establish erasure from historical backups.

## Probe

The CI test uses pinned owner image:
`ghcr.io/umputun/remark42:v1.16.4@sha256:980e0e76a6f241cd181f44c5b4d686f0d8cd7f552e11deb3bdcba223b2c3b866`.

It:
1. starts Remark42 on loopback with synthetic local storage;
2. posts one unique synthetic mark;
3. creates a native backup and verifies the marker exists in that backup;
4. deletes the comment and verifies the current public readback no longer contains the marker;
5. restores the **pre-deletion** backup;
6. checks whether the marker becomes current again;
7. emits a small result JSON.

No external account, provider, public endpoint or real visitor is used.

## Interpretation

If the marker returns after restore:

`CURRENT_DELETE = OBSERVED`
`HISTORICAL_BACKUP_RETENTION = OBSERVED`
`CURRENT_DELETE != BACKUP_ERASURE`

That would mean a future PSFH intake needs a declared operator policy for backup retention/purge and restoration after erasure requests. It would not mean backups are wrong or that Remark42 promises otherwise.

If the marker cannot be restored, inspect why before claiming backup-erasure semantics.

## Boundaries

`SYNTHETIC RESTORE != PRODUCTION DATA GOVERNANCE`
`BACKUP CONTAINS OLD TEXT != PUBLICLY REACHABLE OLD TEXT`
`CURRENT DELETE != LEGAL ERASURE`
`OWNER BEHAVIOUR != PSFH POLICY`

No guestbook deployment follows from this probe.
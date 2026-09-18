# Remark42 backup-erasure result — 18 September 2026

Status: **OWNER BEHAVIOUR OBSERVED / PSFH BACKUP POLICY REQUIRED / NO DEPLOYMENT**

## Exact witness

Pinned owner image:
`ghcr.io/umputun/remark42:v1.16.4@sha256:980e0e76a6f241cd181f44c5b4d686f0d8cd7f552e11deb3bdcba223b2c3b866`

Exact repaired probe head:
`c40b97592013c81aab1990f896c14d265cae075a`

Hosted workflow:
`35394959223 SUCCESS`

Artifact:
- name: `psfh-remark42-backup-erasure-result`
- id: `10566709330`
- zip SHA-256: `a721e2dd2a6f1a376f2534d945cd05dcb0929ed4d53689c6763eebf93b586041`

Measured synthetic lifecycle:

```text
pre_delete_backup_contains_marker              = true
current_after_delete_contains_marker           = false
restored_from_pre_delete_backup_contains_marker = true
```

No real person data or public endpoint was used.

## Interpretation

Remark42 deletion removed the synthetic mark from the current public readback.

A pre-deletion native backup retained the mark.

Restoring that retained backup made the mark current again.

Therefore:

`CURRENT DELETE = OBSERVED`
`CURRENT DELETE != BACKUP ERASURE`
`RETAINED PRE-DELETE BACKUP CAN REINTRODUCE DELETED TEXT = OBSERVED`

This is ordinary backup behavior, not a Remark42 defect.

## Owner backup semantics

Current Remark42 owner docs/code state:
- automatic backups are made daily under `BACKUP_PATH`;
- backup content is exported/gzipped comments;
- `MAX_BACKUP_FILES` defaults to 10;
- restore cleans the current data store and replaces comments from the selected backup;
- manual backup command creates `userbackup-{site}-{timestamp}.gz`;
- automatic cleanup only considers files prefixed `backup-<site>`, so manual `userbackup-…` files are outside that automatic rotation path.

Thus a PSFH removal promise cannot be defined only against current owner readback.

## Smallest PSFH requirement

A future intake architecture using Remark42 needs a written backup/removal policy that distinguishes:

1. current public state;
2. automatic local backups;
3. manual backups;
4. off-host / operator copies if any;
5. restoration procedure after a removal request.

At minimum, restoration must not silently republish text that the project has already accepted should be removed.

The exact retention/purge period is a policy/legal/operator decision and is **not** set by this probe.

## Production-security owner requirement

Current Remark42 documentation also states that when deployed behind a reverse proxy, `trusted-proxy` must be configured to the proxy network. If unset, forwarding headers are trusted from any client and can be spoofed, undermining per-IP rate limiting and vote deduplication.

This is an owner configuration obligation, not a PSFH-specific security mechanism.

## Current #118 consequence

`REMARK42 OWNER ROUTE = PLAUSIBLE`
`SMALL PSFH TRUST/CONTENT ADAPTER = PROVEN IN LOOPBACK`
`CURRENT DELETE = PROVEN IN LOOPBACK`
`BACKUP ERASURE = NOT PROVIDED AUTOMATICALLY`
`BACKUP/RESTORE POLICY = REQUIRED BEFORE INTAKE`
`TRUSTED-PROXY / PRODUCTION CONFIG = REQUIRED BEFORE INTAKE`
`PUBLIC DEPLOYMENT = NOT EARNED`

Do not build a custom persistence layer merely to avoid writing the policy. Use the owner where it fits; make the remaining custody obligations explicit.

`OWNER + SMALL ADAPTER + EXPLICIT CUSTODY POLICY > REBUILD OWNER`
`REMOVAL FROM LIVE VIEW != REMOVAL FROM RETAINED BACKUPS`
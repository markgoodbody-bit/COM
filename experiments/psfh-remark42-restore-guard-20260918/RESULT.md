# Remark42 restore-guard result — 18 September 2026

Status: **RESTORE REPLAY GUARD OBSERVED / BACKUP PURGE NOT ESTABLISHED / NO PUBLIC INTAKE**

## Exact witness

Owner image:
ghcr.io/umputun/remark42:v1.16.4@sha256:980e0e76a6f241cd181f44c5b4d686f0d8cd7f552e11deb3bdcba223b2c3b866

Exact branch head before result note:
e664382c49efa089bc5eda5262d8c6f148d5eb5b

Workflow:
35396238925 SUCCESS

Artifact:
- id 10567791724
- zip SHA-256 77f2c1d092d6a3f71d05ef20cc5bb142117664e21ccae4f2589847396040bd0a

Observed:

pre_delete_backup_contains_marker = true
current_after_accepted_removal_contains_marker = false
after_restore_before_replay_contains_marker = true
comment_id_survived_restore = true
removal_receipt_contains_removed_text = false
replay_admin_delete_status = 200
after_tombstone_replay_contains_marker = false

## What this establishes

A retained pre-removal Remark42 backup can reintroduce removed text.

The restored object keeps the same comment ID.

A separate removal receipt that retains the object identifier but not the removed text can be replayed through Remark42's existing admin deletion route and remove the restored text again.

Therefore the smallest safe restoration procedure is mechanically plausible:

QUIESCE PUBLIC ROUTE -> RESTORE OWNER BACKUP -> REPLAY ACCEPTED REMOVAL RECEIPTS -> VERIFY ABSENCE -> REOPEN

## What this does not establish

RESTORE_GUARD != BACKUP_ERASURE
REPLAYED_DELETE != LEGAL_ERASURE
REMOVAL_RECEIPT != IDENTITY_PROOF
LOOPBACK_ONLY != PRODUCTION_PROXY_GATE_PROVEN

Backups may still contain removed historical text until retention/purge policy removes them. Off-host/operator copies remain a separate custody obligation.

## #118 consequence

REMARK42 OWNER ROUTE = PLAUSIBLE
SMALL PSFH TRUST/CONTENT ADAPTER = PROVEN IN LOOPBACK
CURRENT DELETE = PROVEN IN LOOPBACK
OLD BACKUP RESURRECTION = PROVEN IN LOOPBACK
POST-RESTORE TOMBSTONE REPLAY = PROVEN IN LOOPBACK
BACKUP RETENTION/PURGE POLICY = STILL REQUIRED
PRODUCTION PROXY/SECURITY = STILL REQUIRED
PUBLIC INTAKE = NOT EARNED

This narrows the remaining work from build different storage to explicit custody/retention policy plus production deployment/security gates.

OWNER + SMALL ADAPTER + REMOVAL REPLAY + EXPLICIT CUSTODY POLICY > REBUILD OWNER
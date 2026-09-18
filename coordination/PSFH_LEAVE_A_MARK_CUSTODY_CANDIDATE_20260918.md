# PSFH Leave a Mark — custody and removal candidate — 18 September 2026

Status: **OPERATIONAL CANDIDATE / NOT PRIVACY NOTICE / NOT LEGAL ADVICE / NO PUBLIC INTAKE / NO RETENTION PERIOD SELECTED**

Purpose: turn the now-observed Remark42 lifecycle into a small explicit custody contract for PSFH #118 without pretending that a loopback probe or owner defaults settle UK data-protection obligations.

## 1. Purpose boundary

Leave a Mark exists only to let a visitor voluntarily leave a short record of presence.

It is not:
- an identity system;
- a community membership roll;
- an engagement metric;
- a behavioural tracking system;
- a mailing list;
- a profiling surface.

Purpose drift must trigger review of the data contract before reuse.

## 2. Data minimisation

Candidate visitor-supplied fields remain:
- short plain-text mark;
- optional claimed_name;
- optional claimed_kind;
- optional claimed_note;
- optional claimed encounter metadata, clearly named as claimed rather than observed.

System-established metadata may include:
- receiver receipt time;
- Remark42 comment/object identifier;
- publication/moderation state;
- receiver/deployment version;
- removal/correction state.

No visitor HTML, Markdown links, attachments, fetched URLs or silent tracking are part of v0.

## 3. Removal receipt

When a removal is accepted, keep the smallest receipt needed to honour it after restore.

Candidate receipt fields:
- site / trust-region id;
- thread/register locator;
- Remark42 comment id;
- accepted_removal_at;
- bounded operator/request receipt id;
- replay / verification state.

Do not retain the removed guest text in the removal receipt merely to prove what was removed.

The removal receipt may itself still be personal data if it can be linked to an individual or their contribution. Treat it as governed data rather than a magical non-personal tombstone.

## 4. Live deletion

Observed in the pinned Remark42 loopback:
- current deletion removes the synthetic mark from current readback;
- current deletion does not erase retained pre-deletion backups.

Therefore:

CURRENT_DELETE != BACKUP_ERASURE

## 5. Backup handling

ICO owner guidance currently says that where a valid erasure request applies, organisations must take steps concerning backup systems as well as live systems. It recognises that backup copies may remain for a period before overwrite, but the key issue is putting the data beyond use, not using it for other purposes, and governing replacement through an established schedule.

Owner guidance:
https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/
https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/

PSFH candidate requirement:
- enumerate automatic backups;
- enumerate manual backups;
- enumerate any off-host/operator copies;
- select and justify a retention schedule before intake;
- state the schedule/criteria honestly to visitors;
- ensure removed data in retained backups is beyond ordinary use;
- do not create new manual/off-host copies outside the declared process.

Remark42 owner defaults are implementation facts, not PSFH retention policy.

## 6. Safe restoration

Observed in experiment:
- pre-removal backup can reintroduce removed text;
- restored comment id remained stable;
- replaying the separate removal receipt through Remark42 admin deletion returned 200;
- after replay, the marker was absent again;
- removal receipt contained no removed text.

Required runbook:

QUIESCE PUBLIC ROUTE
-> RESTORE SELECTED OWNER BACKUP
-> REPLAY ALL ACCEPTED REMOVAL RECEIPTS RELEVANT TO THAT BACKUP
-> VERIFY REMOVED CONTENT ABSENT
-> REOPEN

Do not restore an old backup directly into publicly reachable service and repair removals afterward.

RESTORE_GUARD != BACKUP_PURGE
REPLAYED_DELETE != LEGAL_ERASURE

## 7. External recipients / public copies

A published mark is public information. A future privacy notice must be clear that third parties may independently copy public content.

Where applicable, current ICO guidance says erasure of data disclosed or made public can create duties to inform recipients/other controllers, subject to the legal tests and reasonableness/disproportionate-effort provisions.

PSFH must not promise that deleting its copy can erase independent copies from the wider internet.

## 8. Logs and infrastructure

Before intake, identify personal data in:
- reverse-proxy/access logs;
- Remark42 logs;
- hosting/provider logs;
- abuse/rate-limit state;
- monitoring/error services, if any;
- backup/object storage metadata.

No analytics/telemetry should be added merely because intake exists.

Production Remark42 deployment must also satisfy the owner's trusted-proxy requirement where a reverse proxy is used; loopback success is not production network-security evidence.

## 9. Retention decisions still deliberately open

Do not invent a retention number from owner defaults.

Before public intake a human/controller decision is still required for:
- retention period or defensible criteria for published marks;
- automatic backup retention;
- manual backup policy;
- off-host backup policy;
- removal-receipt retention;
- logs/security-event retention;
- lawful basis and privacy-notice wording;
- handling of valid/refused/ambiguous removal requests;
- recipient notification process where applicable.

ICO storage-limitation guidance says retention should be purpose-based, justified, documented, periodically reviewed, and use standard periods where possible. UK GDPR itself does not supply a universal guestbook retention number.

## 10. Current technical disposition

REMARK42 STORAGE / AUTH / MODERATION / EXPORT = OWNER
PSFH TRUST / CONTENT ADAPTER = SMALL CUSTOM BOUNDARY
CURRENT LIVE DELETE = OBSERVED
BACKUP RESURRECTION = OBSERVED
RESTORE REMOVAL REPLAY = OBSERVED
BACKUP PURGE / RETENTION = POLICY NOT YET CHOSEN
PRODUCTION SECURITY = NOT ESTABLISHED
PUBLIC INTAKE = NOT EARNED

## 11. Gate

Do not deploy intake until:
1. retention/custody choices above are explicitly made;
2. privacy transparency is written at the strength actually supportable;
3. production reverse-proxy/security behaviour is tested;
4. operator burden and stop-switch ownership are named;
5. public trust-region separation remains intact.

OWNER + SMALL ADAPTER + REMOVAL REPLAY + EXPLICIT CUSTODY POLICY > REBUILD OWNER
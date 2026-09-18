# PSFH Leave a Mark — smallest remaining human decision packet — 18 September 2026

Status: **DECISION PREP / NOT ADOPTED / NOT PRIVACY NOTICE / NOT LEGAL ADVICE / NO PUBLIC INTAKE**

Purpose: reduce PSFH #118 from an open architecture problem to the smallest set of human/controller choices that genuinely remain after owner reuse, loopback falsification, restore-guard testing and current owner/legal-guidance checks.

## 1. What is already earned

Technical path:

```text
Remark42 v1.16.4
+ small PSFH trust/content adapter
+ explicit removal receipt
+ restore guard:
  QUIESCE -> RESTORE -> REPLAY REMOVALS -> VERIFY -> REOPEN
= technically plausible bounded v0
```

Observed:
- anonymous/account-free intake can work;
- PSFH-specific tiny plain-text/no-link contract can be enforced before owner receipt;
- guest bytes can remain in a separate trust region;
- current deletion removes the mark from current readback;
- pre-deletion backups can reintroduce removed text;
- stable comment id survived restore;
- a separate text-free removal receipt can replay deletion after restore;
- export and stop/read-only controls exist.

Not observed:
- production-host security;
- real visitor custody;
- public removal-request operations;
- off-host backup behavior;
- real-world moderation/operator burden.

## 2. Security correction — pinned v1.16.4 remains a valid tested basis

A fresh security pass initially raised concern because two 2026 Remark42 advisories were published after the 10 July v1.16.4 release.

Commit ancestry resolves that concern.

Email notification sanitization:
- fix commit: `3e18681ca7b9718d5536debc738018ae76cfe964`;
- message: `Sanitize comment text in email notifications (GHSA-74pc-3r2m-ppx3)`;
- commit date: 30 June 2026;
- `v1.16.4` is 24 commits ahead with that fix as merge-base ancestor.

Forwarded-IP / rate-limit bypass:
- primary fix: `b1502801facd7782a1c70fd51f8ad5c2eb650d39`;
- follow-up: `e62b3c830d81659cf5d2687b0c8261da7d42fdab`;
- commit dates: 5 / 9 July 2026;
- both are ancestors of `v1.16.4`.

Therefore:

```text
ADVISORY_PUBLISHED_AFTER_RELEASE != RELEASE_MISSING_FIX
PINNED_V1.16.4_CONTAINS_THE_TWO_CHECKED_FIXES = OBSERVED
TRUSTED_PROXY_CONFIGURATION_STILL_REQUIRED = YES
```

This does not certify v1.16.4 generally secure. It only closes these two specific concerns.

## 3. Current ICO owner guidance

Current ICO guidance checked 18 September 2026 says:
- personal data must not be kept longer than needed for the stated purpose;
- organisations should be able to justify retention and document standard periods where possible;
- UK GDPR supplies no universal time limit;
- valid erasure requests can require action across live and backup systems;
- backup copies may remain pending overwrite under an established schedule if they are put beyond use and not reused;
- people must be told clearly what happens to backup copies.

The ICO pages currently warn that some guidance is under review following the Data (Use and Access) Act. Re-read before deployment.

## 4. Recommended minimal operational candidate

These are **Framework recommendations**, not adopted policy.

### A. Public mark lifetime

Candidate:
> A published mark remains part of the public register while the register exists unless it is corrected/removed under the stated process or continued retention is no longer justified.

Reason:
the purpose is a voluntary historical presence record. Arbitrary short expiry defeats that purpose.

Important:
`PUBLIC_RECORD_PURPOSE != IMMUTABLE_FOREVER`.

### B. Automatic backups

Candidate:
> Use Remark42's bounded automatic backup mechanism only; keep the default maximum of 10 daily backups unless production testing gives a concrete reason to change it.

Owner behavior:
- backup interval = 24 hours;
- `MAX_BACKUP_FILES` default = 10.

This creates a roughly ten-backup rolling window; it is an implementation default, not a legal safe harbor.

Why recommend it:
- enough to make restore mechanically meaningful;
- bounded;
- already tested by the owner path;
- avoids inventing a large archival layer.

### C. Manual / off-host copies

Candidate v0:
> No routine manual or off-host copies of guest content.

If one is later needed, add it to the custody inventory before creating it.

This sharply reduces the erasure surface.

### D. Removal receipts

Candidate:
> Keep only the text-free removal receipt needed to prevent resurrection for as long as any retained backup capable of reintroducing that mark still exists, plus until a verification step establishes that the relevant backup window has expired/been replaced.

Do not pick an arbitrary multi-year period.

Receipt does not retain removed mark text.

### E. Restore behavior

Candidate:
> Never restore directly into a publicly reachable instance.

Required:
```text
QUIESCE
-> RESTORE
-> REPLAY ACCEPTED REMOVALS
-> VERIFY ABSENCE
-> REOPEN
```

Already mechanically demonstrated in the synthetic loopback probe.

### F. Logs / telemetry

Candidate:
- no analytics;
- no behavioral tracking;
- no guest-content copies in application/security logs by design;
- retain only infrastructure/access/security logging actually needed for operation and abuse control;
- production host/proxy retention period must be inspected before deployment rather than assumed.

No numeric log-retention recommendation is adopted here because host/topology is not selected.

### G. Stop switch

Candidate:
> intake can be disabled without removing existing published marks or preventing valid correction/removal work.

No available custody capacity -> close intake visibly rather than accumulate obligations.

## 5. Human decisions that remain

### Decision 1 — public-record purpose

Proposed answer:
**YES** — published marks may remain while the register exists, subject to correction/removal and periodic purpose review.

Human/controller adoption required.

### Decision 2 — automatic backup window

Proposed answer:
**YES** — accept the bounded owner default of 10 automatic daily backups for v0.

Human/controller adoption required because this becomes part of the retention/custody representation.

### Decision 3 — manual / off-host guest-data backups

Proposed answer:
**NO** for v0.

Human/controller adoption required.

### Decision 4 — removal-receipt retention rule

Proposed answer:
**backup-capability bounded**, not a fixed long duration:
retain until no retained backup can resurrect the mark and the removal has been verified across that boundary.

Human/controller adoption required.

### Decision 5 — operator

Needs an explicit human/controller statement naming who is responsible for:
- stopping intake;
- responding to removal/correction requests;
- restoring service;
- inspecting backups/logs;
- deciding ambiguous requests.

Framework can prepare evidence/runbooks but must not silently become legal/data controller or sole operator.

### Decision 6 — lawful basis + privacy information

**OPEN / HUMAN-LEGAL GATE.**

Do not infer a lawful basis merely because submission is voluntary.

Before intake:
- identify controller;
- identify lawful basis at the strength actually supportable;
- write concise privacy information;
- state backup/removal behavior honestly;
- state that public marks may be copied independently by third parties;
- explain how to request correction/removal.

If legal uncertainty remains material, obtain appropriate human legal advice before deployment.

### Decision 7 — production topology

Still choose/test:
- host;
- reverse proxy;
- exact trusted-proxy CIDR/IP;
- TLS;
- public origin;
- storage location;
- infrastructure/access-log behavior;
- spending cap / resource limit.

This is infrastructure selection, not a reason to rebuild Remark42.

## 6. What is no longer an open architecture question

Do not reopen by momentum:
- custom database;
- custom auth;
- custom moderation backend;
- custom backup engine;
- custom evidence-map product;
- public Git as guest-data database;
- engagement counters;
- signature/identity system.

## 7. Current go/no-go

```text
REPRESENTATION = EARNED
OWNER ROUTE = PLAUSIBLE
DELETE / RESTORE GUARD = EARNED IN SYNTHETIC LOOPBACK
SPECIFIC CHECKED SECURITY FIXES = PRESENT IN V1.16.4
RETENTION / CUSTODY DECISION = HUMAN GATE
LAWFUL BASIS / PRIVACY NOTICE = HUMAN-LEGAL GATE
PRODUCTION TOPOLOGY = UNSELECTED / UNTESTED
PUBLIC INTAKE = NOT YET EARNED
```

If the human decisions above are accepted, the next engineering action should be a **private production-shaped deployment rehearsal with synthetic data only**, not a public launch.

That rehearsal should test:
1. exact pinned image digest;
2. TLS + reverse proxy + trusted-proxy behavior;
3. rate limiting from real proxy topology;
4. PSFH adapter;
5. backup schedule;
6. removal + restore replay;
7. stop switch;
8. log/data inventory;
9. export;
10. complete teardown.

Only after that rehearsal survives should public intake return to the decision surface.

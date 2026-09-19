# NVIDIA Claw EvidenceWatch — Claude Code final hostile review packet — 19 September 2026

Status: **PRE-SUBMISSION HOLD FOR INDEPENDENT CC REVIEW / NO SUBMISSION TONIGHT**

Purpose:
Give Claude Code one bounded independent pass before Mark records/submits EvidenceWatch.

This is not an invitation to redesign the product by momentum.

## Exact candidate

Repository:
`markgoodbody-bit/campfire-relay`

Draft PR:
`#248 — NVIDIA Claw: EvidenceWatch long-running evidence drift agent`

Exact head:
`ee362ce0105565815ad2695f12db0481fab5f638`

Base Relay main:
`32143937d6a642a6f5e2404d368fd09aa4d54da9`

Hosted:
`campfire-ci 1598 / 35452177273 — SUCCESS`

Candidate folder:
`competition/nvidia-claw-evidencewatch/`

Do not review mutable later head without first reporting the mismatch.

## Challenge

NVIDIA London Claw Agent Challenge.

Registered judging dimensions:
1. successful deployment / technical execution;
2. innovation & creativity;
3. real-world value.

Submission form accepts:
- demo video up to 3 min, 30–90 sec preferred; OR
- project link.

Parent Campfire Relay repo is private. Current preferred submission route is video; do not make the whole repo public by momentum.

## Current one-sentence product

> EvidenceWatch tells you when the evidence underneath an important claim materially changes after you have already relied on it — and which downstream decision or report now needs review.

## Product claim ceiling

Do not treat EvidenceWatch as:
- truth verification;
- a universal provenance system;
- validated correction classification;
- production-ready;
- proven novel;
- proven demanded by users.

Working product hypothesis is the conjunction:

```text
POST-RELIANCE CLAIM MONITORING
+ CROSS-SOURCE SEMANTIC STATE
+ SOURCE ANCESTRY / INDEPENDENCE
+ EXPLICIT CANONICAL + TEMPORAL AUTHORITY
+ CORRECTION-PRESERVING MEMORY
+ MATERIAL-DELTA FILTER
+ "WHAT MUST I REVISIT?" DEPENDENCY ROUTING
```

## Real evidence already witnessed

### Real NVIDIA provider

Model:
`nvidia/nemotron-3-super-120b-a12b`

Real hosted NVIDIA endpoint returned structured analysis and:
`NVIDIA_PROBE_OK`.

### Real public-source correction sequence

Anthropic July owner page:
- baseline 3 incidents.

Anthropic September owner page:
- later correction 4 incidents.

Clean live run:
```text
July      -> BASELINE_ESTABLISHED -> 3
September -> MATERIAL_DELTA       -> 4
canonical -> 4
alerts    -> 1
```

Fresh process / same ledger:
```text
July      -> DUPLICATE_OBSERVATION
September -> DUPLICATE_OBSERVATION
canonical -> 4
newAlerts -> []
```

### Real unattended scheduler

Exact candidate head ran:
`npm run live`

Fresh unattended audit ledger, 10-second interval.

First autonomous heartbeat:
- baseline 3;
- correction 4;
- one alert.

Six subsequent autonomous heartbeats:
- duplicate observation;
- duplicate observation;
- canonical 4;
- no new alerts.

Operator stopped process only to bound duration.

## Real defects found and repaired during live testing

Do not erase these from assessment.

1. successful fetch + failed analysis was originally mislabelled unreachable;
2. old ledger format could reprocess completed observations after code upgrade;
3. historical July authority could temporarily roll canonical state backward after September;
4. broad `/news` parent page could enter candidate discovery;
5. documented `npm run live` initially had no package script;
6. internal Airtable form map containing Mark's email entered judge-facing branch;
7. private parent repo made proposed GitHub project-link fallback unusable;
8. stale T&C status remained in submission docs.

All above were repaired before current exact head.

## Current source protections

- append-only ledger;
- exact-content fingerprints;
- duplicate suppression;
- explicit `stateAuthority`;
- explicit `authorityAsOf`;
- historical authority cannot roll back newer canonical state;
- supporting/derivative source cannot silently overwrite canonical state;
- fetch failure distinct from analysis failure;
- failed analysis retry does not duplicate source observation;
- bounded same-origin discovery;
- model-invented URLs rejected;
- broad ancestor/root indexes rejected;
- local project `.gitignore` protects `.env*`, `data/`, `*.log`.

## Challenge rules already reviewed

Official Rules Section 2:
- UK resident;
- 18+;
- individual entry.

Source defects preserved:
- Section 3 inexplicably says "Spain";
- Section 5 says "PST" while registered page timing aligns to PDT/BST.

No project ownership assignment or broad project copyright licence was found in the supplied Official Rules.

Do not infer legal certainty beyond supplied text.

## What CC should review

Please perform a hostile, source-bound pre-submission review of exact head.

### A. Functional correctness

Try to falsify:
- canonical state reconstruction;
- temporal authority ordering;
- duplicate suppression;
- crash/retry handling;
- scheduler behavior;
- source discovery constraints;
- downstream dependency routing.

Report any path where the system can:
- silently manufacture canonical truth;
- roll state backward improperly;
- duplicate material alerts;
- lose a material correction;
- call NVIDIA unnecessarily;
- convert model relation into authority.

### B. Competition fit

Evaluate descriptively against:
- successful deployment;
- innovation/creativity;
- real-world value.

Do not predict prize outcome.

Identify any judge-facing gap that is material enough to repair before submission.

### C. Claims / overclaim

Compare:
- README;
- submission packet;
- copy bank;
- demo script;
- source attribution;
- terms review.

Flag:
- unsupported novelty claims;
- statements stronger than live evidence;
- fixture/live ambiguity;
- inaccurate NVIDIA/OpenClaw/NemoClaw framing;
- stale status.

### D. Security / privacy / publication

Check for:
- credentials;
- personal data;
- local paths;
- ledger artifacts;
- private-repo links described as public;
- unsafe API-key instructions;
- accidental publication of internal coordination material.

### E. Demo/video

Review:
`docs/FINAL_DEMO_VIDEO.md`

Ask:
- Can a judge understand the problem in <10s?
- Does the demo prove long-running behavior rather than merely narrate it?
- Is the distinction between deterministic UI demo and real live witness unmistakable?
- Is any scene unnecessary?
- Is there a simpler sequence Mark can actually record cleanly?

## Requested CC output

Return exactly:

```text
CC FINAL REVIEW — EVIDENCEWATCH

EXACT_HEAD:
HEAD_MATCH: YES / NO

BLOCKERS:
- ...

MATERIAL_REPAIRS:
- ...

NONBLOCKING:
- ...

CLAIM_CHECK:
- ...

SECURITY_PRIVACY:
- ...

COMPETITION_FIT:
- ...

VIDEO:
- ...

VERDICT:
CLEAR_TO_RECORD
or
REPAIR_BEFORE_RECORD

EVIDENCE_CEILING:
...
```

No submission, merge, public-repo creation, spending, or external contact.

`CC REVIEW != VALIDATION`
`CLEAR_TO_RECORD != CLEAR_TO SUBMIT`

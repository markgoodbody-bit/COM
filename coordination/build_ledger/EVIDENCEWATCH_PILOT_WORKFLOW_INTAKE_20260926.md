# EvidenceWatch — pre-pilot workflow and burden intake

Date: 26 September 2026

Status: **INTEGRATED / PRE-PILOT ONLY / NO CONTACT / NO PARTNER / NO LIVE PILOT**

Current EvidenceWatch private main:
`f08e35086a3a6b7c16de72f42f060d47b0ab1ae7`

PR:
`#16 — Add pre-pilot workflow and burden intake`

Reviewed head:
`93dd9e6e35007cd07fb6d2f0a176782080d5af1b`

Post-merge CI:
`36236672975 / SUCCESS`
- Ubuntu: SUCCESS
- Windows: SUCCESS
- **59 tests / 59 pass / 0 fail**

## Why this was earned

The public University of Bern living-review specimen established that:
- post-reliance source succession/change is real work;
- competent existing practice already handles at least this class;
- public workload context exists;
- episode-specific current burden/value remains unknown.

Therefore the next gap is not another detection feature.

It is:

```text
CURRENT WORKFLOW
+ ONE COMPLETED UPDATE EPISODE
+ REAL HUMAN MINUTES
+ EXISTING TOOLS / SIGNALS
+ EXISTING DEPENDENCY MAP
+ TEAM-DEFINED USEFULNESS / STOP THRESHOLD
```

before EvidenceWatch output is shown.

## Integrated objects

- `docs/PILOT_WORKFLOW_INTAKE.md`
- `examples/pilot-workflow-intake.template.json`
- `src/pilot-intake.mjs`
- `test/pilot-intake.test.mjs`
- README route

## Intake boundary

The intake captures:
- maintained object + bounded decision;
- what is already monitored and by which tools;
- one completed update episode;
- whether the changed/successor source is the same evidentiary root;
- current-practice setup / maintenance / review minutes;
- optional episode-specific burden detail;
- current dependency map;
- correction/escalation path;
- existing failure modes;
- team-defined usefulness and stop thresholds;
- privacy/provider/institutional constraints;
- a freeze receipt before EvidenceWatch results are unblinded.

It distinguishes:
- current practice vs retrospective reconstruction;
- observed/logged burden vs retrospective estimates;
- intake completion vs partner consent.

## Falsification during build

Framework strengthened the first candidate so a frozen Stage-1 intake **cannot omit the completed comparison episode**.

That strengthening initially caused one test-order failure: the "unmeasured burden" regression did not supply the newly required episode and therefore failed earlier for the correct completed-episode reason.

Repair:
- the burden regression now supplies a valid completed episode;
- it reaches and tests the intended unmeasured-burden refusal;
- final cross-platform suite is green.

Preserve:

```text
FROZEN BASELINE WITHOUT COMPLETED EPISODE = REFUSE
RETROSPECTIVE ESTIMATE != OBSERVED TIME
CURRENT PRACTICE != DO-NOTHING BASELINE
INTAKE COMPLETE != CONSENT TO PILOT
59/59 TESTS GREEN != RESEARCHER VALIDATION
```

## Consequence

The machine-side empirical preparation is now sufficient to receive a real workflow without moving the comparison after results.

No:
- researcher contact;
- pilot invitation;
- personal data collection;
- external model call;
- Zotero/ReadCube live integration;
- Digital Science form entry;
- grant submission.

The next stronger evidence still requires a willing current workflow owner / team or the Digital Science human form gate.

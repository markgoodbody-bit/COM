# EvidenceWatch — research-pilot instrumentation receipt

Date: 26 September 2026

Status: **INTEGRATED / OFFLINE MEASUREMENT ONLY / NO RESEARCHER PILOT / NO MODEL CALLS**

Current EvidenceWatch private main:
`6a06e2e40c6bda110e1431c3e57be0b5dd8b9081`

Post-merge CI:
`36201123445 / SUCCESS`

Hosted reviewed-head result:
- PR #13 exact head `556f6be8e11ee068372a1cbc65d581f1ef36c16c`;
- workflow `36201072735 / SUCCESS`;
- **54 tests / 54 pass / 0 fail**.

## PR #12 — predeclared research-workflow pilot protocol

Merged:
`5df6bebaaac3d5feb1ba28a214289574f631281e`

Adds:
- shadow-mode boundary;
- current-practice comparator rather than a do-nothing straw man;
- human reference labels frozen before EvidenceWatch output;
- materiality / downstream-scope / impact-tier separation;
- configuration/corpus/labels frozen before scoring;
- measures for material sensitivity, false-alert burden, downstream routing, time-to-flag and reviewer minutes;
- authority/provenance safety failures kept separate from ordinary accuracy;
- hard stop / narrow conditions;
- bounded success-claim ceiling;
- minimum run receipt;
- staged offline rehearsal -> one-team shadow pilot -> wider work only if earned.

Cochrane remains the stronger owner for systematic-review methods. This is an EvidenceWatch product-evaluation contract, not a new review standard.

## PR #13 — deterministic offline pilot scorer

Merged:
`6a06e2e40c6bda110e1431c3e57be0b5dd8b9081`

Adds:
- `src/pilot-score.mjs`;
- `scripts/score-pilot.mjs`;
- checked-in synthetic fixture;
- scorer tests;
- package command `npm run score:pilot -- <pilot-input.json>`;
- protocol documentation for the input contract.

The scorer consumes already-frozen human labels and EvidenceWatch outputs. It does **not** decide scientific materiality.

Reported outputs include:
- counts / denominators;
- material sensitivity by impact tier;
- false-alert burden;
- positive predictive value;
- downstream exact / partial / missed / extra routing;
- measured alert latency;
- current-practice vs EvidenceWatch observed human-minute burden;
- explicit authority/state-loss failure receipts;
- human stop flags;
- hard-stop reasons.

## Falsification during build

Framework found and repaired a scorer bug before integration:

The first implementation measured latency over all alerted episodes but computed missing-latency count against only resolved-label alerts. An unresolved alerted episode could therefore make the missing count negative.

Repair:
- latency presence/missing denominator now uses all alerted episodes;
- binary accuracy denominators still exclude unresolved human labels;
- regression added.

Preserve:
```text
UNRESOLVED LABEL != NEGATIVE OR POSITIVE CASE
TIMING DATA EXISTS != LABEL RESOLVED
SCORER OUTPUT != MATERIALITY ADJUDICATION
```

## Current boundaries

```text
PILOT PROTOCOL READY != PILOT PARTNER EXISTS
OFFLINE SCORER GREEN != RESEARCHER VALIDATION
54 TESTS GREEN != PRODUCT EFFICACY
NO HIGH-IMPACT MISS IN FIXTURE != ZERO REAL-WORLD MISS RATE
MEASURED BURDEN DELTA IN FUTURE PILOT != GENERAL ROI
```

No:
- research participant;
- external contact;
- Digital Science form entry/submission;
- live provider inference;
- new credential use;
- Zotero/ReadCube live integration;
- pricing/customer claim.

Digital Science proposal synchronization:
- current proposal: **1,443 words**;
- current packet points to EvidenceWatch `6a06e2e4…` / **54 tests**;
- application remains NOT SUBMITTED.

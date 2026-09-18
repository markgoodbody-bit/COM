# BUILD PROCEED — ATRS calibration held clean / THR observation-state repair

Status: **BOUNDED BUILD RECEIPT / NOT CANON / NOT RELEASE / NOT VALIDATION**  
Date: 18 September 2026

## Reacquire

Live COM main at start of this proceed pass:

`bec5f0874a4ba34416385118c20a093b2f223710`

No Codex or Claude Code 16-case ATRS calibration table had landed on PR #364 at the fresh check. Codex had independently FULL COMSYNCed and explicitly left the new method objects for a subsequent review rather than claiming a completed calibration.

Therefore Framework did not add more ATRS interpretation that could contaminate the requested first-pass coding.

```text
CALIBRATION_PENDING -> DO_NOT_TEACH_THE_CODERS_MORE_ANSWERS
```

## #364 state

Unchanged decision gate:

- exact head `e582b709e025f2907bb850cb2b3c681101504aef`;
- workflow `35324172751 SUCCESS`;
- frozen sample identity `c97ea5548ccc26b130a8ffe2783569d6d365897fcf0e04a35fba033486012b54`;
- independent first-pass request remains open;
- Reader Lens remains secondary;
- no participant / organiser / provider action.

## THR observation-state seam

PR #30 still carried one concrete unresolved semantic acceptance:

```text
REPORT PAGE OBSERVATION
+ assertion state changed reported_by_source -> observed
-> validator previously passed
```

Fresh strong-owner check against CRMsci 3.2 supported the narrow distinction that an observation should explicitly relate to an observed entity/situation/proposition. THR's current source observation envelope records bounded source retrieval/inspection but does not type that semantic target.

Framework therefore created stacked draft THR PR #32:

`https://github.com/markgoodbody-bit/human-record/pull/32`

Exact head:

`845b2a0dfb0de049bafb31f7342eaeae12d1fa60`

Repair:
- clarify source observation = bounded source-representation retrieval/inspection;
- clarify assertion direct-evidence implementation boundary;
- temporarily fail closed cross-record assertion states `observed` and `reconciled` until an earned typed observation/reconciliation relation exists;
- preserve `reported_by_source`;
- add the one-word JFK `observed` mutation and parallel `reconciled` mutation as tests;
- no source-kind heuristic;
- no new target ontology;
- no truth checker.

Exact verification:

```text
workflow = 35325473325 SUCCESS
job = 105537388461 SUCCESS
validate_all = PASS
test_validate*.py = 66 tests / OK
existing open-vocabulary warnings = 11
```

Repository-wide search found legitimate record-local/narrative uses of “observed” and “reconciled”, but no production cross-record assertion currently uses `state=observed` or `state=reconciled`. The repair is scoped to cross-record assertion-state validation.

```text
SOURCE_OBSERVATION != DIRECT_WORLD_OBSERVATION
SOURCE_MEDIUM != OBSERVED_OBJECT
STATE_WORD != EVIDENCE_RELATION
FAIL_CLOSED_NOW != PERMANENT_SCHEMA_DECISION
```

PR #32 remains DRAFT / UNMERGED. Codex/CC hostile review was requested before integration.

## Public break aperture

The known defect and PR #32 repair were also exposed on THR issue #31, the already-authorised public “break The Human Record” aperture.

Project comment id:

`5727498127`

This is an invitation to falsify the repair, not a validation request or vote.

## No authority expansion

No:
- THR main/public-record change;
- Hannibal record-4 promotion;
- stewardship/licence change;
- TRACE/ME change;
- human-study action;
- competition registration/submission;
- provider spend;
- private-data collection.

```text
GREEN_CI != MERGE_AUTHORITY
PUBLIC_CRITICISM != VALIDATION
KNOWN_DEFECT_REPAIRED_ON_BRANCH != DEFECT_RESOLVED_ON_MAIN
```

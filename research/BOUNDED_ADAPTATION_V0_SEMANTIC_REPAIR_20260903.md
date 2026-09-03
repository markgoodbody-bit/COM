# Bounded Adaptation Loop v0 — semantic receipt repair

Status: **NON-CANONICAL / CONTRACT REPAIR / NOT ACTIVATED**  
Date: 2026-09-03

## Failure found after the first green fixture run

The earlier positive fixture was accepted as `MOVED` while carrying:

```json
"source_refs": []
```

That contradicted the candidate's own requirement that each cycle name the evidence basis it actually saw. A green structural validator was therefore weaker than the operating contract.

Framework then found additional schema-valid contradictions that the original validator would accept:

- `MOVED` with no selected move;
- `NO_MATERIAL_DELTA` mixed with a real material-delta code;
- `NONE` mixed with a real unknown code;
- `completed_at_utc` earlier than `started_at_utc`;
- a temporary reprioritisation already expired before cycle completion;
- `oldest_unresolved_lane_code = NONE` paired with a non-null dwell age.

These are not new adaptation powers. They are refusal rules for internally contradictory receipts.

## Repair

`research/validate_bounded_adaptation_v0_fixtures.py` now applies a bounded semantic pass after structural/profile validation:

- at least one source reference is required;
- cycle completion cannot precede start;
- `NO_MATERIAL_DELTA` is exclusive;
- `NONE` unknown is exclusive;
- `MOVED` requires an actual selected move and cannot claim no material delta;
- `NO_MATERIAL_MOVE` requires the corresponding move and delta code;
- `PAUSED` / `ESCALATED` must name their matching move;
- every temporary adaptation must correspond to a selected move and expire after cycle completion;
- oldest-lane code and age must agree about whether a lane exists.

The fixture bundle now contains one valid positive and ten hostile negatives, including the four earlier acceptance fixtures.

Exact CI run `33737880874` passed all 11 fixtures.

## Evidence ceiling

This does not establish that the Bounded Adaptation Loop is safe, useful, complete or merge-ready. It establishes only that these reproduced false-accept paths now refuse in the executable fixture validator.

Independent exact-current-head attack remains required. In particular, reviewers should still look for receipt combinations that are individually well typed but jointly imply an authority, permanence, currentness or evidence claim the profile does not support.

No daemon activation, merge, provider spend, credential use, Square actuation, release/canon mutation or authority expansion follows.

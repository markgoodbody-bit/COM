# CC BUILD CONTRACT — Reciprocal Delegation v0.2 failure/recovery companion

Status: **BUILD ASSIGNMENT / NON-PRODUCTION / NOT AUTHORITY**

Owner: Claude Code aperture  
Base: COM `e2311d37c66c57bb99e487f73cc321a8e70e007f`  
Branch: `cc/reciprocal-delegation-v0-2-failure-recovery-20260911`

## Build, do not merely review

Use the merged v0.2 field repair and the observed D046 trace as inputs. Produce an exact non-production recovery object for the problem D046 exposed: **one mutator stops or stalls and another takes over without overlap, stale-head fiction or accidental authority widening**.

Minimum deliverables under `reference/reciprocal_delegation/v0_2/recovery/`:

1. an inspectable transfer/takeover state machine (`json` preferred);
2. a stdlib validator or deterministic checker for the cross-state rules;
3. at least two PASS fixtures and three FAIL fixtures;
4. a concise README naming what the object does and does not establish.

The build should cover, at minimum:

- exact current head must be reacquired at transfer/takeover;
- old claims become historical when the head moves;
- two active mutators on the same named object are invalid unless the object itself is split into disjoint write scopes;
- takeover/handoff must name why the previous lane stopped, stalled, narrowed or returned control;
- successful prior delivery does not widen the new mutator's scope;
- a hand-back/receipt is not agreement, approval or review;
- recovery after a broken/partial mutation preserves history rather than rewriting the record;
- the new mutator must inherit the no-touch and consequential gates unless a new explicit authorization changes them.

Do **not** assume that elapsed wall-clock time alone proves a lane is stalled. Do not invent identity continuity. Do not add live execution or Campfire Production hooks.

Potential failure fixtures (adapt or replace if a stronger construction emerges):

- `double_mutator_same_object.json` — FAIL;
- `takeover_from_stale_head.json` — FAIL;
- `success_widens_scope_implicitly.json` — FAIL;
- `clean_handoff_exact_head.json` — PASS;
- `stalled_lane_named_transfer.json` — PASS.

Return a build, not a critique essay. If the v0.2 core schema itself must change, isolate the proposed delta and explain why; do not silently mutate the existing reference.

```text
HANDOFF != IDENTITY_TRANSFER
SUCCESS != WIDER_AUTHORITY
RECEIPT != REVIEW
MOVED_HEAD -> OLD_CLAIM_HISTORICAL
SINGLE_MUTATOR != PERMANENT_OWNER
REFERENCE_IMPLEMENTATION != PRODUCTION_ADOPTION
```

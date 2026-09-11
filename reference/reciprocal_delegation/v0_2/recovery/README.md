# Reciprocal Delegation v0.2 — failure / recovery companion

Status: **NON-PRODUCTION REFERENCE / NOT AUTHORITY / NOT CAMPFIRE PRODUCTION**

This companion models one narrow problem: a mutating lane stops, stalls, narrows or hands back, and another mutator takes over without overlapping ownership, stale-head fiction or accidental authority widening.

It does not decide whether the underlying action is justified. It does not infer identity continuity, standing or trust. It does not connect to live execution.

## Core rules

A takeover is valid only when:

1. the previous lane is no longer actively mutating the same scope;
2. a reason for transfer is named;
3. the current head is reacquired at transfer;
4. if that head differs from the previous lane's last claimed head, the old claim is explicitly historical;
5. the new mutator's write scope is no wider than the transferred scope unless a new explicit scope-change authorization is recorded;
6. inherited no-touch constraints remain in force unless a new explicit authorization changes them;
7. consequential work still requires legible request-specific authorization;
8. any recovery mutation preserves history through forward change;
9. hand-back is observable delivery, not agreement, approval or review.

```text
SINGLE_MUTATOR != PERMANENT_OWNER
HANDOFF != IDENTITY_TRANSFER
MOVED_HEAD -> OLD_CLAIM_HISTORICAL
SUCCESS != WIDER_AUTHORITY
RECEIPT != REVIEW
REFERENCE_IMPLEMENTATION != PRODUCTION_ADOPTION
```

## Files

- `state-machine.json` — transfer/takeover states and transitions.
- `validate.py` — stdlib-only deterministic checker.
- `examples/clean_handoff_exact_head.json` — PASS.
- `examples/stalled_lane_named_transfer.json` — PASS.
- `examples/double_mutator_same_object.json` — FAIL.
- `examples/takeover_from_stale_head.json` — FAIL.
- `examples/success_widens_scope_implicitly.json` — FAIL.
- `test_examples.py` — runs the bundled expectations.

## Scope model

The companion uses repository-relative path prefixes. The transferred write scope is the maximum scope the new mutator may claim without a new explicit authorization. A directory path covers descendants. Two concurrent active mutators may operate only on clearly disjoint scopes; this companion's fixtures model the same-scope case.

The previous lane's successful delivery is evidence about that delivery, not a portable trust score. A new task needs its own envelope.

## Head model

`previous_lane.last_claimed_head` records what the earlier lane's claim described. `transfer.current_head` records the head reacquired when control moves. `new_lane.start_head` must equal that current head before mutation begins.

If the head moved in between, the previous claim is not silently updated. It becomes historical.

## Recovery model

A partial or failed mutation is recovered with forward history preserved. Rewriting or force-erasing the failed history is outside this reference.

## Non-goals

This companion does not:

- prove a lane is stalled merely because time elapsed;
- authorize takeover by itself;
- infer one runtime is the same entity as another;
- widen authority because earlier work succeeded;
- replace consequential approval;
- make a receipt equivalent to human review;
- adopt anything into Campfire Production.

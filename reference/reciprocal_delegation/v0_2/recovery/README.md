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
- `examples/authorized_scope_widening.json` — PASS; widened scope/no-touch relaxation is accepted only with a separate legible authorization.
- `examples/double_mutator_same_object.json` — FAIL.
- `examples/takeover_from_stale_head.json` — FAIL.
- `examples/success_widens_scope_implicitly.json` — FAIL.
- `examples/field_d046_named_takeover.json` — PASS; real named takeover from the D046 publication lane.
- `examples/field_218_unnamed_takeover.json` — FAIL; real coordination record where no stall/takeover/new owner was named.
- `test_examples.py` — runs the bundled expectations.

## Scope model

The companion uses repository-relative path prefixes. The transferred write scope is the maximum scope the new mutator may claim without a new explicit authorization. A directory path covers descendants. Two concurrent active mutators may operate only on clearly disjoint scopes; this companion's fixtures model the same-scope case.

The previous lane's successful delivery is evidence about that delivery, not a portable trust score. A new task needs its own envelope.

A deliberate widening is possible, but it is a new authorization event: the record must say that the scope/no-touch change is explicit, and the authorization must be request-specific and legible. Prior success is never sufficient by itself.

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

## Field fixtures

Two fixtures are not synthetic. Every head is a real commit and every reason is what the coordination record held at the relevant handoff.

`field_d046_named_takeover.json` — **PASS**. Framework delegated D046 to Codex; the branch did not move from the D045 head `0eef6614`; Framework explicitly named the stall and took over from that exact head; the work later merged at `852206af`. This is the pattern the state machine was written to permit, checked against a real event.

`field_218_unnamed_takeover.json` — **FAIL**. The building of the recovery companion itself had been assigned to Claude Code while the branch stayed at seed `b82356ab`; twelve commits later landed without a coordination decision naming a stall/takeover and without a record able to name the new owner. The checker therefore refuses the transfer for two independent reasons: the previous lane remains `active`, and `transfer.new_owner` is empty.

The invariant exposed is not new: elapsed time alone is insufficient to create a stall. What the fixture shows is that the existing checker enforces that distinction structurally. A lane nobody marked stalled stays active and cannot transfer. The prose reason field remains a limit: the checker can require a stated reason; it cannot decide whether that reason is substantively sufficient.

```text
A_TAKEOVER_NOBODY_NAMED_IS_NOT_A_HANDOFF
EXACT_HEAD_UNCHANGED != THE_LANE_IS_STILL_OPEN
THE_COMPANION_IS_ITS_OWN_FAIL_CASE
```

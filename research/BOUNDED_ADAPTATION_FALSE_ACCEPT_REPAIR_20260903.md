# Bounded Adaptation v0 — semantic false-accept repair

Status: **NON-CANONICAL / CONTRACT REPAIR / NOT ACTIVATED**  
Date: 2026-09-03

## Independent failure basis

Codex exact-head hostile re-audit of `8c4c734c5cb302967150aec038b1e67514fc181a` returned `REPAIR` with reproducible false accepts. The green fixture suite had closed earlier contradictions but still allowed several declared gates to remain prose rather than mechanism.

The reproduced cases were:

1. selected `REPRIORITISE` with no expiring/default-reversion record;
2. a five-minute receipt span while `wall_clock_seconds=1`;
3. a ~1.5 KiB receipt while `record_bytes=1`;
4. selected recoverable deletion with no typed recovery/target/receipt proof;
5. selected Class-B aperture request while `authority_class_max=NONE`;
6. `ACTIVE_LANE_STUCK` with no named/aged unresolved lane.

Framework also applied the same proof-surface rule to `CONTACT_EXTERNAL_OWNER`: the v0 receipt has no typed standing-grant proof, so it may not execute that move merely because the profile names it grant-dependent.

## Repair

The executable validator now enforces:

- selected `REPRIORITISE` requires exactly one live `temporary_adaptations` record carrying expiry and default reversion;
- reported wall-clock budget may not be smaller than the observable `completed_at - started_at` span;
- reported record bytes may not be smaller than the canonical serialized receipt size;
- `DELETE_RECOVERABLE_CANDIDATE` refuses in v0 because the receipt has no typed recovery pointer / exact-target / retained-receipt evidence surface; use `RETIRE` or `ESCALATE`;
- `CONTACT_EXTERNAL_OWNER` refuses in v0 because the receipt has no typed standing-grant evidence surface;
- selected moves must not understate their profile-declared authority class (`REQUEST_APERTURE` and `CORRECT_COORDINATION` require Class B);
- `ACTIVE_LANE_STUCK` requires a non-`NONE` unresolved lane with positive age.

This deliberately prefers subtraction over adding weak free-text proof fields.

```text
GATE_NAMED_IN_PROFILE != GATE_PROVABLE_IN_RECEIPT
NO_TYPED_PROOF -> DO_NOT_EXECUTE_CONDITIONAL_MOVE
```

## Portability caveat

The branch pins validated artifacts to LF and fresh Windows/Ubuntu checkouts pass. Git does not necessarily renormalise already-present CRLF files in an existing Windows worktree merely because `.gitattributes` was added later. An existing checkout may therefore need an explicit renormalisation/recheckout before exact-byte validation agrees with repository bytes.

That is an upgrade-path requirement, not evidence that fresh-checkout byte identity is false.

## Evidence

Functional repair commit:
`4620a7201ee5c1adbc07a65a0fcc02e58ff9d577`

GitHub Actions run `33742357477` passed the bounded-adaptation validator on both Ubuntu and Windows.

The repair still does not establish usefulness, autonomous operation, safe external contact, deletion authority, or readiness to activate. It establishes only the exercised contract/refusal relations.

No daemon activation, merge, spend, credential use, Square actuation, external contact, release/canon mutation or authority expansion follows.

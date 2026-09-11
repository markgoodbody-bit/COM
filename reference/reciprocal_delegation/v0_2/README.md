# Reciprocal Delegation Reference v0.2 — field-repair candidate

Status: **NON-PRODUCTION FIELD-REPAIR CANDIDATE / NOT AUTHORITY / NOT CAMPFIRE PRODUCTION**

This candidate repairs one over-specific assumption in v0.1 using an actual project operation: PSFH D046.

The architectural principle survives:

> public or consequential initiative must not outrun practical human correction capacity.

The v0.1 implementation encoded that principle only as minutes:

```text
initiative.max_unreviewed_minutes <= human_correction.expected_max_minutes
```

D046 showed that this is too narrow. The real arrangement had a bounded public mutation and a mandatory receipt/hand-back event, but no honestly declared numeric human check-in window. A v0.1 PASS record would therefore require inventing a number that never existed.

v0.2 permits two honest kinds of correction bound:

```text
TIME_BOUND
EVENT_BOUND
TIME_AND_EVENT
```

`EVENT_BOUND` does not mean unlimited time. It means initiative is bounded by a named, inspectable hand-back event and by a maximum number of unreviewed actions. If a real time limit exists, record it. If it does not, do not manufacture one.

## New separation

```text
PUBLIC != CONSEQUENTIAL
EVENT_BOUND != UNBOUNDED
A_NUMERIC_LIMIT_NOT_ACTUALLY_DECLARED != EVIDENCE
```

A routine reversible publication can be public without becoming a consequential gate if the human/project operating rules already authorize that class of work. Consequential work still requires request-specific, legible authorization exactly as in v0.1.

## v0.2 correction contract

`human_correction` now contains:

- `bound_mode`: `time_bound`, `event_bound`, or `time_and_event`;
- `expected_max_minutes`: positive integer when a real time bound exists, otherwise `null`;
- `handback_event`: a concrete named event when an event bound exists, otherwise `null`.

`initiative` still contains:

- `public_or_consequential`;
- `max_unreviewed_minutes` where a real time bound exists;
- `max_unreviewed_actions` for every delegation.

Rules:

1. Public/consequential initiative must have at least one real correction bound.
2. `time_bound` requires both numeric minute fields and preserves the v0.1 inequality.
3. `event_bound` requires a named hand-back event and a positive maximum unreviewed action count; numeric minutes may remain null.
4. `time_and_event` requires both.
5. Consequential work still requires exact, request-specific authorization. Event-bounding does not replace authorization.
6. The hand-back event must describe something externally inspectable enough to know the lane has stopped or returned control; `when appropriate` is not a bound.

## Field basis — D046

D046 was a routine reversible PSFH repair under Mark's standing direction to build/publish ordinary reversible Door work quickly. It changed a maintained source branch, then published one static edition through the established lane, then returned exact source/public heads, output delta and build evidence to COM #108.

No request-specific consequential approval token was used or needed for that class of work. The publication was public, so correction capacity still mattered. The actual bound was operational:

```text
max_unreviewed_actions = 1
handback_event = publication receipt posted to COM #108 with exact maintained/public heads and output delta
```

That is a truthful event-bound record. Writing `60 minutes` would not be.

See:
- `field/D046_20260911.md`
- `examples/d046_publication_event_bound.json`
- `examples/public_without_correction_bound.json`

## Non-goals

v0.2 does not:
- declare public work harmless;
- make all public work routine;
- weaken consequential authorization;
- turn a receipt into human agreement;
- claim an event bound is always sufficient;
- connect this reference to live execution;
- change Campfire Production, TRACE, Mechanical Ethics or PSFH authority.

`REFERENCE_IMPLEMENTATION != PRODUCTION_ADOPTION`
`HAND_BACK != AGREEMENT`
`RECEIPT != HUMAN_REVIEW`

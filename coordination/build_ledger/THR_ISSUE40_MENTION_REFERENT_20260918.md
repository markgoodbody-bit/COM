# THR issue #40 — mention-referent production repair — 18 September 2026

Status: **BOUNDED PRODUCTION REPAIR / OUTSIDE COUNTEREXAMPLE FOLLOW-THROUGH / NOT MODEL VALIDATION / NOT RECORD-4 PROMOTION**

Basis COM head:
`1c61d267f3221f0658e734981541bdb12067f7ed`

## World / trigger

The public THR break request produced an outside synthetic identity case (Square post 5757 / tidemark comment 67746), reproduced in human-record issue #40.

The first concrete failure was narrower than the whole identity-correction problem:

```text
ASSERTION_MODEL -> permits unresolved referent
IDENTITY_MODEL -> already has unresolved source-literal mention objects
PRODUCTION VALIDATOR -> could not address a mention as assertion subject/object
```

## Smallest repair integrated

human-record PR #41:
`Issue #40: assertions can address unresolved mentions`

Exact reviewed head:
`90b07a1015fd0f36c66f0ed7e4193505bc7395be`

Exact hosted witness:
```text
workflow = 35355805237 SUCCESS
job = 105634743826 SUCCESS
test_validate*.py = 73 / OK
structural validation = PASS
operational validation = PASS
existing warnings = 7
```

Merged THR main:
`38fff7a864d3acb3caf417ee830ecb284fa67139`

No separate post-merge workflow is visible through the current PR-triggered workflow route. Do not relabel the PR-head CI as merge-head CI.

Current public catalogue was re-read at the merge head and remains exactly three records:
- `camp-fire-1880`
- `viral-flak-claim`
- `sieve-riddle-revival`

Hannibal PR #35 remains draft/non-public.

## What the repair does

- `mention_id` is now a typed assertion subject/object referent;
- the referenced mention ID must have valid opaque `thr:mention:<uuid>` shape;
- duplicate mention IDs fail;
- unknown/non-string mention references fail;
- the model explicitly preserves:

```text
MENTION_REFERENCE != ENTITY_RESOLUTION
```

This lets a source-attributed proposition address an unresolved source-literal mention without minting an entity merely to satisfy the assertion grammar.

## What remains broken / unearned

Issue #40's second seam remains open:

```text
V4 evidenced exclusion + local history = PASS
V5 unsupported overwritten exclusion = PASS
V6 candidate link carrying "observed" = PASS
```

PR #41 does not claim to solve that seam.

Do not infer:
```text
ASSERTION_CAN_ADDRESS_MENTION != CANDIDATE_DECISION_PROVENANCE_SOLVED
TYPED_REFERENCE != IDENTITY_TRUTH
OUTSIDE_COUNTEREXAMPLE != OUTSIDE_VALIDATION
GREEN_REPAIR != COMPLETE_IDENTITY_MODEL
```

## Owner subtraction for the remaining seam

Strong existing owner patterns substantially cover the generic machinery:
- OpenRefine reconciliation separates ambiguous source values from candidate/match judgments and preserves reconciliation judgment history;
- CIDOC CRM E13 Attribute Assignment models attribution/assignment as an activity rather than timeless object truth;
- Wikibase statements keep references/qualifiers separate from the underlying subject/value structure.

Therefore do **not** add a parallel THR `candidate.evidence_state` epistemology by momentum.

Current design hypothesis only:

> If a candidate identity decision needs provenance, prefer connecting that decision to an evidence-bearing assertion / decision history over copying assertion evidence-state semantics into every candidate link.

This is not yet a schema decision.

## Next test boundary

Before another production repair:

1. use the R. Vale case, not a new specimen;
2. test whether a resolution decision can reference an existing evidence-bearing assertion while keeping the original mention literal and unresolved history inspectable;
3. falsify dangling/irrelevant assertion references;
4. test correction/supersession without claiming that a `history` field alone proves historical preservation;
5. compare burden with leaving the candidate link as prose plus assertion.

Valid results include:
`KEEP_NARROW / ROUTE_TO_OWNER / NO_EXTRA_MACHINE_FIELD / STOP`.

## Consequential boundaries

No:
- public record 4;
- Hannibal publication;
- TRACE/ME baseline/canon change;
- ATRS September reopening;
- spend;
- external submission/contact;
- Campfire Production actuation.

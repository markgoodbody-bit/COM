# THR issue #40 — candidate-boundary shrink — 18 September 2026

Status: **BOUNDED PRODUCTION REPAIR / OUTSIDE COUNTEREXAMPLE FOLLOW-THROUGH / PARTIAL DISPOSITION / NOT IDENTITY VALIDATION**

Basis:
- prior THR main after repair 1: `38fff7a864d3acb3caf417ee830ecb284fa67139`;
- production repair PR #43 exact head: `a564814a6f195f9c1740d39dc5f9b5223de324ac`;
- hosted workflow `35357048111 SUCCESS`;
- hosted job `105638845649 SUCCESS`;
- `test_validate*.py = 76 / OK`;
- Codex exact-head return: `KEEP_SHRINK`;
- merged THR main: `708b9f5f0691e93d052a81431e3c7de9a63a947e`.

## What changed

PR #41 had already made unresolved mentions valid assertion referents.

PR #43 then shrank the remaining R. Vale seam rather than introducing a machine-linked provenance layer:

```text
CANDIDATE LINK
-> MUST CARRY NON-EMPTY HUMAN-INSPECTABLE BASIS

candidate.evidence
candidate.evidence_state
candidate.history
-> REJECT / NOT VALIDATED THR SEMANTICS

SOURCE-ATTRIBUTED CLAIM ABOUT UNRESOLVED MENTIONS
-> ASSERTION LAYER
```

The exact R. Vale representation is regression-tested:

```text
reported_by_source assertion
subject = mention A
object  = mention B
-> PASS
```

No entity needs to be minted or resolved merely to preserve Source C's proposition.

## Owner subtraction

The intermediate `basis_assertion_ids` bridge was probed in PR #42 and retired unmerged.

Generic reconciliation/judgment/provenance/history machinery already has stronger owners such as OpenRefine reconciliation, CIDOC CRM attribution/assignment activity, Wikibase statement references/qualifiers and ordinary repository revision history.

Current THR therefore does not add a second candidate-local epistemology by momentum.

## What remains unresolved

Codex independently reproduced this remaining limitation:

```text
candidate state = excluded
basis = ["not the same maker"]
no machine-readable prior candidate history
-> STILL STRUCTURALLY VALID
```

Therefore:

```text
TYPED UNRESOLVED REFERENT = FIXED
FAKE CANDIDATE EVIDENCE SEMANTICS = FAIL-CLOSED
CANDIDATE BASIS = REQUIRED
MACHINE-READABLE PRIOR CANDIDATE HISTORY = UNRESOLVED
```

Issue #40 remains open on that narrow history question.

Current THR practice preserves accepted corrections through dated record corrections, earlier files/repository history, source observations/assertions and public challenge routes. That does not prove a future typed candidate-history layer is unnecessary; it means no such layer is earned yet.

## Public/product state

Fresh merge-head catalogue read:

```text
THR main = 708b9f5f0691e93d052a81431e3c7de9a63a947e
public records = 3
camp-fire-1880
viral-flak-claim
sieve-riddle-revival
```

Hannibal remains non-public candidate PR #35.

No TRACE/ME change, ATRS reopening, external contact, spend or Campfire Production actuation.

```text
PARTIAL_REPAIR != WHOLE_IDENTITY_PROBLEM_SOLVED
OUTSIDE_COUNTEREXAMPLE != OUTSIDE_VALIDATION
GREEN_VALIDATOR != IDENTITY_TRUTH
```

# Local Continuity Capsule v1 — comparison / transition derivation repair

Status: **NON-CANONICAL / CONTRACT REPAIR / NOT ACTIVATED**  
Date: 2026-09-03

## Failure that forced this repair

The prior repaired contract had a frozen material-delta code `PRODUCER_BUILD_CHANGED`, but the described comparison state did not include `producer.build_sha256`.

That made one declared transition class impossible to derive consistently:

```text
producer build changes
+ evidence/dwell/active conditions unchanged
-> old comparison hash unchanged
-> old transition rule says NO_DELTA

while

PRODUCER_BUILD_CHANGED exists
-> delta vocabulary says DELTA is speakable
```

Therefore:

```text
DELTA_CODE_EXISTS != DELTA_CAN_BE_DERIVED
```

This is a contract defect, not an implementation detail.

## Repaired executable comparison state

The current validator derives the comparison state from exactly the fields needed by the four frozen delta classes:

```text
producer.build_sha256
evidence
observation.dwell
active_conditions
```

`producer.instance_id_sha256` is deliberately not an ordinary delta field. An instance change breaks the transition chain rather than becoming a normal material delta.

The exact delta derivation is now:

```text
build differs              -> PRODUCER_BUILD_CHANGED
evidence differs           -> EVIDENCE_CHANGED
dwell differs              -> DWELL_STATE_CHANGED
active conditions differ   -> ACTIVE_CONDITION_SET_CHANGED
```

The derived code set, not producer preference, determines whether a non-genesis transition is `DELTA` or `NO_DELTA`.

## Hashes are now computed, not merely described

The validator now recomputes:

1. `observation.source_state_hash` from the exact comparison state;
2. `capsule_id` from the canonical capsule payload excluding `capsule_id` itself;
3. exact predecessor linkage;
4. derived material-delta codes from predecessor/current state.

Hostile probes refuse:

- evidence changed while `source_state_hash` remains stale;
- proposal/payload changed while `capsule_id` remains stale;
- wrong profile binding;
- build changed while producer claims `NO_DELTA`;
- wrong predecessor capsule ID.

Positive probes establish:

- an exact predecessor pair with unchanged comparison state validates as `NO_DELTA`;
- a producer build change changes the comparison hash and validates as a derived `DELTA` carrying exactly `PRODUCER_BUILD_CHANGED`.

## Canonicalization ceiling

The executable helper uses sorted compact JSON only over the capsule's deliberately closed value domain: strings, integers, booleans, null, arrays and objects. It is checked against the supplied RFC 8785 vectors. This repair does not claim that Python's generic JSON encoder is a complete JCS implementation over arbitrary numeric/string domains.

If the capsule domain later expands, canonicalization must be re-attacked rather than inheriting this bounded equivalence claim.

## Relationship to older candidate prose

Older candidate prose describing a comparison state that excludes the producer build identity is superseded by this repair. Do not use that older field list as the current executable contract.

The current profile still preserves the frozen four-code vocabulary and other reviewed limits. A later clean profile revision may fold this exact comparison-state field list into one machine-readable location after independent attack. Until then this repair note plus the executable validator is the explicit current boundary; the mismatch is visible rather than silently reconciled.

## Evidence ceiling

Exact current validator head after the brittle stale-profile negative was corrected:

`df08e5c03855781c36a01cfa8310a8e018374fe5`

GitHub Actions run `33742019600` passed the contract validator on both Ubuntu and Windows.

This establishes only the exercised byte/hash/state/transition properties. It does not establish that the capsule reduces human burden, that a publisher is safe, or that activation is warranted.

No outbox retarget, publisher, scheduler activation, provider call, spend, credential use, Square write, TRACE/ME mutation, release/canon change or authority expansion follows.

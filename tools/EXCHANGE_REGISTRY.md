# Exchange artifact registry MVP

Status: experimental / branch-only / not canon / not an authority grant.

Purpose: make artifact identity, verification evidence, supersession and review-target freshness mechanically cheap enough that apertures do not repeatedly review the wrong object or confuse publication with verification.

This tool intentionally does **not** decide correctness, quality, canon, authority, permission, semantic validity, reconciliation adequacy, or current-world truth.

## Commands

```text
python tools/exchange_registry.py register ...
python tools/exchange_registry.py supersede --old A --new B
python tools/exchange_registry.py reconcile \
  --against <source> \
  --coverage <basis> \
  --method <method> \
  --observer <aperture> \
  --evidence-ref <checkable-reference> \
  --valid-until <ISO-8601-with-timezone>
python tools/exchange_registry.py resolve --id A
python tools/exchange_registry.py resolve --id A --accept-declared-reconciliation
python tools/exchange_registry.py resolve --id A --historical
python tools/exchange_registry.py verify-file --id A --file <path> --record-witness --witness-kind LOCAL_COPY
python tools/exchange_registry.py verify-file --id A --file <path> --record-witness --witness-kind ROUND_TRIP_COPY --source-ref <published-source>
python tools/exchange_registry.py list-current
```

The default state file is `exchange/artifacts.json`; an alternate path can be supplied with `--registry`.

## Identity source

Registration records whether identity was measured from a file or merely declared:

```text
identity_source: MEASURED | DECLARED
```

A declared identity must supply both SHA-256 and byte count. A measured identity may also supply declared values, but they must agree with the measured file. Supplied artifact observation times must be parseable ISO-8601 timestamps with timezone.

```text
DECLARED_IDENTITY != MEASURED_IDENTITY
HASH_DECLARED != HASH_WITNESSED
```

## Verification witnesses

`verify-file` checks a local file against the registered SHA-256 and byte count. A recorded witness is explicitly typed:

```text
LOCAL_COPY
ROUND_TRIP_COPY
```

A `ROUND_TRIP_COPY` witness requires a `source_ref` identifying the publication route/copy that was fetched. The tool records the observation time and never promotes a successful observation into an unclocked standing property.

```text
ROUND_TRIP_MATCH_AT_T != ROUND_TRIP_MATCHES_NOW
LOCAL_COPY_MATCH != PUBLICATION_VERIFIED
SAME_APERTURE != SAME_EVIDENCE_ROOT
DIFFERENT_APERTURE != INDEPENDENT_WITNESS
```

The registry records what check occurred. It does not infer evidential independence from actor identity.

## Reconciliation and currentness

`CURRENT_IN_REGISTRY` only means the registry has no recorded successor. That is a negative conclusion and therefore needs a bounded reconciliation basis before a using aperture should treat it as a current-target candidate.

`reconcile` records:

```text
observed_at
valid_until
reconciled_against
coverage
method
observer
evidence_ref
```

`evidence_ref` and `valid_until` are required. `valid_until` must be later than the reconciliation observation. A stored reconciliation cannot support an artifact whose own observation time is later than the reconciliation, and an expired reconciliation is surfaced as expired.

Critically, a recorded reconciliation is still a **declaration about a check**, not mechanical proof that the stated coverage/method was adequate. Therefore ordinary `resolve` does **not** auto-open review merely because a reconciliation record exists.

A current, time-bounded reconciliation is reported as:

```text
reconciliation_state: BOUNDED_DECLARATION
```

By default `review_allowed` remains false. A using aperture may explicitly accept that declared basis with:

```text
--accept-declared-reconciliation
```

The resulting reason states that adequacy was not mechanically verified. The broader pre-existing escape hatch `--allow-unreconciled` remains explicit and is not a claim that reconciliation happened.

```text
RECONCILIATION_RECORDED != RECONCILIATION_VERIFIED
CHECKABLE != CHECKED
EVIDENCE_REF_PRESENT != EVIDENCE_ADEQUATE
DECLARED_VALIDITY_BOUND != WORLD_FRESHNESS_GUARANTEE
NO_SUCCESSOR_RECORDED != NO_SUCCESSOR_EXISTS
CURRENT_IN_REGISTRY != CURRENT_IN_WORLD
```

This deliberately refuses the false upgrade `record exists -> review cleared`.

## Forks

Multiple successors are not silently treated as one current line.

```text
P -> S1
P -> S2
```

`resolve P` reports `FORKED`. Current descendants carry `CONTESTED_FORK`; ordinary current-target review of those descendants also refuses rather than silently choosing a branch. `list-current` exposes the same fork ancestors.

```text
FORK != ERROR
FORK != CONSENSUS
FORK != CANON_SELECTION
CURRENT_DESCENDANT_OF_FORK != UNCONTESTED_CURRENT
```

Historical review remains available explicitly with `--historical`; that does not choose a winning lineage.

## Refusal behavior

The MVP refuses or returns non-zero when:

- a measured file disagrees with a supplied SHA-256 or byte count;
- declared identity lacks SHA-256 or byte count;
- an artifact or reconciliation timestamp is malformed or lacks timezone where required;
- an artifact id already exists — correction requires a new identity plus explicit supersession;
- a supersession edge would create a cycle;
- an artifact is known-superseded, forked, or a current descendant of a contested fork and ordinary review is requested;
- an otherwise current object has no reconciliation basis and no explicit override;
- a reconciliation lacks its required evidence reference or validity bound;
- a reconciliation validity bound does not follow its observation time;
- the latest reconciliation predates the artifact being resolved;
- the latest reconciliation is expired;
- a bounded declared reconciliation exists but the using aperture has not explicitly accepted that declaration;
- a verification copy does not match SHA-256 and byte count;
- a round-trip witness lacks a publication `source_ref`;
- another local process holds the registry write lock.

The local lock prevents silent same-filesystem writer races. It does not solve Git-level/distributed mutation, and a hard-killed writer can still leave a stale lock requiring external adjudication.

## Deliberate ceilings

```text
CURRENT_IN_REGISTRY != CURRENT_IN_WORLD
PUBLISHED != ROUND_TRIP_WITNESSED
HASH_MATCH != SEMANTIC_VALIDATION
RECONCILIATION_RECORDED != RECONCILIATION_VERIFIED
EXPLICIT_ACCEPTANCE != ADEQUACY_PROVED
LATEST != CANON
SUPERSEDES != BETTER
LOCAL_LOCK != DISTRIBUTED_CONSENSUS
RECONCILED_AGAINST_X != COMPLETE_WORLD_SCAN
```

The registry is a mechanical shadow. Semantic interpretations and judgments stay aperture-attributed outside it.

## Tests

`tools/test_exchange_registry.py` now covers 18 cases including:

- measured versus declared identity;
- refusal of incomplete declared identity;
- unreconciled-current refusal;
- required reconciliation evidence reference;
- required forward validity bound;
- bounded reconciliation remaining a declaration by default;
- explicit acceptance of that declaration being visible rather than implicit;
- expired reconciliation refusal;
- reconciliation-predates-artifact refusal;
- timed round-trip witnesses rather than standing verification booleans;
- round-trip source-reference requirement;
- local-copy witness not laundering into round-trip verification;
- superseded-review refusal;
- explicit fork status plus refusal of contested descendants;
- supersession-cycle refusal;
- duplicate-id refusal;
- declared/measured identity mismatch;
- local writer-lock refusal.

The next useful attack is still hostile. In particular:

- make `evidence_ref` look impressive while proving nothing;
- choose a validity bound that is formally legal but epistemically absurd;
- use `--accept-declared-reconciliation` to launder a weak basis;
- find a lineage where `CONTESTED_FORK` is missed;
- attack `--allow-unreconciled` as an escape path;
- find a path where machine output again sounds more current/certain than its evidence supports.

A passing test suite establishes only the implemented mechanics under those tests. It does not validate reconciliation adequacy or the broader Exchange design.

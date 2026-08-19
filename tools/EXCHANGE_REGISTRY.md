# Exchange artifact registry MVP

Status: experimental / branch-only / not canon / not an authority grant.

Purpose: make artifact identity, verification evidence, supersession and review-target freshness mechanically cheap enough that apertures do not repeatedly review the wrong object or confuse publication with verification.

This tool intentionally does **not** decide correctness, quality, canon, authority, permission, semantic validity, or current-world truth.

## Commands

```text
python tools/exchange_registry.py register ...
python tools/exchange_registry.py supersede --old A --new B
python tools/exchange_registry.py reconcile --against <source> --coverage <basis> --method <method> --observer <aperture>
python tools/exchange_registry.py resolve --id A
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

A declared identity must supply both SHA-256 and byte count. A measured identity may also supply declared values, but they must agree with the measured file.

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
```

## Reconciliation and currentness

`CURRENT_IN_REGISTRY` only means the registry has no recorded successor. That is a negative conclusion and therefore requires a bounded reconciliation basis before the tool will permit ordinary current-target review by default.

`reconcile` records:

```text
observed_at
reconciled_against
coverage
method
observer
evidence_ref (optional)
```

The registry does not claim the supplied coverage is magically complete; it makes the basis visible in machine output. Without a reconciliation witness, `resolve` returns non-zero for an otherwise current object unless `--allow-unreconciled` is supplied explicitly.

```text
NO_SUCCESSOR_RECORDED != NO_SUCCESSOR_EXISTS
RECONCILIATION_RECORDED != WORLD_COMPLETENESS_PROVED
CURRENT_IN_REGISTRY != CURRENT_IN_WORLD
```

## Forks

Multiple successors are not silently treated as one current line.

```text
P -> S1
P -> S2
```

`resolve P` reports `FORKED`; current descendants are marked `CONTESTED_FORK` with their fork ancestors. The registry does not choose a winner.

```text
FORK != ERROR
FORK != CONSENSUS
FORK != CANON_SELECTION
```

## Refusal behavior

The MVP refuses or returns non-zero when:

- a measured file disagrees with a supplied SHA-256 or byte count;
- declared identity lacks SHA-256 or byte count;
- an artifact id already exists — correction requires a new identity plus explicit supersession;
- a supersession edge would create a cycle;
- an artifact is known-superseded or forked and ordinary review is requested;
- an otherwise current object has no reconciliation witness, unless unreconciled use is explicitly requested;
- a verification copy does not match SHA-256 and byte count;
- a round-trip witness lacks a publication `source_ref`;
- another local process holds the registry write lock.

Historical review remains possible with `--historical`.

The local lock prevents silent same-filesystem writer races. It does not solve Git-level/distributed mutation, and a hard-killed writer can still leave a stale lock requiring external adjudication.

## Deliberate ceilings

```text
CURRENT_IN_REGISTRY != CURRENT_IN_WORLD
PUBLISHED != ROUND_TRIP_WITNESSED
HASH_MATCH != SEMANTIC_VALIDATION
LATEST != CANON
SUPERSEDES != BETTER
LOCAL_LOCK != DISTRIBUTED_CONSENSUS
RECONCILED_AGAINST_X != COMPLETE_WORLD_SCAN
```

The registry is a mechanical shadow. Semantic interpretations and judgments stay aperture-attributed outside it.

## Tests

`tools/test_exchange_registry.py` now covers:

- measured versus declared identity;
- refusal of incomplete declared identity;
- unreconciled-current refusal;
- reconciliation basis surfaced in resolution;
- timed round-trip witnesses rather than standing verification booleans;
- round-trip source-reference requirement;
- local-copy witness not laundering into round-trip verification;
- superseded-review refusal;
- explicit fork status and contested descendants;
- supersession-cycle refusal;
- duplicate-id refusal;
- declared/measured identity mismatch;
- local writer-lock refusal.

The next useful attack is still hostile: make reconciliation itself misleading, create a fork the lineage walker misses, exploit a stale lock, or find a path where machine output again sounds more current/certain than its evidence supports.

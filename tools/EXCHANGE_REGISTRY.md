# Exchange artifact registry MVP

Status: experimental / branch-only / not canon / not an authority grant.

Purpose: make artifact identity, round-trip verification, and supersession mechanically cheap enough that apertures do not repeatedly review the wrong object or confuse publication with verification.

This tool intentionally does **not** decide correctness, quality, canon, authority, permission, or semantic validity.

## Commands

```text
python tools/exchange_registry.py register ...
python tools/exchange_registry.py supersede --old A --new B
python tools/exchange_registry.py resolve --id A
python tools/exchange_registry.py resolve --id A --historical
python tools/exchange_registry.py verify-file --id A --file <path> --update-round-trip
python tools/exchange_registry.py list-current
```

The default state file is `exchange/artifacts.json`; an alternate path can be supplied with `--registry`.

## Refusal behavior

The MVP refuses or returns non-zero when:

- a measured local file disagrees with a supplied SHA-256 or byte count;
- an artifact id already exists — correction requires a new identity plus an explicit supersession edge rather than destructive replacement;
- a supersession edge would create a cycle;
- an artifact is already known-superseded and ordinary review is requested;
- a round-trip copy does not match both the recorded SHA-256 and byte count;
- another local process holds the registry write lock.

Historical review of a superseded object remains possible only when explicitly requested with `--historical`.

Round-trip observations are appended to `round_trip_witnesses`; the latest `round_trip_verified` value is a derived convenience field and does not erase prior success or failure observations.

The registry has a monotonically increasing local `generation`. This makes a stale snapshot more visible but does not prove that the registry has observed the whole external world.

## Deliberate ceilings

```text
CURRENT_IN_REGISTRY != CURRENT_IN_WORLD
PUBLISHED != ROUND_TRIP_VERIFIED
HASH_MATCH != SEMANTIC_VALIDATION
LATEST != CANON
SUPERSEDES != BETTER
LOCAL_LOCK != DISTRIBUTED_CONSENSUS
```

`CURRENT_IN_REGISTRY` means only that this bounded registry contains no known successor for the artifact at the time the registry was read.

The local lock prevents silent same-filesystem writer races. It does not solve Git-level or distributed concurrent mutation; those still require version-control conflict detection or a later shared-state service.

The registry is a mechanical shadow. Semantic interpretations and judgments stay aperture-attributed outside it.

## Tests

`tools/test_exchange_registry.py` covers:

- measured registration and successful round-trip verification;
- failed round-trip identity;
- preservation of prior round-trip witnesses after a later failure;
- duplicate-id refusal rather than correction-history overwrite;
- default refusal to review a superseded object;
- explicit historical override;
- supersession-cycle refusal;
- disagreement between declared and measured artifact identity;
- refusal when a local writer lock already exists.

The next useful attack is not another feature request. Try to make the registry silently bless the wrong artifact, lose a successor, or manufacture semantic/current-world certainty from bounded registry state.

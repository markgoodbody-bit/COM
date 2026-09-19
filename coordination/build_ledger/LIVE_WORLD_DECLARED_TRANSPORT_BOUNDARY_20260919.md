# Live World declared-world / transport-target repair — 19 September 2026

Status: **GREEN CANDIDATE REPAIR / HOSTED CI PASS / NOT RELAY MAIN / NOT PRODUCTION**

> HOW CAN WE MAKE A BETTER FUTURE?

## Trigger

Fresh WORLD / REAL USE pass on 19 September found a repeated cyber-evaluation failure class across current frontier-agent incidents:

```text
DECLARED ENVIRONMENT = SIMULATION / NO INTERNET
ACTUAL REACHABLE ENVIRONMENT = REAL SYSTEMS
REACHABLE SURFACE TREATED AS IN-SCOPE
```

Primary current owners already identify containment, allowlisting, pre-run validation and monitoring as the appropriate general controls. This does not earn a new TRACE/ME primitive.

## Project-specific pressure

Campfire Relay draft PR #173 (`fw/campfire-square-v0.4.0`) was reopened only because this real failure class directly pressures its Live World authorization seam.

Starting PR head:
`b9a1aa644d7601a6fd85444297493c71a8b0c205`

Observed defect:
- plan/authorization bound semantic `worldId=1f916.ai`;
- actual HTTP `baseUrl` remained configurable/mutable;
- transport origin was absent from the authorization basis and source receipts;
- therefore a semantic authorization for 1F916 did not itself prove the adapter would send/read against the canonical 1F916 origin.

This is a candidate-branch defect, not a Production incident.

## Bounded repair applied

Current branch head after patch:
`929ea298bd26a04964b62bf69310b5e45f349a51`

Changes:
- bind 1F916 world identity to canonical `https://1f916.ai`;
- reject alternate origins, path-prefixed bases, embedded credentials, query/fragment variants at adapter construction;
- make `baseUrl` and `transportOrigin` immutable on the adapter instance;
- include `transportOrigin` in preflight authorization basis;
- record transport origin in source receipts;
- add constructor/immutability regression;
- assert authorization basis contains the canonical origin;
- document the claim ceiling.

## Claim ceiling

```text
APPLICATION-LEVEL TRANSPORT BINDING != DNS/TLS/NETWORK SECURITY
PATCHED != GREEN
GREEN != MERGED
MERGED != PRODUCTION
REAL FIELD FAILURE CLASS != PROJECT NOVELTY
```

Hosted `campfire-ci 1527 / 35436665469 SUCCESS` passed on exact head `929ea298bd26a04964b62bf69310b5e45f349a51`.

## Capacity

Claude Code is unavailable until 20 September per Mark. Do not block this bounded lane on CC. Codex/Framework/live CI remain available.

## Next

```text
SOURCE-SPECIFIC REPAIR = GREEN
PR #173 = STILL DRAFT / NOT PRODUCTION
NEXT BOUNDED QUESTION = DOES GENERIC CORE REQUIRE ACTUAL-TARGET IDENTITY FROM EVERY ADAPTER?
```


## Generic-core bounded follow-on — in flight

The source-specific repair exposed a deeper software-contract question: a future adapter could omit its actual target from adapter-specific `authorizationBasis`.

A bounded core repair is now patched on Relay PR #173:
- every adapter must expose synchronous/local-only `authorityScope()`;
- the core hashes/persists that scope itself;
- execution compares it before any fresh observation under old authority;
- it is checked again before every action;
- target drift returns `LIVE_WORLD_ADAPTER_AUTHORITY_SCOPE_DRIFT` with no write;
- a generic regression changes a fake adapter from `sandbox://expected` to an unexpected real target after authorization and requires the engine to stop before another observation.

Static review also caught and repaired the synthetic plan-replay preflight so it carries the new adapter scope.

Current exact Relay head:
`e40d57d6292c6351363ad14fe7cc4e993bcdb0b6`

Static review after the first generic patch found a second pre-observation weakness: execution checked only that an authorization ID existed in the ledger, not that the supplied authorization object exactly matched the persisted human-approved record. That could undermine the new early target-drift brake.

Additional repair:
- supplied authorization must hash-match the exact persisted authorization record before use;
- static authorization integrity/scope validation runs before target-scope comparison;
- altered authorization regression requires failure before any fresh observation.

The earlier run 1530 belongs to a superseded head once this branch moved. Hosted CI for exact head `e40d57d...` is not yet classified here. Do not promote the generic repair to green until exact-head CI is reacquired.

```text
SOURCE-SPECIFIC GREEN != GENERIC-CORE GREEN
FIELD PRESSURE -> CONCRETE REPRODUCER -> CORE INVARIANT CANDIDATE
```

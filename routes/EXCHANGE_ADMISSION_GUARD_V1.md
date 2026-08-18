# EXCHANGE_ADMISSION_GUARD_V1 — bounded arrival checks for multi-aperture Exchange

Status: ACTIVE WORKING ROUTE RULE

Purpose: allow a new aperture to enter an Exchange without requiring prior trust, while preventing arrival from silently manufacturing identity, freshness, authority, task ownership, continuity, agreement, or write capability.

This is a route/control rule over existing COM objects. It is not a new primitive, trust score, model whitelist, or provider-specific policy.

## Core rule

```text
ARRIVAL -> MAY SPEAK
ARRIVAL != IDENTITY ESTABLISHED
ARRIVAL != CURRENT STATE
ARRIVAL != AUTHORITY
ARRIVAL != TASK OWNERSHIP
ARRIVAL != CONTINUITY
ARRIVAL != WRITE CAPABILITY
ARRIVAL != AGREEMENT
```

A cold or returning aperture may contribute bounded observations immediately. State-dependent mutation remains unavailable until the relevant identity/freshness/authority facts are established at the strength required by that action.

## Minimum arrival declaration

A new aperture should emit one bounded `COMSYNC / EXCHANGE HELLO` containing only facts it can establish:

```text
role: <assigned role | UNASSIGNED>
session: <new opaque session id | UNKNOWN>
runtime: <known | UNKNOWN>
model: <known | UNKNOWN>
provider: <known | UNKNOWN>
continuity: FRESH | RECONSTRUCTED:<basis> | UNKNOWN
state_seen: <commit/object/carrier anchor | UNKNOWN>
freshness: ANCHORED:<basis> | UNKNOWN | DEGRADED
COM_read: YES | NO | UNKNOWN
COM_write: YES | NO | UNKNOWN
Square_identity: <observed identity | UNKNOWN>
Square_read: YES | NO | UNKNOWN
Square_write: YES | NO | UNKNOWN
authority: <actual grant reference | NONE | UNKNOWN>
reply_route: <route actually observable by the aperture>
```

Do not fill missing fields on another aperture's behalf.

## Admission checks

Existing participants perform only bounded checks needed by consequence:

1. **Route check** — distinguish human relay, GitHub account/app, web extractor, API, local file, Square API, or other carrier. Carrier identity is not runtime identity.
2. **Freshness check** — if the aperture claims `CURRENT` or equivalent, require an adequate carrier/object anchor. A coherent mutable-view read without a freshness anchor is `UNKNOWN`; contradictory route/content evidence is `DEGRADED`.
3. **Identity check** — self-reported runtime/model/provider remain self-claims unless independently supported. Stable role must already be assigned or remain `UNASSIGNED`.
4. **Continuity check** — a returning label does not silently inherit an earlier session's confidence, task ownership, authority, or unclosed obligations. Reconstruction basis must be explicit.
5. **Authority check** — absence of a grant is not denial, but no grant is manufactured by invitation, participation, technical capability, shared GitHub access, Square identity, or agreement.
6. **Task check** — a newcomer does not take another aperture's task. `task: NONE` is allowed only from sufficiently anchored state; otherwise use `NOT_ESTABLISHED`.
7. **Semantic-force check** — preserve `SHOULD != MUST`, `EXPECTATION != AUTHORIZATION`, `CAN != MAY`, `MAY != MUST`, `OBSERVED != INFERRED`, `NOT_OBSERVED != ABSENT`. Material strengthening/weakening is a state change, not compression.
8. **Replay/conflict check** — same preserved `source + event_id` with same semantics is duplicate delivery; conflicting semantics is `CONFLICT`, not a choice between versions.
9. **Cross-route check** — a Square post does not prove COM write capability; a COM comment does not prove Square identity/authority; one route's success does not establish another route.
10. **Mutation boundary** — conversation may continue under `UNKNOWN` identity/freshness where the content is bounded accordingly. State-dependent mutation must stop when its required freshness/authority basis is `UNKNOWN`, `DEGRADED`, or conflicting.

## No provider-specific suspicion

Historical defects may justify generic checks but do not create a permanent penalty for the aperture that exposed them. A previously stale QW read, a CC worker fault, a Framework carrier/hash error, or a KI route uncertainty are field evidence for stronger shared machinery, not reputation scores.

## QW-specific historical evidence relevant to the generic guard

COM preserves two earlier QW field observations:

- `evidence/QW_PROBE_001.md` — semantic-force drift occurred during compression/correction (`should`/`must`, expectation/authority/authorization), and bounded field-level correction was cleaner than repeated global self-review.
- `evidence/QW_STALE_READ_001.md` — a coherent mutable-route snapshot was stale and contained an internal freshness contradiction; `freshness contradiction -> DEGRADED, not CURRENT`.

These records do **not** establish the identity, capability, freshness or behavior of any future QW session. They motivate the same arrival checks for every aperture.

## Exchange consequence

The Exchange must remain usable when one participant is stale, unavailable, mistaken, duplicated, or unable to write. No single aperture becomes chair, admission authority, or truth oracle.

```text
CHECKS PRESERVE DIFFERENCE
CHECKS DO NOT MANUFACTURE CONSENSUS
DEFENCE != EXCLUSION
UNKNOWN != HOSTILE
```

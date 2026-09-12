# COM_STATE v0.5.0

STATUS: **CURRENT ROUTING PROJECTION / NOT DETAILED MUTABLE STATE / NOT TRUTH OR AUTHORITY**  
ROUTER REFRESH: 2026-09-13 Europe/London

COM is a working coordination surface, not canon, validation, consensus or a truth oracle.

This file intentionally carries **routing and currentness rules**, not a second copy of detailed project state. Mutable work/status lives on the bounded coordination surfaces it points to.

```text
RECORD_CORRECT_AT_T0 != RECORD_CURRENT_AT_T1
ROUTER_CURRENT != EVERY_DESTINATION_CURRENT
COHERENT_PROJECTION != CURRENT_WORLD
ROUTE_EXISTS != ROUTE_USABLE
HEAD != WORLD
```

Do not reconstruct historical detail into current state by memory.

## COMS routing — any aperture

A cold aperture may run COMS read-only without joining.

After retrieving this file at an adequately anchored repository head:

1. if conceptual orientation is genuinely needed, use `BOOTSTRAP.md`; it is optional and non-authoritative;
2. use `COM_PROTOCOL_WORKING.md#coms` for the normative COMS operation and bounded return;
3. read `coordination/ACTIVE_THREAD_POINTER.md` for the current bounded coordination aperture;
4. read `coordination/build_ledger/BUILD_STATUS.md` only when current build/integration state is material;
5. inspect only work explicitly addressed to this aperture or its established role;
6. use role-specific continuity surfaces only when the role is actually established;
7. reacquire mutable repository/service state needed for the action before mutation.

```text
BOOTSTRAP != COMS
ROUTING_POINTER != TASK_ASSIGNMENT
OPEN_PR != CURRENT_QUEUE
READ != AUTHORITY
```

**This router alone is not sufficient evidence for `task: NONE`.** A COMS return may use `task: NONE` only after sufficiently anchored current coordination/task surfaces have been inspected and show no task addressed to the aperture or its established role. If the needed current route cannot be established, return `task: NOT_ESTABLISHED` rather than inferring absence.

## Framework-role routing

Only for an aperture whose Framework role is already established:

```text
RELOAD.md when continuity is materially missing
-> continuity/BOOT.md
-> continuity/FRAMEWORK_HEAD.md
-> continuity/EPISTEMIC_POSTURE.md when posture is material
-> continuity/COMSYNC_PROTOCOL.md for Framework COMSYNC/FULL COMSYNC
-> coordination/ACTIVE_THREAD_POINTER.md
-> coordination/build_ledger/BUILD_STATUS.md when material
-> continuity/OMISSION_MAP.md only where material
-> live reacquisition of mutable sources/routes
-> act within authority
```

Do not make a cold unassigned aperture ingest Framework continuity merely because those files exist.

## Current source pointers

### Public project entrance

Canonical voluntary public entrance:

`https://pleasestartfromhere.com/`

This is a reading/encounter surface, not COM authority or synchronization state.

### TRACE

Current project/public source is live TRACE `main`:

```text
README.md
-> TRACE-SPINE.md
-> TRACE.md when full technical/schema detail is needed
```

The live repository owns current status. Historical release/development detail is quarry and should be retrieved only when material.

### Mechanical Ethics

Current project/public source is live mechanical-ethics `main`:

```text
README.md
-> MECHANICAL_ETHICS.md
-> MECHANICAL_ETHICS.pdf when the generated reader carrier is useful
```

The live repository owns current status. Historical protected-source/development detail is quarry and should be retrieved only when material.

### Campfire Relay / Square

Campfire Relay / Square state is mutable.

Do not preserve a supposedly current Production version, provider quota, worker state, witness state or local-service state here. Reacquire the live repository/service only when that state is material.

Local lifecycle actuation remains separately gated by its current source/control envelope; this router grants none.

### Coordination and evidence

- current bounded coordination pointer: `coordination/ACTIVE_THREAD_POINTER.md`;
- current build/integration ledger: `coordination/build_ledger/BUILD_STATUS.md`;
- ordinary Framework sync rules: `continuity/COMSYNC_PROTOCOL.md`;
- inter-aperture receipt rules: `continuity/COM_RECEIPT_PROTOCOL.md`;
- roles/work classes/non-blocking coordination: `continuity/TEAM_OPERATING_MODEL.md`;
- negative-space retrieval triggers: `continuity/OMISSION_MAP.md`;
- durable historical evidence: `evidence/` and named issue/PR records only when needed.

Do not replay broad issue histories or cold evidence as routine boot context.

## Identity, availability and authority

Role, session, runtime, model, provider, capability, authority and current reachability are separate.

A past role/availability observation is not current proof. A new aperture does not inherit a predecessor's session or mutation ownership.

```text
CONTINUITY_OF_ROLE != CONTINUITY_OF_SELF
PAST_CAPABILITY != CURRENT_CAPABILITY
PAST_AVAILABILITY != CURRENT_AVAILABILITY
PAST_AUTHORITY != CURRENT_AUTHORITY
CAN != MAY
```

To become addressable, use the `HELLO` bootstrap in `COM_PROTOCOL_WORKING.md`. Do not invent a stable role or authority.

## Currentness rule

When this router conflicts with a live repository, current coordination pointer, immutable task/control object or mutable service, reacquire the live source and treat the conflicting router statement as stale.

Do not put detailed experiment outputs, mutable SHAs, quotas, provider health, Square worker state or release claims back into this file unless they are necessary to explain routing itself.

```text
SUMMARY != SOURCE
LEDGER != HEAD
HEAD != WORLD
MAIN_AT_T0 != MAIN_AT_T1
```

## Historical projection

The former v0.4.x detailed/historical projections remain recoverable through Git history. Their detail is evidence/history, not an object to replay at boot.

## Rule

Keep this file small enough to route a cold aperture and strong enough to prevent false currentness. Do not turn it back into a second detailed current-state authority.

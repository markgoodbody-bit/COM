# COM_STATE v0.3.2

STATUS: WORKING BASELINE / COM PAUSED PENDING REAL-WORK DEFECT

COM is not validated, canon, or a truth oracle. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

## CURRENT

- human_authority: Mark
- active_task: NONE
- execution_mode: IDLE / AVAILABLE TO SUPPORT CAMPFIRE RELAY
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- repository_mutation: NONE unless a concrete new defect or explicit human instruction creates a task
- state_basis: `c299dd9a1f24dd8b3e97eafb69d4bf66fd8d3e6f` — main before this projection update; this file is not self-authenticating freshness
- core_status: v0.3 integrated working baseline
- protocol_status: v0.3.2 integrated working baseline
- next_lane: Campfire Relay product/research-instrument build

## INTEGRATED BASELINE

Core/protocol lineage:
- PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf` — cold bootstrap, freshness, delegated-return discovery;
- PR #8 merged at `5219ca2df18213289948935ecc4b1ffa8925fe0c` — COMS front-door execution repair;
- PR #14 reviewed candidate head `3215f9e41601b6ec4e6854bd441770d38b892dec` was closed unmerged after exact manual integration onto current `main` because the live-state branch had moved.

Exact PR #14 candidate blobs integrated:
- `README.md` blob `cc12ad01b17b6623409eb6eee055f6b47d3dbaf5` -> main commit `d6025c0e47f4e1cc81323ccc603256405b01f8a4`;
- `COM_PROTOCOL_WORKING.md` blob `45c66e7e62530c57de91d8330cc2e1963c8741d1` -> main commit `c299dd9a1f24dd8b3e97eafb69d4bf66fd8d3e6f`.

Integrated v0.3.2 behavior includes:
- GitHub carrier rendezvous through repository-bound `commits/main` -> immutable SHA -> `COM_STATE.md`;
- mutable labels are navigation, not freshness proof;
- stale-carrier and API/rate-limit failure stop bounded rather than silently falling back;
- cold `HELLO` keeps role/session/runtime/model/provider/authority separate;
- literal `COMS` requires an externally auditable bounded return across transports;
- `task: NONE` is distinct from `task: NOT_ESTABLISHED`;
- explanation of COMS is not evidence that synchronization completed;
- missing completion evidence is `NOT_ESTABLISHED` from that return, not refusal/absence/failure;
- retries/re-requests are visible new events, never silent;
- delegated work carries `reply_route`, `integration_owner`, `observation_owner`, and `next_check`;
- absence is recorded as bounded `NOT_OBSERVED`, never inferred global failure.

## EVIDENCE POSTURE

Observed useful successes:
- immutable COM_STATE bootstrap supported task discovery + HELLO;
- fixed public GitHub `commits/main` rendezvous matched independently observed live head at multiple tested boundaries;
- one full cold chain succeeded: fixed rendezvous -> live SHA -> immutable state -> task discovery -> COMS -> protocol-complete HELLO.

Observed useful failures:
- mutable repository-root retrieval repeatedly served coherent historical state to QW;
- QW twice explained COMS accurately without executing it, motivating the auditable completion witness;
- a later QW return replayed historical task `COM-V031-QW-004` / anchor `b0ddef2f...` while FW independently observed a later live head.

Issue #15 (`COM-V032-QW-004`) was cancelled under Mark's instruction to stabilize COM and return to Campfire. Its missing return remains bounded `NOT_OBSERVED`; no QW failure or route diagnosis is inferred.

CC reviews were correlated and returned `NARROW — no BREAK`; they are design review evidence, not validation. QW runtime/model/provider labels remain SELF_CLAIM unless independently established.

## KNOWN LIMITS — CARRY FORWARD, DO NOT BLOCK PRODUCT WORK

- A stale carrier cannot be repaired by prose inside the stale copy it already served.
- The fixed GitHub rendezvous has worked but is not proven universally fresh, continuously available, or portable across providers/carriers.
- QW produced one historical-head replay through a path that had previously worked; exact cause remains unresolved.
- Human relay remains necessary where an aperture has no writable route; provenance/modality must remain explicit.
- `observation_owner + next_check` has not yet completed a fully autonomous asynchronous loop without a human trigger.
- Event identity recovery across a route that strips identity remains untested.

These are known engineering limits, not reasons to keep polishing COM in isolation.

## COMS

`COMS` means synchronize from shared COM before relying on conversational assumptions.

Current result:
- **FW:** synchronized; no active COM task; return to Campfire Relay work.
- **CC:** no active COM task.
- **QW:** no active COM task.
- **Other apertures:** no active COM task.

## ANTI-DRIFT / REOPEN RULE

Do not add schema, CI, automation, cryptographic identity machinery, leases, new failure taxonomies, or new protocol primitives for elegance.

COM work reopens only when:
1. real Campfire Relay work exposes a concrete coordination/provenance/freshness/authority/return-path defect; or
2. Mark explicitly directs a new COM task.

The practical goal is less ambiguity and less human relay burden, not more protocol.

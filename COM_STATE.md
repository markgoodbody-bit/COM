# COM_STATE v0.3.2

STATUS: WORKING BASELINE / ACTIVE BOUNDED INTRODUCTION

COM is not validated, canon, or a truth oracle. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

## CURRENT

- human_authority: Mark
- active_task: `COM-V032-BUILD2-001` — Campfire 1 ↔ Build 2 introduction / routing identity handshake
- execution_mode: BUILD 2 COMS + HELLO/WELCOME ONLY / NO CODE MUTATION
- addressed_to: active Framework aperture/tab carrying the Campfire Relay v0.18.3 build lane; Mark's current human label for that aperture is `Build 2`; session/runtime/model/provider are not established by this label
- lane_evidence: Campfire Relay issue #127 + draft PR #130 `framework/v0.18.3-trace-integration`, frozen candidate head `e84f7e0ac98f309c2ca9339a90d66d0322cc70c5`; if this does not match the receiver's current work, it must not claim `Build 2`
- instruction: execute COMS from a fresh anchor; establish your own role/session/runtime/model/provider honestly; if the lane evidence matches, receive Campfire 1 HELLO `COM-HELLO-CAMPFIRE1-20260728-001` and reply on COM issue #16 with a protocol-complete HELLO or WELCOME/receipt
- integration_owner: Campfire 1 / session `FW-20260728-CAMPFIRE-A91D`
- repository_mutation: Build 2 may reply on COM issue #16 only for this task; no COM file/branch mutation and no Campfire Relay code/build/release/provider action is authorized by this introduction
- reply_route: COM issue #16 `COM v0.3.2 · Campfire 1 HELLO to Build 2`
- observation_owner: Campfire 1 / session `FW-20260728-CAMPFIRE-A91D`
- next_check: MANUAL
- authority_source: Mark current conversation instruction — "Introduce yourself to Build 2 over COMS (it may not know it's Build 2 yet)"
- state_basis: `af083258f42a98c20107d9e767ab6134b4051b57` — main before this projection update; this file is not self-authenticating freshness
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

Current coordination event:
- COM issue #16 carries Campfire 1's protocol-complete HELLO and Mark's human routing label `Build 2`; no Build 2 receipt has yet been observed at this projection boundary.

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
- **Build 2:** if you are the active Framework aperture carrying the Campfire Relay v0.18.3 lane identified above, perform `COM-V032-BUILD2-001`; establish fresh session/identity honestly and reply on issue #16. If the lane evidence does not match, do not claim the role.
- **Campfire 1:** HELLO emitted on issue #16; observe that exact reply route at the next manual check; do not infer receipt before a return is observed.
- **CC:** no active COM task.
- **QW:** no active COM task.
- **Other apertures:** no active COM task.

## ANTI-DRIFT / REOPEN RULE

Do not add schema, CI, automation, cryptographic identity machinery, leases, new failure taxonomies, or new protocol primitives for elegance.

COM work reopens only when:
1. real Campfire Relay work exposes a concrete coordination/provenance/freshness/authority/return-path defect; or
2. Mark explicitly directs a new COM task.

The practical goal is less ambiguity and less human relay burden, not more protocol.

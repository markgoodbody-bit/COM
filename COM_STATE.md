# COM_STATE v0.3.2

STATUS: WORKING BASELINE / IDLE — BOUNDED CANDIDATE RETURNED

COM is not validated, canon, or a truth oracle. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

## CURRENT

- human_authority: Mark
- active_task: NONE
- execution_mode: IDLE / NO COM MUTATION AUTHORIZED BY CURRENT PROJECTION
- addressed_to: NONE
- integration_owner: NONE
- repository_mutation: NONE from current COM state; any further COM mutation requires a fresh explicit task/authority source
- reply_route: NONE for active work
- observation_owner: NONE
- next_check: MANUAL
- authority_source: none for new work; completed bounded task was authorized by Mark's conversation instruction — "very good. proceed. build"
- state_basis: `9e9ddd17c69b032b8a51f190d0c35aade510dc03` — prior main projection; this file is not self-authenticating freshness
- last_returned_task: `COM-V032-PROJECTION-001`
- last_return_route: COM issue #17; return event `COM-BUILD2-PROJECTION-RETURN-20260728-001`
- candidate: draft PR #19 `COM v0.3.2: prevent task replay from projection lag`, branch `framework/com-v032-projection-lag`, exact returned head `8705034806b4e740f82a09d99c9591b8102e3bb8`
- candidate_exact_blobs: protocol `e4392669284dd1d8ad2a3daf818f72e8700c80a9`; witness `6c4c33e1f46a6f9ce72a225dc891f334cdfcd2c9`
- candidate_status: RETURNED / DRAFT / MERGEABLE AT RETURN BOUNDARY / NOT MERGED / NOT INTEGRATED / NOT VALIDATION
- prior_task_correction: `COM-V032-BUILD2-001` remains historical, not active. Build 2 HELLO/receipt `COM-HELLO-BUILD2-20260728-001` and later return `COM-BUILD2-FRONTIER-OUTPUT-RETURN-20260728-001` are preserved on its declared reply route, issue #16. No Campfire 1 acknowledgement is inferred where none was observed.
- core_status: v0.3 integrated working baseline
- protocol_status: v0.3.2 integrated working baseline; projection-lag repair exists only as draft candidate PR #19 until explicitly integrated
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
- one full cold chain succeeded: fixed rendezvous -> live SHA -> immutable state -> task discovery -> COMS -> protocol-complete HELLO;
- issue #16 carried Build 2's protocol-complete HELLO/receipt and a later bounded product-repair return without requiring Mark to carry the work product itself.

Observed useful failures:
- mutable repository-root retrieval repeatedly served coherent historical state to QW;
- QW twice explained COMS accurately without executing it, motivating the auditable completion witness;
- a later QW return replayed historical task `COM-V031-QW-004` / anchor `b0ddef2f...` while FW independently observed a later live head;
- issue #16 exposed a distinct projection-lag defect: COM `main` and `COM_STATE.md` were freshly anchored, but the projection still showed an introduction task active after its declared reply route already contained the required receipt and later terminal return.

Issue #15 (`COM-V032-QW-004`) was cancelled under Mark's instruction to stabilize COM and return to Campfire. Its missing return remains bounded `NOT_OBSERVED`; no QW failure or route diagnosis is inferred.

CC reviews were correlated and returned `NARROW — no BREAK`; they are design review evidence, not validation. QW runtime/model/provider labels remain SELF_CLAIM unless independently established.

Current coordination event:
- `COM-V032-PROJECTION-001` returned on issue #17 and is represented by draft PR #19; it is not active work and has not been integrated;
- issue #16 remains historical route evidence for the prior Build 2 introduction/product-return chain.

## KNOWN LIMITS — CARRY FORWARD, DO NOT BLOCK PRODUCT WORK

- A stale carrier cannot be repaired by prose inside the stale copy it already served.
- The fixed GitHub rendezvous has worked but is not proven universally fresh, continuously available, or portable across providers/carriers.
- QW produced one historical-head replay through a path that had previously worked; exact cause remains unresolved.
- Human relay remains necessary where an aperture has no writable route; provenance/modality must remain explicit.
- `observation_owner + next_check` has not yet completed a fully autonomous asynchronous loop without a human trigger.
- Event identity recovery across a route that strips identity remains untested.
- `COM_STATE.md` is a derived projection and can lag route events until an authorized writer observes and incorporates them. Draft PR #19 contains a bounded candidate repair preventing such lag from causing duplicate task execution; this state does not claim that repair is integrated before merge/integration.

These are known engineering limits, not reasons to keep polishing COM in isolation.

## COMS

`COMS` means synchronize from shared COM before relying on conversational assumptions.

Current result:
- **Build 2:** no active COM task.
- **Campfire 1:** no active COM task. Issue #16 remains historical route evidence; no acknowledgement is inferred if none is observed.
- **CC:** no active COM task.
- **QW:** no active COM task.
- **Other apertures:** no active COM task.

Draft PR #19 is an unresolved integration decision, not an active mutation task. A future aperture may inspect it when an explicit integration/review decision is requested; it must not merge or continue the candidate merely because it exists.

## ANTI-DRIFT / REOPEN RULE

Do not add schema, CI, automation, cryptographic identity machinery, leases, new failure taxonomies, or new protocol primitives for elegance.

COM work reopens only when:
1. real Campfire Relay work exposes a concrete coordination/provenance/freshness/authority/return-path defect; or
2. Mark explicitly directs a new COM task.

The practical goal is less ambiguity and less human relay burden, not more protocol.

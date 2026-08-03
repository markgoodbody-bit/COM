# COM_STATE v0.3.2

STATUS: ACTIVE — BOUNDED CC REVIEW DELEGATED

COM is not validated, canon, or a truth oracle. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

## CURRENT

- human_authority: Mark
- active_task: `CR-V01831-CC-REVIEW-001`
- execution_mode: DELEGATED READ-ONLY HOSTILE REVIEW
- addressed_to: CC
- integration_owner: Framework / Build 3, session `FW-BUILD3-20260803T202518Z-6A91`
- repository_mutation: no Campfire Relay mutation authorized; CC may write only return comments on the declared COM route
- reply_route: COM issue #21, `CC review · Campfire Relay v0.18.31 model-catalogue candidate`
- observation_owner: Framework / Build 3
- next_check: MANUAL on CC terminal return
- authority_source: Mark's 2026-08-03 conversation instruction — “Claude Code (CC) is fresh and available. COMS and proceed. You are Framework (Build 3).”
- state_basis: `5b60bddfa10a2490ef1e8c778ffa4768fd4d30a0` — prior anchored COM main state; this projection is not self-authenticating freshness
- task_event: `COM-FW3-CR-V01831-REVIEW-20260803-001`
- thread_id: `CR-V01831-MODEL-CATALOG-REVIEW`
- work_target: Campfire Relay draft PR #156
- work_target_head: `bf9b7a88698d04cdb3a82ab99e6cee22ae0ae7e6`
- work_target_base: `eeee56b601f4698aadbc56c5665be69093d18245`
- work_target_tree: `3092dcf55fe05f834cd5b20d529987e70c687f57`
- task_status: OPEN / AWAITING protocol-complete CC COMS + HELLO + ACK, then terminal review return
- write_scope: read-only review of `markgoodbody-bit/campfire-relay`; COM issue #21 comments only
- no_touch: Campfire Relay main, PR #156 bytes/metadata, release/tag/package/Production activation, TRACE/COM/Debate semantics, live provider calls/spend, v0.19/Exchange
- required_return: verdict `NO BREAK`, `NARROW`, or `BREAK`; exact evidence; observed/inspected/unverified distinctions; integration recommendation; explicit agreement-is-not-validation boundary
- current_product_lane: Campfire Relay v0.18.31 modular model-catalogue maintenance candidate
- product_candidate_status: draft PR #156; hosted-green built candidate; not merged, tagged, released, published to trusted persistent release channel, or activated in Windows Production
- human_release_authority: Mark retains merge and release authority

Prior completed coordination remains historical, not active:
- last_returned_task: `COM-V032-PROJECTION-001`
- last_return_route: COM issue #17; return event `COM-BUILD2-PROJECTION-RETURN-20260728-001`
- projection-lag candidate: draft COM PR #19, branch `framework/com-v032-projection-lag`, exact returned head `8705034806b4e740f82a09d99c9591b8102e3bb8`
- projection-lag candidate_status: RETURNED / DRAFT / NOT MERGED / NOT INTEGRATED / NOT VALIDATION; not part of the current task
- prior Build 2 introduction/product-return route: COM issue #16; historical only

Core/protocol status:
- core_status: v0.3 integrated working baseline
- protocol_status: v0.3.2 integrated working baseline
- COM status: coordination carrier for real Campfire Relay work; do not reopen protocol design unless a concrete defect appears or Mark explicitly directs it

## ACTIVE TASK ENVELOPE

```text
task_id: CR-V01831-CC-REVIEW-001
addressed_to: CC
instruction: COMS from anchored COM state, emit a fresh protocol-complete HELLO/ACK on issue #21, then independently and hostilely review exact Campfire Relay PR #156 head bf9b7a88698d04cdb3a82ab99e6cee22ae0ae7e6. Do not inherit Build 2 conclusions as validation.
base_anchor: COM prior main 5b60bddfa10a2490ef1e8c778ffa4768fd4d30a0; Campfire Relay PR #156 base eeee56b601f4698aadbc56c5665be69093d18245, head bf9b7a88698d04cdb3a82ab99e6cee22ae0ae7e6, tree 3092dcf55fe05f834cd5b20d529987e70c687f57
write_scope: read-only Campfire Relay review; COM issue #21 comments only
no_touch: main, PR mutation, merge, tag, release, package publication, Production activation, TRACE/COM/Debate semantics, provider spend, v0.19/Exchange
authority_source: Mark current conversation instruction; delegated by Framework / Build 3 for this bounded review only
reply_route: COM issue #21
status: OPEN
integration_owner: Framework / Build 3, FW-BUILD3-20260803T202518Z-6A91
observation_owner: Framework / Build 3
next_check: MANUAL on terminal return
```

The detailed review questions and return contract live in immutable issue event `COM-FW3-CR-V01831-REVIEW-20260803-001` on COM issue #21. The issue thread is the reply route; this state projection is the discovery surface.

Exact-head discipline applies. If PR #156 head moves outside the stated envelope, CC must report drift and stop rather than silently adapting.

## INTEGRATED BASELINE

Core/protocol lineage retained from the prior state:
- PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf` — cold bootstrap, freshness, delegated-return discovery;
- PR #8 merged at `5219ca2df18213289948935ecc4b1ffa8925fe0c` — COMS front-door execution repair;
- PR #14 reviewed candidate head `3215f9e41601b6ec4e6854bd441770d38b892dec` was closed unmerged after exact manual integration onto current `main` because the live-state branch had moved;
- exact PR #14 README blob `cc12ad01b17b6623409eb6eee055f6b47d3dbaf5` integrated at `d6025c0e47f4e1cc81323ccc603256405b01f8a4`;
- exact PR #14 protocol blob `45c66e7e62530c57de91d8330cc2e1963c8741d1` integrated at `c299dd9a1f24dd8b3e97eafb69d4bf66fd8d3e6f`.

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
- issue #16 carried Build 2's protocol-complete HELLO/receipt and later bounded product-repair return without requiring Mark to carry the work product itself.

Observed useful failures:
- mutable repository-root retrieval repeatedly served coherent historical state to QW;
- QW twice explained COMS accurately without executing it, motivating the auditable completion witness;
- a later QW return replayed historical task `COM-V031-QW-004` / anchor `b0ddef2f...` while FW independently observed a later live head;
- issue #16 exposed projection lag: freshly anchored COM state still showed an introduction task active after its declared reply route contained the required receipt and later terminal return.

Issue #15 (`COM-V032-QW-004`) was cancelled under Mark's instruction to stabilize COM and return to Campfire. Its missing return remains bounded `NOT_OBSERVED`; no QW failure or route diagnosis is inferred.

CC reviews are design/review evidence, not validation. Runtime/model/provider labels remain self-claims unless independently established.

## KNOWN LIMITS — CARRY FORWARD, DO NOT BLOCK PRODUCT WORK

- A stale carrier cannot be repaired by prose inside the stale copy it already served.
- The fixed GitHub rendezvous has worked but is not proven universally fresh, continuously available, or portable across providers/carriers.
- QW produced one historical-head replay through a path that had previously worked; exact cause remains unresolved.
- Human relay remains necessary where an aperture has no writable route; provenance/modality must remain explicit.
- `observation_owner + next_check` has not yet completed a fully autonomous asynchronous loop without a human trigger.
- Event identity recovery across a route that strips identity remains untested.
- `COM_STATE.md` is a derived projection and can lag route events until an authorized writer observes and incorporates them. Draft PR #19 contains a bounded candidate repair preventing such lag from causing duplicate task execution; this state does not claim that repair is integrated.

These are known engineering limits, not reasons to polish COM instead of doing the Campfire Relay work.

## COMS

`COMS` means synchronize from shared COM before relying on conversational assumptions.

Current result by role:
- **Framework / Build 3:** active integration/observation ownership for `CR-V01831-CC-REVIEW-001`; inspect issue #21 at the manual observation boundary; do not merge or release without Mark's later decision.
- **CC:** active task `CR-V01831-CC-REVIEW-001`; execute COMS, emit fresh HELLO/ACK, review exact PR #156 head, and return on issue #21.
- **Build 2:** no active task; prior v0.18.31 candidate construction is historical evidence and must not be treated as an independent review.
- **Campfire 1:** no active COM task.
- **QW:** no active COM task.
- **Other apertures:** no active COM task.

Draft COM PR #19 remains an unresolved integration decision, not an active mutation task. It must not be merged or continued merely because it exists.

## ANTI-DRIFT / REOPEN RULE

Do not add schema, CI, automation, cryptographic identity machinery, leases, new failure taxonomies, or new protocol primitives for elegance.

COM protocol work reopens only when:
1. real Campfire Relay work exposes a concrete coordination/provenance/freshness/authority/return-path defect; or
2. Mark explicitly directs a new COM task.

The practical goal is less ambiguity and less human relay burden, not more protocol.

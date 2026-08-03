# COM_STATE v0.3.2

STATUS: ACTIVE — CC REVIEW OPEN / FRAMEWORK REPAIR RETURNED

COM is a working coordination baseline, not canon, validation, consensus, or a truth oracle. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making Mark carry the whole collaboration.

## CURRENT

- human_authority: Mark
- active_task: `COM-V032-CC-REVIEW-002`
- execution_mode: CC READ-ONLY HOSTILE REVIEW + FRAMEWORK PARALLEL BUILD RETURNED
- addressed_to: CC
- integration_owner: Framework / Build 3, session `FW-BUILD3-20260803T202518Z-6A91`
- observation_owner: Framework / Build 3
- next_check: MANUAL on CC terminal return
- reply_route: COM issue #20, `COM-V032-CC-REVIEW-002 · cold review Campfire Relay PR #156`
- authority_source: Mark's 2026-08-03 instructions — `Claude Code (CC) is fresh and available. COMS and proceed`, followed by `COMS and build. CC is available for tasks`
- state_basis: `b3d6d339b648393e41ec99f885fe1224ad7b96ef` plus issue #20 events through `COM-FW3-V01831-RUNTIME-REPAIR-RETURN-20260803-001`; this file is not self-authenticating freshness
- task_status: OPEN / AWAITING CC COMS + fresh HELLO/ACK + terminal review return
- CC_mutation_authority: NONE; issue comments only
- current_product_lane: Campfire Relay v0.18.31 modular model-catalogue maintenance candidate

Original CC review target:
- repository: `markgoodbody-bit/campfire-relay`
- draft PR: #156
- base: `eeee56b601f4698aadbc56c5665be69093d18245`
- head: `bf9b7a88698d04cdb3a82ab99e6cee22ae0ae7e6`
- tree: `3092dcf55fe05f834cd5b20d529987e70c687f57`
- status: CONFIRMED MATERIAL RUNTIME DEFECT / NOT READY FOR INTEGRATION AS-IS

Framework repair candidate:
- draft PR: #157, `v0.18.31: make modular catalogue the runtime authority`
- base: exact PR #156 head `bf9b7a88698d04cdb3a82ab99e6cee22ae0ae7e6`
- head: `b79953b4c54d9e057d6976cb25ca591d6479a187`
- tree: `8c5b58bce19802a0f31c2e2ba835145a9f9e8b3a`
- repaired server Git blob: `5dec56d0b2d71f7a7aa3188450d7beac3f3f230e`
- status: DRAFT / HOSTED-GREEN / OPEN / MERGEABLE / UNMERGED / NOT RELEASED
- final delta: five files; temporary workflows and patch scripts removed
- provider calls/spend: NONE
- human_release_authority: Mark retains integration, merge and release authority

## CONFIRMED PRODUCT DEFECT AND REPAIR

Defect `CR-V01831-RUNTIME-CATALOG-AUTHORITY-001`:

PR #156 introduced the verified modular catalogue and made `loadModels()` default to its manifest, but `src/server.mjs` explicitly supplied `config/models.json`. The actual server bootstrap therefore loaded the legacy compatibility snapshot rather than the hash-bound modular catalogue. Catalogue, provider-module and concrete model-entry identities were not the runtime authority claimed by the candidate.

Framework / Build 3 built draft PR #157 under Mark's explicit build instruction. The narrow final repair:

1. changes `src/server.mjs` to load `config/model-catalog/manifest.json`;
2. adds a real-server runtime-authority regression witness;
3. admits only exact repaired server blob `5dec56d0...` into B7a, B8C and B9 source-lineage guards;
4. introduces no wildcard, mutable-head or generic successor acceptance.

Final hosted board on exact head `b79953b4...`:
- campfire-ci #1026 — SUCCESS;
- budget-core-ci #369 — SUCCESS;
- B8C #146 — SUCCESS;
- B9 #109 — SUCCESS;
- v0.18.31 release-candidate #9 — SUCCESS;
- historical v0.18.2 / v0.18.2.1 / v0.18.3 release workflows — correctly SKIPPED.

Release-candidate evidence:
- application: `0.18.31`;
- model catalogue: `2026.08.03.1`;
- package: `CAMPFIRE_RELAY_v0_18_31.zip`;
- package SHA-256: `bfaf94ba0ec2889820dc8e9df9aba20ae517cf0c5d10bffd98a9d1fc8e70fce1`;
- catalogue manifest SHA-256: `f1fce253299da622e54df571b1551a56a353ef1b51c8014d5836a257c6086eaf`;
- Actions artifact ID: `8871016484`;
- artifact digest: `9675345202f2d943389bf8f9437b186dc9e69e3c8b4fc93f8d5b805792faf38d`.

This is build/test evidence, not validation or release authority. No tag, GitHub release, trusted persistent package publication, Windows Production activation, TRACE/ME/COM/Debate semantic change, or v0.19/Exchange work occurred.

## ACTIVE CC TASK ENVELOPE

```text
task_id: COM-V032-CC-REVIEW-002
addressed_to: CC
instruction: execute COMS from anchored COM, emit a fresh protocol-complete HELLO/ACK on issue #20, then independently and hostilely review exact Campfire Relay PR #156 head bf9b7a88698d04cdb3a82ab99e6cee22ae0ae7e6; confirm, narrow or reject Framework's runtime-authority break from independent evidence; continue searching for other defects; PR #157 may be inspected only as the proposed repair
base_anchor: Campfire Relay base eeee56b601f4698aadbc56c5665be69093d18245; original head bf9b7a88698d04cdb3a82ab99e6cee22ae0ae7e6; repair head b79953b4c54d9e057d6976cb25ca591d6479a187
write_scope: read-only Campfire Relay review; COM issue #20 comments only
no_touch: Campfire Relay branches/PRs/main; merge; tag; release; package publication; Production activation; TRACE/COM/Debate semantics; provider calls/spend; v0.19/Exchange
reply_route: COM issue #20
status: OPEN
integration_owner: Framework / Build 3, FW-BUILD3-20260803T202518Z-6A91
observation_owner: Framework / Build 3
next_check: MANUAL on terminal return
```

Required terminal verdict remains:
- `BREAK — concrete defect`;
- `NARROW — bounded repair required`; or
- `CLEAR FOR FRAMEWORK INTEGRATION DECISION — no material defect observed`.

Return must identify exact reviewed head, inspected files, tests/commands if any, confirmed facts versus inference, unresolved uncertainty, and whether mutation occurred. Agreement is not validation.

Exact-head discipline applies. If PR #156 or the proposed repair moves outside the stated envelope, CC must report drift rather than silently adapting.

## ADDITIONAL READ-ONLY INSPECTION SURFACES

Supplied by Mark and carried on canonical issue #20:

- `http://127.0.0.1:4317/` — same-machine installed Campfire surface where reachable. Read-only observation only. It is not evidence that PR #156 or #157 is installed and not a GitHub freshness anchor. No Relay/Debate/re-judge, provider call, Setup/profile/catalogue/configuration/state/updater/release mutation.
- `markgoodbody-bit/TRACE` — semantic/provenance reference, observed main anchor `0a74b94bbd403756c1f14b23c09fc935bdac46ca`; not an edit target, promotion source or truth authority.
- `markgoodbody-bit/mechanical-ethics` — human/normative provenance reference, observed main anchor `fb2cc9e41107bba6ec66d7788513d6e208af80c5`; not an executable specification or edit target.
- `markgoodbody-bit/campfire-relay` — executable review target. Local installed runtime, repository main/base, original candidate, repair candidate and semantic source repositories must remain separately identified.

## CONTINUITY CORRECTION

Mark supplied the old Framework / Build 2 chat after Framework / Build 3 had opened issue #21 for the same review target.

Recovered evidence established:
- issue #20 was created first by Build 2 for exact head `bf9b7a88698d04cdb3a82ab99e6cee22ae0ae7e6`;
- issue #20 remains the canonical task and reply route;
- Build 3 took over integration/observation ownership without changing CC's original target or authority boundary;
- issue #21 is closed as duplicate, not completed, and remains visible evidence of projection/continuity failure;
- no CC return has yet been observed on the canonical route. This is bounded `NOT_OBSERVED`, not failure, refusal or absence.

Defect record:
- defect_id: `COM-PROJECTION-DUPLICATE-ROUTE-001`;
- immediate repair: preserve earliest task identity/route, transfer ownership, close later route as duplicate, correct COM_STATE;
- broader protocol change: NONE authorized or presently required.

## PRIOR COORDINATION — HISTORICAL, NOT ACTIVE

- Build 2 constructed PR #156 and dispatched issue #20 before its chat reached maximum length.
- duplicate issue #21: CLOSED / DUPLICATE; do not ACK or return there.
- prior returned task: `COM-V032-PROJECTION-001`, return route issue #17.
- projection-lag candidate: draft COM PR #19, exact returned head `8705034806b4e740f82a09d99c9591b8102e3bb8`; RETURNED / DRAFT / NOT MERGED / NOT INTEGRATED / NOT VALIDATION.
- prior Build 2 introduction/product-return route issue #16 remains historical evidence.

Core/protocol status:
- core_status: v0.3 integrated working baseline;
- protocol_status: v0.3.2 integrated working baseline;
- COM protocol work remains paused unless real Campfire work exposes a concrete defect or Mark explicitly directs it.

## EVIDENCE POSTURE

Useful successes retained:
- immutable COM_STATE bootstrap supported task discovery and HELLO;
- fixed GitHub rendezvous has matched independently observed heads at several boundaries;
- issue routes have carried bounded AI returns without Mark transporting the work product itself.

Useful failures retained:
- mutable-root retrieval has served coherent historical state;
- QW has explained COMS without executing it and replayed a historical head;
- issue #16 exposed projection lag after route completion;
- the current Build 3 duplication exposed another projection/continuity failure: issue #20 existed but was absent from the state Build 3 synchronized against.

These are bounded engineering observations. They do not validate COM and are not a reason to stop Campfire product work for protocol polishing.

## COMS

Current result by role:
- **Framework / Build 3:** parallel build returned as hosted-green draft PR #157; owns integration and manual observation for `COM-V032-CC-REVIEW-002`; do not merge or release without Mark's decision.
- **CC:** active review task `COM-V032-CC-REVIEW-002`; COMS, fresh HELLO/ACK and terminal return on issue #20 only.
- **Build 2:** no active task; PR #156 construction and original dispatch are historical evidence.
- **Campfire 1:** no active COM task.
- **QW:** no active COM task.
- **Other apertures:** no active COM task.

## ANTI-DRIFT

Do not add protocol machinery for elegance. Do not turn green CI, repeated model conclusions or clean presentation into validation. Do not reopen COM design unless a concrete coordination defect requires bounded repair or Mark explicitly orders it.

The practical goal is less ambiguity and less human relay burden while getting Campfire Relay into trustworthy usable shape.

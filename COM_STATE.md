# COM_STATE v0.3.2

STATUS: ACTIVE — v0.18.31 INTEGRATED BUILD RETURNED / CC REVIEW OPEN

COM is a working coordination baseline, not canon, validation, consensus, or a truth oracle. Model agreement and green CI are not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making Mark carry the whole collaboration.

## CURRENT

- human_authority: Mark
- active_task: `COM-V032-CC-REVIEW-002`
- execution_mode: CC READ-ONLY HOSTILE REVIEW + FRAMEWORK INTEGRATED BUILD RETURNED
- addressed_to: CC
- integration_owner: Framework / Build 3, session `FW-BUILD3-20260803T202518Z-6A91`
- observation_owner: Framework / Build 3
- next_check: MANUAL on CC terminal return
- reply_route: COM issue #20, `COM-V032-CC-REVIEW-002 · cold review Campfire Relay PR #156`
- authority_source: Mark's 2026-08-03 instructions — `Claude Code (CC) is fresh and available. COMS and proceed`; `COMS and build. CC is available for tasks`; `COMS and build 0.18.31`
- state_basis: issue #20 events through `COM-FW3-V01831-INTEGRATED-BUILD-RETURN-20260803-001` plus exact Campfire candidate head `6e03370794f2269715a1bfc23d6918507ae6c502`; this file is not self-authenticating freshness
- task_status: OPEN / AWAITING CC COMS + fresh HELLO/ACK + terminal review return
- CC_mutation_authority: NONE; issue comments only
- current_product_lane: Campfire Relay v0.18.31 modular model-catalogue maintenance candidate
- human_release_authority: Mark retains main merge and release authority

## ORIGINAL DEFECTIVE CANDIDATE — PRESERVED EVIDENCE

- repository: `markgoodbody-bit/campfire-relay`
- PR: #156
- base main anchor: `eeee56b601f4698aadbc56c5665be69093d18245`
- original head: `bf9b7a88698d04cdb3a82ab99e6cee22ae0ae7e6`
- original tree: `3092dcf55fe05f834cd5b20d529987e70c687f57`
- status: MATERIAL RUNTIME DEFECT / SUPERSEDED AS LIVE CANDIDATE / PRESERVED FOR ATTRIBUTION

Defect `CR-V01831-RUNTIME-CATALOG-AUTHORITY-001`:

PR #156 introduced a verified modular catalogue and made `loadModels()` default to its manifest, but `src/server.mjs` explicitly supplied legacy `config/models.json`. The actual server bootstrap therefore bypassed the modular manifest. Catalogue, provider-module and concrete-model-entry identities were not the runtime authority claimed by the candidate.

## REPAIR AND INTEGRATION

Framework / Build 3 built repair PR #157 under Mark's explicit build instruction.

Repair source:
- PR #157 head: `b79953b4c54d9e057d6976cb25ca591d6479a187`
- repair tree: `8c5b58bce19802a0f31c2e2ba835145a9f9e8b3a`
- repaired server Git blob: `5dec56d0b2d71f7a7aa3188450d7beac3f3f230e`
- status: HOSTED-GREEN / MERGED INTO CANDIDATE BRANCH ONLY

The narrow repair:

1. changes `src/server.mjs` to load `config/model-catalog/manifest.json`;
2. adds a real-server runtime-authority regression witness;
3. admits only exact repaired server blob `5dec56d0...` into B7a, B8C and B9 source-lineage guards;
4. introduces no wildcard, mutable-head or generic-successor acceptance.

Mark then directed `COMS and build 0.18.31`. Framework integrated PR #157 into the PR #156 candidate branch.

Integrated candidate:
- PR: #156
- head: `6e03370794f2269715a1bfc23d6918507ae6c502`
- tree: `8c5b58bce19802a0f31c2e2ba835145a9f9e8b3a`
- application: `0.18.31`
- model catalogue: `2026.08.03.1`
- status: DRAFT / OPEN / MERGEABLE / HOSTED-GREEN / NOT MERGED TO MAIN / NOT RELEASED
- final diff from main: 35 files; no temporary payload, patch workflow, or inspection file remains

## FINAL HOSTED BOARD

On exact integrated head `6e03370794f2269715a1bfc23d6918507ae6c502`:

- campfire-ci #1027 — SUCCESS;
- budget-core-ci #370 — SUCCESS;
- B8C #147 — SUCCESS;
- B9 #110 — SUCCESS;
- v0.18.31 release-candidate #10 — SUCCESS;
- historical v0.18.2 / v0.18.2.1 / v0.18.3 release workflows — correctly SKIPPED.

Successful gates include:

- exact application, catalogue and package identity;
- cold-start and upgrade witnesses;
- modular catalogue hash/capability/provenance witnesses;
- exact B7a server/estimate successor witness;
- focused and full B8C accounting/ledger tests;
- focused and full B9 browser/module tests;
- complete no-spend Campfire suites;
- exact package-candidate construction and evidence upload.

Integrated package evidence:
- package: `CAMPFIRE_RELAY_v0_18_31.zip`;
- package SHA-256: `f8cd3d4725bec93b9bd20f6132a53645b185a99c4d2dac1c3d1218eb41fb6911`;
- catalogue manifest SHA-256: `f1fce253299da622e54df571b1551a56a353ef1b51c8014d5836a257c6086eaf`;
- Actions artifact ID: `8871168356`;
- artifact digest: `8454c163b79426303e51ba150f0776b17cb253d3f7358d1f8011ea2700b911c1`.

Framework downloaded and inspected the artifact. Internal evidence reproduced the exact source commit, tree, catalogue version, manifest hash and package hash.

This is build/test evidence, not validation or release authority.

## ACTIVE CC TASK ENVELOPE

```text
task_id: COM-V032-CC-REVIEW-002
addressed_to: CC
instruction: execute COMS from anchored COM, emit a fresh protocol-complete HELLO/ACK on issue #20, preserve any work against original defective head bf9b7a88698d04cdb3a82ab99e6cee22ae0ae7e6 as original-head evidence, then independently review integrated successor head 6e03370794f2269715a1bfc23d6918507ae6c502; confirm, narrow or reject Framework's runtime-authority defect; test whether the integrated repair closes it; continue searching for any other material defect
base_anchor: main eeee56b601f4698aadbc56c5665be69093d18245; original defective head bf9b7a88698d04cdb3a82ab99e6cee22ae0ae7e6; repair head b79953b4c54d9e057d6976cb25ca591d6479a187; integrated head 6e03370794f2269715a1bfc23d6918507ae6c502
write_scope: read-only Campfire Relay review; COM issue #20 comments only
no_touch: Campfire Relay branches/PRs/main; merge; tag; release; package publication; Production activation; TRACE/Mechanical Ethics/COM/Debate semantics; provider calls/spend; v0.19/Exchange
reply_route: COM issue #20
status: OPEN
integration_owner: Framework / Build 3, FW-BUILD3-20260803T202518Z-6A91
observation_owner: Framework / Build 3
next_check: MANUAL on terminal return
```

Required terminal verdict:
- `BREAK — concrete defect`;
- `NARROW — bounded repair required`; or
- `CLEAR FOR FRAMEWORK INTEGRATION DECISION — no material defect observed`.

Return must identify exact reviewed heads, inspected files, tests/commands if any, confirmed facts versus inference, unresolved uncertainty, and whether mutation occurred. Agreement is not validation.

The head transition was explicitly recorded on issue #20. No silent exact-head adaptation is permitted.

## BOUNDARY

No provider call or spend. No merge to main. No tag, GitHub release, trusted persistent package publication or Windows Production activation. No TRACE, Mechanical Ethics, COM or Debate Hall semantic change. No v0.19/Exchange work.

## CONTINUITY CORRECTION

Issue #20 remains the canonical task and reply route. Duplicate issue #21 is closed as duplicate and remains visible evidence of projection lag. No CC return has yet been observed on the canonical route. This is bounded `NOT_OBSERVED`, not failure, refusal or absence.

Defect record:
- `COM-PROJECTION-DUPLICATE-ROUTE-001`;
- immediate repair: preserve earliest task identity/route, transfer ownership, close later route as duplicate, correct COM_STATE;
- broader protocol change: NONE presently authorized or required.

## PRIOR COORDINATION — HISTORICAL, NOT ACTIVE

- Build 2 constructed the original PR #156 candidate and opened issue #20 before its chat reached maximum length.
- repair PR #157: MERGED INTO CANDIDATE BRANCH / CLOSED / NOT A MAIN MERGE OR RELEASE.
- duplicate issue #21: CLOSED / DUPLICATE; do not ACK or return there.
- prior returned task: `COM-V032-PROJECTION-001`, return route issue #17.
- projection-lag candidate: draft COM PR #19, exact returned head `8705034806b4e740f82a09d99c9591b8102e3bb8`; RETURNED / DRAFT / NOT MERGED / NOT INTEGRATED / NOT VALIDATION.

Core/protocol status:
- core_status: v0.3 integrated working baseline;
- protocol_status: v0.3.2 integrated working baseline;
- COM protocol work remains paused unless real Campfire work exposes a concrete defect or Mark explicitly directs it.

## COMS

Current result by role:
- **Framework / Build 3:** integrated v0.18.31 build returned at exact head `6e033707...`; owns integration and manual observation; main/release untouched.
- **CC:** active review task `COM-V032-CC-REVIEW-002`; COMS, fresh HELLO/ACK and terminal return on issue #20 only.
- **Build 2:** no active task; original candidate construction is historical evidence.
- **Campfire 1:** no active COM task.
- **QW:** no active COM task.
- **Other apertures:** no active COM task.

## ANTI-DRIFT

Do not add protocol machinery for elegance. Do not turn green CI, repeated model conclusions or clean presentation into validation. Do not merge to main or release merely because the build is green. Do not reopen COM design unless a concrete coordination defect requires bounded repair or Mark explicitly orders it.

The practical goal is less ambiguity and less human relay burden while getting Campfire Relay into trustworthy usable shape.

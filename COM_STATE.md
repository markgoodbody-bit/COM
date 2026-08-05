# COM_STATE v0.3.2

STATUS: ACTIVE — TRACE v0.2.7 CAMPFIRE CHANNELS INTEGRATED / LOCAL INSTALL PENDING; TRACE PUBLIC FRONT-DOOR REVIEW ACTIVE

COM is a working coordination baseline, not canon, validation, consensus, or a truth oracle. Model agreement, green CI, installation, polished prose, public interest, and successful model output are not proof.

## CURRENT

- human_authority: Mark
- active_task: `COM-V032-TRACE027-CAMPFIRE-001`
- active_route: COM issue #30
- integration_owner: Framework / Build 3, session `FW-BUILD3-20260803T202518Z-6A91`
- current_product_lane: install and explicitly activate released TRACE v0.2.7 in Campfire
- profile_channel: INTEGRATED / `trace-profile-production` at `8eb0f9e8a73192f3446c05df6564b4d042c3f0d8`
- launcher_channel: INTEGRATED / `launcher-production` at `06716db65a2e85054eb71c8c84f13ad33877e3f7`
- review_task: `COM-V032-CC-REVIEW-004` — CLOSED / issue #32
- review_return: no CC-authored ACK or terminal verdict observed; unresolved coverage preserved
- local_install_gate: READY / waiting for Mark to update launcher and return Stage 1 JSON
- local_activation_gate: HELD until Stage 1 install evidence is reconciled
- provider_calls_or_spend: NONE
- concurrent_task: `TRACE-PUBLIC-FRONT-DOOR-001`
- concurrent_route: COM issue #31
- concurrent_integration_owner: Framework, session `FW-20260805-TRACE-PUBLIC-6B4E`
- concurrent_candidate: TRACE PR #31 — DRAFT / OPEN / UNMERGED
- concurrent_candidate_head: `8029adb7d3cbdb33f75638df13c1303eadadd0f4`
- concurrent_merge_gate: HELD pending CC review integration or explicit Mark override

## CONCURRENT TRACE PUBLIC FRONT-DOOR LANE

Mark asked Framework to update the main TRACE repository so interested parties can inspect it and explicitly requested COMS coordination with Claude Code.

Exact candidate:

```text
repository: markgoodbody-bit/TRACE
PR: #31
base: 6704743ef5435a65793ea35e2c92ca238cc920e1
head: 8029adb7d3cbdb33f75638df13c1303eadadd0f4
branch: framework/trace-public-front-door-001
```

Changed files:

```text
README.md
REVIEW_GUIDE.md
.github/ISSUE_TEMPLATE/trace-review.md
```

The candidate:

- rewrites the root README around the problem TRACE is attempting to solve;
- gives unfamiliar readers a five-minute, human-readable, and exact-formal entry path;
- adds conceptual, formal, operational, adversarial, and empirical review lanes;
- gives reviewers a traceable finding format and issue template;
- explains the formal-source, rendered-carrier, and external-release distinction;
- states current claim ceilings and residual limits;
- discloses that reuse and licensing terms have not yet been specified.

Candidate diff:

```text
commits: 3
files changed: 3
additions: 366
deletions: 20
```

Scope boundary:

```text
PUBLIC_FRONT_DOOR != FORMAL_REWRITE
ACCESSIBILITY != CLAIM_EXPANSION
INVITATION_TO_REVIEW != VALIDATION
REVIEW_TEMPLATE != REVIEW RESULT
```

This concurrent lane does not change the formal seed, PDF, release declaration, schema, compiler, probes, carrier build machinery, formal vocabulary, semantics, release status, authority, permission, clearance, or validation status.

CC review route: COM issue #31. Framework session `FW-20260805-TRACE-PUBLIC-6B4E` owns integration and observation for this lane only. It has no mutation authority over the Campfire local-install lane.

## RELEASED TRACE SOURCE ANCHOR

Repository: `markgoodbody-bit/TRACE`

```text
formal object: TRACE_FORMAL_SEED_v0_2_7.md
release id: TRACE-v0.2.7-FORMAL-BASELINE
released main: 084a8c2ad0f5b54212b079e1a7edd7630932f6eb
compiled source commit: 61393387d930e57450f50818151ba4a0f31023cf
formal blob: 9238986ddc18c34709906b2fc4510d827c68d2b2
formal SHA-256: de21182f42228a0104181fb24f245c652c3150853e14172c4174be4bb9ef03ab
```

State:

```text
RELEASED
ACTIVE_FORMAL_BASELINE
NOT_CANON
NOT_VALIDATED
NOT_AUTHORITY
NOT_PERMISSION
NOT_CLEARANCE
```

TRACE v0.2.7 rendered carrier work is complete and integrated on TRACE main `6704743ef5435a65793ea35e2c92ca238cc920e1`. The Markdown object remains the formal source. The Campfire integration does not depend on the PDF carrier. The public-front-door candidate does not alter either object.

## INTEGRATED PROFILE CHANNEL

PR #162: `Add released TRACE v0.2.7 as a Campfire judging profile`

```text
reviewed head: 36d412e090b09a7328c004352d0558686a4640dd
hosted CI: campfire-ci #1050 SUCCESS
merged channel commit: 8eb0f9e8a73192f3446c05df6564b4d042c3f0d8
channel: trace-profile-production
profile id: trace-formal-v0-2-7
profile version: 1.0.0
install by default: false
activate by default: false
```

The profile:

- preserves the existing ballot-first `[CAMPFIRE_JUDGE]` contract;
- changes only the TRACE analysis/judging projection;
- carries the v0.2.7 target-set-aperture repair;
- preserves action/wait/delay/inaction symmetry, TRACE type boundaries, epistemic distinctions, correction routes/clocks, future-space and residue visibility;
- includes an inspectable manual source-section map;
- explicitly states that it is not the complete formal object or an automatic compiler;
- preserves `trace-judge-v1` as an installed rollback candidate;
- does not install or activate automatically.

## INTEGRATED LAUNCHER INSTALLER

PR #163: `Launcher v0.1.7: install verified TRACE profile channels`

```text
reviewed head: 9a9d34d0f7fad0ba3767f99cabca40961c0a6e4e
hosted CI: campfire-ci #1059 SUCCESS
merged channel commit: 06716db65a2e85054eb71c8c84f13ad33877e3f7
launcher version: 0.1.7
```

The installer:

- holds an exclusive `trace-profile-install.lock` before cache or persistent-state mutation;
- fetches `trace-profile-production` into a dedicated bare cache;
- rejects a non-fast-forward rewrite from the previously accepted channel commit;
- archives the channel manifest and selected profile from one exact commit;
- fetches the TRACE source repository and exact declared source commit;
- verifies source SHA-256 `de21182f...`;
- binds port 4317 to a versioned app root under the expected Campfire directory;
- requires `/api/health.version` to match that root's `VERSION.txt`;
- dynamically imports that exact running Campfire build's `src/traceActivation.mjs`;
- reuses the running build's verified profile install lifecycle;
- installs source under persistent `PROJECT_WORKSPACE/TRACE/CURRENT`;
- installs the profile under persistent `PROJECT_WORKSPACE/TRACE_MODULES`;
- byte-compares `active.json` before and after;
- does not activate or promote;
- rolls back newly created source/profile state on ordinary late transaction failure;
- if operator activation changes `active.json` concurrently, stops and preserves verified state rather than deleting a profile that may now be active;
- appends a no-provider install audit event only on clean success.

## FAILED ATTEMPTS PRESERVED

### Lifecycle-source mismatch

Launcher head `472759a933b8c74470d82c8445afcdbadfb39154` failed `campfire-ci #1048` because the launcher checkout's older lifecycle module lacked the installed application's verified install export. The repair binds to the exact running application root.

### Stale source-contract assertion

Installer head `a6f4eaf0e5829c3d82153d3f42169fa82584a8d3` failed `campfire-ci #1058` because a source-contract test still required wording removed by the concurrency-safe implementation. Executable transaction tests passed; the stale assertion was corrected at final head `9a9d34d0...`.

No failed run was silently retried or erased.

## REVIEW BOUNDARY

CC review issue #32 was given exact anchors, a nonce-bearing execution trigger, successor-head transitions, failure evidence and a required two-target verdict.

No CC-authored ACK or terminal return was observed before bounded integration. This remains unresolved review coverage, not agreement, refusal, failure, clearance or validation. Any late material finding remains admissible evidence.

Framework independently found and repaired the lifecycle-source mismatch, concurrent-activation rollback risk, installer/cache-pin race, insufficient running-root binding and stale source-contract assertion before integration.

## LOCAL STAGE 1 — INSTALL ONLY

1. Close and reopen the Campfire Relay Launcher so the fast-forward bootstrap updates to launcher v0.1.7.
2. Run:

```powershell
$script = Join-Path $HOME 'CampfireRelay\LAUNCHER\campfire-relay\INSTALL_TRACE_PROFILE_FROM_GITHUB.ps1'
if (-not (Test-Path $script)) { throw "TRACE profile installer not found: $script" }
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$script" -JsonOnly
```

Expected boundaries:

```text
profile: trace-formal-v0-2-7
source SHA-256: de21182f42228a0104181fb24f245c652c3150853e14172c4174be4bb9ef03ab
activeRecordChanged: false
activated: false
promoted: false
providerCalls: none
```

Return the complete JSON before activation.

## LOCAL STAGE 2 — EXPLICIT ACTIVATION

After Stage 1 evidence is reconciled:

- open Campfire Setup / TRACE profiles;
- locate `Campfire TRACE v0.2.7 judging profile` / `trace-formal-v0-2-7`;
- require `INACTIVE` and `HASH VERIFIED`;
- press `Activate for test`;
- confirm current `trace-judge-v1` and new `trace-formal-v0-2-7` identities.

Activation affects future TRACE / COMPARE judging only. Historical rounds remain frozen. No provider call is required.

## EXISTING CAMPFIRE BASELINE

Campfire Relay v0.18.31 remains released, installed, healthy, provenance-bound, and rollback-ready. Its versioned application tree is unchanged. The current active TRACE profile remains v0.2.5 until Stage 2 succeeds.

## COMS

- **Mark:** human authority and active local operator for Stage 1; return the complete install JSON before activation.
- **Framework / Build 3:** profile and installer channels integrated; owns Stage 1 evidence reconciliation and Stage 2 activation verification.
- **Framework / `FW-20260805-TRACE-PUBLIC-6B4E`:** owns the concurrent TRACE public-front-door review lane only.
- **CC:** Campfire review task closed with no observed return; public-front-door review task remains separately active on issue #31; no mutation authority.
- **Other Framework sessions / Build 2 / Campfire 1 / QW / other apertures:** no mutation authority on these lanes unless separately assigned.

## BOUNDARY

Do not activate TRACE v0.2.7 before Stage 1 install evidence is reconciled.

Do not merge TRACE PR #31 merely because the prose is clearer or the repository is public.

Do not call the Campfire profile the complete TRACE source, canon, validation, authority, permission, clearance, or promotion.

Do not call the public-front-door candidate a formal repair, semantic revision, validation, endorsement, or licence grant.

Installation and activation remain separate. Activation affects future TRACE/COMPARE judging only and does not rewrite historical rounds.

No provider call is required for install or activation verification.

`TRUNCATED_RETRIEVAL != EXHAUSTIVE_ROUTE_INSPECTION`.

`The lullaby was never for the cradle`.

# COM_STATE v0.3.2

STATUS: ACTIVE — TRACE v0.2.7 CAMPFIRE PROFILE/INSTALLER REVIEW AND TRACE PUBLIC FRONT-DOOR REVIEW

COM is a working coordination baseline, not canon, validation, consensus, or a truth oracle. Model agreement, green CI, installation, polished prose, public interest, and successful model output are not proof.

## CURRENT

- human_authority: Mark
- active_task: `COM-V032-TRACE027-CAMPFIRE-001`
- active_route: COM issue #30
- review_task: `COM-V032-CC-REVIEW-004`
- review_route: COM issue #32
- integration_owner: Framework / Build 3, session `FW-BUILD3-20260803T202518Z-6A91`
- current_product_lane: plug released TRACE v0.2.7 into Campfire as a replaceable hash-bound judging profile
- profile_candidate: Campfire PR #162 — DRAFT / OPEN / MERGEABLE / UNMERGED
- installer_candidate: Campfire PR #163 — DRAFT / OPEN / MERGEABLE / UNMERGED
- merge_gate: HELD pending review integration or explicit Mark override
- local_install_gate: HELD; no Windows mutation yet
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

CC review route: COM issue #31. Framework session `FW-20260805-TRACE-PUBLIC-6B4E` owns integration and observation for this lane only. It has no mutation authority over the concurrent Campfire task.

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

## PROFILE CHANNEL CANDIDATE

PR #162: `Add released TRACE v0.2.7 as a Campfire judging profile`

```text
base channel: trace-profile-production
base: c035d5b65da804f68aad4c2def895848c66f9e2b
head: 36d412e090b09a7328c004352d0558686a4640dd
state: DRAFT / OPEN / MERGEABLE / UNMERGED
hosted CI: campfire-ci #1050 SUCCESS
changed files: 8
```

Profile identity:

```text
profile id: trace-formal-v0-2-7
profile version: 1.0.0
channel: trace-profile-production
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
- does not activate automatically.

## LAUNCHER INSTALLER CANDIDATE

PR #163: `Launcher v0.1.7: install verified TRACE profile channels`

```text
base channel: launcher-production
base: 945903b98e889a9e5712b260d32613df67191ea7
head: 9a9d34d0f7fad0ba3767f99cabca40961c0a6e4e
state: DRAFT / OPEN / MERGEABLE / UNMERGED
hosted CI: campfire-ci #1059 SUCCESS
launcher version: 0.1.7
changed files: 6
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

Launcher head `472759a933b8c74470d82c8445afcdbadfb39154` failed `campfire-ci #1048`.

Demonstrated defect:

```text
launcher checkout's older src/traceActivation.mjs
!=
installed v0.18.31 application lifecycle
```

The launcher checkout lacked `installBundledTraceProfileCandidate`. The successor binds to the actual running application root. The released v0.18.31 source commit `f88e808f13c30abdb646b14876be864db3f14293` exposes the required install function.

### Stale source-contract assertion

Installer head `a6f4eaf0e5829c3d82153d3f42169fa82584a8d3` failed `campfire-ci #1058` because a source-contract test still required wording removed by the concurrency-safe implementation. The executable transaction tests, including concurrent activation preservation, passed. The stale assertion was corrected at final head `9a9d34d0...` and CI #1059 passed.

No failed run was silently retried or erased.

## REVIEW

Campfire CC review task: COM issue #32.

Required terminal form:

```text
PROFILE: BREAK | NARROW | CLEAR WITH RESIDUAL LIMITS
INSTALLER: BREAK | NARROW | CLEAR WITH RESIDUAL LIMITS
COMBINED: HOLD | REPAIR THEN RE-ANCHOR | CLEAR FOR FRAMEWORK INTEGRATION DECISION
```

TRACE public-front-door CC review task: COM issue #31.

Required terminal form:

```text
BREAK
NARROW
CLEAR WITH RESIDUAL LIMITS
```

No CC return is yet observed on either route. Silence is not agreement or clearance. A partial or truncated retrieval is not evidence of absence.

## EXISTING CAMPFIRE BASELINE

Campfire Relay v0.18.31 remains released, installed, healthy, provenance-bound, and rollback-ready. Its versioned application tree is unchanged. The current active TRACE profile remains v0.2.5 until a later explicit local activation.

## COMS

- **Mark:** human authority; requested TRACE v0.2.7 be pluggable into Campfire and separately requested a public-facing TRACE repository update.
- **Framework / Build 3:** built the separate profile and installer channels, preserved both failed candidates, obtained exact-head hosted CI, and owns Campfire review integration.
- **Framework / `FW-20260805-TRACE-PUBLIC-6B4E`:** built TRACE PR #31 and owns public-front-door review integration only.
- **CC:** active read-only reviewer on COM issues #31 and #32; no mutation authority.
- **Other Framework sessions / Build 2 / Campfire 1 / QW / other apertures:** no mutation authority on these lanes unless separately assigned.

## BOUNDARY

Do not merge Campfire PR #162 or #163, install locally, or activate TRACE v0.2.7 merely because CI is green.

Do not merge TRACE PR #31 merely because the prose is clearer or the repository is public.

Do not call the Campfire profile the complete TRACE source, canon, validation, authority, permission, clearance, or promotion.

Do not call the public-front-door candidate a formal repair, semantic revision, validation, endorsement, or licence grant.

Installation and activation remain separate. Activation, when later authorized, affects future TRACE/COMPARE judging only and does not rewrite historical rounds.

No provider call is required for install or activation verification.

`TRUNCATED_RETRIEVAL != EXHAUSTIVE_ROUTE_INSPECTION`.

`The lullaby was never for the cradle`.

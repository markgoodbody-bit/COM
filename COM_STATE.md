# COM_STATE v0.3.2

STATUS: ACTIVE — TRACE v0.2.7 CAMPFIRE PROFILE AND VERIFIED INSTALLER UNDER REVIEW

COM is a working coordination baseline, not canon, validation, consensus, or a truth oracle. Model agreement, green CI, installation, and successful model output are not proof.

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

TRACE v0.2.7 rendered carrier work is complete and integrated on TRACE main `6704743ef5435a65793ea35e2c92ca238cc920e1`. The Markdown object remains the formal source. The Campfire integration does not depend on the PDF carrier.

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
head: dbc6469fbc20b35638922a9d622d6c98f62d8128
state: DRAFT / OPEN / MERGEABLE / UNMERGED
hosted CI: campfire-ci #1054 SUCCESS
launcher version: 0.1.7
```

The installer:

- fetches `trace-profile-production` into a dedicated bare cache;
- rejects a non-fast-forward rewrite from the previously accepted channel commit;
- archives the channel manifest and selected profile from one exact commit;
- fetches the TRACE source repository and exact declared source commit;
- verifies source SHA-256 `de21182f...`;
- binds the process on port 4317 to its `/api/self-test.runtimePaths.appRoot`;
- dynamically imports that exact installed Campfire build's `src/traceActivation.mjs`;
- reuses the running build's verified profile install lifecycle;
- installs source under persistent `PROJECT_WORKSPACE/TRACE/CURRENT`;
- installs the profile under persistent `PROJECT_WORKSPACE/TRACE_MODULES`;
- byte-compares `active.json` before and after;
- does not activate or promote;
- rolls back newly created source/profile state on late transaction failure;
- appends a no-provider install audit event.

## FAILED ATTEMPT PRESERVED

Launcher head `472759a933b8c74470d82c8445afcdbadfb39154` failed `campfire-ci #1048`.

Demonstrated defect:

```text
launcher checkout's older src/traceActivation.mjs
!=
installed v0.18.31 application lifecycle
```

The launcher checkout lacked `installBundledTraceProfileCandidate`. The successor binds to the actual running application root. The released v0.18.31 source commit `f88e808f13c30abdb646b14876be864db3f14293` exposes the required install function. The failed run remains evidence; it was not silently retried.

## REVIEW

CC review task: COM issue #32.

Required terminal form:

```text
PROFILE: BREAK | NARROW | CLEAR WITH RESIDUAL LIMITS
INSTALLER: BREAK | NARROW | CLEAR WITH RESIDUAL LIMITS
COMBINED: HOLD | REPAIR THEN RE-ANCHOR | CLEAR FOR FRAMEWORK INTEGRATION DECISION
```

No CC return is yet observed. Silence is not agreement or clearance.

## EXISTING CAMPFIRE BASELINE

Campfire Relay v0.18.31 remains released, installed, healthy, provenance-bound, and rollback-ready. Its versioned application tree is unchanged. The current active TRACE profile remains v0.2.5 until a later explicit local activation.

## COMS

- **Mark:** human authority; requested TRACE v0.2.7 be pluggable into Campfire.
- **Framework / Build 3:** built the separate profile and installer channels, preserved the failed candidate, obtained exact-head hosted CI, and owns review integration.
- **CC:** active read-only review on issue #32; no mutation authority.
- **Other Framework session:** TRACE v0.2.7 rendered-carrier lane complete; no active mutation authority on this task.
- **Build 2 / Campfire 1 / QW / other apertures:** no active task.

## BOUNDARY

Do not merge PR #162 or #163, install locally, or activate TRACE v0.2.7 merely because CI is green.

Do not call the Campfire profile the complete TRACE source, canon, validation, authority, permission, clearance, or promotion.

Installation and activation remain separate. Activation, when later authorized, affects future TRACE/COMPARE judging only and does not rewrite historical rounds.

No provider call is required for install or activation verification.

`The lullaby was never for the cradle`.

# COM_STATE v0.3.2

STATUS: ACTIVE — CAMPFIRE TRACE v0.2.7 LOCAL INSTALL PENDING; TRACE PUBLIC FRONT DOOR INTEGRATED

COM is a working coordination baseline, not canon, validation, consensus, or a truth oracle. Model agreement, green CI, installation, polished prose, public interest, and successful model output are not proof.

## CURRENT

- human_authority: Mark
- active_task: `COM-V032-TRACE027-CAMPFIRE-001`
- active_route: COM issue #30
- integration_owner: Framework / Build 3, session `FW-BUILD3-20260803T202518Z-6A91`
- current_product_lane: install and explicitly activate released TRACE v0.2.7 in Campfire
- profile_channel: INTEGRATED / `trace-profile-production` at `8eb0f9e8a73192f3446c05df6564b4d042c3f0d8`
- launcher_channel: INTEGRATED / `launcher-production` at `06716db65a2e85054eb71c8c84f13ad33877e3f7`
- local_install_gate: READY / waiting for Mark to update launcher and return Stage 1 JSON
- local_activation_gate: HELD until Stage 1 install evidence is reconciled
- provider_calls_or_spend: NONE
- completed_task: `TRACE-PUBLIC-FRONT-DOOR-001`
- completed_route: COM issue #31
- completed_integration_owner: Framework, session `FW-20260805-TRACE-PUBLIC-6B4E`
- TRACE_public_front_door: INTEGRATED / TRACE PR #31
- current_TRACE_main: `f21408c517dcd5ef1c360d9f5fb8666d9d4dd6cf`
- public_front_door_CC_return: NOT OBSERVED BEFORE HUMAN WAIT OVERRIDE
- late_public_front_door_CC_return: ADMISSIBLE / NON-GATING

## RELEASED TRACE SOURCE ANCHOR

Repository: `markgoodbody-bit/TRACE`

```text
formal object: TRACE_FORMAL_SEED_v0_2_7.md
release id: TRACE-v0.2.7-FORMAL-BASELINE
released baseline commit: 084a8c2ad0f5b54212b079e1a7edd7630932f6eb
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

The public-front-door integration did not alter the formal source, rendered carrier, release declaration, schema, compiler, probes, carrier machinery, formal vocabulary, semantics, release status, authority, permission, clearance, validation status, or licensing status.

## TRACE PUBLIC FRONT DOOR — INTEGRATED

TRACE PR #31: `Build a public front door for external TRACE review`

```text
base: 6704743ef5435a65793ea35e2c92ca238cc920e1
reviewed head: 8029adb7d3cbdb33f75638df13c1303eadadd0f4
merge commit: f21408c517dcd5ef1c360d9f5fb8666d9d4dd6cf
changed files: 3
```

Changed files:

```text
README.md
REVIEW_GUIDE.md
.github/ISSUE_TEMPLATE/trace-review.md
```

The integrated front door:

- explains the problem before repository machinery;
- gives five-minute, human-readable, and exact-formal reading paths;
- distinguishes the released Markdown formal source from the rendered PDF carrier and release declaration;
- states current claim ceilings and residual limits;
- adds conceptual, formal, operational, adversarial, and empirical review lanes;
- asks reviewers to separate fact from inference and provide exact evidence, failure mode, containment, repair, and gate effect;
- provides a structured GitHub issue template for external findings;
- discloses that reuse and licensing terms have not yet been specified.

Scope boundary:

```text
PUBLIC_FRONT_DOOR != FORMAL_REWRITE
ACCESSIBILITY != CLAIM_EXPANSION
INVITATION_TO_REVIEW != VALIDATION
REVIEW_TEMPLATE != REVIEW RESULT
PUBLIC_VISIBILITY != LICENCE_GRANT
```

### Review provenance

A fresh exact-head Claude Code review was dispatched through COM issue #31. The complete route contained only Framework messages before Mark instructed:

```text
COMS and proceed
```

Framework integrated that instruction as:

```text
HUMAN_WAIT_OVERRIDE_RECEIVED
CC_CLEARANCE_NOT_INFERRED
CC_AGREEMENT_NOT_INFERRED
CC_REFUSAL_NOT_INFERRED
LATE_CC_RETURN_REMAINS_ADMISSIBLE
```

Framework completed its own exact-head review and found no blocker. No CI workflow was attached to the documentation-only change. The absence of a CC return is preserved as unresolved review coverage, not clearance or agreement.

## CURRENT RENDERED CARRIER

```text
path: TRACE.pdf
SHA-256: 8cf8233442f034d2495268fb33dfe741ad360260a61b84afab14301c675fbbc6
Git blob: c74d2dafe7870eab1b6a039cecb93d24d5c26ead
size: 313450 bytes
pages: 75
geometry: all A4
```

Carrier state:

```text
CURRENT_RENDERED_CARRIER
NOT_FORMAL_SOURCE
NOT_CANON
NOT_VALIDATED
NOT_AUTHORITY
NOT_PERMISSION
NOT_CLEARANCE
```

## CAMPFIRE TRACE v0.2.7 CHANNELS — INTEGRATED

Profile channel:

```text
PR #162
merged channel commit: 8eb0f9e8a73192f3446c05df6564b4d042c3f0d8
channel: trace-profile-production
profile id: trace-formal-v0-2-7
profile version: 1.0.0
install by default: false
activate by default: false
```

Launcher channel:

```text
PR #163
merged channel commit: 06716db65a2e85054eb71c8c84f13ad33877e3f7
launcher version: 0.1.7
```

The installer verifies the released TRACE source identity, installs the source and profile into persistent workspace locations, does not activate or promote, preserves `active.json`, and emits no provider call.

No CC-authored ACK or terminal return was observed on the Campfire review route before bounded integration. That remains unresolved coverage; any late material finding remains admissible evidence.

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

## COMS

- **Mark:** human authority and active local operator for Campfire Stage 1; authorized the TRACE public-front-door integration through `COMS and proceed`.
- **Framework / Build 3:** owns Campfire Stage 1 evidence reconciliation and Stage 2 activation verification.
- **Framework / `FW-20260805-TRACE-PUBLIC-6B4E`:** completed and integrated TRACE PR #31; owns assessment of any late public-front-door CC return.
- **CC:** no public-front-door terminal return observed before human override; no clearance inferred; late material evidence remains admissible.
- **Other Framework sessions / Build 2 / Campfire 1 / QW / other apertures:** no mutation authority on active lanes unless separately assigned.

## BOUNDARY

Do not activate TRACE v0.2.7 in Campfire before Stage 1 install evidence is reconciled.

Do not call the Campfire profile the complete TRACE source, canon, validation, authority, permission, clearance, or promotion.

Do not call the public front door a formal repair, semantic revision, validation, endorsement, or licence grant.

Do not infer CC review, agreement, refusal, or clearance from silence or human override.

Installation and activation remain separate. Activation affects future TRACE/COMPARE judging only and does not rewrite historical rounds.

`TRUNCATED_RETRIEVAL != EXHAUSTIVE_ROUTE_INSPECTION`.

`The lullaby was never for the cradle`.

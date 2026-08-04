# COM_STATE v0.3.2

STATUS: ACTIVE — CAMPFIRE RELAY v0.18.31 RUNNING ON WINDOWS PRODUCTION / ACTIVATION VERIFICATION INCOMPLETE

COM is a working coordination baseline, not canon, validation, consensus, or a truth oracle. Model agreement and green CI are not proof.

## CURRENT

- human_authority: Mark
- active_task: `COM-V032-PRODUCTION-ACTIVATE-001`
- active_task_route: COM issue #22
- task_status: OPEN / ACTIVATED / VERIFICATION INCOMPLETE
- addressed_to: Mark
- integration_and_observation_owner: Framework / Build 3, session `FW-BUILD3-20260803T202518Z-6A91`
- current_product_lane: Campfire Relay v0.18.31 released and locally running maintenance baseline
- provider_calls_or_spend: live diagnostic probes occurred after activation; Campfire-recorded diagnostic delta approximately £0.0025

## RELEASED TARGET

Repository: `markgoodbody-bit/campfire-relay`

- application: `0.18.31`
- model catalogue: `2026.08.03.1`
- packaged source commit: `f88e808f13c30abdb646b14876be864db3f14293`
- packaged source tree: `6fbfe992ee4b8e04defecdf57c4de0dd53fd121c`
- trusted release-record main commit: `c035d5b65da804f68aad4c2def895848c66f9e2b`
- production tag: `campfire-production-v0.18.31`
- package SHA-256: `70e423075b101905aa65da1277da2799eff7028cddacc67169a27fdc6ec97bd4`
- release-content-manifest SHA-256: `094dfeeb0f5442933cd6b2e682475c7cd00b08dc392f37d6f69a244658dadd12`
- catalogue-manifest SHA-256: `f1fce253299da622e54df571b1551a56a353ef1b51c8014d5836a257c6086eaf`

## LOCAL WINDOWS EVIDENCE — 2026-08-04

Returned diagnostic confirms:

- origin `http://127.0.0.1:4317`;
- browser pre-run and post-run `/api/health`: HTTP 200;
- app version: `0.18.31`;
- runtime app root: `~/CampfireRelay/CAMPFIRE_RELAY_v0_18_31`;
- platform: Windows x64;
- model configuration: 10 records loaded;
- persistent data/workspace/TRACE paths resolve outside the versioned app root;
- ledger integrity: 83/83 files, 1627 lines, malformed 0, duplicate event ids 0, duplicate terminal ids 0, cost history complete;
- all eight requested live provider probes passed.

Decision: Windows Production v0.18.31 is running. This is functional activation evidence, not complete transaction/provenance evidence.

## OPEN DEFECT / EVIDENCE GAP

`CR-V01831-INSTALLED-PROVENANCE-MISSING-001`

The installed diagnostic reports:

- provenance state unavailable;
- source commit not recorded;
- source tree not recorded;
- installed package SHA-256 not recorded;
- installed-at timestamp not recorded;
- launcher current target not recorded;
- launcher rollback target not recorded;
- shipped build verification report missing.

Do not infer exact installed package provenance merely from version and directory name.

## REQUIRED CLOSURE EVIDENCE

Still required from the Windows machine:

1. latest line from `~/CampfireRelay/STATE/release-update-audit.jsonl`;
2. versioned directories matching `~/CampfireRelay/CAMPFIRE_RELAY_v*`;
3. whether `~/CampfireRelay/START_PREVIOUS_CAMPFIRE.ps1` exists;
4. plain `/api/health` JSON from `http://127.0.0.1:4317/api/health`.

Do not run another live-provider diagnostic. No manual overwrite, delete or rename.

## BUDGET STATE

Current handoff generated 2026-08-04 records:

- Money Guard per-round limit: £1.00;
- rolling 24h limit: £5.00;
- rolling 24h headroom: £4.02;
- recorded 24h spend: £0.980, history complete;
- recorded all-time spend: £5.28, history complete;
- known provider credit/snapshots: £59.31 across eight providers;
- unknown pricing blocked: yes.

Price cards are planning evidence, not invoices; use exact Seed Estimate before dispatch.

## REVIEW RECORD

- CC first returned `NARROW` and exposed `CR-V01831-RUNTIME-CATALOG-AUTHORITY-002`.
- Defects 001 and 002 were repaired before release.
- CC's broader Q2-Q7 / repair-successor return was not observed before publication; unresolved coverage remains recorded as uncertainty.
- Previous task `COM-V032-CC-REVIEW-002` is closed on issue #20.

## COMS

- **Mark:** local operator and human authority; return the four bounded closure items above.
- **Framework / Build 3:** confirmed functional Windows activation; owns evidence integration and issue #22 closure decision.
- **CC:** no active task or mutation authority.
- **Build 2 / Campfire 1 / QW / other apertures:** no active COM task.

## ANTI-DRIFT

Do not begin v0.19/Exchange or another catalogue refresh. Do not run paid providers merely to prove installation. Close the activation evidence gap first.

`The lullaby was never for the cradle`.

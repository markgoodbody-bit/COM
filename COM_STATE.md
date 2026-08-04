# COM_STATE v0.3.2

STATUS: STABLE — CAMPFIRE RELAY v0.18.31 RELEASED, INSTALLED, PROVENANCE-BOUND AND ROLLBACK-READY

COM is a working coordination baseline, not canon, validation, consensus, or a truth oracle. Model agreement and green CI are not proof.

## CURRENT

- human_authority: Mark
- active_task: NONE
- integration_owner: Framework / Build 3, session `FW-BUILD3-20260803T202518Z-6A91`
- current_product_lane: Campfire Relay v0.18.31 stable maintenance baseline
- Windows Production activation task: `COM-V032-PRODUCTION-ACTIVATE-001` — COMPLETE / issue #22 closed
- installed-provenance defect: `CR-V01831-INSTALLED-PROVENANCE-MISSING-001` — REPAIRED FOR INSTALLED v0.18.31
- launcher: v0.1.6 on trusted `launcher-production` channel
- next_action: NONE ASSIGNED; await Mark's explicit direction

## RELEASED AND INSTALLED TARGET

Repository: `markgoodbody-bit/campfire-relay`

- application: `0.18.31`
- model catalogue: `2026.08.03.1`
- production tag: `campfire-production-v0.18.31`
- release/tag commit: `c035d5b65da804f68aad4c2def895848c66f9e2b`
- packaged source commit: `f88e808f13c30abdb646b14876be864db3f14293`
- packaged source tree: `6fbfe992ee4b8e04defecdf57c4de0dd53fd121c`
- package SHA-256: `70e423075b101905aa65da1277da2799eff7028cddacc67169a27fdc6ec97bd4`
- release-content-manifest SHA-256: `094dfeeb0f5442933cd6b2e682475c7cd00b08dc392f37d6f69a244658dadd12`
- catalogue-manifest SHA-256: `f1fce253299da622e54df571b1551a56a353ef1b51c8014d5836a257c6086eaf`

## WINDOWS PRODUCTION EVIDENCE

Observed from launcher v0.1.6 reconciliation output on 2026-08-04:

- reconciliation status: `provenance_reconciled`
- health: `ok=true`, name `Campfire Relay`, version `0.18.31`
- health timestamp: `2026-08-04T16:01:44.276Z`
- runtime root: `C:\Users\markg\CampfireRelay\CAMPFIRE_RELAY_v0_18_31`
- persistent provenance: `C:\Users\markg\CampfireRelay\STATE\data\install-provenance.json`
- recorded `installedAt`: `2026-08-04T16:01:44.7395462Z`
- timestamp boundary: this value was established by provenance reconciliation because no earlier exact package record existed; it is not proof of the original activation time
- current target: `CAMPFIRE_RELAY_v0_18_31`
- rollback target: `CAMPFIRE_RELAY_v0_18_3`
- `START_PREVIOUS_CAMPFIRE.ps1` exists: true
- audit timestamp: `2026-08-04T16:01:44.7637072Z`
- audit result: `provenance-reconciled`
- reconciliation: `trusted-github-release`
- local self-test: `completed-without-live-provider-probes`
- reconciliation provider calls: none

The local source commit, tree, package SHA, tag commit and release ref exactly matched the immutable Production release manifest.

Preserved Production directories observed:

- `CAMPFIRE_RELAY_v0_18_31`
- `CAMPFIRE_RELAY_v0_18_3`
- `CAMPFIRE_RELAY_v0_18_2_1`
- `CAMPFIRE_RELAY_v0_18_2`
- `CAMPFIRE_RELAY_v0_18_1`
- `CAMPFIRE_RELAY_v0_18_0`
- `CAMPFIRE_RELAY_v0_17_9`
- `CAMPFIRE_RELAY_v0_17_8`
- `CAMPFIRE_RELAY_v0_17_7`

## LAUNCHER REPAIR RECORD

PR #161: `Launcher v0.1.6: reconcile installed Production provenance`

- exact reviewed head: `4d15864b5c8c16dc0df22054676817542584066e`
- launcher-production merge commit: `945903b98e889a9e5712b260d32613df67191ea7`
- hosted CI: campfire-ci #1044 — SUCCESS
- application v0.18.31, immutable tag and published release: unchanged

The launcher recovery path authenticates the current Production tag, proves the fetched object equals the pinned tag commit, reads the canonical manifest from that exact commit, binds package identity to trusted discovery, binds the process on port 4317 to the selected application root, validates the actual rollback pointer, writes install provenance atomically and appends a no-provider audit event.

## SPEND AND REVIEW BOUNDARIES

- successful provenance reconciliation made no live provider calls;
- the earlier full diagnostic's approximately £0.0025 provider-probe delta remains preserved as a separate historical fact;
- CC review task `COM-V032-CC-REVIEW-003` was requested with explicit nonce and exact-head transitions;
- no CC-authored ACK or terminal verdict was observed before bounded integration;
- this remains unresolved review coverage, not agreement, refusal, failure, clearance or validation.

## COMS

- **Mark:** human authority; no active local task.
- **Framework / Build 3:** v0.18.31 release, Windows activation and installed-provenance reconciliation closed.
- **CC:** no active task or mutation authority.
- **Build 2 / Campfire 1 / QW / other apertures:** no active COM task.

## BOUNDARY

Do not infer general product validation from release, CI, installation or provenance closure. Do not begin v0.19/Exchange, another model-catalogue refresh or paid-provider work without new explicit authority.

`The lullaby was never for the cradle`.

# COM_STATE v0.3.2

STATUS: ACTIVE — CAMPFIRE RELAY v0.18.31 RUNNING / INSTALLED-PROVENANCE REPAIR UNDER REVIEW

COM is a working coordination baseline, not canon, validation, consensus, or a truth oracle. Model agreement and green CI are not proof.

## CURRENT

- human_authority: Mark
- primary_task: `COM-V032-PRODUCTION-ACTIVATE-001`
- primary_route: COM issue #22
- primary_status: OPEN / FUNCTIONALLY ACTIVATED / TRANSACTION-PROVENANCE INCOMPLETE
- review_subtask: `COM-V032-CC-REVIEW-003`
- review_route: COM issue #23
- review_status: OPEN / AWAITING CC HELLO-ACK + TERMINAL VERDICT
- integration_owner: Framework / Build 3, session `FW-BUILD3-20260803T202518Z-6A91`
- current_product_lane: Campfire Relay v0.18.31 released and running; launcher v0.1.6 provenance recovery candidate
- next_action: finish independent review of PR #161, integrate only if clear or narrowly repaired, then use the trusted launcher recovery tool locally and close issue #22 from returned no-provider evidence

## RELEASED AND RUNNING TARGET

Repository: `markgoodbody-bit/campfire-relay`

- application: `0.18.31`
- model catalogue: `2026.08.03.1`
- packaged source commit: `f88e808f13c30abdb646b14876be864db3f14293`
- packaged source tree: `6fbfe992ee4b8e04defecdf57c4de0dd53fd121c`
- release-record main commit: `c035d5b65da804f68aad4c2def895848c66f9e2b`
- production tag: `campfire-production-v0.18.31`
- package SHA-256: `70e423075b101905aa65da1277da2799eff7028cddacc67169a27fdc6ec97bd4`
- Windows origin: `http://127.0.0.1:4317`
- observed app version: `0.18.31`
- observed runtime root: `~/CampfireRelay/CAMPFIRE_RELAY_v0_18_31`
- observed ledger integrity: 83/83 files, 1627 lines, malformed 0, duplicate event ids 0, duplicate terminal ids 0, cost history complete

The returned diagnostic ran eight live provider probes and recorded approximately £0.0025. No further provider call is required or authorized for this repair.

## DEFECT

`CR-V01831-INSTALLED-PROVENANCE-MISSING-001`

Confirmed root cause:

1. the v0.18.31 Production ZIP was created with raw `git archive`;
2. the source runtime only persists exact installed identity when local/package provenance metadata exists;
3. the release builder did not inject that metadata;
4. the installed diagnostic therefore reports source commit, source tree, package SHA, installed-at and launcher targets as unavailable.

The version and directory name alone do not prove exact installed package identity.

## REPAIR CANDIDATE

PR #161: `Launcher v0.1.6: reconcile installed Production provenance`

- base: `launcher-production`
- exact base: `03f7346cb968bd4e02102bcced6fe0af9d88230c`
- exact head: `25e65e398ed386c45bb75e2dac964ed51449f839`
- changed files: exactly 3
  - `LAUNCHER_VERSION.txt`
  - `RECONCILE_CAMPFIRE_PROVENANCE_FROM_GITHUB.ps1`
  - `test/releaseProvenanceReconciliation.test.mjs`
- hosted CI: campfire-ci #1040 — SUCCESS
- PR state: DRAFT / OPEN / MERGEABLE / NOT MERGED

The candidate:

- authenticates and pins the current stable Production tag through the existing release channel;
- requires installed Production to be up to date with that exact release;
- reads the canonical release manifest from the just-fetched `FETCH_HEAD`;
- verifies source commit, source tree, package SHA and tag commit shapes;
- verifies health name/version;
- uses the free local `/api/self-test` runtime path to bind the port-4317 process to the selected app directory;
- derives rollback identity from the actual `START_PREVIOUS_CAMPFIRE.ps1` pointer;
- refuses an outside-root, invalid or missing-directory rollback target;
- atomically writes `STATE/data/install-provenance.json`;
- appends a `provenance-reconciled` audit event;
- performs no live provider calls.

## CC REVIEW

Task: `COM-V032-CC-REVIEW-003`, issue #23.

- exact review head: `25e65e398ed386c45bb75e2dac964ed51449f839`
- nonce: `FW3-CC-PROV-25E65E-0956`
- mutation authority: NONE
- required verdict: BREAK / NARROW / CLEAR FOR FRAMEWORK INTEGRATION DECISION
- current observation: no CC-authored ACK or verdict yet observed

Silence is not agreement and green CI is not validation.

## COMS

- **Mark:** human authority; no local action required until launcher repair integration is complete.
- **Framework / Build 3:** owns PR #161 integration, COM issues #22/#23 and final local-evidence reconciliation.
- **CC:** active read-only review task on issue #23; no mutation authority.
- **Build 2 / Campfire 1 / QW / other apertures:** no active task.

## BOUNDARY

Do not begin v0.19/Exchange or another model-catalogue refresh. Do not rerun live-provider diagnostics. Do not manually fabricate or edit installed provenance. Production v0.18.31 remains running while the launcher repair is reviewed.

`The lullaby was never for the cradle`.

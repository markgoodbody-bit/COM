# COM_STATE v0.3.2

STATUS: ACTIVE — CAMPFIRE RELAY v0.18.31 RUNNING / LAUNCHER v0.1.6 PROVENANCE RECOVERY READY

COM is a working coordination baseline, not canon, validation, consensus, or a truth oracle. Model agreement and green CI are not proof.

## CURRENT

- human_authority: Mark
- active_task: `COM-V032-PRODUCTION-ACTIVATE-001`
- active_route: COM issue #22
- task_status: OPEN / FUNCTIONALLY ACTIVATED / LOCAL PROVENANCE RECONCILIATION READY
- integration_owner: Framework / Build 3, session `FW-BUILD3-20260803T202518Z-6A91`
- current_product_lane: Campfire Relay v0.18.31 released and running; launcher v0.1.6 integrated
- next_action: update the installed launcher to v0.1.6, run the no-provider provenance reconciliation tool, and return its complete JSON output

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

The returned full diagnostic ran eight live provider probes and recorded approximately £0.0025. No further provider call is required or authorized for this repair.

## DEFECT

`CR-V01831-INSTALLED-PROVENANCE-MISSING-001`

Confirmed root cause:

1. the v0.18.31 Production ZIP was created with raw `git archive`;
2. the runtime persists exact installed identity only when local/package provenance metadata exists;
3. the release package did not contain that metadata;
4. the installed diagnostic therefore could not attest source commit, source tree, package SHA, installed-at timestamp or launcher targets.

The version and directory name alone are not exact package provenance.

## INTEGRATED REPAIR

PR #161: `Launcher v0.1.6: reconcile installed Production provenance`

- base: `launcher-production` at `03f7346cb968bd4e02102bcced6fe0af9d88230c`
- exact reviewed head: `4d15864b5c8c16dc0df22054676817542584066e`
- merge commit: `945903b98e889a9e5712b260d32613df67191ea7`
- launcher version: `0.1.6`
- changed files: exactly 3
- hosted CI: campfire-ci #1044 — SUCCESS
- state: MERGED INTO TRUSTED LAUNCHER CHANNEL

The recovery tool:

- authenticates and pins the current stable Production tag through the existing release channel;
- requires installed Production to be up to date with that exact release;
- proves `FETCH_HEAD^{commit}` equals the authenticated tag commit;
- reads the manifest from the exact authenticated commit and canonical path;
- binds package SHA to trusted discovery;
- verifies health name/version and binds the port-4317 process root through the free local `/api/self-test`;
- reads the actual rollback target from `START_PREVIOUS_CAMPFIRE.ps1`;
- refuses an outside-root, invalid or missing rollback directory;
- atomically writes `STATE/data/install-provenance.json`;
- appends a `provenance-reconciled` audit event;
- performs no live provider calls.

## REVIEW BOUNDARY

CC review task `COM-V032-CC-REVIEW-003` on issue #23 is closed after bounded integration.

- nonce-bearing request was persisted;
- no CC-authored ACK or terminal verdict was observed;
- this remains unresolved review coverage, not agreement, refusal, failure, clearance or validation.

Framework's own hostile pass found and repaired four material weaknesses before integration: running-root binding, actual rollback-pointer binding, mutable fetched-object binding, and the PowerShell literal-`$previous` parser defect.

## LOCAL EXECUTION

1. Open the Campfire Relay Launcher.
2. Press `CHECK GITHUB`.
3. Apply the launcher update to `0.1.6` and allow restart.
4. Run in PowerShell:

```powershell
$script = Join-Path $HOME 'CampfireRelay\LAUNCHER\campfire-relay\RECONCILE_CAMPFIRE_PROVENANCE_FROM_GITHUB.ps1'
if (-not (Test-Path $script)) { throw "Reconciliation tool not found: $script" }
& $script -JsonOnly
```

Return the complete JSON output. Do not edit provenance manually and do not rerun the full live-provider diagnostic.

## COMS

- **Mark:** active local operator and human authority; run the bounded reconciliation and return JSON.
- **Framework / Build 3:** launcher repair integrated; owns issue #22 evidence reconciliation and closure decision.
- **CC:** review task closed with no observed return; no mutation authority.
- **Build 2 / Campfire 1 / QW / other apertures:** no active task.

## BOUNDARY

Production v0.18.31 remains running. Do not begin v0.19/Exchange or another catalogue refresh. Do not call providers to prove installation. Do not manually fabricate installed provenance.

`The lullaby was never for the cradle`.

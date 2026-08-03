# COM_STATE v0.3.2

STATUS: ACTIVE — CAMPFIRE RELAY v0.18.31 RELEASED / WINDOWS PRODUCTION ACTIVATION READY

COM is a working coordination baseline, not canon, validation, consensus, or a truth oracle. Model agreement and green CI are not proof.

## CURRENT

- human_authority: Mark
- active_task: `COM-V032-PRODUCTION-ACTIVATE-001`
- active_task_route: COM issue #22
- task_status: READY / WAITING FOR LOCAL OPERATOR CONFIRMATION
- addressed_to: Mark
- local_operator: Mark
- integration_and_observation_owner: Framework / Build 3, session `FW-BUILD3-20260803T202518Z-6A91`
- authority_source: Mark's 2026-08-03 instruction — `COMS and proceed and very good`
- current_product_lane: Campfire Relay v0.18.31 released maintenance baseline
- next_action: use the installed Campfire Launcher to check the trusted GitHub Production channel, review the verified v0.18.31 offer, and authorize the local commit point only if the isolated no-paid-provider health gate passes and rollback is preserved
- provider_calls_or_spend: NONE AUTHORIZED

## RELEASED TARGET

Repository: `markgoodbody-bit/campfire-relay`

- application version: `0.18.31`
- model catalogue: `2026.08.03.1`
- packaged source commit: `f88e808f13c30abdb646b14876be864db3f14293`
- packaged source tree: `6fbfe992ee4b8e04defecdf57c4de0dd53fd121c`
- trusted release-record main commit: `c035d5b65da804f68aad4c2def895848c66f9e2b`
- production tag: `campfire-production-v0.18.31`
- package SHA-256: `70e423075b101905aa65da1277da2799eff7028cddacc67169a27fdc6ec97bd4`
- release-content-manifest SHA-256: `094dfeeb0f5442933cd6b2e682475c7cd00b08dc392f37d6f69a244658dadd12`
- catalogue-manifest SHA-256: `f1fce253299da622e54df571b1551a56a353ef1b51c8014d5836a257c6086eaf`
- published GitHub release: non-draft / non-prerelease

## ACTIVATION READINESS

Repository-side inspection confirms the existing `launcher-production` channel requires no v0.18.31-specific patch:

1. stable tag discovery accepts `campfire-production-v0.18.31`;
2. stable semantic-version comparison accepts `0.18.31` and refuses downgrade or same-version replacement;
3. canonical release paths resolve under `releases/0.18.31/`;
4. tag movement is pinned and refused;
5. package, content manifest, release notes and seed guide are hash-verified;
6. the complete staged tree is verified before activation;
7. an isolated local health gate runs with paid provider calls forbidden;
8. persistent STATE, PROJECT_WORKSPACE, TRACE_MODULES, credentials and accounting are required to remain preserved;
9. the current Production build and rollback launcher are written before the commit point;
10. failed post-activation health triggers quarantine and attempted rollback.

## REQUIRED LOCAL RETURN

Success requires evidence from the Windows machine:

```text
health.name == "Campfire Relay"
health.version == "0.18.31"
audit.result == "success"
previous build preserved == true
START_PREVIOUS_CAMPFIRE.ps1 exists == true
paid provider calls == none
```

Return:

- the `/api/health` result from `http://127.0.0.1:4317/api/health`;
- the latest `STATE/release-update-audit.jsonl` event;
- the preserved previous Production version/build directory;
- any exact activation or rollback error if success is not reached.

Do not manually overwrite, delete or rename Production directories to force success.

## REVIEW RECORD

- CC's first v0.18.31 verdict was `NARROW` and materially exposed `CR-V01831-RUNTIME-CATALOG-AUTHORITY-002`.
- Defects 001 and 002 were repaired before release.
- CC's broader Q2-Q7 / repair-successor return was not observed before publication; that remains unresolved review coverage, not agreement, refusal, failure, or validation.
- Previous task `COM-V032-CC-REVIEW-002` is closed on issue #20.

## PRODUCTION BOUNDARY

Confirmed:

- main integration: COMPLETE
- trusted release record: COMPLETE
- immutable production tag: COMPLETE
- GitHub release publication: COMPLETE
- repository-side launcher compatibility: CONFIRMED

Not yet observed:

- local Windows activation at `127.0.0.1:4317`
- installed version `0.18.31`
- local no-paid-provider health result
- rollback-path evidence on the installed machine

Released and activation-ready do not mean installed.

## COMS

- **Mark:** active local operator and human authority for task `COM-V032-PRODUCTION-ACTIVATE-001`.
- **Framework / Build 3:** repository readiness confirmed; observing issue #22 and integrating returned local evidence.
- **CC:** no active task or mutation authority.
- **Build 2 / Campfire 1 / QW / other apertures:** no active COM task.

## ANTI-DRIFT

Do not begin v0.19/Exchange or another catalogue refresh. Do not run paid providers merely to prove installation. Complete the bounded local Production activation and preserve failure evidence if the gate stops.

`The lullaby was never for the cradle`.

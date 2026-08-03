# COM_STATE v0.3.2

STATUS: STABLE — CAMPFIRE RELAY v0.18.31 RELEASED / WINDOWS PRODUCTION ACTIVATION NOT OBSERVED

COM is a working coordination baseline, not canon, validation, consensus, or a truth oracle. Model agreement and green CI are not proof.

## CURRENT

- human_authority: Mark
- active_task: NONE
- last_task: `COM-V032-CC-REVIEW-002`
- last_task_route: COM issue #20
- last_task_status: CLOSED / COMPLETED
- integration_owner: Framework / Build 3, session `FW-BUILD3-20260803T202518Z-6A91`
- independent_reviewer: CC, session `CC-20260803T2205+0100-9E4C`
- current_product_lane: Campfire Relay v0.18.31 released maintenance baseline
- next_product_action: Windows Production upgrade only under Mark's direct authority and with rollback + local version/smoke verification
- provider_calls_or_spend: NONE

## RELEASED IDENTITY

Repository: `markgoodbody-bit/campfire-relay`

- application version: `0.18.31`
- model catalogue: `2026.08.03.1`
- packaged source commit: `f88e808f13c30abdb646b14876be864db3f14293`
- packaged source tree: `6fbfe992ee4b8e04defecdf57c4de0dd53fd121c`
- trusted release-record main commit: `c035d5b65da804f68aad4c2def895848c66f9e2b`
- production tag: `campfire-production-v0.18.31`
- GitHub release: `Campfire Relay v0.18.31`
- published at: `2026-08-03T21:37:05Z`
- release state: non-draft / non-prerelease

Package evidence:

- path: `releases/0.18.31/CAMPFIRE_RELAY_v0_18_31.zip`
- package SHA-256: `70e423075b101905aa65da1277da2799eff7028cddacc67169a27fdc6ec97bd4`
- package file count: `336`
- release-content-manifest SHA-256: `094dfeeb0f5442933cd6b2e682475c7cd00b08dc392f37d6f69a244658dadd12`
- catalogue-manifest SHA-256: `f1fce253299da622e54df571b1551a56a353ef1b51c8014d5836a257c6086eaf`
- release notes SHA-256: `906219a671c4cd635ba693fa7ce85fac6e5520750e05fdbf9167b09913284c52`
- seed guide SHA-256: `a29c66f302f9aad1530f785cf41110369cbc3327bd02bbef9054a69179e71a7a`

Publication verification:

1. package built directly from exact main source `f88e808f...`;
2. content manifest checked all 336 packaged files;
3. trusted release record merged through PR #159 with four release files only;
4. tag created at exact release-record main commit `c035d5b...`;
5. GitHub release and assets created;
6. published package downloaded and SHA-256 re-matched;
7. temporary publication workflow deleted;
8. publication carrier PR #160 closed with zero changed files and no merge.

## REVIEW AND DEFECT RECORD

Two-way COM communication with CC was proven using nonce `FW3-CC-LINK-6E03-210249` and CC acknowledgement `COM-CC-LINKCHECK-ACK-20260803-001`.

### Defect 001 — runtime catalogue authority

`CR-V01831-RUNTIME-CATALOG-AUTHORITY-001`

The original PR #156 candidate loaded legacy `config/models.json` from `src/server.mjs`, bypassing the hash-bound modular catalogue. Framework found and repaired it through PR #157.

### Defect 002 — source-text regression bypass

`CR-V01831-RUNTIME-CATALOG-AUTHORITY-002`

CC returned `NARROW` and demonstrated that the first regression test could pass while legacy runtime authority was restored. Framework accepted the finding and repaired it through PR #158.

Final behavior:

- runtime `loadModels()` rejects non-modular catalogue authority by default;
- legacy snapshot access requires explicit `{ allowLegacy:true }` compatibility authority;
- server uses the fail-closed default;
- behavioral tests prove modular acceptance, legacy rejection, and explicit compatibility access;
- B7a/B8C/B9 lineage guards were not weakened.

CC's broader Q2-Q7 / repair-successor terminal return was not observed before integration and publication. That is unresolved review coverage, not agreement, refusal, failure, or validation. Any late CC evidence may be appended to closed issue #20 and assessed on its merits.

## FINAL TEST EVIDENCE

Exact integrated candidate head before main merge: `bcd928aef7da41d128b8abfbdfb37a071115b2eb`.

- campfire-ci #1029 — SUCCESS
- budget-core-ci #372 — SUCCESS
- B8C #148 — SUCCESS
- B9 #111 — SUCCESS
- v0.18.31 release-candidate #12 — SUCCESS

Exact final release-record branch head `eaf55b67885b328d567cfb4177c9729c152c135e`:

- campfire-ci #1034 — SUCCESS
- v0.18.31 release-candidate #15 — SUCCESS

Historical v0.18.2, v0.18.2.1 and v0.18.3 release workflows skipped correctly on successor branches.

## PRODUCTION BOUNDARY

The following are confirmed:

- main integration: COMPLETE
- trusted release record: COMPLETE
- immutable production tag: COMPLETE
- GitHub release publication: COMPLETE

The following is not observed:

- Windows Production installation or upgrade at `127.0.0.1:4317`
- local installed version `0.18.31`
- local no-paid-provider health smoke
- rollback-path observation on the installed machine

Released does not mean installed. Do not infer Production activation from repository or release state.

## COMS

- **Mark:** human and release authority.
- **Framework / Build 3:** v0.18.31 integration, repair and publication complete; no active task.
- **CC:** first terminal return was NARROW and materially useful; broader requested return not observed; no active mutation authority.
- **Build 2:** historical construction evidence only.
- **Campfire 1 / QW / other apertures:** no active COM task.

## ANTI-DRIFT

Do not begin v0.19/Exchange or another model-catalogue refresh merely because v0.18.31 is released. Do not treat release, green CI, repeated model conclusions, or clean presentation as validation. The next concrete product step is the bounded Windows Production upgrade and local verification when Mark directs it.

`The lullaby was never for the cradle`.

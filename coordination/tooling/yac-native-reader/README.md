# YAC pinned native runtime — one bounded Ubuntu setup

**20 October 2026, 20:40 UTC — Codex terminal reports INSTALLED + VERIFIED PACKAGE METADATA in the restricted Ubuntu guest; independent Build acceptance PENDING; actual Workerd/D1 runtime test NOT RUN.**

Mark has expressly directed the team to **install and set up the tools needed** to proceed with YAC, TRACE and practical Framework-Lab engineering. This supersedes the earlier *no install/download within the prior bounded inventory task* for **ordinary non-admin local development dependencies only**. It does not authorise authentication changes, third-party spending, global security-policy changes, another native AI-model attempt, unattended queue activation, real Cloudflare bindings, or public deployment.

## Why this exact toolchain

Codex's [native inventory terminal](https://github.com/markgoodbody-bit/COM/issues/873#issuecomment-6300062090) established that the required versions were **NOT INSTALLED** at the bounded authorised Ubuntu paths. The r2 reader currently has accepted Python/Node/SQLite *bridge* evidence, NOT real Workerd/Miniflare/local-D1 execution. We are closing precisely that gap, not installing an unrelated platform.

Source pin: YAC draft PR134 `1abfe95c6cae3f49c7799caed177e3bcf3b9d18f` (same package/lockfile as the accepted r2 integration). Existing `v1/package.json` Git blob `bbde5af13814d687e7233f977b5f2111a02f85be`; `v1/package-lock.json` blob `91a2b03e403fdc6f387c00ec636d4d290a347b6e`.

Lockfile pins:

| Component | Exact version |
| --- | --- |
| Node | 22+ (Ubuntu guest observed 22.23.3) |
| Wrangler | `4.143.1` |
| workerd | `1.20260926.1` |
| Miniflare/local D1 | `5.20260926.1-alpha` |
| Linux x64 native package | `@cloudflare/workerd-linux-64@1.20260926.1` |

All **91** lockfile resolved package entries inspected by Campfire use `https://registry.npmjs.org/` and `sha512-` integrity entries. Codex's one bounded Ubuntu installation reports 38 applicable packages added and exact package metadata PASS; this is not a global network-egress proof or real runtime acceptance.

## Installation boundary

Run as the already-existing **non-admin guest development UID**, inside an **isolated, disposable YAC source worktree**, with known package/lockfiles, no personal or provider credentials, and only ordinary npm registry downloads. No host Windows changes and no root, apt/sudo, global npm, Python-managed-WASM install or security-profile adjustment. Package lifecycle scripts stay disabled (`npm ci --ignore-scripts`). No `npx` auto-install or bare latest. No `wrangler login`, `dev --remote`, `deploy`, real D1 binding, remote state or Cloudflare access.

Read and execute `install-pinned-v1.sh` with `--repo /absolute/path/to/staged/yac-source --install`. The script rejects changed lockfile/package bytes, unsupported Node, existing `node_modules` (because `npm ci` would delete it), symlinked install targets, `.npmrc` and selected credential environment variables; uses a blank npm user/global config and disposable cache; verifies the three exact package versions afterwards and records native binary SHA when present.

**One finite installation completed (Codex #873 c6301021432).** Do not run `--install` again against the now-populated worktree. If rebuilding from scratch becomes necessary, make a fresh, separately reviewed disposable worktree and record a new grant/attempt. Never silently enable lifecycle scripts, retry with broad network/permissions or choose mismatched tool versions.

## Verified native provisioning receipt (not Workerd execution)

Codex [#873 c6301021432](https://github.com/markgoodbody-bit/COM/issues/873#issuecomment-6301021432) reports one restricted UID995/GID986 Ubuntu `npm ci` subphase completed at 2026-10-20 20:40:23.916 UTC, unit `yac-toolchain-setup-20261020` exit 0. Wrangler 4.143.1, workerd 1.20260926.1, Miniflare 5.20260926.1-alpha and the Linux x64 package metadata matched the lock; Node 22.23.3/npm 10.9.9. The native binary was present, SHA256 `10503477380aaf7bc04cd9e5bbe4f18c831e11713123f0d0a8d063ab57a0034b`. The exact private immutable packet is recorded there; Build independent acceptance remains **PENDING**. No Workerd, local D1, browser, model, provider or hosted runtime command was executed in this subphase.

The Codex START receipt [#873 c6300988276](https://github.com/markgoodbody-bit/COM/issues/873#issuecomment-6300988276) discovered an npm USERCONFIG/GLOBALCONFIG collision **before** installation. Codex used two distinct blank config files and preserved an exact two-line original-to-corrected diff in the private carrier. Campfire corrected the same two lines in the isolated source branch, commit `1da42dd3c98dd43e1443346a2b42c6fbe2548fab`, without overwriting Codex's evidence. The independently modified Git blob is `dd6b5748e82cb2bf7d6b34d562f9cc0c4b59efad`. Exact cross-environment script-byte equivalence is not asserted until compared.

**Next:** Build independently accepts/rejects that installation and its correction, then coordinates ONE genuinely isolated local Workerd/Miniflare/D1 synthetic reader journey. No second installation, no provider-auth retry, no live hosting and no fourth model call.

## First actual runtime test — separate gate

After the package metadata check and independent Build acceptance of provisioning, use the already-existing **synthetic-only** `v1/native_reader/operator/wrangler.local.toml` in a NEW isolated no-egress runtime process; its entry `entry-local.mjs`, `database_id=000...000`, `remote=false`, `LOCAL_FIXTURE_ONLY=true`, no route/credentials. Never use `v1/wrangler.live.toml` or `wrangler.rehearsal.toml` for this test.

The pre-existing [YAC PR134 operator instructions](https://github.com/markgoodbody-bit/yet-another-clearing/blob/1abfe95c6cae3f49c7799caed177e3bcf3b9d18f/v1/native_reader/operator/README.md) describe exact local D1 schema/fixture and `wrangler dev` commands. First verify they remain compatible with the accepted **r2 corrected** `v1/native_reader/worker.mjs` SHA256 `d7b9bdf54ebd48c2f4954f4cd3ad2dc8c74f993165406ba019733c3828c508a3`, not the stale PR134 donor SHA. This is a distinct test of actual runtime/HTTP/D1, not a rerun of the 10+4 CPython/SQLite bridge tests.

Prove egress isolation at the OS boundary, not merely by a `--local` flag. Keep first failure, source and native hashes, exact commands, exit status, local schema snapshot, response clocks and write-refusal results. Stop all test processes. Report **INSTALLED / VERIFIED PACKAGE METADATA / RUNTIME TEST PASS/FAIL/NOT_RUN** separately. Acceptance does not mean hosted compatibility or a public release.

## Engineering ownership

Codex Windows/Ubuntu operates the supported local wrapper and performs this **one** installation and finite native synthetic test, under Mark's explicit tool-setup permission. Build independently reviews and accepts/rejects evidence, prioritising YAC's public read-only route and later separately reviewed public writing. Campfire has a GitHub connector and an independent ephemeral shell, **not direct cloud-to-Mark-VM SSH**. This branch now contains the corrected installer for provenance/reproducibility. Codex's dated native receipt is evidence of installed packages on the specific guest worktree; it is **not** evidence of an executed Workerd/local-D1 reader or a live deployment.

### Distinctions to preserve

`PACKAGE_INSTALLED != ACTUAL_RUNTIME_PASS != HOSTED_DEPLOYED != PUBLIC_WRITING_OPEN`

`NO_EGRESS_TEST != NAMED_CONFIG_LOCAL`

`TOOL_INSTALL_PERMISSION != PROVIDER_AUTH_PERMISSION`

No changes to original queue PAUSED, model/browser STOP, YAC public writing OFF, protected stage HARD_OFF or private Mechanical Ethics editorial HOLD.

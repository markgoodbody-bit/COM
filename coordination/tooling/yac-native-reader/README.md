# YAC pinned native runtime — one bounded Ubuntu setup

**20 October 2026 — source preparation, NOT installed in Mark's VM.**

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

All **91** lockfile resolved package entries inspected by Campfire use `https://registry.npmjs.org/` and `sha512-` integrity entries. That is a source observation; package registry and exact runtime availability are not confirmed by this file.

## Installation boundary

Run as the already-existing **non-admin guest development UID**, inside an **isolated, disposable YAC source worktree**, with known package/lockfiles, no personal or provider credentials, and only ordinary npm registry downloads. No host Windows changes and no root, apt/sudo, global npm, Python-managed-WASM install or security-profile adjustment. Package lifecycle scripts stay disabled (`npm ci --ignore-scripts`). No `npx` auto-install or bare latest. No `wrangler login`, `dev --remote`, `deploy`, real D1 binding, remote state or Cloudflare access.

Read and execute `install-pinned-v1.sh` with `--repo /absolute/path/to/staged/yac-source --install`. The script rejects changed lockfile/package bytes, unsupported Node, existing `node_modules` (because `npm ci` would delete it), symlinked install targets, `.npmrc` and selected credential environment variables; uses a blank npm user/global config and disposable cache; verifies the three exact package versions afterwards and records native binary SHA when present.

**One finite attempt.** If registry access, optional Linux native binary or the no-install-script choice fails, record the first limit and report to Build. Do not silently enable lifecycle scripts, retry with broad network/permissions or choose mismatched tool versions.

## First actual runtime test — separate gate

After the package metadata check and independent Build acceptance of provisioning, use the already-existing **synthetic-only** `v1/native_reader/operator/wrangler.local.toml` in a NEW isolated no-egress runtime process; its entry `entry-local.mjs`, `database_id=000...000`, `remote=false`, `LOCAL_FIXTURE_ONLY=true`, no route/credentials. Never use `v1/wrangler.live.toml` or `wrangler.rehearsal.toml` for this test.

The pre-existing [YAC PR134 operator instructions](https://github.com/markgoodbody-bit/yet-another-clearing/blob/1abfe95c6cae3f49c7799caed177e3bcf3b9d18f/v1/native_reader/operator/README.md) describe exact local D1 schema/fixture and `wrangler dev` commands. First verify they remain compatible with the accepted **r2 corrected** `v1/native_reader/worker.mjs` SHA256 `d7b9bdf54ebd48c2f4954f4cd3ad2dc8c74f993165406ba019733c3828c508a3`, not the stale PR134 donor SHA. This is a distinct test of actual runtime/HTTP/D1, not a rerun of the 10+4 CPython/SQLite bridge tests.

Prove egress isolation at the OS boundary, not merely by a `--local` flag. Keep first failure, source and native hashes, exact commands, exit status, local schema snapshot, response clocks and write-refusal results. Stop all test processes. Report **INSTALLED / VERIFIED PACKAGE METADATA / RUNTIME TEST PASS/FAIL/NOT_RUN** separately. Acceptance does not mean hosted compatibility or a public release.

## Engineering ownership

Codex Windows/Ubuntu operates the supported local wrapper and performs this **one** installation and finite native synthetic test, under Mark's explicit tool-setup permission. Build independently reviews and accepts/rejects evidence, prioritising YAC's public read-only route and later separately reviewed public writing. Campfire has a GitHub connector and an independent ephemeral shell, **not direct cloud-to-Mark-VM SSH**. This repository branch is therefore a prepared executable installer, **not a claim that packages already exist on the VM**.

### Distinctions to preserve

`PACKAGE_INSTALLED != ACTUAL_RUNTIME_PASS != HOSTED_DEPLOYED != PUBLIC_WRITING_OPEN`

`NO_EGRESS_TEST != NAMED_CONFIG_LOCAL`

`TOOL_INSTALL_PERMISSION != PROVIDER_AUTH_PERMISSION`

No changes to original queue PAUSED, model/browser STOP, YAC public writing OFF, protected stage HARD_OFF or private Mechanical Ethics editorial HOLD.

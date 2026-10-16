# PSFH D099 first-visitor release candidate: human/operator gate

**Status:** exact-source DRAFT only. No public website release or protected merge has been authorised or performed.

## Why this exists

One first-time human or AI reader can begin with the original painting and authored housing story, read the **complete released Mechanical Ethics v0.8.0** in HTML or source carriers, continue through the PSFH link to the public Yet Another Clearing, inspect the read-only Human Record window, or prepare a local challenge to copy/save. The local export is **NOT SUBMITTED**. YAC public read was observed by a separate native client, but public write admission is closed; its hosted HEAD defect has a separate unmerged repair [YAC PR137](https://github.com/markgoodbody-bit/yet-another-clearing/pull/137). No site can promise outsider uptake.

## Source and publication ancestry

- Maintained PSFH D098 branch: `codex/psfh-d098-read-hallway-20261006` at `c1abe573581cdcf7d2c2485d817c3fea631f5981`.
- Frozen three-donor unified product: [COM PR829](https://github.com/markgoodbody-bit/COM/pull/829) at `b5f1b438fd4467f5c97323631cd9f929115cf83c`; tree `4ecd5f564c536c76f62f53606140ac8a27240e20`.
- This isolated [COM PR833](https://github.com/markgoodbody-bit/COM/pull/833) is based **directly on D098**, not a chain of draft PRs. Its first commit `9474b10f6d5bc630658a2dec0fa98dbec3f15e2c` had **exactly that donor tree** (14 source-diff files). Later review-only script, target inventory and CI instrumentation do not change the site's intended visitor text.
- Actual public static Pages branch at reviewed point: `gh-pages` commit **`6d52e35be8f7d81ff44c1bbde59c6dd15d719579`**, Git tree **`60081abd350cf16c04194760fe03b5fce23ca062`**. Its live CDN bytes/devices were not proved identical to the Git tree. Before any real release, verify this exact ref hasn't moved and obtain an independently retained rollback copy; if changed, **STOP and reconcile**.
- Site manifest remains Preview **0.8.55**. The released ME Markdown SHA256 remains `e3267c3e41e7fdfb44c9a9279250a1a7a38d5b9c389a594fef40cfea75fdbe76`; private ME10 DEV4 has not been inserted.

## Executed *no-deployment* rehearsal

Exact-head source-only CI: [push run 38885852811](https://github.com/markgoodbody-bit/COM/actions/runs/38885852811) and [pull-request run 38885860133](https://github.com/markgoodbody-bit/COM/actions/runs/38885860133), both **SUCCESS** on `7384dc2aeeb406b745797a76b71a79e0a8b1c061` as tested. Static build, released-book/source/figure/link routes, local challenge CSP/export safeguards, YAC primary route, deterministic complete offline archive, synthetic negative controls for release target/source/head drift and no-submission, and actual byte/hash comparison from `out/` to the pinned Pages Git tree passed. **No browser/keyboard/print run**; previously denied Chrome navigation was not retried or routed around.

From the actual generated site relative to the pinned public Pages Git tree:
- Existing public files **201**; generated site files **199**.
- **2 additions:** `explore/challenge-local.html`, `read/me-v0.8.html`.
- **7 modified:** `explore/challenge.html`, `explore/challenge.md`, `explore/map.json`, `explore/yac/index.html`, `index.html`, `manifest.json`, `style.css`.
- **190 unchanged** (including original art, original story source resources and released-book carriers).
- **4 public-only files would be lost by a naive wholesale replacement:** `.gitattributes`, `.nojekyll`, `CNAME`, `README.md`. **STOP: keep all four byte-identical to the pinned Pages branch.** Of these `CNAME` and `.nojekyll` are publication-critical. Do not publish the raw `out/` directory as a deletion-capable replacement.

The complete per-file compare and exact target blob inventory are the CI artifact files `PSFH_D099_RELEASE_REHEARSAL.json` and `public_target_git_tree.json`.

## Reversible operator rehearsal, *not a deploy command*

1. Re-read protected/main/source rules and identify the human-designated publisher. Do **not** treat a successful PR as release authority.
2. In a disposable checkout, pin the reviewed PR833 product source and run `npm ci && npm run build`, then existing tests, `python scripts/package_psfh_offline.py`, `python -m unittest scripts.test_psfh_release_rehearsal -v`, and `python scripts/psfh_release_rehearsal.py`. Commands write local review files only.
3. Re-read current `gh-pages` HEAD. If different from `6d52e35be8f7d81ff44c1bbde59c6dd15d719579`, **STOP**; the rehearsal is historical. Otherwise preserve an independently readable snapshot of its tree/files.
4. In an **offline staging directory only**, place 199 built `out/` files, then restore **all four unchanged public-only custody files** from the pinned Pages checkout. Verify they match their prior blobs, preserve the original CNAME and domain status, and rerun the full deterministic file inventory. Expected staging shape under these pins: **203 files**, **2 additions, 7 modifications, 0 deletions** compared with the public tree, without any silent redirect/write opening. This stage is a specified acceptance target, **not** a claim it was generated or uploaded by this CI.
5. Human/rights/editorial/accessibility operator reviews the actual visitor pages, keyboard/mobile/print behaviour in a permitted environment, and any required source/edition changes. These gates are **open**, not passed by source CI.
6. Only a **separately authorised** publisher may later merge/publish, preserve exact prior `gh-pages` commit `6d52e35...` as rollback target, and recheck actual served-domain convergence. Rollback itself is another explicit, logged publisher action; no automation here performs it.

## Decision requested of Mark

**ACCEPT FOR RELEASE PLANNING / CHANGE / HOLD** this specific visitor text and navigation. Acceptance of draft preparation is not release. Public rights/licence, domain/rollback, actual device/AT testing, protected merge and public deployment remain separate decisions. Visitor responses may be prepared locally but are **not transmitted**. YAC read-only public HEAD repair belongs to a separate source/deployment gate and does not block private PSFH human review.

The reader is free to leave. No visitor, correction response, uptake, or real-world benefit has been inferred.

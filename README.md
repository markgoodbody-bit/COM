# Campfire Door public preview

## Current publication: Partial views, 8 September 2026

Maintained local source: `4ba354a405cb6941f3ea3b6c65a5d37394edbdfc`.
COM content source: `74d72cf47085c2f8eac1daeae1c4e72e1f075a65`;
source with test maintenance: `d2e4756b73b9f9a8bc9274b430a7894f35328ab7`.
Authority: [FW handoff](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5584894263).

Adds only the two approved clarifications to Partial views. Nine generated
Explore files change: three aperture formats, two packets, two question-menu
size records, the machine index size record and map. The root manifest source
pin changes. Of 68 public build files, 58 remain byte-identical to predecessor
`c11f45e5d446a00a8fe9619fba9f72bad9e7c38c`. No paths are added or removed.
All 50 generator checks pass; the greeting isolation test now compares current
packets under changed greetings instead of freezing historical reading text.
The 60 Explore outputs total 173,670 bytes with tree SHA-256
`01bff6735dfc83ca0874e9b585e252047c331f27b07acd3ed3df18713a3d0cef`.

Homepage, greeting, seed, other readings, examples, source definitions,
styling, crawler policy, TLS, CNAME and rights are unchanged. The offline
layered-arrival prototype is not deployed. Wording improvement is not
demonstrated reader benefit. Publishing success and served bytes require
separate checks; see the bounded completion return on COM #108.
Rollback is an ordinary revert of this content publication, not a domain reset.
Older sections below are chronological history, not live domain-repair tasks.

Publishing branch only. COM `main` remains the coordination repository.

Preview 0.6, prepared 7 September 2026 from local source commit
`7f20b46d64cbacb90bd1fcbf19af89e071865a64`.
Authority and discussion: [COM #108](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5576230968).
The previous 0.3/0.4 comparison objects remain in [PR #110](https://github.com/markgoodbody-bit/COM/pull/110).

GitHub Pages serves this branch's root. No Jekyll processing, application server,
JavaScript, credentials, forms or analytics are part of the page. The preview
does not promote TRACE/ME status or prove the material helps a reader.

Static machine-reading additions 0.1, prepared 8 September 2026 under
[Framework's bounded direction](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5577437335).
Local maintained source commit: `fe28ff6e5f64acb41f0bb3c3650930cae41f23a5`.
The human preview keeps its text and styling, with one discovery-link paragraph
and an HTML `describedby` link added. Its existing `noindex,nofollow` remains;
the sitemap advertises routes but does not override indexing preferences.
The five machine files are working orientations, not new project canon or an
efficacy result. The manifest is project-specific, not a Web App Manifest.

Intended `index.html`: 5,113 bytes, SHA-256
`2a5994cf91d30c15ed4b76063c83ecf6111f4d995ce7f1844f80b4556f287bc8`.
CSS SHA-256: `4487822f7ac1369ae16cac356e3c5301b0b9e4ed89b5e5fc1a3746f414bdef98`.
Served bytes must be checked separately after publishing.

## Update and rollback

Temporary transport repair, 8 September 2026: self-references use the working
`http://pleasestartfromhere.com/` origin while the custom-domain certificate is
absent. This is unencrypted public retrieval, not HTTPS readiness. No reader
wording, external HTTPS link, permission, DNS setting or CNAME changed.
After normal HTTPS certificate verification succeeds, restore only these
self-reference schemes to HTTPS in the maintained source (the five `public/`
files, `app/page.tsx`, and `scripts/build.mjs`), rebuild and publish the exact
outputs, preserving this branch's CNAME. Verify the resulting link destinations
as well as content hashes. The existing HTTPS follow-up carries this completion
step; do not leave an HTTP canonical URL as the final deployment contract.

The existing local source project is `campfire-door-preview`; use its normal
build, then copy only `index.html`, `style.css`, `404.html`, `llms.txt`,
`seed.txt`, `manifest.json`, `robots.txt`, and `sitemap.xml` from `out/`
into this checkout. Review and
commit the diff on this branch. A push updates the public preview, so it needs
the applicable publication authority. Do not copy the source project's entire
directory, its dependencies, or the COM tree into the reader path.

Keep the root `CNAME` file containing `pleasestartfromhere.com` when updating
content. This custom-domain connection was configured on 8 September 2026;
it does not change the preview's content or evidential status. The old
`markgoodbody-bit.github.io/COM/` address redirects to the custom domain, so
it is not an independent fallback while that connection is enabled.

DNS uses an apex ALIAS and an explicit `www` CNAME, both targeting
`markgoodbody-bit.github.io`, with TTL 600. Do not introduce wildcard routing
or change unrelated email records. Account-level GitHub domain verification
is still pending; custom-domain configuration alone does not establish it.
Check HTTPS certificate readiness and enforcement separately before reporting
the new address live.

Keep exact build hashes in the update receipt. After GitHub reports a successful
build, verify the canonical HTTPS root, CSS and five machine files with
unauthenticated GETs. Check UTF-8, JSON/XML parsing, route existence and links;
the source build keeps the seed under 1 KiB. A
successful Git push or cached page alone is not deployment verification.

For a content rollback, revert the relevant publishing commit normally, push,
and verify the resulting public bytes. This first publication has no earlier
live version: withdrawing it means disabling Pages, not deleting COM or its
history. Before disabling Pages or removing its custom domain, remove or
repoint the GitHub-directed DNS records to avoid leaving an unclaimed route.
The pre-connection publishing head was
`0f6a0ac5bca782de58be5ae47b8c49daaee84ab8`; a domain rollback is a separate
DNS/Pages operation, not just a content revert.
Disabling Pages also requires applicable authority. No automatic
rollback, public update or deletion is authorized by this README.

## Explore 0.2 additive publication — 8 September 2026

Built from COM PR114 source `c20f644eda2eda0a5bdf9bb4fa8f8dc8f854fa2f`, directory `door-prototypes/perspective-walk-20260908/`.
The 57 generated `explore/` files have deterministic output-tree SHA256 `18bbd9d058cae597df10eb867a77d503f26d98b66cd13c83642ce27243ffd91c`.
Only root discovery links/map and this publishing guide changed outside that directory.
CNAME, seed, CSS, existing crawler/indexing policy and account settings are unchanged.
This commit is source publication, not proof of public HTTPS or reader benefit.

Future site builds MUST preserve or regenerate `explore/` from the pinned builder; do not
silently drop it when copying the old eight-file local build. Codex should incorporate the
same generated assets and discovery additions into the maintained local project.
Rebuild command: `python build.py --output NEW_EMPTY_STAGING_DIRECTORY`; copy only its
`explore/` child, never the COM source branch. Run `python -m unittest -v test_build` first.
The root temporary HTTP restoration remains the separate TLS task. Explore has relative
navigation and intended HTTPS machine-index links; certificate readiness is not inferred.
Rollback is a normal revert of the additive publication commit; no domain reset.

## Small entrance integration — 8 September 2026

Maintained source commit: `503b80ac86110269c0ba126d50cc58ae0dbd8e58` in `campfire-door-preview`.
Explore generator: COM PR114 commit
`323a3fa9c96bd67c323bab967607c4855508b531` (includes the small entrance and packet repair).
Authority and source receipt:
[FW handoff](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5582682363).

This update adds `explore/start.json`, `explore/questions.json` and
`explore/questions.txt`, modifies five Explore discovery/map outputs and adds
one root machine-index link. The root manifest records generator provenance.
The packet repair also changes both full packets. All 50 other Explore outputs and the existing root human page, seed, CSS,
404, robots and sitemap are unchanged from publishing commit `ff10f254`.

All three generator test modules passed (42 tests). Exact LF Git source reproduced
60 Explore outputs, 170,508 bytes, output-tree SHA-256
`1dfd219f6c5156d17cab323393b4a1acea2c34609adb1d6ff5e85a9250f0a80f`.
The maintained build emits 68 files and matches those generated Explore bytes.
These are structural and build-identity checks, not reader-benefit evidence.
An initial CRLF source checkout failed the identity comparison and was rejected.

Keep using the maintained build and copy its complete generated Explore set
as well as the eight root outputs. Preserve publishing-only metadata. Rebuild
Explore from its exact pinned source when changing the reading library; run
`python -m unittest -v test_build test_arrival test_packet` before `python build.py`.

The full packets previously embedded 20 example references without their
example-directory base. This generation rebases those references in both packet
forms while retaining the original example inputs, facts and standalone pages.
The regression verifies relative resolution and reverses only the path prefix
to check source preservation. This is a packaging repair, not new case evidence.
HTTPS still fails normal certificate verification. No DNS, CNAME, account,
licence, enforcement or domain-reset change is included. Roll back content
with a normal revert, not a domain operation.

## Homepage wording/navigation follow-up — 8 September 2026

Current maintained source: `f8ad742aed00d90a50320acd5f0c81a8fa863ac7`.
Authority: [FW's bounded copy direction](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5583036844).
The preceding routing publication `602b65c5aa07e38c6789d077bfa33fe2b5869a62`
passed Pages deployment and all 68 outputs matched public HTTP at 09:50:50Z.

This follow-up changes only generated `index.html`: title/masthead now use
Please Start From Here; Explore names its ten readings and separate example;
the first AI link says 'AI reading: start here'; the footer distinguishes
preparation from navigation/naming update. The H1, substantive opening,
boundaries, all previous destinations and other 67 generated files are preserved.
This is a wording/navigation improvement, not a reader-effectiveness result.

Current index: 5,283 bytes, SHA-256
`970aa98765a4a1654db6345d6fe3ba009ec3bfaffc0ae247dc8394c53e7c0018`.
The earlier index identity above is historical. Explore remains pinned to
`323a3fa9c96bd67c323bab967607c4855508b531` and tree `1dfd219f6c5156d17cab323393b4a1acea2c34609adb1d6ff5e85a9250f0a80f`.
No account, DNS, certificate, source term, release or indexing-policy change.

## Missing-page recovery — 8 September 2026

Maintained source `dbd5fb51eb4edff3181afec479490275b85177fb` changes only the
generated `404.html`. The previous response had no navigation and said the
prototype had one entry page. It now offers the existing introduction and
Explore routes, using the existing stylesheet and root-relative URLs so a
nested missing address does not misresolve them. It adds no redirect or runtime.
The other 67 generated files remain identical to publishing commit `26ecf85`.

Current 404 output: 576 bytes, SHA-256
`ae79cf8b50005b4224260e171cd52852b5e3fe2296a85997db2955c650f3f33a`.
Verify the actual missing-path HTTP status and returned bytes after deployment,
not just the directly addressable `/404.html`. The status must remain 404.
HTTPS and account verification remain unresolved and outside this repair.

## First-contact value/routing copy — 8 September 2026

Current maintained source: `74a7ff3b706e2c3efa37bf6f1916af78ce5d48d5`.
Direction: [FW 5583292550](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5583292550).
The existing two-sentence value declaration from Explore appears once near
the beginning of both the human introduction and root machine orientation.
The existing AI entrance link moves to the first Start item in `llms.txt`;
its old lower placement is removed. Previous destinations and seed are retained.
The footer distinguishes the wording/navigation update from original preparation.

Only `index.html` and `llms.txt` change from `916c804`; other 66 generated outputs
are byte-identical. No new theory, reader outcome, release, permission or host
change is claimed. Previous index/llms identities above are historical.
- `index.html`: 5,454 bytes; SHA-256 `cd050e1893da5b883fee16f2127035b5451cd9f3c6d3b500d2eb0004318227a9`.
- `llms.txt`: 3,808 bytes; SHA-256 `0ec46a2258233cd8ce56d020ec1e1386097b14ea98828c9f1d737a1ff9e0d22c`.
# Current welcome and HTTPS update — 8 September 2026

Maintained source: `b7a395ba0ccb033751fb9b7d8af9d96680dcf3a5`.
Explore generator: `77165a1fb67215506128814939c9635e9b3e6ba1`,
`door-prototypes/perspective-walk-20260908/`; all four modules / 49 tests passed.
Exact source reproduces 60 Explore files / 172,236 bytes, tree SHA-256
`975c16885d9fc24b1dd970cffc6737a77a5a20e6fd4bfd1b132a954d1da4eb2f`.

Before: the entrances introduced the work but did not ask a reader's question;
root self-references temporarily used HTTP. After: five Explore entrances and
the human/root-machine introduction share the optional welcome and explicit
no-replies boundary. Their map and root provenance are current. Root self-links
use HTTPS after normal certificate verification succeeded at 10:59:42Z.
Exactly 12 of 68 generated files change from `8d23f18`; all paths remain.
The other 56 files, including all readings, full packets, CSS and 404, are identical.
Seed wording is preserved apart from HTTPS schemes (999 bytes).

One domain removal and immediate restoration ran at 10:57Z. GitHub's restoration
head `8d23f18` has the exact same complete tree as `3eaf0da`. Approved apex/www
certificate and HTTPS enforcement were subsequently read back. Do not repeat
that recovery. Domain account protection remains unconfirmed. No DNS, source
terms, indexing or project status changed. This is transport/wording work, not
reader-benefit evidence. These build identities require separate public checks:

- index.html: 5,834 bytes; SHA-256 `e1bdbebad2c6301b0c3944ed290f69e6ef972c5b705f7a3c1defc6543622cfdf`.
- llms.txt: 4,159 bytes; SHA-256 `3ce4f9b71b28b2b271207e4b4f8f33f09b9ea9833e93b06d171d9715133e6e66`.
- seed.txt: 999 bytes; SHA-256 `484cb0fa39471bedd8d7ad64f768b6b709d7b454890221f8d410930da73bcd8a`.

Future updates use the maintained build and exact pinned generator as described
in its README. Preserve CNAME and publishing-only metadata. Historical receipts
below describe named earlier revisions, not current state. Content rollback is
an ordinary reviewed revert, never another domain reset.
# Current public discovery policy — 8 September 2026

Maintained source `4a8739768548812a087b98b509b943728401ad2e`; Explore generator
`969e67d002605cc4ea91f72b4da415fd13889576` on existing COM PR114.
Authority: [FW5584293683](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5584293683).
Historical noindex-preservation instructions below are superseded only for the
already-public homepage and 18 Explore HTML reading pages. Their only HTML change
is removing the preview robots exclusion. Text, examples, greeting and source
terms remain exact. Error-page and local downloadable-preview bytes are unchanged.

The existing sitemap lists the 19 human-readable public routes, with no error,
private/control or duplicate-format inventory and no invented lastmod. robots.txt
keeps public Allow and reuse boundaries; only its stale preview comment changes.
The root manifest pins the new generator. Existing 68 output paths are retained.
50 generator tests passed, including parsed public robots regression; local
checks confirmed exact tag-only HTML diffs and sitemap coverage of all19 pages.
Explore:60 files/171390bytes/tree SHA256
`a2d1987a208bd7b7e3885438c8215a73f92daccaee2fb62b401aae8d386c97a6`.
Root index:5787bytes/SHA256
`ff6bd2b39d8522abd0c4c4c60938aaf9c9dd8ac6ccdce34ac74b96bf6706fad7`.
Sitemap:1645bytes/SHA256
`460fcb58ddada9f3d1bd40862d6c5ac5c5f149f99ea26368ff4ca6a7fb2341a5`.

These are build checks, not a search-inclusion or provider-access result. Verify
actual HTTPS bytes, final URL/status and HTTP/HTML robots directives after serving.
No new paths, account, submission, service, scheduler, DNS/TLS or rights mutation.
The earlier domain recovery remains consumed. Keep using the maintained build.

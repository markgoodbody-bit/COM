# Maintained Please Start From Here source

## Current release preparation, 8 September 2026

The accepted content is f7d606b219ad7c969717376b711c7541ab6100fd: five starting
points before the optional AI handoff, six unnumbered optional questions, and
extract-local value disclosure. CC accepted this exact content in COM5590871067;
Codex reproduced the build, 26 checks and two native browser sizes in COM5590901242.
Release preparation changes only transient not-published labels, their source pin
and assertion, and existing reader history. Working-preview status and all
accepted substantive content remain. Delivery is a separate, later verification.
The gh-pages README owns the publication receipt. Older sections below are dated
history, not current publication instructions or readiness claims.

## Earlier shared house-style preparation

Following Mark-relayed Gemini advice recorded in FW5586692116, one maintained
stylesheet now supplies root, Explore, discussion, catalogue, history and source
views. Before: separate inline skins, mismatched heading sizes and light-only
root. After: system sans/monospace roles, a descending 1.25 heading scale, neutral
light/dark tokens, underlined links, visible focus, rem spacing and wrapping.
The build replaces only generated head styles. It preserves body markup, reading
order, destinations, source text, raw originals, PDFs and fixed editions.
Explore output sizes/hashes and discussion delivered-HTML identity are recomputed;
the original discussion rendering hash is retained separately as an input pin.

Local validation: build, preview delivery, source/discussion preservation and
`node --test scripts/test-house-style.mjs`. The latter compares every HTML body
and all non-presentation files to public50caedc8, checks generated inventory and
stylesheet hashes, and calculates eight declared light/dark text contrast pairs.
These checks do not establish browser usability, actual computed styles or WCAG
conformance. Keyboard, 200% text enlargement, 320 CSS-pixel reflow and text-spacing
overrides remain unverified. Preview handoff returned queued, not a visual pass.

Public remains0.7.2/50caedc8. No release/history entry claiming delivery, provider
login, public contribution collection, DNS change or spending is included here.
Before publishing: complete or explicitly disposition the browser acceptance,
record the actual presentation change in existing history, then publish the exact
candidate with an updated site edition. Do not report this candidate as live.

## Local preview route repair, 8 September 2026

Before: the hand-written preview route list returned 404 for `/explore/`,
`/read/start.html` and the ME PDF, despite their presence in the published build.
After: the server inventories the generated `out/` tree at startup and serves
its exact file bytes plus directory-index aliases. Request paths never become
filesystem paths. Hidden entries are omitted; linked and unknown file types
stop startup. Only GET/HEAD are accepted. This remains a local static preview,
not a receiver. Restart after rebuilding; there is no live reload.

The preview CSP now permits the generated pages' inline CSS and same-origin
diagrams. Scripts, forms and external resources remain blocked by that policy.
This is not a browser visual review or a general security audit.

`npm run build` and `node --test scripts/test-serve.mjs` pass. The test requests
all 111 current output files and directory aliases, compares exact bodies, and
checks HEAD, ETag, missing/private paths, malformed URLs, PDF type and rejected
POST. All 111 output files remain byte-identical to public commit
50caedc89646b7337a86a5610cef24426b518cf3. No release or deployment is needed.

Coordination supersedes the older assignment below: FW owns receiver PR116;
CC reviews/reproduces it. Codex retains the maintained site and deployment.
Public receiving, provider authentication and the shared-style pass remain open.

## Delivered discussion reading and history

Preview0.7.2 public81ca060433144a028ec78db294b4e9d878c3a1bf / Pages34240219144
succeeded. At14:45:17Z,111 Git/build files and63 ordinary HTTPS responses matched,
including discussion HTML/MD/directory and same-domain active next targets.
COM5587003596 records scope, source identities and unchanged receiving gap.

Existing history Edition0.5/D009 follows actual delivery: source74560b174fb24523186ba321a2fde4f3d23bad70,
generator e63d4fa7c2f6533366ee80f55726cd9ac85e962b. MD20804bytes SHA256
acf25114a35794c5e77864f3562d929a647d1a759b3589758789bffef4980965;
HTML23581bytes SHA256b0067d5c640c6dcfb24a1bc92db8f1e4803dd0bb72b97e86a142f0330335c9f2.
57 generator/history/discussion tests pass. Only historyMD/HTML and manifest
history pins change in this follow-through; earlier entries remain intact.

## Preview 0.7.2: discussion reading, not reply access

FW5586836238 supplies the complete editorial source9ceae9d27fd2b64550148bed622955b13a8740a6.
No source wording changed. New /discussion/index.md is8008bytes SHA256
7117f1acf2c6cce494da2413c82fe8185f99dcb21342e4053ceb545efa222c18;
HTML9675bytes SHA25698310708d53cf919392854a3e71cccac349c9562cdc95c6a0990f69732815405.
Existing COM prose renderer extended with explicit stable heading IDs and return
paths at1b41e0c9fec685dcd462c925c651ec6bd4debd3a. Seven section anchors;
all41 source blocks and13 link occurrences preserved. Editorial summaries,
constructed possibility and unavailable receiving are explicit, not live comments.

The existing homepage route gains one optional local discussion link. Challenge
HTML/MD defaults to local reading, with legacy GitHub participation preserved;
its map inventory is regenerated. Manifest pins both outputs and their sources;
normal build rejects changed/missing discussion copies. Sitemap adds the page.
One maintained site-edition value moves to0.7.2; the four source-text wrappers
change only their site edition, never their embedded source. All raw originals,
snapshots, CSS, root orientation, seed, domain/crawler settings and previous
history are unchanged. Initial comparison:111 files,2 new,10 changed,99 unchanged.

57 COM generator tests,2 maintained discussion tests,4 source-view tests and
visible-route check passed. Text/link/anchor checks are not browser usability
or receiving-service tests. Local preview adds only explicit discussion GET/HEAD
routes; no POST. No form, storage, backend, login or new dependencies. CC owns
the isolated receiver prototype. Public delivery and existing-history record
follow; no accountless reply-completion claim.

## Delivered 0.7.1 and reader history follow-through

Publication acff173ed906414c28ecc82830bec0ec0e6c3385 / Pages34238551769
succeeded. At14:29:55Z,109 generated files matched Git and56 selected ordinary
HTTPS responses matched exact bodies, including all four new views and their
advertised active next targets, all28 original copies and selected metadata.
Expected media types passed; redirects were refused. Completion COM5586767917.
This is bounded delivery, not provider acceptance or browser visual review.

Existing reader history Edition0.4 adds D008 with actual delivery, returning
report provenance, compatibility hypothesis and CC's withdrawn movement claim.
Source3f7bc2e8e7a0be855d2642a9b984304f17bc5b7e; generator
d58419a851193c5b6c1d2e6102433c269c168d7d. MD18228bytes SHA256
7b68b38df0121b2627347df9cf1f5d580ba892508ab1a751ef8b1fe1aefdf906;
HTML20842bytes SHA2568d0bd491ae87f7e130123246f72f1664ec4d13b53fcede31e3df474a1c360def.
54 generator/history tests passed. This follow-through changes only history
MD/HTML and manifest provenance; prior dated entries and all reading sources
remain intact. The four source-view tests and visible-route check pass again.

## Current compatibility successor: Preview 0.7.1

Direction FW5586494717 supplies a disposition of five distinct returning-reader
reports (one duplicate excluded), not cold trials or witnessed provider logs.
Do not infer provider identity, mistake tool refusals for origin responses,
or treat CC's withdrawn purpose-movement claim5586601708 as a repaired defect.

Four transparent source-text HTML views are generated offline under read/ for
the original start JSON, root llms guide, TRACE spine and ME Markdown. Complete
escaped text, raw address, source edition/hash and next links are retained.
Links resolve against the original file directory; existing example/challenge
HTML is reused. There is no runtime fetch, executable embedding or full Markdown
rendering. The raw llms guide retains its original0.7 label and bytes; the wrapper
explicitly distinguishes source0.7 from the current site edition. All original
JSON/Markdown/text and fixed resource copies stay byte-identical.

scripts/site-edition.mjs supplies the root body, masthead, footer, generated
manifest and view labels. It is a site edition, not the manifest schema or the
TRACE/ME version. Existing resource catalogue alternatives are reassembled from
the maintained importer; inventory SHA256
948c07c95715d5d4215c35166f0afe209a7431e80f506b9b9ac3d6ce90afdca8.
No new dependencies or host. Earlier0.7 remains at publicba181af0.

Run npm build, python -B scripts/test_source_views.py (4), existing resource
tests (10) and literal-route check. The HTMLParser check reconstructs the four
UTF-8 payloads exactly and covers leading whitespace, Unicode, CR via character
references, BOM and markup-like text. Invalid UTF-8/NUL or changed source is
refused. This is a bounded parser test, not a browser/provider simulation or
universal encoding guarantee. Raw files remain the byte authority. Advertised
same-domain next targets and fragment IDs are checked against actual output.
Before history is updated,109 outputs comprise4 new/6 changed/99 old unchanged;
all62 Explore outputs and28 original current/snapshot resource copies are exact.
Ordinary HTTPS delivery and the reader history are handled after publication.

## Final reader-trial label: Preview 0.7

FW5586136661 requested consistent site edition labels after confirming the
resource copies. Root masthead/footer and guide now say Preview0.7; manifest
has separate site_edition0.7 while its format version remains0.1. History
source05223c48/generatorecdd938 labels the same trial without promoting TRACE/ME.
The33 resource and62 Explore outputs remain unchanged. Scope is frozen for
Mark's next reader encounters; no extra content gate, feature or automatic import.

## Delivery history update, 8 September 2026

Resources were published at7ab5d915 and checked13:44:03Z:39 selected HTTPS
responses exact, including all28 original copies and expected media types.
CHANGES.md edition0.3 now records D007 and its limits, source2868b36c,
generatorb28fa5ad. SHA256cb5d9185a95207d817a37e3b947daf50d0121793c0e5ef3845c97c0a820ab49e.
The existing54 history/Explore checks pass; all62 Explore outputs remain exact.
This follow-up changes only the two history files and their manifest provenance.
The prior source/build notes below retain their original temporal scope.

## Current update: same-domain reading copies, 8 September 2026

The Door's normal TRACE/ME reading routes now point to direct static files under
resources/. Repository/history/participation routes remain distinct and outbound.
The fourteen originals at TRACE46f4fcd1 and ME44f7efb5, including the existing
50-page ME PDF and four PNG/SVG pairs, are copied exactly at current and fixed
snapshot paths. Notices and candidate/baseline distinctions remain unchanged.
The catalogue links all files; two figures directory indexes close the preserved
README's directory link. No general Markdown renderer or PDF authoring is used.

33 resource files total2,122,697bytes. Inventory SHA256:
`26963e06a95925ab1e0f48366cee27d0c34fe6cb851616ea139bf5edfd2c90bc`.
`scripts/RESOURCE_COPIES.json` is the exact reviewed input from COM10c23eb.
All selected Git commit/tree/path/blob/size identities and four source-declared
SHA256 values were checked. Acquisition is explicit through gh; normal npm builds
are offline and verify all resource hashes before copying. The importer requires
Python and pypdf for deliberate imports; normal builds use the existing Node runtime.

For a future edition, review the inventory and update its explicit pin, acquire
into a new empty directory, then assemble into another new empty directory with
the existing public/resources as --previous. Previously recorded snapshots must
remain identical. Review the new inventory hash and update scripts/resources.mjs
and root manifest deliberately. Import the completed directory without deleting
old snapshots, run npm build and the resource tests, and publish only after exact
output comparison. Acquisition/validation failures must leave the last public
site untouched. The build refuses missing/changed/extra files and fixed snapshot
replacement; it does not fetch moving main branches automatically.

Checks: `node --test scripts/test-resources.mjs` (6 tests),
`python -B scripts/test_import_resources.py` (4 tests), existing literal-route
check and unchanged Explore output comparison. Parsed PDF object checks, restricted
SVG checks and Markdown link closure are bounded, not a comprehensive security
audit or visual review. FW4c942e3's17 fixture tests pass, but its unmodified raw
PDF-token check rejected /AA inside encoded image object134. That rejection was
reported in COM5586078108, not silently counted as a passed corpus test. Its SVG
namespace/ID/style checks informed the maintained importer.

105 public outputs:33 added,4 changed,68 old outputs unchanged from486c148b.
All62 Explore assets remain exact, including their upstream provenance pointers.
Third-party texts, original source pointers, history and live discussion remain
outbound; no claim of a completely self-contained ecosystem or provider access.
No new host, rights, dependency lockfile, browser script, service, or DNS/TLS change.
The reader change history is updated after actual public delivery is checked.

## Current update: reader change history, 8 September 2026

Root changes.md preserves CHANGES.md edition 0.2 from COM commit
`4609bd04b0053959da39ba4fde4f20c29316c558`, SHA256
`5fd4c0e3d164e351e660533f73ef9243b2f9fcc9296580786a1f3d325b8c9489`.
The earlier entries and cutoff are retained, with a separate dated P001
publication update. Root changes.html carries the complete prose, evidence
links and nine stable lowercase D/P/R entry anchors. This is an authored
history, not independent custody or a live monitoring claim.

Generator `3246a9de0936ee28b8fa17b9e15f73fd2896d15a` extends the existing
reviewed prose renderer only with bold labels and entry headings. Run its
six test modules (54 checks) and `python -B build.py --history-output NEW_EMPTY_DIR`,
then import the two files into public and run the maintained npm build.
Existing 62 Explore outputs remain byte-identical. A compact footer URL,
root guide, manifest and sitemap provide optional discovery; no new service,
hosting, licence, content theory or reader-benefit claim. The same-domain
TRACE/ME resource inventory is received but is not included in this release.

## Current update: worked revision, 8 September 2026

FW's source `730ece48c96fae27d66c797c2fc8fe96a61e8d39`, WORKED_REVISION.md,
is preserved exactly at public/explore/worked-revision.md. Its SHA256 is
`c2f41ce55fdea96361d9716116fd6ad016a55c24651a7c6c72d62d51a0d70421`.
It is a dated project-authored account, not independent evaluation or a live
status page. Its project execution reports and relayed reader reports remain
distinguished; no claim that TRACE caused the engineering result is added.

COM generator source `453326cd663859cc88bb77d535bb072c72f3a713` produces
the matching script-free HTML through the existing template, preserves all
paragraphs/headings/evidence links, and adds optional Explore discovery.
The narrow renderer accepts only the reviewed prose/heading/HTTPS-link subset;
changing the source requires deliberate review and pin update. It is not a
general Markdown engine. Run the existing four test modules plus
test_worked_revision: 52 checks passed. Then regenerate into an empty staging
directory and import Explore through the normal npm build.

62 Explore files total 187,994 bytes; output-tree SHA256
`7e993faed8fdb34b329f79cb06d2d06369c5c70fd0ede80db92cf07d91326bff`.
The existing ten-reading/appeal packets remain unchanged and do not include
this separate technical example; discovery text makes that boundary explicit.
Only the new page, Explore entry/discovery/map records, root manifest provenance
and sitemap change. Homepage, greeting, seed, all original readings/examples,
rights and infrastructure remain unchanged. CHANGES.md and the offline layered
prototype are not included in this publication.

## Current update: visible route addresses, 8 September 2026

Under FW direction [5585434316](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5585434316),
the existing root route area now displays literal absolute URLs for the small
machine entrance, example entry and reply-limits page. The root llms guide
uses absolute addresses for those three destinations. No reading, greeting,
seed, path, licence, crawler policy or infrastructure changes.

After `npm run build`, run `python -B scripts/check-visible-routes.py`.
This standard-library parser discards attributes and non-body content, then
checks the three addresses in the homepage and generated local preview. It
also checks their absolute links in the guide. The check failed on the prior
homepage and passed after this change. It is not a provider emulator, browser
rendering check, access diagnosis or reader-benefit result.

Of 68 public output files, only index.html and llms.txt change from public
`edefdeee6ba890ea0776d1fb518549120c5b276d`; the other 66 remain identical.
The local downloadable preview regenerates from the same root content.
All 60 Explore assets, including their relative navigation, are preserved.
The offline layered-arrival repair and FW's worked-revision source are not
part of this publication. Keep using the existing GitHub Pages host.

## Current update: Partial views, 8 September 2026

FW's content commit `74d72cf47085c2f8eac1daeae1c4e72e1f075a65` adds
two clarifications to the existing aperture reading: failed retrieval alone
does not establish absence or cause, and non-detection needs established
coverage, timing and detection ability to support absence. All preceding
sentences, other readings, examples and source definitions are preserved.

Reproducible source including the greeting-test maintenance is COM commit
`d2e4756b73b9f9a8bc9274b430a7894f35328ab7`. The test previously froze old
packet hashes; it now compares the same library with and without greeting
text. All 50 existing checks pass. The generator itself is unchanged.
The 60 Explore outputs total 173,670 bytes, output-tree SHA-256
`01bff6735dfc83ca0874e9b585e252047c331f27b07acd3ed3df18713a3d0cef`.
Nine Explore files change: the three aperture formats, two full packets,
two question-menu size records, the machine index size record and the map.
The other 51 Explore files are byte-identical to public commit `c11f45e`.
Only manifest provenance changes outside Explore; the homepage, greeting,
seed, examples, styling, crawler policy, TLS and rights remain unchanged.
FW's separate layered-arrival prototype is not included.

These are wording and test-maintenance changes, not demonstrated reader
benefit or a new TRACE definition. Older sections below are dated history,
not live instructions to repeat the completed domain repair.

This local project reproduces the static public site. Existing GitHub Pages
hosting remains the publication route; do not register another host.

## Initial Explore handoff, 8 September 2026

The accepted publication is COM gh-pages commit
`ff10f254bece7b62d02af52d9cd16cfebcda72d4`, from Framework's handoff in
[COM comment 5578120799](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5578120799).

- `public/explore/` preserves all 57 generated assets exactly as committed.
- `app/page.tsx`, `public/llms.txt` and `public/manifest.json` reproduce the
  publication's additive discovery changes.
- `PUBLISHING.md` is an exact copy of that publishing commit's README, not a
  claim that its old local-source identity remains current.
- The original editable Explore content and generator remain in COM at
  `c20f644eda2eda0a5bdf9bb4fa8f8dc8f854fa2f`, under
  `door-prototypes/perspective-walk-20260908/`. Future content changes should
  update that single source and import its generated assets, not separately
  rewrite its JSON, Markdown and HTML forms.

Run `npm run build`. The 65 generated files in `out/` were compared with the
exact Git blobs of the accepted publishing commit: all matched, including the
57 Explore files. Compare against Git blobs, not a Windows publishing working
tree whose Markdown files may have been converted to CRLF. Explore assets use
`-text` here to preserve bytes through future checkouts.

The publishing checkout separately owns `.gitattributes`, `.nojekyll`, `CNAME`
and `README.md`. They are not generated by this build. Preserve those files;
update the publishing README's source identity deliberately when publishing.
Do not replace a whole publishing tree with the `out/` directory.

That initial maintenance pass did not publish anything or change content semantics.
TLS is still incomplete. Keep the existing HTTPS follow-up and its concurrency
guard; do not perform a domain reset as part of source maintenance. Reacquire
the live publishing head before any publication, and retain all later changes.

## Small entrance update, 8 September 2026

Current Explore generator source: COM commit
`6c037c8e3779f19e633ae5f549927a078a85a075`, in the same source directory.
Authority: [Framework's handoff](https://github.com/markgoodbody-bit/COM/issues/108#issuecomment-5582682363).
The generated set is now 60 files. It adds `start.json`, `questions.json` and
`questions.txt`, and updates five discovery/map files. All 52 other Explore
files are preserved. The root machine index gains one discovery link and the
manifest records the new generator source; the human landing page is unchanged.

Both generator test modules passed (36 tests). Building from exact LF Git
source reproduced 169,546 bytes and output-tree SHA-256
`8f48f08ed886510e39d812c05a80e63c3d1fd31fedbccb46f54ffc66938f255c`.
A Windows CRLF checkout passed the structural tests but failed this identity
comparison; it was not accepted for publication. Use exact source bytes.
The normal local build now produces 68 files. These checks establish build
identity and routing structure, not cold-reader usefulness.

`PUBLISHING.md` remains the historical ff10f254 publishing-guide snapshot.
The gh-pages README owns the current publication receipt and rollback details.

## Packet repair integrated before publication

The subsequent generator source `323a3fa9c96bd67c323bab967607c4855508b531`
supersedes the source above. It fixes 20 embedded example references in each
full packet by making their example-directory base explicit. Original source
facts and all individual readings/examples remain unchanged. Only `packet.json`,
`packet.md`, `llms.txt` and `map.json` differ from the small-entrance generation.

All 42 tests passed, including source preservation and packet-relative routing.
The exact build has 60 Explore files, 170,508 bytes and output-tree SHA-256
`1dfd219f6c5156d17cab323393b4a1acea2c34609adb1d6ff5e85a9250f0a80f`.
The normal maintained build remains 68 files. Compare publication against this
generation, not the superseded small-entrance identity above.

## Homepage wording pass after routing publication

Routing was published at `602b65c5aa07e38c6789d077bfa33fe2b5869a62` and all
68 generated outputs matched public HTTP retrieval at 09:50:50Z. HTTPS was not
established. FW's next bounded direction is comment 5583036844 on COM #108.

This separate pass changes the title/masthead from Campfire to Please Start
From Here, gives Explore a concrete ten-readings-plus-one-example description,
labels `/explore/start.json` as the first AI reading route, and distinguishes
the original preparation date from today's navigation/naming update. The H1,
concrete opening, evidence limits, source basis, all Explore bytes and existing
other destinations remain unchanged. These are wording/navigation improvements,
not measured improvements in reader outcomes.

## Missing-page recovery

An unknown public path returned HTTP 404 with the old unlinked sentence
'This prototype has one entry page.' The fallback now identifies the site and
offers two existing destinations: the introduction and Explore. Root-relative
links and the existing stylesheet also resolve from nested missing paths.
HTTP 404 remains an error response; there is no redirect, search, script,
tracking, invented destination or claim about why the path is absent.
Only the generated `404.html` changes; the other 67 outputs are preserved.

## First-contact value and routing copy

FW direction: COM #108 comment 5583292550. The existing two-sentence value
choice from `explore/start.json` now appears once after homepage authorship and
once after the root machine guide's opening description. The machine guide's
existing small entrance link moves to the first Start item and uses the same
'AI reading: start here' label as the homepage, without duplicating its URL.
The footer describes today's wording/navigation update, not a new source review.

Only `index.html` and root `llms.txt` change from publication `916c804`.
All reading content, seed, prior destinations, limits and hosting settings are
preserved. This makes an existing value choice visible; it adds no new theory
and does not demonstrate improved reader outcomes.
# Welcome and secure-link maintenance — 8 September 2026

The current Explore generator is COM PR114 commit
`77165a1fb67215506128814939c9635e9b3e6ba1`, directory
`door-prototypes/perspective-walk-20260908/`. Its four test modules passed
49 checks; exact Git source produced 60 files / 172,236 bytes, tree SHA-256
`975c16885d9fc24b1dd970cffc6737a77a5a20e6fd4bfd1b132a954d1da4eb2f`.
Only five Explore entrances and their map changed; 54 other Explore outputs,
including complete packets and all individual readings, are byte-identical.
The same optional welcome appears at the root, with a real Challenge link and
an explicit no-replies boundary. The root manifest updates generator provenance.
This is wording and navigation work, not demonstrated reader benefit.

Normal verified custom-domain HTTPS succeeded at 10:59:42Z after the one-shot
domain remove/restore recovery. GitHub confirmed an approved apex/www certificate
and HTTPS enforcement. The temporary HTTP self-references in seven maintained
source files are now HTTPS; seed wording is unchanged apart from those schemes.
The seed is 999 UTF-8 bytes. No DNS, account-protection, indexing or source-term
change. Account-level domain protection remains unconfirmed. Do not repeat the
domain recovery. Public delivery of this build must be verified separately.

Rebuild Explore from exact Git bytes with
`python -m unittest -v test_build test_arrival test_packet test_greeting`, then
`python build.py --output NEW_EMPTY_STAGING_DIRECTORY`. Copy generated Explore
assets into `public/explore`, then run the existing `npm run build`. Preserve
all 68 output paths and publishing-only metadata. Historical receipts below
describe their named revisions, not current transport or content state.
# Public search-discovery update — 8 September 2026

FW direction5584293683 retires preview indexing exclusion only for the existing
public homepage and Explore HTML. It supersedes historical noindex-preservation
instructions below. The error page and downloadable local preview retain their
original exclusion and bytes. Public substantive text, greeting, seed, source
terms, indexing-independent retrieval rules, domain and TLS settings are unchanged.

Current generator: `969e67d002605cc4ea91f72b4da415fd13889576` on COM PR114.
Four modules pass 50 tests, including parsed public-page robots regression.
Explore tree SHA-256 `a2d1987a208bd7b7e3885438c8215a73f92daccaee2fb62b401aae8d386c97a6`;
60 files / 171,390 bytes. Only 18 HTML robots tags and map hashes change there.
The existing sitemap now lists 19 human-readable routes (root plus Explore),
not the technical/control inventory. No invented lastmod dates or new paths.
The root manifest pins this generator. Build using the existing commands below.

This removes an authored search exclusion. Actual indexing, search inclusion,
and provider-specific access are not established by build or HTTPS checks.
No new service, submission, account, rights grant or domain recovery is included.

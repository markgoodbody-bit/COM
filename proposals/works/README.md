# Works collection preview: five works, repaired Powers included

SOURCE-ONLY / WORK IN PROGRESS / NOT FOR MERGE OR PUBLICATION

## Current state

Powers now comes from the exact repaired PR127 tree
`548e1fe316d1ccb58b3f4008097deb9d0dbe6c39`, with no proposal-path differences.
FW supplied the full source repair at PR127 comment5606873932 and #108
5606877010. Codex then built that exact detached checkout with the real image
files: eight outputs, twelve tests, four actual-image render states, eight exact
HTTP deliveries. Both mobile text sizes retain the image at358x299.8125 CSSpx;
all eleven subjects appear before the smaller PSFH response. This closes the
mechanical evidence gap, not a new independent museum-source or CC review.

Only after that check was Powers included in the local collection. Current
output is `outputs/works-five-repaired/works/index.html`: five work pages plus
index, 36 exact routes, 32 tests and 24 browser states with no measured horizontal
overflow. Selected index image files total712977 bytes. The site-building checks
preserve full images and text enlargement; they do not establish usability,
colour fidelity, native zoom, physical-device behaviour or reader benefit.

Current records use `repaired-five-` and `powers-548e1fe-` prefixes under
`evidence/`. Unprefixed records describe the earlier four-work output; those and
the initial-fixture records are historical. The unchanged historical instructions
below are retained for the correction trail, not as current status. No public
deployment, maintained merge or new CC review is claimed.

## Historical correction: four-work interim output

The initial local five-work fixture included unrepaired Powers. That conflicted
with FW's explicit repair-before-inheritance direction. A WIP label did not cure
that scope error. The current builder excludes Powers completely: no Powers
page, image, card or record is emitted. Its partial edits remain an independent
proposal, not a collection input. Nothing was merged or published.

Current output: four work pages plus the index, 28 exact inventory routes.
All 30 checks pass, including a negative check that no Powers/quilt route is
emitted. The revised 20 browser states (five pages at desktop/mobile and root
16/32) show no measured horizontal overflow. Current selected index images total
511,562 bytes. Complete-document eager-loading and DPR1 limitations still apply.

Current records: `evidence/render-measurements.json`,
`delivery-observation.json`, `output-inventory.json`. Earlier records are retained
with an `initial-fixture-` prefix. They are historical observations, not evidence
for the corrected current output. The old fixture is not the handoff.

The sections below describe the initial experiment and its limits. Where they
refer to five works, 36 routes or 24 states, this correction supersedes them.

Base: maintained `e30debac2a8c32c37d2abfaa32e988c11fe98e79`.
Commit `1aaab03dcf92d92599b32c9e12d926a05bc2cf35` copied the exact Powers
`fd4be44799c47bd4c0df6cf5c0bd470ca30f33d2` and Vermeer
`cf1e4e985563c011c7c838af835b35a138d7b37d` proposal paths. They were reviewed
with repairs requested, not accepted as complete.

## Initial fixture before / after (historical)

- Before: two independent work-page proposals. After: a local index and five
  distinct pages, adding Atkins, Shen Zhou and two photographs of Lewis's sculpture.
- Powers: fixed-pixel gutters; donor credit and recorded title added with CC
  provenance; the insistence on recording the panels made explicit; project
  response removed. The eleven factual panel subjects are STILL MISSING. The
  page says so. This does not complete PR127's requested repair.
- Vermeer: fixed-pixel gutters; clearer distinction between the selected small
  acquired image and a higher-resolution viewer reported by CC. That viewer
  extent is attributed, not represented as independently verified here.
- Original acquisition receipts remain unchanged. Later reports are separate.
- Four previously acquired source photographs are retained byte-for-byte. Eight
  smaller full-frame JPEGs are generated with recorded parameters and parent
  hashes. No new acquisition, crop, AI image, synthetic angle or master claim.
- New work records have null project responses. Museum accounts are attributed;
  the modern English translation of Shen's poem is linked, not reproduced.
- The composite builder adds only a shared stylesheet link and shelf-return
  navigation to the two imported page outputs. Those two emitted HTML files are
  therefore NOT byte-identical to their independent proposal outputs.

No normal site source/build wiring, maintained branch, public output, book,
protocol, edition, analytics or stateful machinery is changed.

## Reproduce

From the checkout root, with Python and Pillow installed:

```text
python proposals/works/build.py
python -m unittest discover -s proposals/powers -p test_powers.py
python -m unittest discover -s proposals/vermeer -p test_proposal.py
python -m unittest discover -s proposals/works -p test_shelf.py
```

Output: `outputs/works-five-repaired/works/index.html`. All assets are relative and
included. The output is a standalone local collection, not a website deployment.

`prepare.py` is an explicit acquisition-workspace preparation helper, not a
normal-build dependency. Its original custody paths are local to this machine.
The committed parents and derived files suffice for the normal preview build.
Pillow 12.2.0 / JPEG 8.0 produced identical variant hashes in two local runs;
this is not a cross-version reproducibility or colour-fidelity claim.

## Initial fixture checks, 9 September 2026 (superseded output)

- 30 automated checks passed (10 Powers, 10 Vermeer, 10 shelf).
- 36 inventory routes returned exact bytes and hashes over the local HTTP server.
- Edge 152.0.4191.66: six pages at 1440 and 390 CSS pixels, each at root font
  sizes 16 and 32 pixels, DPR1: 24 render states. None had measured horizontal
  overflow or an out-of-bounds main-content element.
- Powers and Vermeer image widths remain 358 CSS pixels at mobile 16px and 32px
  root font sizes. Fixed gutters address the reported text-enlargement shrink.
- Selected shelf images total 712,977 bytes. This is image-file payload, not
  transfer measurement, first-paint timing or initial-viewport loading cost.
- QA forced lazy images eager to inspect the complete document. The first
  attempt instead waited for offscreen lazy images to decode and timed out.
  The instrument was corrected; that failed attempt is not a passing test.
- Screenshots were captured for all states; selected desktop, mobile and enlarged
  text layouts were visually inspected. Measurements do not establish visual
  perfection. No native zoom, physical device, DPR2 perception, screen-reader
  session or colour-fidelity validation is claimed.
- Raw numeric observations and output inventory accompany this source proposal
  under `evidence/`. `verify_delivery.py` is a local-session checker tied to its
  recorded localhost port and local measurements file, not a portable test gate.

## Initial open gate (historical; repaired source now received above)

CC's full ordered eleven-panel Powers account and its source anchor have been
requested in PR127 comment 5606575311. Do not infer missing subjects from the
partial review. This shelf is a presentation fixture only: it does not satisfy
FW's requirement to inherit Powers from a repaired, reviewed head. Original
PR127/129 heads have not been advanced by these local edits. No broad review or
merge should treat this fixture as accepted Powers integration.

The Vermeer image is a deliberately small acquired tier. Potential high-DPR
softness remains a sampling inference, not an observed perceptual failure here.
The tall Shen image is whole but small in the index; its dedicated page provides
space and the unchanged image link. Representation is not equivalent to looking
at the original object.

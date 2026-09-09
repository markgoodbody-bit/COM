# Harriet Powers: isolated work-page proposal

SOURCE ONLY / NOT PUBLISHED / NOT PART OF PREVIEW 0.8.4

Base: maintained PSFH `d28121c7fca9d064226670fc568dad57073c836c`.
Authority: Framework COM #108 comments `5604976850` (build) and `5605023335` (placement), within Mark's continuing project-work instruction.

## What changed

Before: one acquired image and its original observation receipt, no viewing copies or page.
After: exact acquired parent retained, two proportional viewing copies, a separately attributed successor provenance record, and one human work-page proposal.

All additions are confined to `proposals/powers/`. No normal site source, build, homepage, Explore map, edition, book, release or publication branch is changed. The separate build emits `/works/harriet-powers/` and `/art/` assets into ignored `outputs/powers-work-page/`. It deliberately does not connect the page to the live homepage. A possible later entry in “The work and its neighbours” requires review; no gallery/index is invented.

## Image custody

| File | Dimensions | Bytes | SHA-256 |
| --- | --- | --- | --- |
| bible-quilt-delivered.jpg | 2880 × 2412 | 2671829 | fd8280dd502f0fb21c4c030f9a018560d1928fe66a671edfccaadf9a13b0197d |
| bible-quilt-720.jpg | 720 × 603 | 201415 | c424b6927b35b4546850b317a303699cad952d1852d1e9c6d77dc246e29ba802 |
| bible-quilt-1440.jpg | 1440 × 1206 | 862531 | 816b56a1f0f650c882fa151b7c30d0a6e5d32fe218a70bfee675004b9bb9c59f |

The original `acquisition.json` is byte-preserved with SHA-256 `a78d84f490d0331724150ab6ac2a0cd8690ab067ddd214db7e8da360b9d2288f`; its acquisition-time unknowns have not been rewritten. `artwork.json` records Framework's later authoritative NMAH/Open Access observation with an exact comment and evidence commit. Codex did not independently recover those rights statements from the blocked acquisition metadata route. Master status remains UNKNOWN. Donor credit is not used as creator or image-author credit.

`prepare.py` is the recorded, network-free preparation recipe: Pillow 12.2.0 / JPEG 8.0, Lanczos proportional resize, quality85/86, chroma subsampling2, no optimization/progressive encoding, source ICC retained, no EXIF copied or orientation transform. No crop, retouch or generative operation. A second run reproduced the same derivative hashes. Do not silently regenerate with another encoder or repin the tests.

## Checks and their limits

Run from the site checkout:

```text
python proposals/powers/build.py
python -m unittest discover -s proposals/powers -p 'test_*.py'
```

Separate proposal build PASS; ten tests PASS, including deliberate parent/derivative corruption, receipt rewrite, master overclaim, collapsed rights attribution, detached parent, wrong fallback, script insertion and record/page drift. Parent and derivative hashes are pinned independently of the editable metadata. These are narrow integrity and contract checks, not an HTML security validator or proof of museum provenance.

All eight emitted files returned HTTP200 with exact byte counts and SHA-256 values from the local preview. `/works/harriet-powers/` returned HTTP200. This is local delivery evidence, not public PSFH readback.

The ordinary `npm run build` was also attempted and FAILED at the inherited `Source changed: llms.txt` pin in exact maintained d281. No tracked site source changed here. That known baseline mismatch is repaired separately in Preview0.8.4 RC `3f7803d27c3615d81ede643f153dc2ec20270e01`; it has not been silently cherry-picked into this art proposal. Do not describe the full maintained site build as green on this branch.

## Presentation judgement

Earned: the browser accessibility tree on the first route exposed the intended order: maker/work/date, unchanged-image link and visible credit, mediated museum account, then the separately labelled project response. The 720-pixel viewing copy was visually inspected: the delivered outer textile boundary remains visible. This is not a colour-fidelity or completeness authentication.

Provisional source-level judgement: desktop gives the complete work up to1136 CSS pixels across with prose below, not an image thumbnail beside framework text. At a390px viewport and default16px root type, the specified side padding leaves358px for the image; it remains proportional, with caption and text following in a single column. Rem-sized body text, wrapping links and no fixed-height image container are intended to tolerate enlarged text. These are CSS deductions, not observations of those rendered viewports.

UNRESOLVED: representative desktop/mobile screenshots and overflow/enlarged-text inspection. The available browser entry points returned the accessibility tree but no documented screenshot/resize controls. No alternative browser-control channel was improvised. CC is asked to provide that missing inspection alongside the independent source/interpretation review. Do not mark this rendering gate complete from the checks above.

## Interpretation boundary

No individual panel meanings are supplied. Powers's account is identified as mediated through Jennie Smith and the museum. The separate PSFH response is a provisional editorial choice about keeping that account within reach, not a discovered moral lesson, an intention attributed to Powers, museum endorsement, or reader-benefit evidence. Whether the page earns its place rather than becoming ornamental remains an independent review question.

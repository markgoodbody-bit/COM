# Harriet Powers: isolated work-page proposal

SOURCE ONLY / NOT PUBLISHED / NOT PART OF PREVIEW 0.8.4

Base branch: `codex/door-maintained-source-20260908`.
Original candidate reviewed at `fd4be44799c47bd4c0df6cf5c0bd470ca30f33d2`.
Independent four-part review: PR127 comment `5606429869` → `REPAIR_SMALL x4`, nothing false, nothing rights-unsafe.
Framework repair direction: COM #108 comment `5606571607`.

All files remain confined to `proposals/powers/`. No normal site source, homepage, Explore map, site edition, book, release or publication branch is changed.

## What the repair changes

The repair is deliberately bounded:

1. **Provenance:** remove the contradicted `3000x2512` advertisement and record what the museum surfaces now establish. The acquired 2880×2412 bytes are the museum's own High-resolution JPEG and match its IIIF canvas. The museum also offers a High-resolution TIFF. Whether that TIFF is a master remains UNKNOWN. Carry the museum Credit Line: `Gift of Mr. and Mrs. H. M. Heckman`.
2. **Powers's agency and title:** the museum records that Powers **insisted** Jennie Smith record exactly what each panel depicted. It also records Powers's own title for this quilt: *Adam and Eve in the Garden of Eden*.
3. **Maker account:** the page now carries the factual eleven-panel subject sequence itself instead of merely saying that an account exists. The list is a factual enumeration, not copied museum descriptive prose. PSFH supplies no new panel meanings.
4. **Presentation:** `main` keeps its `max-width` in `rem` but changes the horizontal gutter from `1rem` to fixed `16px`, removing the mechanism that made the artwork shrink on a 390px viewport when root text doubled.
5. **Project voice:** the PSFH response is reduced to two short sentences so the maker-account section no longer exists mainly as a preface to our own explanation.

`THE_MAKER'S_ACCOUNT != SPACE_RESERVED_FOR_THE_MAKER`

## Image custody

| File | Dimensions | Bytes | SHA-256 |
| --- | --- | --- | --- |
| bible-quilt-delivered.jpg | 2880 × 2412 | 2671829 | fd8280dd502f0fb21c4c030f9a018560d1928fe66a671edfccaadf9a13b0197d |
| bible-quilt-720.jpg | 720 × 603 | 201415 | c424b6927b35b4546850b317a303699cad952d1852d1e9c6d77dc246e29ba802 |
| bible-quilt-1440.jpg | 1440 × 1206 | 862531 | 816b56a1f0f650c882fa151b7c30d0a6e5d32fe218a70bfee675004b9bb9c59f |

Those image bytes are unchanged by this repair.

The corrected `acquisition.json` preserves the acquisition-time transport failures as historical observations and separately records the later authorised source resolution rather than allowing the earlier failures to stand as current metadata. The validator pins the corrected receipt and rejects later source-tier, credit-line or master-status inflation.

`prepare.py` remains the network-free viewing-copy recipe: Pillow 12.2.0 / JPEG 8.0, proportional Lanczos resize, quality 85/86, source ICC retained, no crop, retouch or generative operation.

## Recorded panel subjects

In the museum-recorded order from the top left:

1. Adam and Eve in the Garden of Eden
2. Paradise continued, with Eve and a son
3. Satan among seven stars
4. Cain killing Abel
5. Cain travelling to the land of Nod to find a wife
6. Jacob's dream
7. The baptism of Christ
8. The Crucifixion
9. Judas Iscariot and the thirty pieces of silver
10. The Last Supper
11. The Holy Family

Source: National Museum of American History object record `nmah_556462`. This is a concise factual enumeration, not a reproduction of the museum's surrounding descriptive prose.

## Checks and evidence ceiling

Normal isolated checks remain:

```text
python proposals/powers/build.py
python -m unittest discover -s proposals/powers -p 'test_*.py'
```

The repaired validator now also pins:
- museum source tier and Credit Line;
- Powers's recorded title;
- presence of all eleven subjects;
- maker-account-before-response ordering;
- exact parent and viewing-copy identities;
- the prohibition on silently promoting UNKNOWN master status.

There are now twelve targeted unit tests.

**Important:** this runtime edited the branch through the GitHub API and could not execute the local image-dependent build or browser rendering. Therefore the repaired head is **not yet build-green and not yet post-repair render-verified**.

Pre-repair measured evidence from Codex on `fd4be447...` remains useful for identifying the defect:
- 390px mobile / root16: image 358×299.813;
- 390px mobile / root32: image 326×273.016;
- no horizontal overflow in either case.

The source repair changes the causal declaration from `padding: 0 1rem` to `padding: 0 16px`. That is a source-level correction, not a substitute for rerunning the measured render on the repaired exact head.

`SOURCE_REPAIR != POST_REPAIR_MEASUREMENT`
`CSS_CAUSE_REMOVED != RENDER_OBSERVED`

## Interpretation boundary

Powers's account remains visibly mediated through Jennie Smith and the museum record. The page now carries her recorded title and the factual subjects she insisted be preserved, but it does not claim access to an unmediated transcript, infer new meanings for the panels, attribute PSFH values to Powers, or imply Smithsonian endorsement.

The page remains a review object. No merge, shelf inheritance or public wiring is authorised merely because these source repairs exist.

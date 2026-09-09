# Works collection preview: four available, Powers held out

SOURCE-ONLY / WORK IN PROGRESS / NOT FOR MERGE OR PUBLICATION

Base: maintained PSFH `e30debac2a8c32c37d2abfaa32e988c11fe98e79`.
Current purpose: review the discovery shelf and four complete available work routes while Harriet Powers remains a separately owned repair lineage.

## Current state

The current output contains four work pages plus the shelf index:

1. Johannes Vermeer — *The Geographer*
2. Anna Atkins — *Ulva lactuca*
3. Shen Zhou — *Anchorage on a rainy night*
4. Edmonia Lewis — *The Death of Cleopatra* (two distinct museum photographs)

Powers is not emitted: no Powers page, image, card or record appears in the current output. The shelf source must also not carry a private fork of Powers. The only valid future Powers input is the repaired PR127 lineage, currently `548e1fe316d1ccb58b3f4008097deb9d0dbe6c39` or a later exact successor after its remaining post-repair build/render evidence is recorded.

The initial local fixture did include an unrepaired Powers copy. That was a scope error even though the fixture was labelled WIP. Its old measurement/inventory files are retained under `initial-fixture-*` only as historical evidence. They are not current build inputs or current acceptance evidence.

`REPAIR_BEFORE_INHERITANCE`
`ONE_WORK_ONE_SOURCE_LINEAGE`

## What this shelf does

The shelf unifies discovery, not presentation.

- The index gives every work a route without ranking, likes, carousel, autoplay, infinite scroll or analytics.
- Images keep their complete supplied aspect ratio; the common shelf image area centres them without cropping.
- Each work opens onto a dedicated page with its own geometry and source account.
- Atkins retains the photographed book/page edges.
- Shen Zhou retains the complete supplied tall photograph, including pictured inscriptions. The museum poem/translation is linked, not reproduced.
- Lewis uses two different museum photographs of the same sculpture. They are not synthesized angles and are explicitly not presented as a complete three-dimensional encounter.
- The three newly built work records keep `project_response: null`.
- Vermeer remains an independent proposal imported through its own validator rather than being rewritten into a generic template.

No normal site source/build wiring, homepage/root, Explore map, edition, book, protocol, analytics, stateful machinery or public branch is changed.

## Source custody

The three new source identities remain pinned:

- Atkins source SHA-256 `ae5864af965af2d8a063016b1df67a9e765270281b9bc313513cde12d9f974a6`.
- Shen Zhou source SHA-256 `e9bc05358ce37ef9eae53dd5454fca797b1e1f43ba4dbdb9164e702493282004`.
- Lewis source photographs SHA-256 `d6494d0620ad68d9e35aaafda8d298891c783bfbc6cef21c729865fdb1230b28` and `e9b53e97cf3e7c9cf7bb0de851f6e6c4c14e6fb2b0c73f0591687cef521bca24`.

Four retained source parents and eight proportional viewing copies are committed for Atkins, Shen Zhou and Lewis. The builder checks parent hashes, decoded dimensions, derivative parent links, no upscale/crop geometry and retained ICC profiles. Museum-master status remains UNKNOWN for the new records.

Original acquisition observations remain distinct from later source reports. Nothing here promotes a downloaded or record-linked image to a museum master.

## Build and current evidence

From the checkout root:

```text
python proposals/vermeer/build.py
python proposals/works/build.py
python -m unittest discover -s proposals/vermeer -p test_proposal.py
python -m unittest discover -s proposals/works -p test_shelf.py
```

The corrected four-work handoff recorded:

- 28 exact current output routes;
- 30 automated checks before the later source-cleanup test was added;
- exact local HTTP byte/hash delivery for the recorded inventory;
- 20 browser states: shelf + four work pages at desktop/mobile and root 16/32;
- no measured horizontal overflow in those states;
- selected shelf images total 511,562 bytes.

The render evidence used Edge 152.0.4191.66, DPR1. Lazy images were forced eager for complete-document QA. That is not an initial-viewport network-load measurement, native browser zoom test, physical-device test, DPR2/perceptual sharpness test, screen-reader session or colour-fidelity validation.

Recorded dedicated-page image widths remain stable under root-text doubling. The discovery shelf likewise keeps the same image boxes when the root font changes. Shen Zhou is intentionally much narrower than the other works on the shelf because its full vertical aspect ratio is preserved inside the common discovery area; its dedicated page gives the work substantially more space.

## Known limits

- Vermeer uses a deliberately small authoritative record-linked image tier; high-DPR softness remains possible and has not been perceptually validated here.
- Shen Zhou's supplied photograph is whole but cannot substitute for examining the physical hanging scroll or every mounting element.
- Lewis's two photographs improve spatial understanding but do not constitute a full 3-D view.
- Index payload size is not paint timing or reader-benefit evidence.
- The shelf is not proof that the selected works form the right public collection.

## Powers boundary

PR127 has now advanced beyond the old shelf-local copy. Framework applied the independent `REPAIR_SMALL x4` findings at repaired head `548e1fe316d1ccb58b3f4008097deb9d0dbe6c39`:

- museum High-resolution JPEG / TIFF-above / master-UNKNOWN distinction;
- Smithsonian Credit Line;
- Powers's insistence that Jennie Smith record the panels;
- Powers's own recorded title;
- factual eleven-panel subject list;
- fixed-pixel mobile gutter;
- smaller PSFH response.

That source repair is complete, but its exact image-dependent post-repair build/render rerun remains open. Therefore Powers is still excluded from this shelf object. When that narrow evidence closes, the next five-work candidate must import from the exact repaired PR127 lineage rather than reconstructing Powers here.

## Review status

This four-work shelf is a useful source/product review object. It is not accepted for merge or publication. The next judgement is whether the shelf itself is a good quiet encounter with four different media; Powers integration is a separate final assembly step once its exact evidence boundary closes.

`SHELF_UNIFIES_DISCOVERY_NOT_PRESENTATION`
`FOUR_WORK_REVIEW != FIVE_WORK_RELEASE`
`SOURCE_READY != PUBLIC`

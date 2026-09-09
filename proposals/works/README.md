# Works collection preview: five works with repaired Powers

SOURCE-ONLY / WORK IN PROGRESS / NOT FOR MERGE OR PUBLICATION

Base: maintained PSFH `e30debac2a8c32c37d2abfaa32e988c11fe98e79`.
Current purpose: review the five-work discovery shelf. Powers is imported from its exact repaired lineage after the missing mechanical evidence was obtained.

## Current state

The current output contains five work pages plus the shelf index:

1. Harriet Powers — *Bible Quilt*
2. Johannes Vermeer — *The Geographer*
3. Anna Atkins — *Ulva lactuca*
4. Shen Zhou — *Anchorage on a rainy night*
5. Edmonia Lewis — *The Death of Cleopatra* (two distinct museum photographs)

All Powers proposal paths are identical to repaired PR127 `548e1fe316d1ccb58b3f4008097deb9d0dbe6c39`. Codex first built and rendered that detached checkout with the actual committed images: eight exact outputs/HTTP deliveries, twelve tests and four actual-image render states passed. Only then was it included here. The composite builder adds a stylesheet link and shelf-return navigation to emitted HTML; it does not rewrite the independent proposal source.

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
python proposals/powers/build.py
python proposals/works/build.py
python -m unittest discover -s proposals/powers -p test_powers.py
python -m unittest discover -s proposals/vermeer -p test_proposal.py
python -m unittest discover -s proposals/works -p test_shelf.py
```

Current output: `outputs/works-five-repaired/works/index.html`.

The repaired five-work handoff records:

- 36 exact current output routes;
- 33 automated checks (12 Powers, 10 Vermeer, 11 shelf);
- exact local HTTP byte/hash delivery for the recorded inventory;
- 24 browser states: shelf + five work pages at desktop/mobile and root 16/32;
- no measured horizontal overflow in those states;
- selected shelf images total 712,977 bytes.

Current observations use `repaired-five-` and `powers-548e1fe-` prefixes in `evidence/`. Unprefixed observations describe the prior four-work output; `initial-fixture-` records describe the earlier mistaken inheritance. They are preserved as history, not current acceptance evidence. The first initial-fixture browser attempt timed out on offscreen lazy-image decoding; corrected instrumentation is explicit below.

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

That source repair now has exact image-dependent build/render evidence. At390px, the actual quilt is358x299.8125 CSSpx for both root16 and root32; all eleven subjects precede the smaller response and no horizontal overflow was measured. This verifies the repair mechanism, not a new museum-source acquisition or a fresh independent CC review. The corrected acquisition receipt comes from FW's repaired lineage; its original version remains in Git history.

## Review status

FW's four-work KEEP review at PR131 comment5606952580, head `a9556623b544adbbba7812260af835586c488f1e`, remains attributed to that exact object. Its simultaneous source cleanup was preserved, then the newly verified Powers lineage added. This five-work successor is not accepted for merge or publication. No new CC review, public deployment or reader-benefit claim is implied.

`SHELF_UNIFIES_DISCOVERY_NOT_PRESENTATION`
`FOUR_WORK_REVIEW != FIVE_WORK_RELEASE`
`SOURCE_READY != PUBLIC`

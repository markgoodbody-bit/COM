# Feathered readability repair

Source basis: no-card candidate `190c9547bacf6928181d9120741b07150c51b33d`.
CC review: COM #108 comment5600049937, REPAIR_SMALL. FW5600027907 accepts the
composition direction conditionally on narrow review. Public589514f is unchanged.
This record is local evidence, not a publication or accessibility-conformance claim.

## Before / after

The high-left placement, H1/figure siblings, below-image credit, full painting,
all original/viewing-copy bytes, wording and routes are unchanged. A feathered
backing replaces reliance on the naturally dark pixels alone. No new asset or
machine entrance is introduced. Following FW5600097467, ordinary `src` now uses
the pinned1440px viewing copy; the unchanged museum original remains served,
hash-bound and explicitly linked. The offline build still embeds the720px copy.

The backing is one noninteractive pseudo-element behind the heading: 60% black,
expanded 2rem on every side. Two intersecting linear masks fade only the outer
1.5rem. The full-opacity region therefore includes the heading plus .5rem (8px at
the checked root size). Feathering occurs outside the text region. The backing
is translucent and remains in the upper canopy; it is not claimed to be invisible.

Below60rem the backing is disabled and title remains in its solid row. Engines
without subgrid OR intersecting masks receive ordinary image/credit/title flow
and a separate solid title panel. The fallback is in source, not an exercised
old-browser compatibility result.

## Calculation and actual coverage are different checks

White over a .60-black backing on the brightest possible sRGB background gives
a calculated floor of5.74:1. Using whole-image independent channel maxima gives
conservative bounds: original5.74:1,720px6.15:1,1440px5.83:1. The mobile row remains
17.39:1. This replaces the old fixed-text-rectangle pass condition. Original
no-card adverse results remain preserved in the preceding review directory.

These are sRGB alpha-compositing calculations, not sampled browser glyph pixels.
They require the declared backing to render behind the text with full mask
coverage. In the inspected browser, computed style showed alpha0.6, inset-32px,
24px feather stops and mask-composite intersect. All observed Range text-line
rectangles lay within the full-coverage heading-plus8px region at the three
desktop widths, including the small font-line overhang above the heading box.
An additional1440px read confirmed the fallback attribute and original link,
heading551.45x204.13px, image1260.80x785.37px, and scroll width1425px.

Requested viewport widths1600,1280,1024,375 produced widths1600,1280,1025,375.
Scroll widths1585,1265,1009,360 showed no horizontal overflow. Desktop image
selection was1440px; phone selection was720px after decoding completed. H1 remained
outside figure. The phone backing was disabled (`content:none`) and the title
followed the complete image. The two people and fire remained clear in inspected
desktop screenshots. No crop, input control or script was added.

| Requested width | Image width x height | Heading width x height | Saved screenshot |
| --- | --- | --- | --- |
|1600|1248.01 x777.40|559.74 x206.41|[Desktop](desktop.png)|
|1280|1162.16 x723.92|490.18 x183.91|[Intermediate](desktop-1280.png)|
|1024|927.13 x577.51|392.36 x151.99|Geometry only|
|375|328.01 x204.55|328.01 x190.61|[Phone](mobile.png)|

Limits: no universal viewport/font/translation guarantee, no text-only200% test,
no old-engine execution, no screen-reader study and no real-network timing claim.
The whole-container no-card contrast failure was a conservative warning, not
proof that every hypothetical reflow or every fallback browser actually failed.
This repair addresses the warning without upgrading those unobserved states.

## Verification

Build,11 Node and20 Python tests passed.115 generated files passed exact local
HTTP delivery checks before the fallback adjustment. The subsequent fallback edit
also changes root HTML and the offline substitution source; it does not change
the embedded offline image. Final test rerun is recorded in the COM return.

Generated standalone root preview:103,828bytes,
SHA256 `f47c69207e7c5658cdd97a67bdaded65e9adc854fb77fe7806358356cd116133`.
Manifest:7,084bytes,
SHA256 `9fae19bedaaf14d5590f7dbb31e6f38db961bae76089eb23763cd32f7c6ddab4`.
Root HTML is14,588bytes,
SHA256 `aff96c683dba2dffabefb3e96061c793840b74f0179f5332c4936d470e55d794`.

Narrow review requested against this successor, especially actual backing coverage
and preserved composition. The enlarged-page test was not completed before the
desktop-console incident took priority; publication remains held. The backing is
visibly darker and feathered, so acceptance of its visual weight is still a review
question, not a result established by the contrast calculation.
No public deployment has occurred in preparing it.

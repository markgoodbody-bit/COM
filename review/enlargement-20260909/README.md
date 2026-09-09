# Homer presentation: bounded layout successor

Basis: maintained60f6886; FW COM108/5601044283; Codex 9 September 2026.
Unpublished; exact CC review is still required.

## Before / after

- Before: viewport-only60rem fallback. Under a disposable root32px stress at
  requested1024px (reported1025), the title occupied y564–880 over an image
  y524–1102. Its feather extended further down toward the seated figure.
  No horizontal overflow, but composition was not acceptable.
- After: named inline-size container adds a60rem threshold that responds to
  the computed root size. The same stress places the title below the image,
  y1102–1454, with no image/title overlap. The caption follows it. Unsupported
  container engines use the existing separate-panel fallback.
- Before60% / after55% black plateau. Compared locally at1280 normal text;
  the lighter version preserves readable canopy placement and slightly more
  painting detail. This is visual judgement, not external validation.
- No text, image bytes, attribution, figure/H1 relationship, source routes or
  site edition changed. The test-only text override is not in product source.

## Earned checks

Normal root16px: observed widths390,640,1025 use separate row;1280/1600 use
canopy overlay. None of those measurements showed horizontal overflow.
The640px check is a half-width page-zoom layout PROXY, not actual browser zoom.
An attempted960px measurement returned stale390px geometry and is not evidence
for960; the raw normal geometry file retains that duplicate rather than hiding it.

Disposable root32px stress: observed1025,1280,1600 use separate title row,
with image bottom equal to title top (rounding tolerance), caption following,
and no horizontal overflow. This doubles the root size; fluid/clamped title
type does not necessarily double every glyph. It is a stress test only.

Screenshots from the supported in-app browser are included. The1024-labelled
stress image was captured after navigating to the introduction anchor, so
it shows the whole painting, separate title and credit rather than masthead.
Normal desktop and mobile screenshots use the document opening.

Build passed.11 Node tests passed, including115 exact local delivery checks.
20 Python tests passed after updating the test's explicit alpha from.60 to.55
and retaining the same >=4.5 contrast requirement. The worst white-background
sRGB plateau bound is4.76:1;720px viewing copy bound5.13;1440px bound4.83.
This mathematical bound presumes full opaque mask coverage beneath the glyphs;
it is not sampled browser pixels or universal accessibility conformance.

## Review boundary

Check the exact CSS fallback, title/painting/caption placement, scrim coverage
and old-engine branch. Original artwork remains unchanged. Normal dark-scheme
browser appearance was observed; no independent light-scheme screenshot,
native browser zoom, assistive-technology pass or external cold-reader result
is claimed. The story/guestbook/research work is not bundled.

Container implementation reference: [MDN size queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_size_and_style_queries).
The disposable local harness is preserved with this review for reproduction;
it serves a copied build on3001 and is not imported by the production build.

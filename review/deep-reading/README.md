# Deeper reading presentation candidate, 23 September 2026

Base: maintained source eafaf40e83d723e577a8cb78469a95946c334edd (D079).
Requested by Mark after the site-map inventory. This is a presentation candidate,
not a release entry. Framework retains publication ownership.

## Before / after

- Ten reading pages: boxed 48rem panel -> unboxed 42rem essay, 20px body at
  default root size, rem-based headings, more space around the question.
- Five artwork entrances: coloured stage and duplicate large page title ->
  theme-consistent whole-frame artwork, compact credit and one page title.
- Placement qualification: repeated visible project-centred paragraph ->
  neutral wording inside native `About this placement` disclosure.
- Credits and rights remain visible; canonical artwork pages remain linked.
- Source-format links move beneath `Sources and other formats`; destinations
  remain unchanged. Two museum views retain separate images and captions.
- No homepage HTML, source node JSON/Markdown, artwork bytes/records, licence,
  released document or archived snapshot changes.

## Checks

- Normal static build succeeds.
- 18 maintained/focused Node tests pass, including the new deep-reading suite.
- Nine Python resource/source-view tests pass.
- Local link check: 39 HTML pages, 688 references, 82 fragments, zero problems.
- Browser sample: Futures artwork and reading at desktop/default viewport;
  Futures reading and Lewis paired images at 320px. Images remain whole.
- All ten readings checked for horizontal overflow at 320px: none observed;
  one H1 each. No failed completed image observed during this check.
- These are one-engine observations, not a screen-reader, real-device or
  comprehensive zoom assessment. Final paired-image gap increased to 1.5rem
  after the first visual sample to separate stacked captions/images.

## Remaining site-map work

Published sitemap: 34 HTML pages and one PDF. All 34 returned HTTP200 during
the inventory; HTTP success is not visual quality.

1. Explore hub: simplify its six-section preamble and prioritise the map.
2. Five appeal-example pages: review hierarchy, consistent exits and spacing.
3. Six Works pages + gallery: compare image scale, captions and attribution.
4. Resources + four source readers: distinguish reading from raw-source views.
5. Worked revision, sources, challenge, discussion and change history.

Current art mapping: Homer/opening; Atkins/Explore; Vermeer/Partial views;
Powers/Significance; Shen Zhou/Futures; Lewis/Hardening. Six other readings
remain intentionally text-only. Frozen figure indexes are not redesign targets.

Unresolved: the large all-caps reading footer remains; source-bound status
wording needs a deliberate presentation decision, not silent removal. Existing
historical tests pin superseded layouts; this patch adds current regressions
without claiming that all historical suites pass.

# Local integration observation, 9 September 2026

Source-only work based on PR134's initial `10607eba19f92899bc03854c5796503cc1ecd83b`.
Not a publication and not yet evidence for Framework's concurrently edited PR134 head.

Before: first-five works required an isolated proposal build.
After: ordinary `npm run build` copies 36 pinned public-source files. One homepage
navigation link opens Works; the shelf has a homepage return and explicit selection
limits. All five work pages, their styles, art records and images retain the PR132
reviewed output bytes. Git attributes preserve the new copied bytes across checkout.

The former two-column mobile navigation split “Discussion” within a word at root32.
A single grid rule now permits one column when text needs it. No book, Homer,
opening prose, seed, rights, licence or project-source change.

Observed checks:

- Normal build passes; 16 Node checks and 22 existing Python checks pass.
- Preview server checks all154 built files by response bytes, plus directory aliases.
-435 local references across36 HTML pages and10 HTML anchors resolve locally.
- `renders.json`:28 states (homepage, shelf, five works;1440/390; root16/root32).
  JavaScript disabled, DPR1, actual images loaded. Whole-document geometry passes.
  These captures predate the final navigation-grid repair; the separate repaired
  homepage observation must be consulted. Work-page assets and styles did not change.
- `navigation.json`: native-link keyboard activation works from home to shelf,
  every work back to shelf, and shelf back home. Focus was set directly; not a
  complete Tab-order or screen-reader examination.
- Full-page screenshot capture failed in this runtime. Viewport captures succeeded.
  Do not present them as full-document manual visual review.

Concurrent source collision: Framework pushed an alternative generator and wrapper
normalizer to PR134 after the implementation handoff. This local implementation is
preserved separately rather than overwriting those changes. Evidence does not transfer
to its different output by assertion. No second PR or publication is requested.

Limit: normal public copies use the same asset Git blobs but duplicate checkout paths.
This is a tradeoff for a small, byte-preserving normal copier rather than a second
renderer. It is not a curation or reader-benefit finding.

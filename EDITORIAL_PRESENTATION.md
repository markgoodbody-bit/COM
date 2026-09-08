# Editorial presentation, Preview 0.8.2

Based on maintained source `3f5212e0a18627482ac972c6610a42a61ee54ee9` and public
`e0d765b3d203035971b5fa544eb5f5b48cc0f518`. Mark directly found that presentation
too basic and asked for much more within the existing constraints. The source
records the implementation; actual deployment and received public bytes are
separate observations in COM.

## Before and after

- Repeated rounded cards and a painting below the opening become a title/art
  composition, editorial columns, generous type and simple dividing rules.
- Four early navigation links reach existing choices/readings directly. The
  painting is not a required interaction and no text is hidden behind disclosure.
- Optional questions remain unordered, with local value-choice disclosure. They
  use three columns on wide screens, two at intermediate widths and one on phones.
- The explanation has a distinct reading column. Book introductions and sources
  have clear typographic hierarchy. Artist attribution is a separate quiet entry
  within the existing page, not another library or invented cultural claim.
- The shared CSS also improves reading-page typography. Raw sources, PDFs,
  paragraphs, original headings and link destinations are not rewritten.
- System fonts only; no browser scripts, animations, remote font fetches, tracking,
  forms, new artwork or schema. Existing project and art rights remain unchanged.

## Costs and limits

The painting moves before the detailed choices. This improves its prominence but
costs vertical space, particularly on mobile; Ways to begin is an early direct
jump to those choices. The museum JPEG remains exact and about 2.35 MB. Earlier
visibility may trigger its lazy load sooner. Neither trade-off is disguised as
faster access or measured reader benefit.

No separate non-public teaching/index code is included. This is a presentation
and navigation improvement, not theory, validation or a receiving service.

## Verification

An explicit regression compares every original paragraph and heading as a
multiset, ignoring only the changed edition label, and requires all original
destinations. It permits the declared relocation, not arbitrary content changes.
Existing checks cover exact source-text views, source/resource pins, local HTTP
output, image identity, static/no-form operation and declared contrast in both
themes. D013 is appended using the existing pinned history renderer; earlier
entries remain verbatim after the new entry.

Requested browser inspection covers desktop and mobile. It is a bounded layout
and navigation check, not a complete accessibility audit or a reader study.
The final 0.8.2 build was checked at 1440x1000 and 320x800 in the native dark-themed
browser. Neither overflowed horizontally (document widths 1425 and 305). The
first navigation row begins at y23.99 on desktop and y57.98 on mobile; mobile
navigation targets are about44 CSS pixels high. The detailed choices begin at
y771.28 and y1014.70 respectively. The mobile Ways to begin link landed on the
first choice at y0.16. The desktop artist link reached the correct entry with
the intact biography, source links and credit. Screenshots establish the opening
composition and mobile navigation; screenshot capture failed after two anchor
clicks, so those transitions have DOM evidence only. The viewport override was reset.

The final build, ten Node tests and eighteen Python tests passed, including exact
local delivery of all 113 output files. The lowest selected declared light/dark
text contrast pair is above4.5:1; that arithmetic is not conformance certification.
Light-theme browser behaviour, enlarged text and universal provider delivery
remain unestablished unless a later explicit record supplies those observations.

The already-recorded custom-domain safe-open refusal is not bypassed through
another transport. Source/publishing identity and hosting success must not be
reported as a fresh direct-domain root receipt.

## Attribution follow-through

FW5593126537 clarified that human authorship should be immediately legible rather
than mistaken for generated decoration. The exact title/artist/museum/public-domain
caption was moved above the image in DOM and visual order. The artist link and
unaltered image remain. A regression asserts attribution-before-image order.
This does not promise first-viewport visibility at every screen/text setting.

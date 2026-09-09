# Human artwork: source and viewing copies

This is a small delivery/provenance mechanism, not a new theory or curation system.

## Current integration edge — first five works, source only

Status: **SOURCE-ONLY INTEGRATION CANDIDATE / NOT PUBLISHED / NOT A CURATION CANON**

Exact reviewed source object: PR132 `dfe4b5fcfa279ef08a1d5aac5d3c3a1c59494175`, built from repaired Powers PR127 `548e1fe316d1ccb58b3f4008097deb9d0dbe6c39` and repaired Vermeer PR129 `36cc8c54e937318c61d2c317ff71c7f66bc38687`, with Anna Atkins, Shen Zhou and Edmonia Lewis retained from the kept five-work shelf.

The first five are a project-curated starting shelf, not a ranking, representative canon, completeness claim or diversity proof. Selection is an aperture: other creators, media, histories and affected perspectives remain outside this first view. Nothing about omission here establishes irrelevance or absence.

Current source-ready first five:

1. Harriet Powers — *Bible Quilt*;
2. Johannes Vermeer — *The Geographer*;
3. Anna Atkins — *Ulva lactuca*;
4. Shen Zhou — *Anchorage on a rainy night*;
5. Edmonia Lewis — *The Death of Cleopatra*, represented through two distinct museum photographs.

The homepage keeps Winslow Homer. The next normal-source candidate gives these five works an optional `/works/` route rather than turning the homepage into an image wall. The shelf unifies discovery, not presentation: each work keeps the geometry and source context appropriate to its medium. Lewis keeps two real museum views; no missing angle is synthesized.

Artwork is not evidence that TRACE or Mechanical Ethics is correct and is not required to illustrate either framework. A null project response is a valid editorial result. Powers carries the maker-linked recorded account because it materially changes what the page can preserve; any PSFH response remains visibly separate and smaller. Sources, institutions, rights, acquisition limits and reproduction limits stay visible per work.

The current reviewed source/evidence state is positive but bounded. PR132 records exact lineages, 33 combined tests, 36 exact local delivery checks and targeted fresh evidence for the Vermeer bytes that differ from the frozen measured assembly. Those checks establish source/build/presentation properties only; they do not establish reader benefit, representativeness, moral value, curation quality or public usefulness.

No public, root, edition or release mutation follows from this record. Normal-site integration must preserve the Door's voluntary reading and exit boundaries, add no feed/ranking/likes/carousel/autoplay/analytics, and earn its own normal-build, link, route, accessibility and render evidence before any publication decision.

`FIRST_FIVE != REPRESENTATIVE_FIVE`  
`SELECTED != COMPLETE`  
`ART_ENCOUNTER != FRAMEWORK_EVIDENCE`  
`SOURCE_READY != PUBLIC`

## Historical delivery and presentation notes

The sections below preserve earlier Homer/Vermeer delivery and presentation work in historical order. Their old current-state wording is not the live integration queue; the current integration edge above wins where states differ.

## Local readability successor, 9 September 2026

CC5600049937 requested a small contrast repair to the no-card candidate. The current
local successor preserves its placement and adds a 60%-black backing whose outer
edges fade, with full coverage throughout the heading and .5rem spare. This is not
the former opaque middle-left card. Narrow screens, and engines without either
subgrid or the required mask composition, keep a separate solid title row.

The sRGB calculation now covers the complete original and both viewing copies,
conditional on the backing being rendered at the checked coverage. Browser checks
include the previously missing 1280px intermediate width. No painting bytes, text
or routes changed. [Successor evidence](review/scrim-20260909/README.md) separates
calculation, observed geometry and untested cases. Publication still awaits the
narrow review; the public page remains589514f. FW5600027907 allows publication
after that review clears, not before. FW5600097467 adds a meaningful enlargement
check, still incomplete when desktop-console triage took priority. The ordinary
image fallback is now the pinned1440px copy, with the unchanged original linked.

## Earlier no-card candidate, 9 September 2026

Candidate only, not published. The public page remains Preview 0.8.3 at
`589514fff41d0a65315377093089838026bbd1ec`. Mark's screenshot review, relayed in
COM #108 comments 5599679905 and 5599831198, takes priority over further design work.

Before: the title sat in a hard black panel across the middle-left of the painting,
and the source credit appeared above it. After: white type sits high in the dark
canopy, with text shadow but no backing box. Credit follows the full image, aligned
right on desktop and left on narrow screens. The title moves below the image at
60rem or less. H1 and figure remain siblings; no words, art bytes or routes changed.

This uses FW's no-card direction, not its provisional CSS numbers. The 60rem
breakpoint is a conservative layout choice, not a demonstrated universal boundary.
The checked desktop viewing copies have sufficient contrast in the measured text
regions; that result does not extend to the full-resolution fallback or every
possible viewport, font or zoom. See the [review evidence and limitations](review/composition-20260909/README.md).
Visual acceptance and a narrow CC review are still required before publication.

## Published 0.8.3 integration, before this local correction

The completed initiative-cycle source5ff03dc supplies the original and two viewing
copies. This integration keeps those exact720/1440-pixel files rather than ship
the separate480/960/1600 set in the preserved local candidate3a1528e6.

The published full frame fills the opening. Above42rem the white title/question
sits in a local black74%-opacity panel over the painting; below42rem a solid dark
panel follows the complete frame. The local candidate above changes that placement.
There is no crop. Other pages do not inherit this image-background treatment.
Early navigation skips to the starting choices.

The source note distinguishes smaller viewing copies from the unchanged original.
The additional interpretation is explicitly project-authored, not attributed to
Homer. All non-art paragraphs and prior destinations are preserved by regression.

## One accepted record, checked copies

The original and every derivative have byte counts and SHA-256 identities. The
responsive record names its parent, source commit, date and preparation settings.
The normal Node build validates all accepted bytes before copying; it does not
resize art or silently regenerate identities. scripts/artwork.mjs is the small
shared copier. scripts/camp-fire.mjs supplies the accepted source fields used by
the visible page and generated art/camp-fire.json. No new runtime package is needed.
Unacquired or unreviewed art must not enter the accepted list.

The preserved derivatives were prepared by the initiative cycle using ImageMagick
6.9.11-60, Lanczos resizing, auto-orientation, stripped metadata, JPEG quality85
at720w and86 at1440w. They were not regenerated here. The master has no ICC profile
or EXIF orientation to strip. Resizing and re-encoding are lossy; viewing copies
are not the museum's original file. A changed encoder/output requires review.

FW5593496393 confirms5ff03dc as the integration base and retains the original
as the fallback for browsers without responsive-image support. Such a browser
can still load2.35MB. Modern source selection is not a universal payload ceiling.
CC must review the exact candidate before public publication.

Viewing copies are57,147 and255,138bytes; original2,350,423bytes. The sizes hint is
a conservative estimate of the existing CSS slots. Browser choice depends on
viewport, density, cache and implementation. The eager image may load below a short
viewport. The offline handoff embeds the720px copy with no responsive/preload
network image references. No real-network paint-time benefit is established.

## Record requirements

Human creator; work/title/date/medium; institution and authoritative source;
rights evidence; inspection/retrieval date; local original and hash; source-bound
derivatives/settings/hashes; alt text; visible credit; artist route; a clearly
project-authored interpretation distinct from artist intention where a project interpretation is actually used.

Use existing fields, not an art taxonomy. No bulk curation or machine image
payload. Choose each work's presentation; busy imagery under text or a repeated
background template is not the default. A project response may be null. An initial
selection is an aperture rather than a diversity or completeness claim. Future
selection should not stay inside the easiest rights category; living creators
require appropriate permission.

## Historical Vermeer acquisition note — superseded by repaired PR129 / PR132

The earlier acquisition pass below is preserved because it records the route that
failed before the later exact record-linked thumbnail was pinned and reviewed. It
must not be read as current Vermeer status.

Städel's [work record](https://sammlung.staedelmuseum.de/en/work/the-geographer)
identifies Johannes Vermeer, The Geographer,1669, oil on canvas, inventory1149,
acquired1885. Credit: Städel Museum, Frankfurt am Main. The reproduction is marked
Public Domain. Its [Digital Collection rights statement](https://www.staedelmuseum.de/de/bildnachweise)
permits reuse and links Public Domain Mark1.0, not CC0. The
[artist record](https://sammlung.staedelmuseum.de/en/person/vermeer-johannes)
identifies1632–1675, Delft. Sources inspected9 September2026 Europe/London.

The full-image download received a non-retryable safe-open refusal. No alternative
transport or inferred image URL bypassed it. At that stage no local original/hash
or responsive Vermeer set was established. A later bounded pass acquired the exact
record-linked 915×1024 thumbnail and PR129/PR132 now carry that current source
identity plus the reviewer-observed higher-resolution viewer limit. English/German
museum descriptions disagree about which geography appears on which cartographic
object; that detail is not repeated.

An earlier provisional project reading associated the painting with pausing among
maps and instruments. The current reviewed Vermeer work page deliberately carries
`project_response: null`: the painting does not need to become an illustration of
this project in order to belong beside it.

# PSFH human-art rolling set — third wave

Status: CURATION / SOURCE-ACQUISITION CANDIDATES / NOT PUBLICATION / NOT CANON
Date: 9 September 2026, Europe/London

This wave deliberately broadens both **medium** and **institutional custody**. It is not a target count and not a diversity scorecard.

`LOTS_OF_ART != ONE_MUSEUM_API`
`DIFFERENT_INSTITUTION != INDEPENDENT_TRUTH`
`MAKER_ATTRIBUTION_MUST_TRAVEL_WITH_THE_WORK`

## 16. Attributed to Nainsukh — *Raja Balwant Singh’s Vision of Krishna and Radha* — ca.1745–50 — opaque watercolor/ink/gold on paper

Institution: The Metropolitan Museum of Art.
Object: `38009` / `1994.377`.
`https://www.metmuseum.org/art/collection/search/38009`

The authoritative Met record attributes the painting to Nainsukh, identifies its Jasrota/Punjab Hills context, and exposes Public Domain + Download Image/Open Access.

The attribution qualifier is part of the identity. Do not collapse `Attributed to Nainsukh` into certain authorship. Do not turn threshold/devotion imagery into a PSFH metaphor.

Status: `ACQUISITION_CANDIDATE`.

## 17. Lala Deen Dayal — *The Great Elephant* —1885–1900 — albumen silver print from glass negative

Institution: The Metropolitan Museum of Art.
Object: `291060` / `2011.599.1b`.
`https://www.metmuseum.org/art/collection/search/291060`

The authoritative Met record identifies Lala Deen Dayal and marks the image Public Domain. Use the documented Met Open Access primary-image route if an exact source is returned.

This adds nineteenth-century Indian photography and a very different relationship between photographer, animal, spectacle and historical setting. Do not turn the elephant into a generic “scale” illustration.

Status: `ACQUISITION_CANDIDATE`.

## 18. Adelaide Alsop Robineau — *Vase* —1927 — porcelain

Institution: The Metropolitan Museum of Art.
Object: `487653` / `29.130.3`.
`https://www.metmuseum.org/art/collection/search/487653`

Authoritative record: designer Adelaide Alsop Robineau; porcelain;1927. The Met Open Access programme covers public-domain images where the API supplies them. Acquisition must establish an actual image route; the generic Open Access statement is not enough.

This is the first ceramic vessel in the rolling shelf. A photograph of a three-dimensional vessel is not the vessel; source records must keep that mediation visible. If the Met exposes several authoritative views, preserve them independently. Never synthesize rotation.

Status: `ACQUISITION_CANDIDATE_PENDING_IMAGE_ROUTE`.

## 19. Henry Ossawa Tanner — *The Canyon* — date not recorded — oil on canvas

Institution: Smithsonian American Art Museum.
Record: `saam_1983.95.183`.
`https://www.si.edu/object/canyon:saam_1983.95.183`

Smithsonian marks the media public domain / Restrictions & Rights CC0 and exposes IIIF/Open Access routes. The museum label associates the scene with Tanner’s Middle Eastern travel in1897–98; preserve that as museum account rather than project certainty.

Status: `ACQUISITION_CANDIDATE`.

## 20. Rachel Ruysch — *Still Life with Flowers in a Glass Vase* — c.1690–c.1720 — oil on canvas

Institution: Rijksmuseum.
Object number: `SK-A-354`.
Authoritative record:
`https://www.rijksmuseum.nl/en/collection/object/Still-Life-with-Flowers-in-a-Glass-Vase--210e3fc99bb8b3a875fcd7b57fce1a83`
Persistent object URL: `https://id.rijksmuseum.nl/200108485`.

Rijksmuseum record identifies Rachel Ruysch, medium/dimensions/signature and Copyright: Public domain.

Acquisition must use a documented Rijksmuseum image/download/IIIF route actually exposed for this object. Do not construct image CDN variants from HTML. If no exact reusable delivery route is available to the operator, return BLOCKED and keep the work in the horizon.

Status: `ACQUISITION_CANDIDATE_PENDING_IMAGE_ROUTE`.

## 21. Mary Cassatt — *The Black Hat* — ca.1890 — pastel on tan wove paper

Institution: National Gallery of Art, Washington.
Accession: `1985.64.81`.
`https://www.nga.gov/collection/art-object-page.66479.html`

The authoritative NGA record identifies Mary Cassatt, medium/dimensions/credit and provides Download; it states that the object’s media is free and in the public domain under NGA Open Access.

Presentation should retain the pastel/paper character rather than treat the image as another oil portrait. No project lesson about “identity” is required.

Status: `ACQUISITION_CANDIDATE`.

## Batch C execution boundary

Lower priority than Powers closure, the first-five `/works/` prototype and batch B. It may run opportunistically in parallel when the local acquisition lane is free.

For works16–21:
- use only documented authoritative museum download/Open Access/API/IIIF routes;
- preserve exact returned source bytes before any transformation;
- return `ACQUIRED | BLOCKED | SOURCE_TOO_SMALL` per work;
- record final URL/source category/status/MIME/dimensions/profile/orientation/bytes/SHA/object URL/rights observation;
- preserve attribution qualifiers exactly;
- `MUSEUM_MASTER_STATUS = UNKNOWN` unless explicitly established;
- for ceramics/objects, preserve separate authoritative views separately and never generate missing angles.

No public integration, no page-generation obligation and no claim that acquisition means curatorial acceptance.

The rolling horizon is now21 works. **21 is not a goal or stopping number.** The next useful work after this wave is implementation/review, not immediately finding work22.

`TWENTY_ONE != TARGET_TOTAL`
`CURATION_PAUSES_WHILE_PRESENTATION_CATCHES_UP`

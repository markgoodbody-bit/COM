# PSFH human-art rolling set — first ten works

Status: CURATION / ACQUISITION PIPELINE / NOT PUBLICATION / NOT CANON / NO AI-GENERATED ART
Date: 9 September 2026, Europe/London

Mark has explicitly said he would like to see **lots of art**. That changes the product boundary: a lightweight human **Works** shelf is now worth building. It does not change the provenance or non-wallpaper constraints.

The aim is not `MORE_IMAGES`. The aim is more human makers, media, periods, places and ways of seeing that can be encountered on their own terms.

`LOTS_OF_ART != WALLPAPER`
`WORKS_SHELF != ENGAGEMENT_FEED`
`CREATOR_ACCOUNT != PROJECT_INTERPRETATION`
`ACQUIRED_SOURCE_IMAGE != MUSEUM_MASTER`

## Public/product shape now authorised for source-only prototyping

A future `/works/` human route may become the quiet index for individual work pages.

Rules:
- the homepage keeps Homer as the opening composition; do not turn `/` into a gallery;
- each work gets its own `/works/<slug>/` page or another medium-appropriate presentation;
- no work enters the public index until exact source bytes, provenance, rights and presentation have been reviewed;
- index entries are creator/title/date/medium plus a restrained viewing image, not engagement cards or rankings;
- no likes, popularity counts, recommendation algorithm, infinite scroll, carousel, autoplay or analytics requirement;
- works may have a separately labelled `Why this spoke to us` / PSFH response, but that response is optional and should be cut when it weakens the work;
- museum/creator account must precede project interpretation;
- different media should be presented differently. A handscroll is not a portrait image; sculpture may need more than one museum-supplied view; a cyanotype does not need Homer's hero treatment;
- no AI-generated art or AI reconstruction on the actual site;
- acquire many in parallel, but public integration can happen in small reviewed batches.

A source-only `/works/` prototype may be built once it can point to at least three real acquired/reviewable work records. Do not create empty placeholders.

## Current first ten

### 1. Winslow Homer — *Camp Fire* — 1880 — oil on canvas

Status: **PUBLIC / ACCEPTED FIRST WORK**.
Institution: The Metropolitan Museum of Art.
Existing public presentation remains the opening. Do not duplicate it into a generic template.

### 2. Harriet Powers — *Bible Quilt* — 1885–1886 — textile/quilt

Status: **SOURCE ACQUIRED / WORK PAGE BUILT / MEASURED / INDEPENDENT EDITORIAL REVIEW OPEN**.
PR127 exact source: `fd4be44799c47bd4c0df6cf5c0bd470ca30f33d2`.
Smithsonian IDS-delivered source: 2880×2412 JPEG, SHA256 `fd8280dd502f0fb21c4c030f9a018560d1928fe66a671edfccaadf9a13b0197d`.
`MUSEUM_MASTER_STATUS = UNKNOWN`.
Measured desktop/mobile/doubled-root-text states now exist at COM evidence commit `0d4aa67dba6412420a575c2a19a993eb946f2779` with no observed horizontal overflow/crop/section-order defect.
Do not merge/public-wire until CC returns the independent art/provenance/editorial verdict.

### 3. Johannes Vermeer — *The Geographer* — 1669 — oil on canvas

Status: **EXACT AUTHORITATIVE RECORD-LINKED SOURCE ACQUIRED / PRESENTATION TO BUILD**.
Institution: Städel Museum, Frankfurt am Main.
Authoritative object page: `https://sammlung.staedelmuseum.de/en/work/the-geographer`.
Exact record-linked image: `https://cdn.staedelmuseum.de/images/49/7c/1149/thumb-xl.jpg`.
Acquired: HTTP 200 `image/jpeg`, 915×1024 RGB, 147,792 bytes, SHA256 `2eb8819e4afe22c219d7fbd01766e41338c5fbe460d0d41c250f8c698fd39106`, no ICC/EXIF orientation flag.
Source category: `AUTHORITATIVE_RECORD_LINKED_THUMB_XL`.
`MUSEUM_MASTER_STATUS = UNKNOWN`.
Native size is sufficient for a bounded presentation without upscaling. At ~148KB no smaller lossy copy is automatically justified.

### 4. Anna Atkins — *Ulva lactuca*, from *Photographs of British Algae: Cyanotype Impressions* — ca. 1853 — cyanotype

Status: **ACQUISITION CANDIDATE — AUTHORITATIVE PUBLIC-DOMAIN SOURCE VERIFIED**.
Institution: The Metropolitan Museum of Art.
Object: `https://www.metmuseum.org/art/collection/search/291638` / object ID `291638`.
The Met marks the image Public Domain and exposes Download Image under its Open Access programme.
Why this earns investigation: a radically different medium and mode of attention — specimen, light, process, classification and composition — without requiring a PSFH lesson.

### 5. Utagawa Hiroshige — *Sudden Shower over Shin-Ōhashi Bridge and Atake* — 1857 — woodblock print

Status: **ACQUISITION CANDIDATE — AUTHORITATIVE PUBLIC-DOMAIN SOURCE VERIFIED**.
Institution: The Metropolitan Museum of Art.
Object: `https://www.metmuseum.org/art/collection/search/55433` / object ID `55433`.
The Met marks the image Public Domain and exposes Download Image/Open Access.
Presentation should preserve the vertical print and its rain/bridge spatial rhythm; do not crop into a generic landscape banner.

### 6. Maria Sibylla Merian — *Study of Capers, Gorse, and a Beetle* — 1693 — watercolor and gouache on vellum

Status: **ACQUISITION CANDIDATE — AUTHORITATIVE PUBLIC-DOMAIN SOURCE VERIFIED**.
Institution: The Metropolitan Museum of Art.
Object: `https://www.metmuseum.org/art/collection/search/399922` / object ID `399922`.
The Met marks the image Public Domain and exposes Download Image/Open Access.
Different from Atkins: observation is rendered by hand and joins organism, plant and composition rather than photographic contact-print process.

### 7. Artemisia Gentileschi — *Esther before Ahasuerus* — 1620s — oil on canvas

Status: **ACQUISITION CANDIDATE — AUTHORITATIVE PUBLIC-DOMAIN SOURCE VERIFIED**.
Institution: The Metropolitan Museum of Art.
Object: `https://www.metmuseum.org/art/collection/search/436453` / object ID `436453`.
The Met marks the image Public Domain.
Do not reduce the work to a slogan about courage/power or to the artist's biography. The work must stand before any project response.

### 8. Shen Zhou — *Anchorage on a rainy night* — dated 1477 — hanging scroll, ink on paper

Status: **ACQUISITION CANDIDATE — AUTHORITATIVE PUBLIC-DOMAIN SOURCE VERIFIED**.
Institution: The Metropolitan Museum of Art.
Object: `https://www.metmuseum.org/art/collection/search/49549` / object ID `49549`.
The Met marks the image Public Domain and supplies the artist's poem/account in the object record.
Presentation must respect scroll format and inscription rather than flattening it into a square thumbnail-first experience.

### 9. José Guadalupe Posada — *Skeletons (calaveras) riding bicycles* — ca. 1891 — type-metal engraving

Status: **ACQUISITION CANDIDATE — AUTHORITATIVE PUBLIC-DOMAIN SOURCE VERIFIED**.
Institution: The Metropolitan Museum of Art.
Object: `https://www.metmuseum.org/art/collection/search/372097` / object ID `372097`.
The Met marks the image Public Domain and exposes Download Image/Open Access.
Chosen because it brings popular print culture, humour, movement and a different publication context; do not turn it into a death/mortality lesson for PSFH.

### 10. Edmonia Lewis — *The Death of Cleopatra* — carved 1876 — marble sculpture

Status: **ACQUISITION CANDIDATE — AUTHORITATIVE CC0 MEDIA VERIFIED**.
Institution: Smithsonian American Art Museum.
Object: `https://www.si.edu/object/untitled:saam_1994.17` / record `saam_1994.17`.
Smithsonian marks the media public domain/CC0 and exposes IIIF/open-access image routes.
This is the first sculpture in the rolling set. A source-only proposal should consider whether one museum image is enough to encounter a three-dimensional work; if authoritative multiple views are available, preserve their distinct identities instead of synthesising a turntable.

## Important blocked / worth-pursuing works

These are not rejected merely because acquisition is less convenient.

- **Olowe of Ise — Òpó (veranda post) with equestrian and female figure**, before 1938, Yoruba, The Met object 1996.558. The object record is compelling and names the artist, but The Met page currently says the image cannot be enlarged/full-screen/downloaded. Do not scrape or substitute an unverified reproduction. Search later for an authoritative reusable image route.
- **Bichitr — Jahangir Preferring a Sufi Shaikh to Kings**, ca. 1615–1618, Smithsonian National Museum of Asian Art F1942.15a. The object is strongly worth considering, but the current Smithsonian record says usage conditions apply. Keep research-only until image reuse terms are cleanly resolved.

`RIGHTS_FRICTION != ART_REJECTED`

## Next executable work

### Codex — acquisition batch A

Without touching public PSFH, acquire exact authoritative source images for works 4–10 where the documented museum route allows it.

For Met objects 291638, 55433, 399922, 436453, 49549 and 372097:
- use the object page's Download Image or documented Met Open Access API `primaryImage` route;
- do not infer neighbouring filenames;
- preserve exact returned bytes before transformation;
- record final URL/status/MIME/dimensions/profile/orientation/bytes/SHA256/object URL/rights observation;
- source category should name the actual route (`MET_OPEN_ACCESS_PRIMARY_IMAGE` or more precise);
- master/highest-resolution status remains UNKNOWN unless the museum explicitly establishes otherwise;
- do not resize yet unless a candidate is unreasonably large and a source-only viewing copy is actually useful; preserve source first.

For Smithsonian `saam_1994.17`:
- use the documented Open Access/IIIF media route only;
- preserve every acquired authoritative view separately; never generate missing angles;
- record the same custody fields.

Return each work independently as `ACQUIRED`, `BLOCKED`, or `SOURCE_TOO_SMALL`, so one failure does not block the batch.

### Codex — Vermeer page

Build a source-only Vermeer work-page candidate from the exact acquired 915×1024 source, without upscaling and without inventing a 720/1440 pair just for symmetry. Preserve Städel identity/credit/Public Domain evidence, source category and master-status ceiling. The project reading remains optional and visibly project-authored.

### Works shelf prototype

Once Powers, Vermeer and at least one newly acquired work have reviewable source records, build the smallest source-only `/works/` index prototype. It should demonstrate the information architecture with real records only. Do not wire it to the live root or `gh-pages` yet.

## Public release posture

Acquire broadly; publish deliberately.

A reasonable next public batch could contain Powers + Vermeer + one or two additional reviewed works and a quiet `/works/` route. Do not wait until all ten are perfect, and do not push every acquisition immediately.

`ACQUIRE_IN_PARALLEL`
`REVIEW_PER_WORK`
`PUBLISH_IN_SMALL_BATCHES`

# PSFH human-art rollout — Homer -> Vermeer -> broader set

Status: COORDINATION / SOURCE EVIDENCE / NO NEW PUBLICATION / NO EXTERNAL CONTACT / NOT A CURATION CANON
Date: 9 September 2026, Europe/London

## Purpose

Make the human-facing Door genuinely human without turning art into wallpaper, decoration or a rights-convenience catalogue.

Current maintained source `HUMAN_ART.md` is controlling for the existing implementation:
- Winslow Homer, *Camp Fire* (1880) is the accepted first work;
- Johannes Vermeer, *The Geographer* (1669) is the second proof, but its local asset remains incomplete;
- unacquired/unreviewed art must not enter the accepted list;
- each work needs creator/title/date/institution/source/rights, acquired bytes + hash, reviewed viewing copies, visible credit, artist route, and project interpretation kept distinct from artist intention;
- future selection should not remain only two historic European male painters or the easiest rights category.

`ART_INTEGRATED != ART_AS_WALLPAPER`
`FREE_TO_USE != CREATOR_SHOULD_DISAPPEAR`

## Fresh Städel source check — Vermeer

Fresh public-source check on 9 September 2026:

Authoritative object record:
`https://sammlung.staedelmuseum.de/en/work/the-geographer`

It currently identifies:
- Johannes Vermeer;
- *The Geographer*;
- 1669;
- oil on canvas;
- inventory 1149;
- Städel Museum, Frankfurt am Main;
- picture copyright: **Public Domain**;
- last object-record update: 14 July 2026.

The Städel Digital Collection concept page currently states that images of public-domain artworks are available for download free of charge, may be edited/remixed/shared/reproduced in any format and used for any purpose, with mention `Städel Museum, Frankfurt am Main`.

The object page currently exposes a record-linked image at:
`https://cdn.staedelmuseum.de/images/49/7c/1149/thumb-xl.jpg`

That URL is evidence that the image path is again reachable through the authoritative object page. It is **not** treated as the museum's full downloadable original merely because it is record-linked; it is explicitly named `thumb-xl` and is not enough to satisfy the maintained asset contract by itself.

The Städel OAI guide additionally states that image resources appear in LIDO `linkResource` and are available for download under CC BY-SA 4.0 with the Städel credit. The public OAI landing page currently asks for name/email registration before access. **Do not create an OAI account or infer an image URL from undocumented naming patterns for this task.**

## Next executable boundary — Vermeer asset proof

CODEX/local browser operator may perform one bounded acquisition attempt through the **documented Städel Digital Collection download control on the Vermeer object page**.

Allowed:
1. Open the authoritative Vermeer object page in an ordinary browser.
2. Use the museum-provided download control if it is available without account creation or new terms/identity submission.
3. Preserve exactly returned bytes before transformation.
4. Record final download URL only if the browser/museum actually supplies it; do not construct or guess it.
5. Record byte count, dimensions, MIME type and SHA-256.
6. Reconfirm rights/credit from the authoritative object/source pages.
7. Prepare source-only 720/1440 viewing copies using the established Homer delivery pattern, with separate hashes/settings, only after an original/downloaded master is established.
8. Return a source-only Vermeer record + proposed Explore/inset presentation for review. No public wiring or gh-pages publication yet.

Not allowed:
- guessing `original.jpg`, `download.jpg`, image API paths or CDN variants;
- using the accessible `thumb-xl` as if it were a verified full original;
- creating a Städel/OAI account;
- scraping around a refusal or bypassing museum access controls;
- changing Homer while acquiring Vermeer;
- bulk-curating more works before this second proof is complete.

If the official download control remains inaccessible, return `ASSET_BLOCKED` with exact observed evidence. That is a complete result.

## After Vermeer

Once the second proof is complete, the next art selection should deliberately broaden the human-cultural aperture rather than merely repeat the same provenance convenience.

Candidate selection should consider:
- creator/period/geography not already represented;
- a work that earns its place through the encounter rather than illustrating TRACE vocabulary;
- authoritative provenance and honest rights/custody;
- for a living creator, permission and credit route before public use;
- presentation chosen for the work itself rather than a repeated hero/background template.

Do not invent a fixed quota or bulk gallery. Add one work at a time when it adds a genuinely different human perspective.

`SECOND_PROOF_COMPLETE -> BROADEN_APERTURE`
`MORE_ART != MORE_WALLPAPER`
`RIGHTS_EASY != CURATORIALLY_RIGHT`

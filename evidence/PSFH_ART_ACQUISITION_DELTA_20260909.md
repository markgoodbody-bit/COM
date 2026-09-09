# PSFH human-art acquisition delta — Vermeer blocked, Harriet Powers opened

Status: SOURCE EVIDENCE / ACQUISITION COORDINATION / NO NEW PUBLICATION
Date: 9 September 2026, Europe/London

## Homer

Homer presentation is now publicly deployed at `gh-pages dd06d95cb880208b30f703c54af33c2440c97812` from exact maintained source `cfdacc4df35c4e536d58bba71a9dd4dc7693eb7b`.

Claude Code subsequently corrected one sentence in its pre-publication review: the reachable ordinary `img src` fallback is the pinned 1440px copy, not the museum original. The 1440 fallback change and the 55% feathered scrim both shipped. CC's corrected read-only verification says the publication remains KEEP and the actual 1440 fallback measured 9.89:1 in its named 1600-wide case. Keep all contrast claims bounded to named measured cases.

## Vermeer — ASSET_BLOCKED for this acquisition path

Authoritative object:
`https://sammlung.staedelmuseum.de/en/work/the-geographer`

Fresh bounded attempt in Framework's public-web aperture established:
- the object page is reachable and identifies Johannes Vermeer, *The Geographer*, 1669, Städel Museum, Public Domain;
- its record-linked image resolves only to `https://cdn.staedelmuseum.de/images/49/7c/1149/thumb-xl.jpg` through the available link surface;
- the page exposes no fetchable/documented full-download link to this aperture;
- a direct container download of the object page failed;
- no guessed CDN variant, OAI account, undocumented `original` path or access-control bypass was attempted.

Disposition for this lane: `ASSET_BLOCKED`.

The accessible `thumb-xl` remains useful visual/source evidence but is **not promoted to a verified full master**.

`RECORD_LINKED_THUMBNAIL != MASTER`
`ASSET_BLOCKED != RIGHTS_BLOCKED`

## Harriet Powers — next acquisition proof opened

Authoritative Smithsonian object:
`https://www.si.edu/object/1885-1886-harriet-powerss-bible-quilt:nmah_556462`

Smithsonian Learning Lab resource:
`https://learninglab.si.edu/resources/view/6249991`

Fresh source retrieval exposes the exact Smithsonian image identity:
- `image_id`: `NMAH-75-2984`
- official image service: `https://ids.si.edu/ids/deliveryService?id=NMAH-75-2984`
- thumbnail variant separately identified by Smithsonian;
- Learning Lab advertises high-resolution JPEG `3000x2512`, high-resolution TIFF, screen and thumbnail downloads and states the image is public domain;
- source: National Museum of American History.

Framework's web/cache and container could identify the official master service but could not fetch the binary bytes in this aperture. This is a tool-transport limit, not evidence that the Smithsonian asset is unavailable.

### Local acquisition authority

CODEX/local browser operator may now:
1. fetch the exact Smithsonian-delivered master from the official `NMAH-75-2984` service / documented Learning Lab high-resolution control;
2. preserve returned bytes unchanged and record final URL, MIME, dimensions, byte count and SHA-256;
3. preserve authoritative object metadata and the exact media-rights wording encountered at acquisition time;
4. create source-bound 720/1440 viewing copies using the established reviewed art-delivery method, recording settings/hashes;
5. build a **source-only** artwork record and one proposed human presentation for review.

Do not publish or wire it into PSFH yet. Do not infer a media licence from generic page boilerplate if the exact download surface says something different; preserve both and resolve before publication.

## Presentation boundary

Powers' quilt is not a diversity token or TRACE illustration. If it earns public use, creator/maker, medium, object history and Powers' own recorded panel meanings stay visible. Project interpretation remains separate.

`CREATOR_ACCOUNT != PROJECT_INTERPRETATION`
`HORIZON_CANDIDATE -> ACQUISITION_PROOF != ACCEPTED_ART`
`MORE_ART != MORE_WALLPAPER`

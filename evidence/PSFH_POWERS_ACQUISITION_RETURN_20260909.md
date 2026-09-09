# Harriet Powers acquisition: exact Smithsonian-delivered source image

Status: SOURCE-ONLY ACQUISITION ACCEPTED / MASTER STATUS UNKNOWN / NO PUBLICATION
Date: 9 September 2026
Original Codex acquisition basis: Framework direction `5604056609`; return `5604491852`; source evidence commit `106fe8acb69e2920b7b84e5175cdc913c56b699f`.
Framework gate correction: `5604591035`.

## Earned image result

The exact authorised Smithsonian IDS service returned HTTP200 and a decodable JPEG:

- Requested and observed final URL: `https://ids.si.edu/ids/deliveryService?id=NMAH-75-2984`
- Image identity: `NMAH-75-2984`
- MIME: `image/jpeg`
- Response Content-Length and actual file length: **2,671,829 bytes**
- Decoded dimensions: **2880 x 2412**, RGB; embedded ICC profile 560 bytes
- SHA-256: `fd8280dd502f0fb21c4c030f9a018560d1928fe66a671edfccaadf9a13b0197d`
- Local completed-file write time: `2026-09-09T15:30:49.9780387Z`
- Local carrier: `C:/Users/markg/Downloads/PSFH-Powers-source-proof-20260909/NMAH-75-2984-delivered.jpg`
- Local machine-readable receipt: sibling `acquisition.json`

Bytes are unchanged. Local visual inspection shows the textile with its outer boundary and surrounding background in the delivered frame. This is not a museum-authenticated colour-fidelity or completeness judgement. No cropping, retouching, transcoding or generative processing occurred in the acquired file.

The binary is preserved locally, not yet uploaded to COM or wired into PSFH.

## Source category and dimension mismatch

A prior Learning Lab observation advertised a 3000 x 2512 high-resolution JPEG. The exact IDS response is 2880 x 2412. The advertisement is therefore **not** a measurement of these delivered bytes.

Do not infer from HTTP200, file size or the advertisement that the delivered file is the Smithsonian's highest-resolution asset, original capture or museum master.

Disposition:

`DELIVERED_SOURCE_IMAGE = ESTABLISHED`

`MUSEUM_MASTER_STATUS = UNKNOWN`

The earlier gate required a complete master proof before derivatives. Framework has withdrawn that requirement as unnecessarily strong. Honest custody of the exact Smithsonian-delivered bytes plus authoritative rights/provenance is sufficient for a source-bound viewing-copy candidate. Unknown master status stays visible rather than being repaired by inference.

## Authoritative rights and object evidence — independently reacquired

After Codex's acquisition-time metadata routes were blocked, Framework independently reacquired the public authoritative records without bypassing those failures.

Current authoritative sources:

- National Museum of American History object record: `https://americanhistory.si.edu/collections/object/nmah_556462`
- Smithsonian object record: `https://www.si.edu/object/1885-1886-harriet-powerss-bible-quilt:nmah_556462`
- Smithsonian Open Access FAQ: `https://www.si.edu/openaccess/faq`
- Smithsonian Open Access: `https://www.si.edu/openaccess`

The NMAH object record identifies **Harriet Powers** as quilter and the work as *1885–1886 Harriet Powers's Bible Quilt*. It marks the media **public domain**, says it is free of copyright restrictions and may be copied, modified and distributed without contacting the Smithsonian, and routes to Smithsonian Open Access.

Smithsonian Open Access states that assets designated CC0 are dedicated to the public domain and may be used, transformed and shared without permission or fee, subject to any non-copyright rights or laws that might independently apply.

Smithsonian Collections Search results for Powers show this object with CC0 online media.

For PSFH provenance, use a visible institutional credit such as **National Museum of American History, Smithsonian Institution** and link the authoritative object/source and Open Access records even though CC0 does not require attribution. Do not confuse the object's donor credit line (`Gift of Mr. and Mrs. H. M. Heckman`) with image authorship or creator credit.

`FREE_TO_USE != CREATOR_SHOULD_DISAPPEAR`

## Creator account and interpretation boundary

The Smithsonian object record states that Powers explained each of the quilt's eleven panels before transfer and that Jennie Smith recorded those explanations. This is material provenance/history because it preserves a maker-linked account of the work.

Do not infer panel meanings from the image or silently replace the recorded account with PSFH interpretation. If panel meanings are quoted or paraphrased later, verify the exact museum/source wording at that time and distinguish:

1. Powers as maker;
2. the museum/historical record of her explanations and their mediation;
3. any separately labelled PSFH response.

`CREATOR_ACCOUNT != PROJECT_INTERPRETATION`

## Next source-only build boundary

Codex/local operator may now proceed from the already-preserved exact IDS file:

1. Prepare proportional 720w and 1440w viewing copies using the established reviewed art-delivery pattern. Record tool/version/settings, dimensions, byte counts, SHA-256 values and parent hash. Do not crop or generatively alter.
2. Prepare a source-only Powers artwork record containing creator/work/date/institution/object URL/Open Access/rights URLs/IDS source URL/actual dimensions/bytes/hash and an explicit `master_status: UNKNOWN` (or equally clear field).
3. Preserve the exact acquired 2880 x 2412 source file as the parent; do not label it master/highest resolution/original capture.
4. Add deterministic byte/provenance checks analogous to Homer where useful.
5. Return one source-only presentation candidate for independent review. **No public wiring yet.**

## Provisional presentation direction

Use a separate optional work page linked from an art/Explore route, not another homepage hero, random background or repeated Homer template.

Suggested order:

1. **Maker and work.** Harriet Powers and the quilt, with institution/source/rights visible outside the image.
2. **The maker's recorded account.** Route to the museum record and clearly state that Powers explained the panels and Smith recorded those explanations; do not invent or collapse the mediation.
3. **Our response.** A short separately labelled project response only after the maker/source account is within reach.

Let the whole textile be the principal object and keep prose/caption outside it. Reject the placement if it needs an imposed TRACE lesson or identity-token rationale to justify itself.

`POWERS_WORK_PAGE != SECOND_HOMER_TEMPLATE`

`MORE_ART != MORE_WALLPAPER`

## Residual limits

- Exact delivered bytes are established; museum-master status is not.
- Advertised 3000 x 2512 and delivered 2880 x 2412 remain distinct facts.
- Framework's authoritative rights check is a later independent source observation, not Codex's acquisition-time observation.
- Public CC0 status does not establish every conceivable non-copyright right in every jurisdiction.
- No public PSFH route, derivative, publication, external contact, account or spend is created by this record.

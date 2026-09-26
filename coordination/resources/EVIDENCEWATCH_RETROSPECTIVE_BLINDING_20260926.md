# EvidenceWatch retrospective challenge — blinded packet boundary

Date: 26 September 2026

Status: **BLINDING PREPARED / NO PACKET EXECUTION / NO MODEL OR PROVIDER RUN**

Purpose:

Prevent the frozen Brierley retrospective challenge from leaking the owner label into a later EvidenceWatch analysis path.

Builder:
`research/evidencewatch_retrospective/build_blinded_brierley_packet.py`

Inputs:
- exact owner `all_pairs.tsv` from the pinned Brierley repository commit;
- frozen challenge manifest already merged in COM.

Outputs are deliberately split:

```text
BLINDED PACKET
= opaque case_id
+ preprint abstract
+ published abstract

SEPARATE KEY
= case_id
+ DOI identities
+ owner label
+ positive/control role
+ source row
+ blind ordering hash
```

The packet contains no owner label, DOI, source row, role or blind salt.

Case order is independent of the owner label:
- fixed salt: `evidencewatch-brierley-blind-v1`;
- rank = SHA-256(salt + newline + preprint DOI);
- `case-001` ... `case-044` assigned after rank sort.

The script fails closed if:
- a selected DOI is absent or duplicated;
- a published DOI disagrees with the frozen manifest;
- either abstract is missing;
- packet and key paths collide;
- a known label/identity token leaks into the packet.

Both output files receive SHA-256 receipts.

Preserve:

```text
BLINDED_PACKET != VALIDATION
OWNER_LABEL_HIDDEN != MODEL_INDEPENDENCE_PROVED
RETROSPECTIVE_TEXT_PAIR != LIVE_WORKFLOW
GOOD_DISCRIMINATION != REVIEWER_BURDEN_REDUCTION
```

No output packet is committed here because the source abstracts are owner material and the packet can be reconstructed from the pinned owner dataset when a run is separately authorised.

No provider/model call, EvidenceWatch source mutation, grant submission or external contact is performed by this preparation.

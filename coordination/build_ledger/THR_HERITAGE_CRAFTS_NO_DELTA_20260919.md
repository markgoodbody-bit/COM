# THR — Heritage Crafts currentness no-delta / preservation ceiling

Date: 19 September 2026 — Europe/London

Status: FIELD CURRENTNESS CHECK / DRAFT MAINTENANCE PR / NOT RECORD EVIDENCE

## Target

Existing registered source:

`thr:source:2790ee98-28a4-4fca-bd80-b5b5484c47ef`

Heritage Crafts:
`https://heritagecrafts.org.uk/craft/sieve-and-riddle-making/`

Used by public record:
`sieve-riddle-revival`

## Fresh field result

A public retrieval surface checked on 19 September 2026 returned the Heritage Crafts page
still showing:

- `CRITICALLY ENDANGERED`;
- status `Critical`;
- 0 professionals using the craft as main income;
- 1 professional using the craft as side income;
- 1 trainee;
- 2025 Red List reviewer section present.

Load-bearing record result:

```text
CURRENT HERITAGE CRAFTS STATUS
= NO DELTA ON VISIBLE STATUS
```

The public Sieve/Riddle record and current-status assertion were not changed.

## Retrieval ceiling

The available retrieval aperture does not independently establish origin-server live HTTP
state or byte identity.

Therefore the draft source-check receipt uses:

```text
outcome = retrieval_surface_content_available
live_http_state = not_established
fingerprint = null
record_evidence_promoted = false
```

Preserve:

```text
SOURCE CHECK != RECORD EVIDENCE
RETRIEVAL SURFACE != LIVE ORIGIN
CRAWLED CONTENT AVAILABLE != LIVE TODAY
NO DELTA IN VISIBLE STATUS != BYTE IDENTITY
CURRENT OWNER STATUS != INDEPENDENT THR CENSUS
```

## Preservation lookup

A stronger-owner archive lookup was attempted through the available aperture.

- Memento TimeTravel endpoint: inaccessible through retrieval tool.
- Internet Archive CDX endpoint: inaccessible through retrieval tool.
- no archival/preservation route was established.

A separate search surfaced an older `heritage.wp-support.team` copy with different
maker/trainee counts.

That copy was **not** promoted into:
- a prior authoritative Heritage Crafts state;
- a preservation copy;
- a known temporal revision.

Its relationship/currentness was not established.

```text
DIFFERENT SURFACE VALUES != KNOWN TEMPORAL CHANGE
RELATED-LOOKING COPY != PRESERVATION ROUTE
```

Current preservation result:

```text
INSUFFICIENT EVIDENCE / NO ROUTE ESTABLISHED
```

## Draft maintenance PR

PR #53:
`THR: record Heritage Crafts currentness no-delta check`

Branch:
`framework/source-check-heritagecrafts-20260919`

Exact current head:
`22579e0306d7a432af2a5fc10169c5985ba3adc8`

Hosted:
`Validate Human Record integrity — run 160 / 35467624171 — SUCCESS`

Scope:
- one append-only operational source-check receipt;
- source-check registry updated date;
- no record/assertion/source/catalogue/human-view change;
- no evidence promotion.

Bounded semantic review requested on PR #53 comment:
`5745076242`

Current response:
PENDING.

## Related RFC lane

PR #52 remains separately held:
- exact head `d5621c7e701825bfd743b823aa1c97b352dec7cb`;
- run 157 SUCCESS;
- impact helper independent repair verification pending on comment `5745019308`.

Do not mix PR #53 currentness maintenance into RFC #52.

## Current next

```text
PR53 REVIEW PASS
-> ELIGIBLE FOR ROUTINE NO-DELTA MAINTENANCE DECISION

PR53 REPAIR
-> SMALLEST SEMANTIC REPAIR ONLY

PR52 VERIFIER PASS
-> STOP IMPACT-HELPER CHURN / RETURN TO FIELD PRESSURE

NO REVIEW RETURN
-> HOLD; DO NOT SUBSTITUTE FRAMEWORK AGREEMENT
```

# THR — Nepos edition preservation route merged

Date: 20 September 2026 — Europe/London

Status: MERGED PUBLIC MAINTENANCE / HISTORICAL FINDINGS UNCHANGED

## Public state

Human Record main:

`09013b2ec47aa1fc60ab7fbd011a33de296ffc83`

Merged PR:
#62 — `THR: identify preservation routes for Nepos edition`

Branch final head:
`628d2637798341dd5483ba059ed8b160f68f2982`

Hosted exact-head validation:
run 215 / `35476102293` — SUCCESS

Public records:
4 / unchanged count

Hannibal record version:
`0.1.1 -> 0.1.2`

No historical assertion or finding changed.

## Field pressure

Load-bearing Hannibal source:

`thr:source:8d40b5c1-3eb6-47d3-86e2-48e95853e930`

Dickinson College Commentaries:
Nepos, Life of Hannibal, chapter 13.

Before:

```text
preservation.status = not_yet_checked
```

Archive lookup through the available aperture did not establish a preserved copy of the
exact DCC chapter-13 web representation.

Stronger edition-level recoverability did emerge:

1. DCC chapter 13 directly links its "Get print book" route to Open Book Publishers.
2. Open Book Publishers identifies:
   - Dickinson College Commentaries volume 1;
   - Bret Mulligan;
   - DOI 10.11647/OBP.0068;
   - open-access formats;
   - contents including Text of Nepos' Life of Hannibal and Notes.
3. Library of Congress catalogues an unrestricted digital copy of the Bret Mulligan
   open-access book edition under LCCN 2019467885 / persistent handle.

Therefore the final merged state is deliberately narrower than the first candidate:

```text
institutional_preservation_route_identified
```

not:

```text
multiple_preservation_routes
```

Ceiling:

```text
RELATED EDITION RECOVERABLE
!= EXACT DCC WEB REPRESENTATION PRESERVED

INSTITUTIONAL COPY
!= BYTE-IDENTICAL DCC PAGE

PRESERVATION ROUTE
!= HISTORICAL TRUTH
```

## CI pressure / repairs

Initial candidate changed only `registry/sources.json`.

Run 211 failed because the public Hannibal machine record embeds the same source object and
the existing test requires registry/source copies to match.

Result:
- did not weaken the test;
- propagated the same bounded preservation state into
  `cases/hannibal-barca.json`;
- advanced record version to 0.1.2;
- exposed the recoverability boundary in the full human record and readable page;
- re-pinned catalogue and view-basis blobs.

Run 214 then failed because the Hannibal public-record test intentionally pinned
`record_version == 0.1.1`.

Result:
- advanced that exact expected version to 0.1.2;
- did not remove or generalise the version check.

Final run 215: SUCCESS.

## External review

Preservation review request:
- original comment 5746087631 against discarded broad `multiple_preservation_routes`
  candidate;
- superseding comment 5746099116 against final narrowed head.

No hostile return had landed before merge.

This was treated as optional answer-back rather than a release gate because:
- change is routine/reversible preservation maintenance;
- exact-head CI is green;
- field evidence and scope ceilings are explicit;
- no historical finding changes.

A later concrete adverse review should trigger correction, not retrospective silence.

## What this demonstrates

```text
LIVE URL
!= PRESERVED

FAILED EXACT-WEB ARCHIVE LOOKUP
!= NO RECOVERABILITY

RELATED PUBLISHED EDITION
+ STRONGER INSTITUTIONAL CUSTODY
-> BOUNDED RECOVERY ROUTE

RECOVERY ROUTE
!= SOURCE-REPRESENTATION IDENTITY
```

No THR-owned archival stack was added.

## Next

Do not re-run this DCC preservation quarry by momentum.

Useful next field pressure:
- exact DCC web capture appears;
- preservation route fails;
- publisher/library relationship changes;
- another load-bearing source has explicit preservation debt;
- real correction/challenge/contribution arrives.

```text
NEXT = STRONGEST UNRESOLVED LOAD-BEARING SOURCE PRESERVATION GAP
OR REAL EXTERNAL CORRECTION
```

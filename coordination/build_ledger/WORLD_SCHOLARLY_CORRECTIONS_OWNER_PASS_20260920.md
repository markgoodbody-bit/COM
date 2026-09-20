# WORLD / REAL USE — scholarly corrections owner pass

Date: 20 September 2026 — Europe/London

Status: **OWNER FOUND / NO THR DELTA / NO NEW TYPE**

## Pressure

Fresh world search tested the case where:
- a published work is corrected/retracted;
- downstream readers/copies/indexes may continue to carry or cite stale state.

## Strongest owners

Crossref / Crossmark already provide explicit post-publication update relations:
- correction notice -> original DOI;
- retraction notice -> original DOI;
- update metadata discoverable through Crossmark;
- original metadata can be updated to expose changed/retracted state.

Crossref's Retraction Watch dataset adds a second owner route for retractions and
some other update types when publisher deposits are incomplete.

BMJ and other publishers also explicitly push updated metadata to downstream
indexes such as PubMed and Web of Science.

## Project result

The material relation is real:

```text
SOURCE CORRECTED
!=
ALL DOWNSTREAM COPIES / INDEXES / CITATIONS CORRECTED
```

But scholarly publishing already has mature owners for:
- update/retraction identity;
- linked correction notices;
- DOI metadata propagation;
- index notification;
- retraction aggregation.

THR should interoperate where a record uses scholarly sources rather than create
parallel scholarly correction machinery.

```text
OWNER FOUND = YES
THR RECORD 5 = NO
THR TYPE/SCHEMA DELTA = NO
ME PATCH = NO
TRACE PATCH = NO
```

Potential THR use remains record-local:
if a cited scholarly source is corrected/retracted, preserve the source's update
relation and whether the THR finding needs review.

No external contact.
No account.
No outreach.

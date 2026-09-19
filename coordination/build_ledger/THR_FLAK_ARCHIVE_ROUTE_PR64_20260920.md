# THR field pressure — Westermann archival citation route

Date: 20 September 2026 — Europe/London

Status: DRAFT FIELD REPAIR / HOSTILE REVIEW PENDING / NO HISTORICAL VERDICT CHANGE

## Live baseline

THR main at branch point and last recheck:

`09013b2ec47aa1fc60ab7fbd011a33de296ffc83`

Public record count remains four.

The flak record on main is v0.2.7 before this candidate.

## Real field delta

A re-read of the already checked Westermann reproduction recovered footnote 75 precisely.

Westermann cites:

- “Abschlussmeldung über Flakartillerie im Bereich des Gen.d.Lw.Ob.d.H.” — 28 February 1942 — N 529/Folder 7, BA-MA;
- “Tagesbefehl des Flakregiments 102” — 8 July 1940 — RL 12/Folder 457, BA-MA;
- plus Koch.

Independent inspectable catalogue evidence from Deutsche Digitale Bibliothek / Bundesarchiv identifies `BArch RL 12/457` as Flak-Regiment 102 material from May/July 1940 and describes:
- a 14 May 1940 war-diary extract with map sketch;
- an 8 July 1940 daily order.

The exact N 529/7 document title has **not** been independently recovered from an archive catalogue in this aperture. It is preserved as Westermann's citation wording only.

Therefore:

```text
N 529/7 TITLE = RECOVERED FROM WESTERMANN NOTE

RL 12/457 IDENTITY / DATE CLASS
= INDEPENDENTLY MATCHED AT DDB/BUNDESARCHIV CATALOGUE LEVEL

ARCHIVAL PAGES = NOT INSPECTED

WHICH ARCHIVAL STATEMENT SUPPORTS 60 / 890
= UNKNOWN
```

## Candidate PR

Draft PR #64:
`THR: narrow Westermann archival citation route`

Exact current head:
`45114e248a5e7bb52313a0aefd4c3f02105598f0`

Hosted integrity:
run 220 / `35477129788` — SUCCESS

Base main:
`09013b2ec47aa1fc60ab7fbd011a33de296ffc83`

Mergeable:
YES at latest PR metadata check.

Files changed:
- `cases/viral-flak-claim.md`
- `cases/viral-flak-claim.json`
- `registry/assertions.json`
- `records/flak-claim.html`
- `records/catalog.json`

Candidate record version:
`0.2.8`

Claim state remains:

```text
UNSUPPORTED_IN_SOURCES_CHECKED
TRUE AGGREGATE RATE = UNKNOWN
```

## Wording self-repair

An ambiguous catalogue summary initially risked implying that both N 529/7 and RL 12/457 were independently catalogue-matched.

Current wording now distinguishes:
- N 529/7 report = recovered from Westermann's note;
- RL 12/457 daily order = independently matched at DDB/Bundesarchiv catalogue level.

This is why current exact head is `45114e24...`, not the earlier green `c2637ca...`.

## Hostile review

Initial bounded review request:
PR #64 comment `5746201721`

Exact-head target update:
comment `5746211462`

Requested verdict:
- PASS_WITH_CEILINGS; or
- smallest concrete REPAIR.

No independent return had landed at the last check.

## Original contribution ancestry

Issue #20 received field continuation comment:
`5746204156`

This preserves that:
- the original Grok contribution was a research lead;
- Codex recovered bibliographic/passage material;
- Framework performed this archive-route follow-up;
- later work is not retroactively attributed to Grok.

## Stronger-owner operational next hop

Official Bundesarchiv guidance gives three routes for non-digitized military archival material:
1. Freiburg reading room;
2. private research service;
3. Digitisierung on demand.

Military Archive contact:
`militaerarchiv@bundesarchiv.de`

The exact bounded research target is now:

```text
N 529/7
"Abschlussmeldung über Flakartillerie im Bereich des Gen.d.Lw.Ob.d.H."
28 February 1942

RL 12/457
"Tagesbefehl des Flakregiments 102"
8 July 1940
```

Question:

> Do the cited archival pages contain the underlying basis for Westermann's reported 60 officer / 890 enlisted flak-force casualties for 10 May–22 June 1940?

No external archive request has been sent.

Preserve:

```text
ACCESS ROUTE IDENTIFIED != DOCUMENT INSPECTED
DIGITISATION REQUEST != EVIDENCE
ARCHIVE STAFF RESPONSE != HISTORICAL VERDICT
```

## Next

```text
FIRST:
FOLLOW PR #64 HOSTILE REVIEW

IF REPAIR:
-> SMALLEST FIX + EXACT-HEAD REVALIDATION

IF PASS_WITH_CEILINGS:
-> RELEASE DECISION STILL SEPARATE

PARALLEL REAL-WORLD NEXT HOP:
-> BOUNDED BUNDESARCHIV REQUEST FOR N 529/7 + RL 12/457
   ONLY THROUGH EXPLICIT EXTERNAL-CONTACT GATE

NO FIFTH RECORD
NO NEW GLOBAL TYPE
NO CLAIM VERDICT BY MOMENTUM
```

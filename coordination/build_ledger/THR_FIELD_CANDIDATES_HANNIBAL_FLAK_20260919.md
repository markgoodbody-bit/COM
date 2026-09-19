# THR field candidates — Hannibal lemma repair + Westermann targeted search

Date: 19 September 2026 — Europe/London

Status: TWO DRAFT FIELD CANDIDATES / PUBLIC MAIN UNCHANGED / NOT CANON

## Public baseline

Current public THR main:

`6e5a2eff69e17e85a743d54501eac4ab0a1d527b`

Exactly four public records.

No public merge from the two candidates below has occurred.

---

## Candidate A — Hannibal / Polybius Greek vocabulary index

Draft PR #57:
`THR: narrow Hannibal Greek source-literal boundary`

Current exact head:
`99e2cbb8fd3dc07ec0316970ff50460f9d463cdc`

Hosted:
`Validate Human Record integrity — run 187 / 35471893328 — SUCCESS`

### First candidate defect

Initial candidate treated the Perseus passage-vocabulary output as direct source-literal
attestation:

```text
3.33.17 / 3.33.18
-> Ἀννίβας
-> SOURCE LITERAL ATTESTED
```

Codex bounded review comment `5745577355` returned **REPAIR**.

The vocabulary page explicitly exposes lemma/index output. Codex separately reported that
the underlying Greek XML has inflected `Ἀννίβου` in both cited sections.

Therefore the earlier formulation was an evidence upgrade.

### Current repaired claim

Framework chose the smaller repair route: preserve only what Framework directly observed
from the vocabulary pages.

```text
PASSAGE VOCABULARY INDEX
-> ASSOCIATES 3.33.17 AND 3.33.18 WITH LEMMA Ἀννίβας

VOCABULARY LEMMA != SOURCE-LITERAL SPELLING

FRAMEWORK DIRECT INSPECTION OF INFLECTED GREEK SOURCE TEXT
= NOT ESTABLISHED
```

Repairs carried through:
- source registry;
- entity note;
- mention candidate basis;
- machine record;
- Markdown record;
- human view;
- catalogue summary/pins.

The record now distinguishes:
- 2 ancient-text reading surfaces;
- 1 derived Perseus vocabulary/index surface.

It does **not** count the vocabulary index as a third ancient text or independent witness.

Follow-up verification request remains on PR #57 comment `5745550856`.

Disposition pending:
`PASS_WITH_CEILINGS` or smallest remaining `REPAIR`.

No merge approval has been inferred.

---

## Candidate B — flak / Westermann targeted full-text search

Draft PR #58:
`THR: narrow Westermann book-wide search boundary`

Current exact head:
`adbf50ee80ed9e5ed0e516010b7b99dad631db65`

Hosted:
`Validate Human Record integrity — run 182 / 35471799195 — SUCCESS`

### Field delta

A targeted text/OCR search of an accessible full third-party Westermann reproduction found:

1. an **80-percent flak-casualty** passage in RAF/Bomber Command operational-research
   context — Allied aircraft/aircrew casualties over target areas, not German flak crew
   mortality;

2. a late-1944 German ground-based air-defense force strength of **1,110,900 persons**,
   including 448,700 from outside the Luftwaffe — a personnel snapshot, not a whole-war
   mortality denominator;

3. the known May–June 1940 German flak casualty passage remains **dead + wounded +
   missing**, not deaths;

4. no literal OCR match for `mortality` — preserved only as a search result, not proof
   of semantic absence.

Current record implication:

```text
SAME NUMBER != SAME POPULATION
SAME NUMBER != SAME MEASURE
NUMERICAL PROXIMITY != TRANSMISSION
TARGETED SEARCH != EXHAUSTIVE BOOK REVIEW
THIRD-PARTY REPRODUCTION != AUTHENTICATED EDITION
```

The prior custos hypothesis that an Allied flak statistic may have been transposed into
the viral German-crew claim is **narrowed by a concrete nearby 80-percent occurrence but
remains unresolved**. No ancestry/transmission is asserted.

The claim remains:

`unsupported_in_sources_checked`

Historical truth remains:

`unknown`

Hostile review requested on PR #58 comment `5745578189`.

Disposition pending:
`PASS_WITH_CEILINGS` or smallest `REPAIR`.

No merge approval has been inferred.

---

## Overmans follow-up

A fresh search confirmed:
- primary Google Books metadata exposes organisation-level death/loss tables;
- a secondary dissertation reproduces an Overmans p.255 table with approximately
  433,000 Luftwaffe deaths.

But:

```text
LUFTWAFFE != FLAK CREWS
SECONDARY TABLE REPRODUCTION != DIRECT PRIMARY TABLE INSPECTION
```

The primary p.255 values were not directly inspectable in this aperture.

Disposition:

`NO DELTA`

Do not add the 433,000 figure to THR merely because it is available second-hand.

---

## Bundesarchiv follow-up

BArch / Deutsche Digitale Bibliothek confirms:
- `BArch RL 12/457`;
- Flak-Regiment 102;
- May / July 1940;
- Kriegstagebuch extract and related material.

This corroborates the archival route already preserved in THR. It does not expose or
independently verify Westermann's casualty count in the material inspected here.

Disposition:

`NO NEW CASUALTY EVIDENCE`

---

## Current next

```text
FIRST:
FOLLOW #57 + #58 HOSTILE REVIEW RETURNS

#57 PASS
-> CONSIDER BOUNDED PUBLIC MERGE DECISION
#57 REPAIR
-> SMALLEST SEMANTIC FIX

#58 PASS
-> CONSIDER BOUNDED PUBLIC MERGE DECISION
#58 REPAIR
-> SMALLEST EVIDENCE/SCOPE FIX

MEANWHILE:
CONTINUE REAL FIELD SOURCE WORK
NO FIFTH RECORD
NO RFC POLISH
NO SECONDARY NUMBER BY MOMENTUM
```

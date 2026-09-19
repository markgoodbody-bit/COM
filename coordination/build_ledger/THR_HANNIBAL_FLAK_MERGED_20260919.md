# THR — Hannibal and flak field repairs merged

Date: 19 September 2026 — Europe/London

Status: PUBLIC MAIN UPDATED / FOUR RECORDS / FIELD REPAIRS ONLY

## Public main

Exact THR main:

`29acc6ee090fc0b2897e90a2fc33efeb41cc2770`

Recent merge sequence:

1. PR #57 — Hannibal Greek vocabulary-index/source-literal boundary
   - merge commit `913daba7de05cfac72ed17182508a5018eeb0514`
2. PR #58 — Westermann targeted-search boundary
   - merge commit `29acc6ee090fc0b2897e90a2fc33efeb41cc2770`

Public record count remains exactly 4.

Shared current counts:
- sources: 27
- assertions: 8

## Hannibal

Current record version:

`0.1.1`

Current bounded result:

```text
PERSEUS PASSAGE VOCABULARY INDEX
-> ASSOCIATES 3.33.17–18 WITH LEMMA Ἀννίβας

VOCABULARY LEMMA != SOURCE-LITERAL SPELLING
FRAMEWORK DIRECT INSPECTION OF INFLECTED GREEK SOURCE TEXT = NOT ESTABLISHED
PASSAGE INDEX != MANUSCRIPT WITNESS
```

Codex found and helped repair an earlier semantic over-upgrade from lemma index to exact
source-text form, then found two stale reader-facing remnants. Those were repaired.

Exact repaired candidate head before merge:
`02e03871fe824196a6966d53f44dbb69fe09e597`

Hosted validation:
run 206 / `35474605004` SUCCESS.

No fifth record, no identity upgrade, no manuscript claim.

## Flak

Current record version:

`0.2.7`

Current status:

`unsupported_in_sources_checked`

Historical truth status:

`unknown`

Westermann targeted-search result now preserves:

```text
"UP TO 80 PERCENT OF FLAK CASUALTIES"
-> RAF / BOMBER COMMAND CASUALTY CONTEXT
-> NOT GERMAN FLAK-CREW MORTALITY

1,110,900 PERSONS
-> LATE-1944 GROUND-BASED AIR-DEFENSE PERSONNEL STRENGTH
-> NOT DEATH NUMERATOR
-> NOT WHOLE-WAR MORTALITY DENOMINATOR
```

Codex independently inspected the checked third-party PDF carrier and supplied bounded
reproducibility locators:
- carrier PDF page 96 (one-based), section “The RAF's Reaction to the Luftwaffe's Air Defense Initiatives”;
- carrier PDF page 183 (one-based), section “The State of the Flak Arm”.

These are carrier-page locators, not authenticated publisher pagination.

Codex also caught one inference overreach:
“strengthens a previously recorded ancestry hypothesis”.

That was narrowed to:
the passage is a concrete candidate to investigate under the existing ancestry hypothesis;
no evidence links it to the viral claim or ranks it above other possible origins.

Exact combined candidate head before merge:
`d0bf1e860afd62e4c9ce91984ca734641abf3618`

Hosted validation against post-PR57 main:
run 209 / `35474751920` SUCCESS.

Preserve:

```text
SAME NUMBER != SAME POPULATION OR MEASURE
NUMERICAL PROXIMITY != TRANSMISSION
TARGETED SEARCH != EXHAUSTIVE BOOK REVIEW
THIRD-PARTY REPRODUCTION != AUTHENTICATED EDITION
UNSUPPORTED_IN_SOURCES_CHECKED != PROVED_FALSE
```

## Current strongest unresolved field gap

Flak claim ancestry remains unresolved.

The live question is not:
“What nearby 80-percent statistic exists?”

It is:

> Where did the specific German flak-crew mortality claim come from before the visible
> August 2025 online chain, if anywhere?

Current result remains:

```text
VISIBLE PROPAGATION CHAIN = PARTIAL
PRE-AUGUST-2025 ORIGIN = UNRESOLVED
WESTERMANN TRANSMISSION = NOT ESTABLISHED
TRUE AGGREGATE MORTALITY RATE = UNKNOWN
```

## Next

```text
SEARCH EARLIER SOURCE ANCESTRY
-> EXACT / NEAR-EXACT FORMULATIONS
-> ENGLISH + GERMAN
-> ARCHIVE / VIDEO / FORUM / BOOK-CITATION ROUTES

IF EARLIER OWNER FOUND
-> INSPECT / RECORD BOUNDED DELTA

IF NO STRONGER SOURCE
-> NO DELTA / KEEP ORIGIN UNKNOWN
```

Do not invent an ancestor from numerical similarity.
Do not produce a replacement mortality estimate.

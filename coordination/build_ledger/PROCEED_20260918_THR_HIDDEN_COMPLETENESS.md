# PROCEED — THR hidden-completeness bounded repair

Status: **BOUNDED BUILD RECEIPT / NOT CANON / NOT MERGE AUTHORITY / NOT VALIDATION**  
Date: 18 September 2026

## Context

ATRS #364 independent relation calibration remained pending with no first-pass table observed during this pass. Framework therefore did not add new ATRS interpretation.

THR PR #32 observation-state fail-closed repair remained draft / green / hostile-review pending.

The next independent THR pressure came from the already-returned hidden-completeness attack:

```text
A_LIST_WITHOUT_ITS_SEARCH_CAN_IMPLY_COMPLETENESS
```

## Owner subtraction

Strong systematic-review owners already exist.

PRISMA / PRISMA-S / Cochrane require detailed reporting of information sources searched and search methods so readers can assess completeness and reproduce search processes.

THR is not a systematic-review engine. No PRISMA schema or search ontology was adopted.

Existing THR objects already preserve substantial boundedness:
- flak record lists unexamined books/archives and says archive search is not exhaustive;
- JFK fixture states it is a bounded selected representation probe rather than a survey;
- Hannibal probe is explicitly one bounded source check.

## Executable local defect

Despite that prose, the assertion validator allowed:

```text
state = unsupported_in_sources_checked
evidence.source_ids = []
evidence.observation_ids = []
-> PASS
```

This is a structural contradiction: the state says sources were checked while no checked source aperture exists.

## Draft repair

Human Record PR #33:

`https://github.com/markgoodbody-bit/human-record/pull/33`

Exact head:

`1b332ece1571705a2fbaf16ec843a1794928d983`

Repair:
- `unsupported_in_sources_checked` requires a non-empty source list;
- requires a non-empty observation list;
- every source counted as checked must own at least one listed evidence observation;
- source-only evidence remains allowed for other states;
- record contract now states that negative/unsupported findings should expose the bounded checked aperture and material unexamined leads;
- no universal search schema or completeness score.

Exact verification:

```text
workflow = 35326431061 SUCCESS
job = 105540438211 SUCCESS
validate_all = PASS
test_validate*.py = 67 tests / OK
existing open-vocabulary warnings = 11
```

The current production flak cross-record assertion already satisfies the new rule. No production assertion was edited.

## Review status

PR #33 remains:

```text
DRAFT
GREEN
UNMERGED
HOSTILE_REVIEW_PENDING
```

Hostile review requested:
- find legitimate checked-source use with no observation object;
- find a false sense of completeness that still passes;
- argue state belongs only in record-local structure;
- show owner analogy overreaches;
- provide smaller rule.

THR issue #31 also exposes PR33 as public break target comment `5727598402`.

PR32 and PR33 remain sibling repairs stacked on PR30. Do not merge them together by momentum.

## Ceilings

```text
EMPTY_CHECKED_SET != UNSUPPORTED_FINDING
SOURCES_CHECKED != ALL_POSSIBLE_SOURCES
NOT_FOUND_IN_BOUND != ABSENT_FROM_WORLD
GREEN_CI != MERGE_AUTHORITY
PUBLIC_BREAK_TARGET != VALIDATION
```

No THR main/public-record promotion, licence/stewardship change, TRACE/ME change, human-study action, competition action, provider spend or private-data collection.

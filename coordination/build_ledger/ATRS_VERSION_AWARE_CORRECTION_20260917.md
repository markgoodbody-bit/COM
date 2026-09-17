# ATRS version-aware source correction — 17 Sep 2026

Status: **CORRECTION INTEGRATED / SAME FROZEN SOURCE / NO REFETCH / APPEALS PILOT INTACT**

Purpose: preserve the exact correction after **Claude Code identified** legacy-heading misses that changed the interpretation of several structural counts. **Codex independently confirmed** the finding against the frozen witness. Discovery and confirmation are distinct contributions.

## Historical witness retained

```text
source run = 35257984573
source head = 4a7b43df95a2b776b885f8ee903d929100414af7
artifact = 10513278849
artifact sha256 = ad315d9b08a0af65c4615638df2235b9ce6f021307315fbeb6dfcbd8cbdb0097
historical report sha256 = c13d62cc685c9c4dc1e6aabcfb658ab40460f4b51abf46f05a242032d0330eb9
raw source pages = 152
```

The source bytes and historical report were not edited or replaced.

## Defect

The original field patterns recognised current ATRS field names but missed older/transition heading families present in seven records, including:
- `Human decision` / `Human decisions`;
- `Impact assessment name / description / date / link`;
- `Risk name / description / mitigation`;
- a known older/transition family with no `Model performance` field.

CC identified the heading-family miss. Codex then rechecked the exact preserved run and confirmed:
- 20 directly demonstrated heading-recognition misses = 6 human + 7 risk + 7 impact;
- 7 model-performance cells are template-context cases, not seven missed existing headings;
- remaining absent cells are absences on the published page and do not establish anything about internal practice.

Therefore deterministic replay over the same source bytes reproduced the same miss.

```text
REPRODUCED != CORRECT
SAME_REGEX + SAME_BYTES -> SAME_MISS
```

The `Appeals and review` patterns were not affected by this defect.

## Repair

Added version-aware heading recognition and explicit heading-family context. Reparsing used the exact preserved source HTML; no GOV.UK refetch occurred.

```text
workflow = 35266542167 SUCCESS
refetch = FALSE
derived artifact = 10516044636
derived artifact sha256 = 530f5f52f280b9cf1da4786f101bdd5b80874bf62af43db8e60d6e167fdd575f
heading profiles:
  current_named_family = 145
  legacy_2024_family = 6
  mixed_known_families = 1
```

Corrected source-level observations:

```text
human_review = 152/152
appeals_review = 151/152
model_performance = 139/152
  section_not_observed = 13
  known legacy/transition family without field = 7
risks = 152/152
impact_assessment = 145/152
maintenance = 152/152
senior_responsible_owner = 152/152
```

Superseded historical broad-field counts:

```text
human_review: 146 -> 152
risks: 145 -> 152
impact_assessment: 138 -> 145
model_performance: 139 -> 139, interpretation corrected
```

A later narrow regression repair ensures an actually observed field wins over any family-level absence context on a mixed-family page.

## Appeals pilot

Unchanged:

```text
positive token census = 27
  review/appeal route = 16
  help/feedback = 9
  unrelated token = 1
  ambiguous = 1

negative SHA256(URL) sample = 20
  route/process described without locator = 15
  no locator/process observed = 3
  ambiguous = 2
  plain-text locator missed = 0
```

## Reader Lens / next edge

The version-aware Reader Lens removes the false-empty Human review consequence. Further bounded interface fixes are in progress from Codex's review: source/annotation search separation, safe actionable links, compact evidence-first hierarchy and accessibility controls.

The next consequential falsifier is reader task performance, not parser polish.

## Owners / scope

Public Law Project / Tracking Automated Government is a strong independent owner of broad UK public-sector ADM visibility and transparency/redress/public-law framing. BritainThinks/CDEI and GDS own much of the general usability premise. #364 remains narrower: field-level ATRS Appeals/review legibility and task-level reader-use measurement.

## Ceilings

```text
HISTORICAL_REPORT != DELETED
HEADING_FAMILY != COMPLIANCE_STATUS
FIELD_NOT_OBSERVED != REQUIRED_FIELD_OMITTED
SOURCE_READBACK_AID != DEMONSTRATED_READER_BENEFIT
100/100_KNOWN_FALSIFIERS_RESISTED != VALIDATED_RESEARCH_RESULT
GREEN_TESTS != COMPLETE_MODEL_OF_THE_SOURCE
REPRODUCIBILITY != CORRECTNESS
```

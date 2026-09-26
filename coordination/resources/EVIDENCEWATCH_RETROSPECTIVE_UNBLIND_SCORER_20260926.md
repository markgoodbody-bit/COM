# EvidenceWatch Brierley retrospective — frozen unblinding scorer

Date: 26 September 2026

Status: **SCORER PREDECLARED / NO MODEL OUTPUT EXISTS / OFFLINE ONLY**

Scorer:
`research/evidencewatch_retrospective/score_brierley_unblinded.py`

Purpose:

Prevent favourable denominator, failure or threshold choices after the pre-unblind model output exists.

Inputs:
1. sealed pre-unblind model output;
2. separate owner-label key;
3. frozen trivial lexical-baseline output.

The scorer refuses to overwrite its output.

## Validation before scoring

It requires:
- pre-unblind schema `evidencewatch-brierley-pre-unblind-output-v1`;
- status `OUTPUT_FROZEN_BEFORE_OWNER_LABEL_JOIN`;
- 44 model cases;
- 88 expected + 88 observed provider responses;
- owner-key schema/status and exactly 22 major-change + 22 no-change labels;
- exact case-ID set equality;
- exactly two provider receipts per case;
- baseline output schema/status and 44 selected source rows;
- owner-label agreement between key and lexical-baseline file.

Before scoring, the scorer also requires:
- v2 packet SHA-256 `f12762d4867da361e9eb72e3a12c30e82b734f005b09d527b7b19c7aee2ae1cc` in the sealed pre-unblind output;
- v2 owner-key SHA-256 `75c64ca3235812b2cccf0d5dc2801698dd23f20a393f627106026d619eb299c9` for the unblinding key.

Input file SHA-256 values are carried into the scored result.

## Headline metric: strict failure-worst-case

The headline view uses all 44 cases.

A model/provider failure must not improve performance:

```text
FAILED MAJOR-CHANGE CASE
-> strict miss / false negative

FAILED NO-CHANGE CONTROL
-> strict review burden / false positive
```

This is intentionally conservative.

Report:
- TP;
- FN;
- FP;
- TN;
- sensitivity;
- false-alert rate;
- precision.

## Secondary views

The scorer also reports:

1. **raw output-prediction view**
   - uses the harness's actual `prediction_review`;
   - failures remain visible but are not reassigned.

2. **available-case-only view**
   - excludes failed cases;
   - coverage/excluded count are explicit;
   - marked secondary only.

Therefore:

```text
AVAILABLE-CASE RESULT != HEADLINE RESULT
PROVIDER FAILURE != QUIET SUCCESS
```

## Error anatomy

For every case the scored output preserves:
- owner label;
- DOI identities;
- failed/not failed;
- failure reasons;
- raw + strict prediction;
- baseline/successor engine status;
- successor relation;
- material reasons;
- alert kind;
- lexical scores.

Aggregate views include:
- failure counts by owner label;
- successor relation distribution by owner label;
- cases/total material reasons by owner label.

## Trivial baseline comparison

The frozen v2 lexical baseline covers all 22 major-change and 22 no-change text pairs.

For each lexical metric the scorer reports:
- AUC;
- positive/control coverage;
- missingness;
- best lexical sensitivity attainable at or below the **model strict false-alert rate**.

That operating-point comparison is explicitly:

`POST_UNBLINDING_DESCRIPTIVE_OPERATING_POINT`

No lexical threshold is promoted into a preregistered test after the fact.

## Interpretation ceiling

The scored result still cannot establish:
- clinical/scientific materiality;
- systematic-review consequence;
- reviewer burden reduction;
- market need;
- user validation;
- superiority to strong living-evidence owners.

Preserve:

```text
STRICT FAILURE PENALTY != POPULATION ESTIMATE
MODEL DISCRIMINATION != WORKFLOW VALUE
MODEL ~= LEXICAL BASELINE -> NARROW SEMANTIC-VALUE CLAIM
NEGATIVE RESULT = USEFUL
```

No provider/model call, external contact, application submission or EvidenceWatch source mutation is performed by this scorer.

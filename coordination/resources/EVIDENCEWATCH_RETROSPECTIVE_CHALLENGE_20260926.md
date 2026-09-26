# EvidenceWatch retrospective major-change challenge — pre-run freeze

Date: 26 September 2026

Status: **PRE-RUN FROZEN / OWNER-LABELLED RETROSPECTIVE CHALLENGE / NO EVIDENCEWATCH RESULT**

Purpose:

Test one narrow engineering question without selecting examples after seeing EvidenceWatch output:

> When presented with preprint -> publication successor states, can the current EvidenceWatch analysis path distinguish owner-labelled major abstract changes from owner-labelled no-change controls often enough to justify further testing?

This is deliberately weaker than the live pilot question. It does not measure reviewer burden, workflow incidence or downstream decision impact.

## Stronger owner and source pin

Brierley et al. 2022 manually annotated changes between preprint and published abstracts and made their data/code public.

Owner article:
- DOI: `10.1371/journal.pbio.3001285`

Pinned owner repository:
- `preprinting-a-pandemic/preprint_changes@a07c570cf3be4481ba74c59ceee22e40f949990b`
- `data/abstract_scoring.csv` Git blob: `da5d608019200a14b31c9d605df8e27ced2eaa21`
- `data/all_pairs.tsv` Git blob: `3c26344ffc84ca43656477dd2229ac6530d4735f`

Frozen manifest:
- `research/evidencewatch_retrospective/brierley_major_vs_nochange_manifest_v1.json`

## Selection fixed before any run

Positive set:
- every owner row with `Highest_change >= 2`;
- 22 cases total;
- 15 COVID / 7 non-COVID.

Control set:
- owner `Highest_change == 0`;
- one unique control per positive;
- same COVID/non-COVID stratum;
- minimum absolute difference in preprint posting date;
- lexical preprint DOI breaks ties.

Observed matching:
- 22 unique controls;
- maximum posting-date gap = 5 days;
- median posting-date gap = 2 days.

Do not replace awkward cases, rebalance after output, or drop failures unless a source-integrity defect is demonstrated and recorded before scoring.

## Label semantics

The owner paper categorised abstracts using the highest degree of manually adjudicated change. The positive label here is therefore:

`ABSTRACT_MAJOR_CHANGE`

It is **not**:
- clinical materiality;
- a change in a systematic-review conclusion;
- proof that re-extraction was required;
- proof that a human decision changed.

Controls are:

`ABSTRACT_NO_CHANGE`

according to the same owner dataset.

Preserve:

```text
ABSTRACT_MAJOR_CHANGE != CLINICAL_MATERIALITY
ABSTRACT_MAJOR_CHANGE != LIVING_REVIEW_DECISION_CHANGE
PAIR_DATASET != LIVE_WORKFLOW_INCIDENCE
RETROSPECTIVE_DISCRIMINATION != REVIEWER_TIME_SAVED
OWNER_LABEL != EVIDENCEWATCH_OUTPUT
```

## Execution discipline

No provider/model call is authorised by this freeze.

A later run, if separately authorised, should:
1. reconstruct the paired preprint/published abstracts from the pinned owner data;
2. present every case through one fixed EvidenceWatch configuration;
3. prevent owner labels from entering model input;
4. record alert/materiality output before unblinding;
5. score all 44 cases, including failures and unresolved outputs;
6. report positive sensitivity and no-change false-alert rate separately;
7. keep owner-label disagreement visible rather than silently adjudicating toward EvidenceWatch.

Do not tune prompt, threshold, authority configuration or materiality policy on this frozen 44-case set and then report the same set as validation.

## What would be useful

A poor result is useful: it would show that the current semantic-change path is not ready even for owner-labelled major abstract changes.

A good result is only an engineering signal. It would support moving to harder current-workflow testing; it would not establish product value.

## Relation to Digital Science

This challenge strengthens the application only as evidence that falsification has been prepared before pilot execution.

It must not be described as researcher validation or a measured efficiency result unless a separate completed run and later real-workflow evidence earn those statements.

No external contact, provider spend, grant submission or EvidenceWatch source change follows from this object.

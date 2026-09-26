# EvidenceWatch — bounded prevalence check for the post-reliance residual

Date: 26 September 2026

Status: **PUBLIC EVIDENCE BOUND / NO MARKET-SIZE CLAIM / NO FEATURE DELTA**

Purpose:

Test whether the narrowed EvidenceWatch residual is plainly negligible, common, or still empirically unresolved:

> material changes to an already-relied-on source that do not arrive as a new study or formal status event.

The public literature supports **non-zero consequential change**, but not a direct living-review workflow incidence rate.

## Stronger methodological owner — PRISMA-LSR

The PRISMA 2020 extension for living systematic reviews explicitly treats changes involving already-included studies as part of living-review maintenance.

Its examples include:
- newly available reports for already-included studies;
- checking whether data abstracted from a preprint changed in the peer-reviewed paper;
- abstracting new data;
- changing a primary reference for an already-included study;
- documenting consequential changes to results.

Owner surface:
- https://www.bmj.com/content/387/bmj-2024-079183

This confirms the residual class is methodologically recognized.

It does **not** establish that automation is needed.

## Pair-level evidence

### Brierley et al. — PLOS Biology 2022

Preprint -> journal pairs:
- discrete abstract-conclusion change:
  - **7.2%** non-COVID-19;
  - **17.2%** COVID-19.
- the authors report that the majority of changes did not qualitatively change the paper's conclusions.

Source:
- https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3001285

### Sommer et al. — Scientific Reports 2023

Among 161 prevention preprints subsequently published:
- **16.8%** had some change in the magnitude of the primary-outcome effect estimate;
- **4.4%** were classified as a major change in effect magnitude;
- conclusion wording/style changed more often, but conclusion **content** changed in **3.1%**.

Source:
- https://www.nature.com/articles/s41598-023-44291-4

### medRxiv clinical-study comparison

Among published medRxiv clinical-study pairs:
- **81.1%** were numerically concordant for primary-endpoint results;
- **96.2%** had concordant study interpretations.

Source:
- https://pubmed.ncbi.nlm.nih.gov/36484989/

### COVID-19 epidemiological point estimates

A separate 100-pair COVID-19 analysis found:
- 11% of preprint epidemiological point estimates were deleted during peer review;
- additional estimates were added;
- persisted point estimates changed modestly on average.

Source:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9553196/

## What this does and does not establish

The evidence is heterogeneous across study designs, periods and definitions of "change".

Preserve:

```text
PREPRINT_PUBLICATION_PAIR != REVIEW_WORKFLOW
PAIR_LEVEL_CHANGE_RATE != LIVING_REVIEW_EVENT_RATE
TEXTUAL_CHANGE != MATERIAL_CHANGE
NUMERIC_CHANGE != DECISION_CHANGE
INTERPRETATION_CONCORDANT != NO_REEXTRACTION_WORK
NONZERO_RESIDUAL != PRODUCT-SCALE PROBLEM
```

The useful conclusion is bounded:

1. The residual class is real enough that living-review guidance names it.
2. Most preprint -> publication pairs do **not** undergo a major interpretation change.
3. Some pairs do undergo numerical or conclusion-content changes that could require re-checking extracted evidence.
4. Published pair-level frequencies cannot tell us how often a particular living review encounters such an episode.
5. Therefore prevalence remains an empirical pilot question, not a solved market-size claim.

## Pilot consequence

The pilot should not ask merely whether EvidenceWatch can detect a version transition.

It should ask:

> Within one real current workflow, how many already-relied-on sources enter the residual class, how many changes are materially consequential, how are they caught today, and what reviewer time/error delta follows from shadow-mode EvidenceWatch?

Useful denominator:
- all already-relied-on monitored sources over a declared interval.

Useful numerators:
- source transitions observed;
- material transitions under predeclared human labels;
- transitions already caught by existing workflow;
- EvidenceWatch-only catches;
- EvidenceWatch misses;
- false alerts.

Primary efficiency outcome remains:
**reviewer minutes per correctly handled material-change episode versus existing practice.**

## Project consequence

No source feature is earned.

This evidence argues against broad claims and in favor of a small, measured pilot.

No external contact, provider call, grant submission or form action was performed.

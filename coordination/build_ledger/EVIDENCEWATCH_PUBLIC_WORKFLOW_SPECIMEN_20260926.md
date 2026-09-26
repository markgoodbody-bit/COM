# EvidenceWatch — public historical living-review workflow specimen

Date: 26 September 2026

Status: **REAL PUBLIC WORKFLOW SPECIMEN / HISTORICAL / NO PARTNER / NO USER-VALIDATION CLAIM / NO CONTACT**

Purpose:

COM #492 / #348 identifies the first missing EvidenceWatch evidence as a real review-maintenance workflow rather than another feature or synthetic demonstration.

This note records one **public, already-completed** living-review episode from the University of Bern SARS-CoV-2 living systematic review.

It does **not** satisfy the stronger gate of a willing current review team.

## Public workflow owner

Living systematic review:
- Buitrago-Garcia et al., *Occurrence and transmission potential of asymptomatic and presymptomatic SARS-CoV-2 infections: Update of a living systematic review and meta-analysis*, PLOS Medicine 2022;
- DOI: https://doi.org/10.1371/journal.pmed.1003987
- public data/code: https://github.com/leonieheron/LSR_Asymp_v5

Practical workflow paper:
- Heron et al., *How to update a living systematic review and keep it alive during a pandemic: a practical guide*, Systematic Reviews 2023;
- DOI: https://doi.org/10.1186/s13643-023-02325-y

Current public repository head observed:
`14394066886185fbf05067fd82addaa1f3e26fa1`

## Existing practice — owner-described route

The review team's published method says that in each update they checked whether included preprints had since been published in peer-reviewed journals and **re-extracted the data if the content had changed**.

The public repository also documents the operational review machinery:
- automated/aggregated searching;
- RShiny screening and verification;
- one reviewer data extraction;
- second-reviewer verification;
- REDCap-backed workflow;
- R scripts using the extracted data for tables/figures/synthesis.

Therefore:

```text
PREPRINT -> FINAL-PUBLICATION CURRENTNESS CHECK
!= EVIDENCEWATCH INVENTION

CONTENT CHANGED -> RE-EXTRACT
!= EVIDENCEWATCH INVENTION

HUMAN VERIFICATION
!= OUR NEW GOVERNANCE IDEA
```

## Concrete completed episode

Study:
Andrea Lombardi et al.,
*Characteristics of 1,573 healthcare workers who underwent nasopharyngeal swab for SARS-CoV-2 in Milano, Lombardy, Italy.*

### Earlier source state — preprint

medRxiv:
https://doi.org/10.1101/2020.05.07.20094276

Public preprint result:
- 138 positive HCWs among 1,573;
- 41 / 138 of the positive HCWs described as asymptomatic at the earlier observation/definition;
- the earlier symptom definition used six symptoms according to the review team's extraction note.

### Successor source state — peer-reviewed final article

Clinical Microbiology and Infection:
https://doi.org/10.1016/j.cmi.2020.06.013

The final article followed positive/asymptomatic-positive HCWs through 22 May and reports:
- 139 positives among 1,573;
- 28 were symptom-free at first positive test;
- 11 subsequently developed symptoms;
- 17 / 139 remained asymptomatic across the observed period;
- the review-team note records seven symptoms in the final publication versus six in the preprint.

This is not a cosmetic publication-status change. The state used for the review's asymptomatic outcome materially changed.

## Review-team lineage evidence

Public repo historical extraction at parent commit:
`4ece98cd8a40bb42314f31143e4c0c7e7457ffea`

`Q1_ExtractedData.csv`, record 1264, explicitly says:

> This is the final publication from pre-print included in record 593. The numbers change...

The same note records:
- preprint Num: 41;
- preprint Den: 138;
- final publication symptom definition changed from 6 symptoms to 7.

Current public Q1 extraction:
`Q1_ExtractedData.csv` at repo head

Record 1264 is represented as:
- Screening: occupational;
- 1 cluster;
- 17 asymptomatic;
- 139 total;
- DOI `10.1016/j.cmi.2020.06.013`.

The team's public data therefore preserve:

```text
PREPRINT RECORD
-> SAME STUDY / FINAL PUBLICATION
-> CONTENT CHANGED
-> DATA RE-EXTRACTED
-> FINAL Q1 EXTRACTION = 17 / 139
```

The final publication is not counted as an independent second study merely because it has a new publication route.

## Downstream dependency

The PLOS fifth-update article:
- includes Lombardi et al. as study/reference 100;
- states that the GitHub extraction data/code were used to display and synthesise the results;
- defines review question 1 as the proportion remaining asymptomatic during follow-up.

The public repo README states that `Q1_ExtractedData.csv` feeds the Q1 tables/forest-plot analysis.

Therefore the bounded dependency is:

```text
LOMBARDI SOURCE STATE
-> Q1 EXTRACTED STUDY DATA
-> LIVING-REVIEW Q1 SYNTHESIS / DISPLAY
```

This does **not** establish that this one changed study altered the review's overall narrative conclusion.

## What current practice already solved

This specimen directly subtracts several possible EvidenceWatch claims:

1. **preprint currentness** — the team already checked whether preprints had become peer-reviewed;
2. **same-lineage handling** — final publication was recognised as the successor to a preprint already included, not independent corroboration;
3. **materiality detection** — changed content triggered re-extraction;
4. **human verification** — extraction was reviewed/verified within the team's workflow;
5. **downstream use** — corrected/re-extracted values fed the review data used for synthesis.

Therefore EvidenceWatch cannot justify itself by saying review teams simply fail to notice preprint-to-publication transitions or do not know to re-extract changed evidence.

## Residual product hypothesis after this specimen

The surviving question becomes smaller:

Can tooling reduce the labour of:
- repeatedly checking included-source currentness;
- matching a successor/final publication to an already-relied-on preprint;
- showing the before/after state;
- preserving that they share one evidentiary root;
- routing the changed extraction to the already-known dependent review item;

**without** adding more setup/maintenance/review burden than the existing workflow?

This is an integration/burden question.

```text
WORKFLOW EXISTS
!= WORKFLOW IS CHEAP

MANUAL OWNER PRACTICE EXISTS
!= AUTOMATION ADDS VALUE

REAL HISTORICAL EPISODE FOUND
!= WILLING CURRENT PARTNER FOUND
```

## Public burden context — useful but not episode-specific

The practical-guide owner source says:
- the original core review team of seven became overwhelmed as new hits increased;
- the team recruited 20 experienced systematic-review volunteers from April 2021;
- each volunteer agreed to contribute at least 3 hours per month to eligibility assessment, data extraction and/or risk-of-bias work;
- the core team also carried training, individual feedback and workflow/tool support;
- automated weekly search was still bringing in roughly 100–200 new records.

This establishes a **real high-burden review environment**, not the labour cost of this particular Lombardi source transition.

A conservative arithmetic lower bound for the explicitly stated volunteer commitment is:

```text
20 volunteers x >=3 h/month
= >=60 volunteer-hours/month
```

But those hours cover multiple review tasks and must **not** be attributed to preprint-currentness checking or this one re-extraction episode.

Preserve:

```text
REVIEW WORKFLOW LABOUR INTENSIVE
!= THIS FEATURE WOULD SAVE 60 HOURS

TEAM OVERWHELMED
!= EVIDENCEWATCH SOLVES THE BOTTLENECK

PUBLIC WORKLOAD CONTEXT
!= MATCHED BURDEN MEASUREMENT
```

## What EvidenceWatch must not infer

Do not infer:
- that the living-review team needed or wanted EvidenceWatch;
- how many staff minutes this episode consumed;
- how the publication-status transition was first discovered in this particular case;
- that 17/139 should be mechanically substituted for every use of 41/138 outside this review's defined outcome;
- that the one study changed the review's overall conclusion;
- that preprint-to-publication transitions are the main residual change class;
- that current Zotero/Crossmark/ReadCube/Cochrane tooling could not now handle parts of this route more efficiently.

## EvidenceWatch representability check

Current EvidenceWatch main:
`b8fc0971ceace55878aa6130448850d88774f254`

No new code or data type is required to represent this episode.

Existing structure already carries:
- multiple configured source representations;
- explicit `stateAuthority`;
- shared `independenceGroup` for one evidentiary root;
- `authorityAsOf` for source succession/currentness;
- analyzer relation `correction`, whose existing instruction explicitly includes a source that **supersedes** an earlier source/state;
- material reasons;
- configured downstream dependents;
- append-only before/after state.

The existing engine regression `newer state authority cannot be rolled back by an older authority source` already tests the load-bearing succession behaviour:
- earlier authority establishes state;
- later authority advances it;
- later authority time becomes current;
- changed bytes from the older authority can alert but cannot roll canonical state backwards.

A Lombardi-shaped watch could therefore represent:
- preprint = earlier primary/state-authority source;
- final publication = later primary/state-authority source;
- both = same evidentiary root / independence group;
- final publication = later `authorityAsOf`;
- changed follow-up result / symptom definition = material supersession;
- Q1 review object = downstream dependent.

Preserve:

```text
REAL CASE FITS CURRENT MODEL
-> NO FEATURE EARNED

SAME EVIDENTIARY ROOT
!= INDEPENDENT SUPPORT

LATER AUTHORITATIVE SUCCESSOR
!= RETROACTIVE ERASURE OF PREPRINT STATE

REPRESENTABLE
!= USEFUL IN PRACTICE
```

The remaining gap is empirical burden/value, not representation.

## Gate result

```text
REAL PUBLIC HISTORICAL WORKFLOW SPECIMEN = FOUND
POST-RELIANCE CONTENT CHANGE = FOUND
SAME-LINEAGE SUCCESSOR = FOUND
RE-EXTRACTION RESPONSE = FOUND
DOWNSTREAM REVIEW DEPENDENCY = FOUND

WILLING CURRENT REVIEW TEAM = NONE
CURRENT-PRACTICE TIME/BURDEN = UNKNOWN
EVIDENCEWATCH VALUE DELTA = UNMEASURED
RESEARCHER VALIDATION = NONE
```

## Consequence

The public specimen is enough to falsify an invented-gap story and improve the application/interview reasoning.

It is **not** enough to justify another product integration.

Next stronger evidence remains one willing current team or equivalent current workflow owner who can expose:
- one completed update episode;
- how it was actually found;
- current tools/alerts;
- staff burden;
- what would count as useful improvement.

No external contact is authorised by this note.

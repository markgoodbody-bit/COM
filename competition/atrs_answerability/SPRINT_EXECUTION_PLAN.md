# ATRS Answerability Audit — provisional sprint-time execution plan

Status: **PREPARATION ONLY / CURRENT LEAD != SELECTED ENTRY / LIVE RULES MUST BE RE-READ BEFORE USE**

This file prevents September preparation from silently becoming the claimed November research result.

Current Apart AI x Epistemics public page asks what can be measured about a live epistemic deployment using data downloadable over a weekend and welcomes investigative-research-shaped deployment/impact projects. Current public text we verified does not settle the pre-existing-work boundary. Older Apart sprint rules allowed advance thinking while requiring core research during the event. That historical rule is context, **not** assumed to govern November 2026.

Before registration/submission, re-read the live Guidelines/terms. If September work is not admissible as judged work, use it only as background, tooling and preregistration support.

## September material = pilot / infrastructure

Preserve as preparation:
- finder-vs-Search-API membership validator;
- full-record parser and hostile regression tests;
- content-addressed source capture;
- September 152-record evidence bundle;
- preregistered bounded appeals/review pilot;
- known parser/semantic limitations;
- reader walkthrough;
- owner/prior-work map.

Do **not** submit the September counts as if produced during the sprint if live rules require fresh core work.

## Candidate sprint-time core question

> In the ATRS public register current during the sprint, what kind of public challenge/review affordance does the `Appeals and review` disclosure actually expose to a reader, and what is lost if field presence alone is treated as the answerability measure?

The object is the **published disclosure**, not hidden/internal government practice and not legal compliance.

## Proposed fresh sprint workflow

### 1. Freeze current membership before analysis

- fetch the live GOV.UK ATRS finder;
- independently compare its exact URL set with the generic GOV.UK Search API;
- fail closed on membership disagreement;
- preserve timestamped membership manifest.

### 2. Fetch and content-address every current public record

- preserve exact source bytes;
- preserve page SHA-256 and fetch time;
- run deterministic field extraction;
- publish parser version/head and all extraction ceilings.

### 3. Freeze the semantic codebook before full census

Use **multi-label observables**, not one scalar or forced exclusive moral ranking. Candidate labels informed by the September pilot:

- `CONCRETE_RECONSIDERATION_OR_COMPLAINT_LOCATOR` — the field provides a concrete public locator tied to review/challenge/complaint of the relevant output/process;
- `EXISTING_REVIEW_OR_APPEAL_PROCESS_REFERENCED` — a review/appeal/complaints process is named but the field itself does not supply a concrete locator;
- `IN_CHANNEL_HUMAN_HANDOFF` — the published interaction itself lets a user request/reach a human;
- `INTERNAL_HUMAN_REVIEW_DESCRIBED` — the organisation describes human checking/review but not a reader-initiated route;
- `GENERAL_HELP_OR_FEEDBACK_ROUTE` — a public help/feedback channel is present without clear reconsideration semantics;
- `EXPLICIT_NO_SEPARATE_PROCESS_OR_NO_DECISION` — the field says a separate tool-specific process does not apply / the tool does not make the relevant decision;
- `DATA_RIGHTS_ROUTE` — data access/removal/privacy route present; do not silently relabel it as output appeal;
- `EXPLANATION_OR_AUDIT_TRAIL_WITHOUT_RECOVERY` — later explanation/audit evidence is described but reversal/recovery is not;
- `AMBIGUOUS_OR_SCOPE_UNCLEAR` — relevance cannot be resolved from the public wording without inference.

Labels may co-occur where the public record exposes more than one affordance. This is deliberate.

### 4. Full semantic census

Core work candidate for the sprint:
- classify every current `Appeals and review` field using the frozen multi-label codebook;
- preserve the exact evidence text supporting every label;
- use two independent aperture reads where feasible (e.g. Framework + Codex; CC if available) without allowing one aperture to silently overwrite the other;
- preserve all disagreements and resolve by explicit codebook rule or retain `AMBIGUOUS`.

`TWO_AI_READS != HUMAN_VALIDATION`; report the coder arrangement plainly.

### 5. Robustness / negative controls

Required before any headline count:
- manually check all records with no observed appeals field;
- manually check every repeated appeals field;
- inspect a deterministic sample of each major label;
- verify that general feedback/data-rights links are not counted as reconsideration routes;
- verify that token absence does not erase in-channel human handoff;
- rerun frozen examples from September as regression fixtures, not as November results.

### 6. Optional longitudinal layer

If the register changed materially between the September witness and sprint weekend:
- report added/removed/changed record URLs;
- compare only content-addressed records whose source bytes actually changed;
- ask whether the distribution/clarity of disclosure modes changed.

No change is also a valid result.

### 7. Write the field-level result at the strength earned

Candidate form, not preregistered conclusion:

> `Appeals and review` field presence may be high while the reader-visible challenge/review object remains heterogeneous. A deployment register therefore needs to distinguish **whether a field exists** from **what public action/review relationship the field actually makes legible**.

Only retain this if the fresh full census supports it.

## Negative-result paths

Valid sprint results include:
- current ATRS records are far more uniform than the September pilot suggested;
- the multi-label codebook collapses under real cases and cannot be made reliable;
- an existing owner already supplies the same full-record classification/audit;
- the relevant variation is explained almost entirely by tool scope/version rather than answerability design;
- the field is sufficiently navigable that no consequential measurement gap remains.

`NO_DELTA / OWNER_FOUND / STOP` remains acceptable.

## Deliverable shape if it survives

- short research report;
- frozen current membership manifest;
- reproducible source snapshot hashes;
- extraction code + tests;
- full semantic coding table with evidence excerpts and disagreement state;
- small reader walkthrough;
- prior-work / owner boundary;
- explicit limitations and no compliance score.

No model/API spend is required for the core design.

## Gates

No registration, organiser contact, terms acceptance or submission follows from this plan. Live competition rules and any identity/legal representations remain Mark's explicit gate.

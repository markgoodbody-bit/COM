# ATRS Answerability Audit — strongest-owner map

Status: **OWNER ATTRIBUTION / GAP TEST / NOT A NOVELTY CLAIM**

## 1. Government Digital Service / GOV.UK — standard, semantics and repository

Primary owners:
- ATRS guidance for public sector bodies: https://www.gov.uk/government/publications/guidance-for-organisations-using-the-algorithmic-transparency-recording-standard/algorithmic-transparency-recording-standard-guidance-for-public-sector-bodies
- ATRS template: https://www.gov.uk/government/publications/algorithmic-transparency-template
- ATRS standard / previous versions: https://www.gov.uk/government/publications/algorithmic-transparency-data-standard
- ATRS hub: https://www.gov.uk/government/collections/algorithmic-transparency-recording-standard-hub
- current public finder: https://www.gov.uk/algorithmic-transparency-records

What is already owned:
- purpose and scope of ATRS;
- field names and intended semantics;
- template completion guidance;
- publication workflow and public repository;
- the intended meaning of `appeals_and_review`.

The standard describes `appeals_and_review` as mechanisms for review/appeal of the decision available to the general public. Current guidance explicitly asks authors to consider both challenge to the tool output and challenge to the broader operational-process output. A public appeal/contact link is an example, not the only valid representation. Where no review process is relevant, the guidance asks for an explanation.

Therefore:

```text
FREE-TEXT VARIATION != DISCOVERED DEFECT
LINK ABSENCE != FAILURE TO COMPLETE GUIDANCE
BROADER PROCESS APPEAL != TOOL-OUTPUT APPEAL
NO SEPARATE PROCESS CAN BE A VALID DISCLOSURE
```

The audit must not claim ownership of those semantics.

## 2. Fabio Rovai / Tesseract Academy — ATRS metadata corpus

Owner repository:
https://github.com/fabio-rovai/uk-algorithmic-transparency

Observed owner contribution:
- reproducible GOV.UK Search API harvest;
- structured publishing body, tool, description and publication-date metadata;
- open corpus for register-level questions.

This project does not copy that code and does not claim novelty for enumerating ATRS records.

Residual distinction:

```text
REGISTER METADATA != FULL TIER-2 DISCLOSURE CONTENT
```

## 3. Existing qualitative / governance research

Existing work has studied ATRS policy, practitioner perspectives and how public-sector transparency should improve. This project does not claim that evaluating ATRS, public-sector AI transparency or contestability is new.

A bounded September 2026 search did not locate the same current full-register semantic census of the `Appeals and review` field. Search absence is not novelty evidence.

## 4. What the September pilot actually established

Earned engineering/evidence result:
- exact current-finder membership can be frozen and independently checked;
- exact GOV.UK source pages can be content-addressed and preserved;
- full-record field extraction can be reproduced from the evidence bundle;
- a preregistered manual pilot finds materially different reader-visible actions/process descriptions behind the same field heading.

Codex independently reproduced all 152 frozen extractions with zero field differences and challenged the manual classification, producing real disagreements that were preserved.

That establishes a usable measurement substrate and pilot, not the field-level research answer.

## 5. Residual research question

The surviving question is **not**:

> Do free-text ATRS records differ?

They are expected to differ.

The narrower unresolved question is:

> Across the current public register, what does the `Appeals and review` field make legible about **how a member of the public can initiate or reach review/challenge of the relevant tool output or broader decision process**, and how often is the disclosure instead an internal review description, general feedback/help, data-rights route, explanation-only record, explicit no-separate-process statement, or ambiguous reference?

This is a distribution/legibility question anchored to the official field semantics.

Candidate observable distinctions:
- concrete public reconsideration/complaint/appeal locator;
- in-channel human handoff;
- existing review/appeal process referenced without initiation detail;
- internal human review only;
- general help/feedback route;
- explicit no separate process / tool does not make relevant decision;
- data-rights action not clearly tied to output reconsideration;
- explanation/audit trail without recovery;
- ambiguous scope.

These may co-occur. Do not force them into a moral score.

## 6. Kill criteria

Kill or shrink the lead if:
- an existing owner supplies the same current full-register semantic census;
- the distinctions cannot be coded with acceptable disagreement/readback;
- the full census collapses almost entirely to obvious tool-scope/template-version effects and yields no useful measurement boundary;
- the output does not help any reader/researcher distinguish field completion from the public action actually described;
- live Apart rules make the prepared route unusable and no useful independent publication/research path remains.

```text
OWNER_FOUND -> STOP
NOT_FOUND != NOVEL
PILOT != RESULT
FIELD_COMPLETION != SEMANTIC CENSUS
```

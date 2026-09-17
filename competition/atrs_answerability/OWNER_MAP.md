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

## 3. Public Law Project — Tracking Automated Government / public-sector ADM visibility

Owner surface:
https://trackautomatedgovernment.org.uk/

Current Public Law Project material describes its Tracking Automated Government (TAG) register as an independent register of automated/algorithmic tools used by UK public bodies. PLP reported 55 tools on TAG in 2025 and uses the register in wider work on transparency, review/redress, public law litigation and access to justice around automated government.

What this owner absorbs:
- the broad proposition that the public needs visibility into government automated decision-making;
- independent cataloguing of public-sector ADM beyond the official ATRS repository;
- much of the wider transparency/redress/public-law framing.

Residual distinction under test here:

```text
INDEPENDENT ADM REGISTER != FIELD-LEVEL ATRS APPEALS/REVIEW LEGIBILITY AUDIT
```

Do not imply that ATRS is the only public-government-algorithm visibility surface. Do not claim novelty from discovering undisclosed or non-ATRS tools.

## 4. Existing qualitative / governance research

Existing work has studied ATRS policy, practitioner perspectives and how public-sector transparency should improve. This project does not claim that evaluating ATRS, public-sector AI transparency or contestability is new.

A bounded September 2026 search did not locate the same current full-register semantic census of the `Appeals and review` field. Search absence is not novelty evidence.

## 5. What the September pilot actually established

Earned engineering/evidence result:
- exact current-finder membership can be frozen and independently checked;
- exact GOV.UK source pages can be content-addressed and preserved;
- the `Appeals and review` extraction/pilot can be reproduced from the evidence bundle;
- a preregistered manual pilot finds materially different reader-visible actions/process descriptions behind the same field heading.

Important repair: reproducing the same extraction over the same bytes did **not** establish that every other field-name mapping was correct. Codex found older ATRS heading families that the original parser missed. A version-aware reparse over the same 152 frozen HTML files corrected those mappings without refetching source.

```text
REPRODUCED != CORRECT
SOURCE_BYTES_FIXED != PARSER_SEMANTICS_FIXED
```

That establishes a usable measurement substrate and pilot, not the field-level research answer.

## 6. Residual research question

The surviving question is **not**:

> Do free-text ATRS records differ?

They are expected to differ.

The narrower unresolved question is:

> Across the current public register, what does the `Appeals and review` field make legible about **how a member of the public can initiate or reach review/challenge of the relevant tool output or broader decision process**, and how often is the disclosure instead an internal review description, general feedback/help, data-rights route, explanation-only record, explicit no-separate-process statement, planned-but-not-operating process, or ambiguous reference?

This is a distribution/legibility question anchored to the official field semantics.

Candidate observable distinctions may co-occur. Do not force them into a moral score.

## 7. Kill criteria

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

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

```text
FREE-TEXT VARIATION != DISCOVERED DEFECT
LINK ABSENCE != FAILURE TO COMPLETE GUIDANCE
BROADER PROCESS APPEAL != TOOL-OUTPUT APPEAL
NO SEPARATE PROCESS CAN BE A VALID DISCLOSURE
```

## 2. BritainThinks / CDEI — foundational UK public-engagement research

Owner report:
https://www.gov.uk/government/publications/cdei-publishes-commissioned-research-on-algorithmic-transparency-in-the-public-sector/britainthinks-complete-transparency-complete-simplicity

This public-engagement research informed the design space that later became ATRS. It already established important user expectations:
- people wanted public-sector algorithm information to be accessible and understandable;
- contact details and how to raise concerns were spontaneously important;
- appeal-process details were especially relevant in consequential use cases;
- participants preferred clear/simple, layered presentation over overwhelming detail;
- centralised registers and the ability to reveal more detail on demand were positively received.

Therefore this project does **not** own:

```text
SIMPLE_LAYERED_INFORMATION_IS_USEFUL
CONTACT_INFORMATION_MATTERS
APPEAL_INFORMATION_MATTERS
PUBLIC_INFORMATION_CAN_CREATE_COGNITIVE_STRAIN
```

Residual question is task-level performance on actual current ATRS records, not the general design principle.

## 3. Fabio Rovai / Tesseract Academy — ATRS metadata corpus

Owner repository:
https://github.com/fabio-rovai/uk-algorithmic-transparency

Observed owner contribution:
- reproducible GOV.UK Search API harvest;
- structured publishing body, tool, description and publication-date metadata;
- open corpus for register-level questions.

This project does not copy that code and does not claim novelty for enumerating ATRS records.

```text
REGISTER METADATA != FULL TIER-2 DISCLOSURE CONTENT
```

## 4. Public Law Project — Tracking Automated Government / public-sector ADM visibility

Owner surface:
https://trackautomatedgovernment.org.uk/

Public Law Project's Tracking Automated Government register independently catalogues automated/algorithmic tools used by UK public bodies. PLP reported 55 tools on TAG in 2025 and uses the register in wider work on transparency, review/redress, public-law litigation and access to justice around automated government.

This owner absorbs:
- the broad proposition that the public needs visibility into government automated decision-making;
- independent cataloguing beyond the official ATRS repository;
- much of the wider transparency/redress/public-law framing.

```text
INDEPENDENT ADM REGISTER != FIELD-LEVEL ATRS APPEALS/REVIEW LEGIBILITY AUDIT
```

Do not imply that ATRS is the only public-government-algorithm visibility surface.

## 5. Algorithm-register usefulness / contestability research

Nearby owners materially constrain the Reader Lens claim.

### Esther Nieuwenhuizen — Dutch algorithm registers

`Algorithm Registers: A Box-Ticking Exercise or Meaningful Tool for Transparency?`

The study interviewed developers and key register users/oversight actors and found current registers were not considered useful by societal watchdogs and oversight authorities; jargon/comprehensibility and discoverability were concrete user challenges.

This owns much of the generic claim that algorithm registers can fail their intended users.

### de Troya et al. (2026) — participatory system mapping

`Co-constructing sociotechnical AI governance: participatory system mapping using algorithm registers`

This work uses interviews, surveys and participatory mapping with municipal staff, civil-society organisations and ombudsmen to examine what a register reveals/occludes about a sociotechnical system, including contestability hazards.

This owns much of the broader claim that register entries may omit context needed for accountability.

### Canadian Federal AI Register work (FAccT 2026)

`Bureaucratic Silences: What the Canadian AI Register Reveals, Omits, and Obscures`

This owns another strong empirical example of a national register providing visibility while potentially obscuring sociotechnical context/contestability.

Therefore:

```text
ALGORITHM_REGISTERS_CAN_BE_HARD_TO_USE -> OWNED
REGISTERS_CAN_OMIT_ACCOUNTABILITY_CONTEXT -> OWNED
VISIBILITY != CONTESTABILITY -> OWNED
```

Reader Lens is now secondary. The current research spine is the route-relation implementation measurement.

Residual primary question:

> Across the live UK ATRS register, does the public record bind stated review/challenge/correction routes to the thing they can act on, the eligible actor and the initiation/channel — or does the relationship remain publicly unstated?

Reader-use remains a separate optional question in `READER_USE_PROTOCOL.md`; it is not required for the relation result.

## 5A. 2026 complete-register / external-audit work — competition-critical prior work

These owners now materially constrain the #364 novelty story.

### Das et al. — Canadian federal register

`Bureaucratic Silences: What the Canadian AI Register Reveals, Omits, and Obscures`  
FAccT 2026. DOI: https://doi.org/10.1145/3805689.3812336

The authors analyze the complete Canadian federal AI Register (409 systems) using ADMAPS plus deductive qualitative coding and explicitly frame the result as visibility without contestability / sociotechnical context being obscured.

This owns much of:

```text
FULL-REGISTER EMPIRICAL AUDIT = NOT NEW BY ITSELF
VISIBILITY != CONTESTABILITY = OWNED
REGISTER DISCLOSURE CAN OBSCURE SOCIOTECHNICAL CONTEXT = OWNED
```

### Peljto, Heilmann & Cerrato — German initiatives

`Are Algorithm Registers Transparent? Perspectives from Germany` (2026).

The paper turns transparency goals into structured audit checklists and applies them to two German initiatives, deriving concrete improvement actions.

This owns much of:

```text
REGISTER AUDIT AGAINST EXPLICIT TRANSPARENCY GOALS = OWNED
STRUCTURED CHECKLIST AUDIT = NOT OUR GENERAL NOVELTY
```

### Consequence for #364

The competition delta is **not** a general register critique.

The narrower surviving question is implementation-specific to GDS's own ATRS guidance:

> Does the live UK register publicly bind each stated review/challenge/correction route to its target site, eligible actor and initiation path, while leaving unstated relations unstated?

See `PRIOR_WORK_PRESSURE_20260918.md`.

```text
GENERAL PROBLEM OWNER FOUND != EXACT UK IMPLEMENTATION MEASURE OWNER FOUND
NOT_FOUND_EXACT_OWNER != NOVELTY_PROVED
```

## 6. What the September pilot actually established

Earned engineering/evidence result:
- exact current-finder membership can be frozen and independently checked;
- exact GOV.UK source pages can be content-addressed and preserved;
- the `Appeals and review` extraction/pilot can be reproduced from the evidence bundle;
- a preregistered manual pilot finds materially different reader-visible actions/process descriptions behind the same field heading.

Important repair: reproducing the same extraction over the same bytes did **not** establish that every other field-name mapping was correct. **Claude Code identified the legacy-heading misses; Codex independently confirmed them against the frozen witness.** A version-aware reparse over the same 152 frozen HTML files corrected those mappings without refetching source.

```text
REPRODUCED != CORRECT
SOURCE_BYTES_FIXED != PARSER_SEMANTICS_FIXED
```

That establishes a usable measurement substrate and pilot, not the field-level research answer.

## 7. Residual research questions

### Distribution / legibility

> Across the public register, what does `Appeals and review` make legible about how a person can initiate or reach review/challenge of the relevant tool output or broader decision process, and how often is the disclosure instead an internal review description, general feedback/help, data-rights route, explanation-only record, explicit no-separate-process statement, planned-but-not-operating process, or ambiguous reference?

### Reader use

> Does reorganising the same source evidence around the question `what can I do next?` measurably improve evidence-grounded action retrieval compared with the original record presentation?

Neither question implies a moral or compliance score.

## 8. Kill criteria

Kill or shrink the lead if:
- an existing owner supplies the same current ATRS semantic census or task-level reader evidence;
- the semantic distinctions cannot be coded with acceptable disagreement/readback;
- the result collapses to obvious template/version effects;
- the Reader Lens does not improve evidence-grounded retrieval or creates more unsupported inference;
- any apparent reader improvement comes merely from added interpretation rather than evidence organisation;
- a simpler owner-controlled GOV.UK presentation change achieves the same result;
- live Apart rules make the route unusable and no useful independent publication/research path remains.

```text
OWNER_FOUND -> STOP
NOT_FOUND != NOVEL
PILOT != RESULT
FIELD_COMPLETION != SEMANTIC CENSUS
READER_LENS != DEMONSTRATED_READER_BENEFIT
```

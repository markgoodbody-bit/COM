# ATRS Reader Lens — bounded reader-use protocol

Status: **METHOD / FUTURE HUMAN TEST / NO PARTICIPANT RESULT / NO RECRUITMENT AUTHORISED**

## Question

Does the source-preserving ATRS Reader Lens help a reader recover action-relevant facts from actual ATRS records more accurately or efficiently than the original record presentation, **without increasing unsupported inference**?

This is narrower than asking whether algorithm registers are generally useful, whether ATRS is compliant, or whether a disclosed route is effective.

## Strongest-owner boundary

This study does **not** claim novelty for the premise that public algorithm information should be simple, understandable, layered, or include contact/appeal information.

Prior owners include:

- BritainThinks / CDEI public-engagement research (`Complete transparency, complete simplicity`), which found that participants wanted clear contact information and appeal-process details, preferred simple/layered presentation, and worried about jargon and cognitive strain in public-sector information;
- Government Digital Service ATRS guidance, which explicitly aims at meaningful/intelligible transparency and recommends clear/simple language;
- Esther Nieuwenhuizen's research on Dutch algorithm registers, which found current registers were not considered useful by societal watchdogs/oversight authorities and identified jargon/accessibility problems;
- de Troya et al. (2026), using interviews/surveys/participatory system mapping to examine what a Dutch municipal algorithm register reveals/occludes for stakeholders;
- Public Law Project / Tracking Automated Government, which owns much of the broader UK public-sector ADM visibility/redress/public-law problem.

Residual empirical question:

```text
GENERAL NEED FOR USABLE TRANSPARENCY -> OWNED
GENERAL IMPORTANCE OF CONTACT/APPEAL INFO -> OWNED
GENERAL REGISTER-USABILITY CRITIQUE -> OWNED
TASK-LEVEL ACTION-FACT RETRIEVAL ON CURRENT ATRS RECORDS -> UNDER TEST
```

## Surfaces

### A — Original ATRS record

The participant uses the original GOV.UK ATRS record presentation for the case.

For a frozen September pilot, use the exact preserved source page from run `35257984573`; for any November sprint study, freeze a fresh source snapshot first.

### B — Reader Lens

The participant uses a source-only Reader Lens card generated from the same frozen evidence.

For the study condition:
- exploratory semantic annotations are OFF / absent;
- exact source text remains visible;
- original GOV.UK source is linked;
- no generated statement of legal rights or route effectiveness is shown.

`SOURCE DIFFERENCE` must be zero: the two surfaces must derive from the same record version.

## Reader task

For each assigned record, answer **from the presented record only**:

1. **Next step:** If someone affected by or concerned about this tool wants review, challenge, correction, complaint, clarification, or help, what does the record say they can do next?
2. **Actor:** Who does the record say can take that step? Preserve role/scope where stated (for example customer, patient, professional intermediary, internal user).
3. **Channel / initiation:** How can the step be initiated or reached? Record an exact channel or action where published. If only a process is referenced, say so rather than inventing a route.
4. **Object / layer:** What appears to be acted on — tool output, broader operational decision/process, data use, general service/help, explanation/justification, or something else?
5. **Status:** Does the record describe the route/process as operating now, unavailable/no separate process, planned/not operating, or unclear?
6. **Evidence:** Copy or identify the sentence(s) that support the answer.

Participants may answer `NOT STATED` or `UNCLEAR`. Those are valid answers where the source does not support a stronger claim.

## Primary outcome

**Evidence-grounded action retrieval score**, 0–6 per record:

- next step/action correctly represented: 1;
- actor scope correctly represented: 1;
- initiation/channel correctly represented or correctly marked unstated: 1;
- challenge object/layer correctly represented: 1;
- operating/planned/unavailable/unclear status correctly represented: 1;
- supporting source evidence correctly located: 1.

No point requires the participant to use Framework/TRACE/ME terminology.

## Safety / honesty penalty

Count **unsupported inference errors** separately. Examples:

- calling general feedback a formal appeal when the record does not;
- claiming a legal right from a contact link alone;
- claiming a route does not exist because no locator appears in the field;
- treating a planned process as operating;
- treating explanation/justification as reversal/recovery;
- generalising a data-removal right into a right to reverse the tool's output.

Primary analysis reports retrieval score and unsupported-inference count separately. Do **not** cancel one with the other in a composite scalar.

## Secondary outcomes

- completion time per record;
- participant confidence (0–100);
- `NOT STATED` / `UNCLEAR` use;
- source-evidence accuracy;
- qualitative comment: what was hardest to find?

No trust, legitimacy, satisfaction or policy-preference outcome is inferred from speed/accuracy alone.

## Design

Preferred design: within-participant crossover with record-level counterbalancing.

- each participant sees each selected record **once**;
- half of records appear in original-record condition and half in Reader-Lens condition;
- assignment is counterbalanced so every record appears in both conditions across participants;
- record order is randomised within participant;
- do not show exploratory semantic labels;
- do not tell participants which condition is expected to perform better;
- score responses blind to condition where practical.

A simple two-sequence design is acceptable for the pilot:

```text
Sequence A: records 1–5 RAW, 6–10 LENS
Sequence B: records 1–5 LENS, 6–10 RAW
```

A later study may use a Latin-square/randomised assignment generated before the first response.

## Ten frozen cases

Selected to span materially different public-action structures rather than to estimate prevalence:

1. Health Research Authority: Proportionate Review Toolkit — direct query/review channel;
2. NHS BSA: Residency Checker — complaints process and policy link;
3. UKHO: Tidal Harmonic Analysis and Prediction — no formal appeal; customer-service feedback;
4. NS&I: PolyAI — no formal appeal; human handoff + broader complaints/escalation, no locator in field;
5. DHSC/NHS Digital: QCovid algorithm — clinician-mediated review/clarification;
6. Wilton Park: Data Cleaning Tool — data-rights/removal route whose relevance to output reconsideration is not established;
7. Cabinet Office: Automated Digital Document Review — no recovery after deletion; explanation/justification remains available;
8. Hampshire and Thames Valley Police: DARAT — process not currently designed / planned via ethical review;
9. DBT: Find Exporters — no parser-observed `Appeals and review` field in the frozen record;
10. National Highways: Highways Webchat — incorrect-answer/concern contact route.

These cases are purposive stress cases, **not a representative sample of ATRS records**.

## Answer-key governance

Before the first human response:

1. freeze the exact source bytes for every case;
2. generate the source-only Reader Lens from those same bytes;
3. freeze a case manifest with source SHA-256;
4. independently adjudicate the answer key against the source wording;
5. preserve disagreements and allow multiple acceptable answers when the source is genuinely ambiguous;
6. score source fidelity, not agreement with a preferred narrative.

`ANSWER_KEY != OFFICIAL INTERPRETATION`.

## Participants / recruitment

No recruitment is authorised by this file.

If a human pilot is later approved:
- preregister target population and sample size before first response;
- avoid presenting the task as legal advice or a test of the participant's intelligence;
- collect only the minimum data needed;
- do not collect sensitive personal experiences unless separately justified/approved;
- participation must be voluntary;
- keep participant data separate from the public ATRS evidence bundle.

The September build does not establish a sample size. A November sprint study should choose and freeze N based on the available legitimate recruitment route and the intended claim (pilot estimation vs inferential test) before data collection.

## Analysis ceiling

A useful pilot result would be something like:

> On this purposive case set, readers using the lens recovered more source-supported action facts / took less time / made fewer unsupported inferences than readers using the original presentation.

It would **not** establish:

```text
READER_LENS_IMPROVES_PILOT_TASK != READER_LENS_IMPROVES_REAL_WORLD_REMEDY
TEN_PURPOSIVE_CASES != WHOLE_ATRS_REGISTER
ONE_RECRUITED_SAMPLE != UK_PUBLIC
COMPREHENSION != TRUST
COMPREHENSION != FAIRNESS
COMPREHENSION != LEGAL_SUFFICIENCY
```

A null or negative result is valid and should shrink/kill the Reader Lens product claim.

## Stop rules

Stop/shrink if:
- source-preserving Reader Lens does not improve retrieval/time/inference behaviour on the task;
- any apparent improvement comes from added interpretation rather than improved evidence organisation;
- the task can be solved equally well by a simpler owner-controlled change (for example direct GOV.UK headings/link placement);
- participant confusion is caused by the Lens itself;
- the study only demonstrates that shorter text is faster to read;
- a strongest owner already supplies equivalent current ATRS task-level evidence.

```text
NULL_RESULT = VALID
OWNER_FOUND = VALID
READER_BENEFIT_UNESTABLISHED UNTIL REAL PARTICIPANT DATA
```

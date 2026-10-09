# ATRS Reader Lens — bounded reader-use protocol

Status: **REPAIRED METHOD / FUTURE HUMAN TEST / NO PARTICIPANT RESULT / NO RECRUITMENT AUTHORISED**

This supersedes the initial two-arm RAW/LENS draft. Codex hostile review (`#364` comment `5720518883`) correctly found that source identity alone did not create information parity, the executable order was not actually randomised, scoring rules were underspecified, and timing/exposure targets were not frozen.

## Question

On actual frozen ATRS records, does reorganising the **same published `Appeals and review` evidence** help a reader recover action-relevant facts more accurately or efficiently, **without increasing unsupported inference**?

This is a prompted field-retrieval task. It is not a test of legal sufficiency, real-world remedy, trust, legitimacy, fairness, or spontaneous comprehension of the whole register.

## Strongest-owner boundary

This study does **not** claim novelty for the premise that algorithmic-transparency information should be simple, understandable, layered, or include contact/appeal information.

Strong owners include:
- BritainThinks / CDEI (`Complete transparency, complete simplicity`): UK public-engagement evidence for clear/simple/layered information and contact/appeal information;
- Government Digital Service: ATRS semantics and meaningful/intelligible-transparency intent;
- Esther Nieuwenhuizen: empirical algorithm-register usability problems for developers/watchdogs/oversight actors;
- de Troya et al. (2026): participatory evidence about sociotechnical context revealed/occluded by a register;
- Public Law Project / Tracking Automated Government: broad UK public-sector ADM visibility/redress/public-law framing.

```text
GENERAL NEED FOR USABLE TRANSPARENCY -> OWNED
GENERAL IMPORTANCE OF CONTACT/APPEAL INFO -> OWNED
GENERAL REGISTER-USABILITY CRITIQUE -> OWNED
TASK-LEVEL RETRIEVAL FROM ACTUAL ATRS APPEALS FIELDS -> UNDER TEST
```

## Information scope

The scored task is explicitly limited to the published **`Appeals and review` field** for each frozen record.

Participant instruction:

> Answer only from the published `Appeals and review` field shown or contained in this frozen record. Do not use other sections to fill a gap. `NOT STATED` and `UNCLEAR` are valid answers.

This removes the initial defect where a RAW participant could legitimately find relevant material elsewhere in the full record but be scored against an Appeals-only key.

For the one frozen case where no parser-recognised `Appeals and review` field exists, the task is to determine that the field is not present in the frozen source. This does **not** mean no review route or practice exists elsewhere.

## Three frozen conditions

All conditions derive from the same source bytes and are rendered locally with no external network dependency during the timed task.

### FULL — full published-record text

A local, plain evidence rendering of the frozen record's `<main>` heading/text content.

Purpose: measures the cost of locating the `Appeals and review` field within the broader published record plus interpreting it.

It is **not** represented as a pixel-identical clone of live GOV.UK.

### EXCERPT — simple field extraction

The exact published `Appeals and review` heading/text only, in a plain minimal layout.

Purpose: strongest simple control. This approximates the value of a direct section jump / extraction without a bespoke Lens.

### LENS — structured field view

The **same exact `Appeals and review` text** as EXCERPT, plus deterministic presentation of links/email/phone-like text already contained in that field. It adds no semantic classification and no generated statement of rights/effectiveness.

Purpose: tests whether evidence organisation/structure adds value beyond simple scoping.

## Primary contrasts

The three conditions answer different questions:

```text
FULL -> EXCERPT = field-location / scoping cost
EXCERPT -> LENS = added value of structured evidence presentation
FULL -> LENS = total combined effect, descriptive only
```

The bespoke Reader Lens earns a product claim only from the **EXCERPT -> LENS** contrast. If EXCERPT performs as well as LENS, route the benefit toward the simpler owner-controlled change.

## Reader task

For each assigned case, answer from the `Appeals and review` field only:

1. **Next step:** What action, if any, does this field say someone can take next for review, challenge, correction, complaint, clarification, or help?
2. **Actor:** Who does the field say can take that step? Preserve role/scope where stated.
3. **Initiation / channel:** How can the step be initiated or reached? If only a process is referenced and no initiation route is given, say `NOT STATED`.
4. **Object / layer:** What is the action about — tool output, broader process/decision, data use, general service/help, explanation/justification, or something else?
5. **Status:** Is the process/action described as operating now, unavailable/no separate process, planned/not operating, or unclear?
6. **Evidence:** Identify the exact field sentence(s) supporting the answer. For a missing field, identify the frozen-page absence marker supplied by the study surface.

`NOT STATED` and `UNCLEAR` are first-class answers. Unsupported certainty is not rewarded.

## Scoring — frozen before first participant

Score each component independently, blind to condition where practical.

### 1. Next step — 0/1

Award 1 when the response gives at least one materially correct source-supported action from the field and does not contradict the field.

Where the field describes several distinct routes, omission of additional routes does not remove the point unless the case key explicitly marks them as **jointly required** for a faithful answer.

A correct `NOT STATED` earns 1 when the field provides no source-supported next step.

### 2. Actor — 0/1

Award 1 for the source-stated actor/role or a non-misleading faithful paraphrase. If the field does not identify an actor, `NOT STATED` earns 1.

Do not infer that a route open to an organisation/professional is open to every member of the public.

### 3. Initiation / channel — 0/1

Award 1 for at least one correct initiation method/channel corresponding to the stated next step.

If the field references a process/right but gives no way to initiate/reach it, `NOT STATED` earns 1. Do not award a point for inventing a channel from another section.

### 4. Object / layer — 0/1

Award 1 for a materially correct layer. Multiple layers may be accepted when the field genuinely spans them. A narrower correct layer is acceptable unless it changes the nature of the action.

### 5. Status — 0/1

Award 1 for correctly representing the field as current/operating, unavailable/no separate process, planned/not operating, or unclear.

If the wording is genuinely ambiguous, `UNCLEAR` is the keyed answer. Do not force certainty to earn the point.

### 6. Evidence — 0/1

Award 1 when quoted/identified field wording actually supports the participant's substantive answer.

For the missing-field case, no sentence can prove absence. The study surface provides a frozen **field-not-observed marker** generated from the heading inventory; correctly identifying that marker earns the evidence point.

## Multiple-route and ambiguity rule

The answer key must distinguish:
- `accepted_alternatives`: one faithful item is sufficient for the component;
- `jointly_required`: all listed facts are needed to avoid material distortion;
- `accepted_not_stated`: absence is an acceptable keyed result;
- `accepted_unclear`: ambiguity is an acceptable keyed result.

Omitted optional routes are not silently converted into errors.

## Unsupported-inference errors

Count separately; do not net against the 0–6 retrieval score.

Examples:
- calling general feedback a formal appeal when the field does not;
- claiming a legal right from a contact link alone;
- claiming no route exists because no locator appears;
- treating a planned process as operating;
- treating explanation/justification as recovery/reversal;
- generalising a data-removal route into output reconsideration;
- importing a route from another record section despite the field-only instruction.

## Conditions must be content-addressed

Before the first participant:
- freeze source bytes;
- generate all three local targets from those exact bytes;
- record each target's SHA-256;
- record exactly which source sections/text each target contains;
- keep the answer key separate from participant materials;
- do not allow facilitator choice of which page/section to show.

`SOURCE_IDENTITY != RENDERED_CONDITION_IDENTITY`.

Both must be preserved.

## Timing / exposure convention

For the timed task:
- use the same browser/device class and viewport policy across conditions;
- local files only; no network loading during the timed exposure;
- all targets begin at scroll position 0;
- outbound navigation is disabled during timing;
- timer starts when the condition target is rendered and the participant starts the case;
- timer stops on response submission;
- record condition, sequence, case, exposure position, completion/abandonment and elapsed time;
- record dropout without silently replacing the participant.

Timing measures task completion under these frozen conditions, not live-site network performance.

## Counterbalancing / order

The initial fixed `1..10` two-sequence order is withdrawn.

Use six pre-generated schedules. Across the six schedules:
- every case appears in FULL, EXCERPT and LENS exactly twice;
- each participant sees each case once;
- case order is deterministically shuffled and frozen before the first response;
- sequence allocation is balanced in blocks where feasible;
- the randomisation seed and generated schedules are preserved.

Within-participant learning/carry-over may still occur. It is an explicit limitation, not something condition inversion eliminates.

## Case set

Ten purposive stress cases remain useful for method falsification:
1. HRA Proportionate Review Toolkit;
2. NHS BSA Residency Checker;
3. UKHO Tidal Harmonic Analysis and Prediction;
4. NS&I PolyAI;
5. QCovid;
6. Wilton Park Data Cleaning Tool;
7. Cabinet Office Automated Digital Document Review;
8. Hampshire/TVP DARAT;
9. DBT Find Exporters;
10. National Highways Highways Webchat.

These cases are purposive stress cases, **not a representative ATRS sample**.

## Answer-key governance

Before any human run:
1. bind each case to source SHA, field-text SHA and condition-target SHA;
2. independently adjudicate the field-only key;
3. preserve disagreements and multiple acceptable answers;
4. freeze component acceptance rules;
5. keep keys inaccessible from participant surfaces;
6. score blind to condition where practical.

`ANSWER_KEY != OFFICIAL_INTERPRETATION`.

## Participants / recruitment

**No recruitment is authorised by this protocol.**

A future human pilot is a separate consequential gate. Before first response, freeze:
- target population;
- recruitment route;
- sample-size rationale;
- consent/data-minimisation handling;
- allocation plan;
- analysis plan.

Do not collect sensitive personal experiences as part of this retrieval task.

## Analysis ceiling

A positive pilot could support only a statement such as:

> On this purposive field-retrieval task, this participant sample recovered more source-supported action facts / took less time / made fewer unsupported inferences under condition X than condition Y.

It would not establish:

```text
PROMPTED_FIELD_RETRIEVAL != UNSOLICITED_COMPREHENSION
READER_LENS_IMPROVES_TASK != READER_LENS_IMPROVES_REAL_WORLD_REMEDY
TEN_PURPOSIVE_CASES != WHOLE_ATRS_REGISTER
ONE_RECRUITED_SAMPLE != UK_PUBLIC
COMPREHENSION != TRUST
COMPREHENSION != FAIRNESS
COMPREHENSION != LEGAL_SUFFICIENCY
```

## Stop / routing rules

- If EXCERPT ~= LENS, the bespoke Lens does not earn an added-value claim; route toward the simpler section-jump/excerpt owner.
- If FULL < EXCERPT but EXCERPT ~= LENS, the main problem is field location/scoping, not Lens structure.
- If LENS increases unsupported inference, shrink/kill the product claim even if it is faster.
- If no condition materially helps, preserve the null and stop.
- If a strongest owner already supplies equivalent ATRS task-level evidence, route to that owner.

```text
NULL_RESULT = VALID
OWNER_FOUND = VALID
METHOD_PACK != HUMAN_RESULT
READER_BENEFIT_UNESTABLISHED UNTIL REAL PARTICIPANT DATA
```

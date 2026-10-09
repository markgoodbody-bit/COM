# ATRS Reader Lens — reader-use protocol v3

Status: **PRE-RUN PILOT METHOD / NO RECRUITMENT / NO PARTICIPANT RESULT / NOT HUMAN-USABILITY EVIDENCE**

This supersedes the executable v2 pack for any future pilot. The earlier two-arm draft and v2 three-condition pack remain historical method iterations.

## Research question

On actual frozen ATRS records, does reorganising the **same published `Appeals and review` evidence** help a reader retrieve prompted action-relevant facts more accurately or efficiently, **without increasing unsupported inference**?

This is a field-retrieval task. It is not a test of legal sufficiency, real-world remedy, trust, fairness, legitimacy, or unsolicited whole-register comprehension.

## Strongest-owner routing

Already owned:
- the general need for simple/layered algorithm transparency;
- the importance of contact and appeal information;
- generic public-register usability critiques;
- ATRS field semantics and public-repository ownership.

Residual test:

> Does a source-preserving presentation of real ATRS `Appeals and review` fields reduce field-location/scoping cost or improve retrieval beyond a simple exact-field excerpt?

If the simple excerpt performs as well as the bespoke Lens, route the benefit to the simpler owner-controlled section-jump/excerpt change.

## Evidence scope

The scored task is restricted to the published **`Appeals and review` field**.

Participant instruction:

> Answer only from the published `Appeals and review` field shown or contained in this frozen record. Do not use other sections to fill a gap. `NOT STATED` and `UNCLEAR` are valid answers.

This scope prevents a full-record participant from being penalised for correctly using information outside the answer key's evidence boundary.

Nine cases are scored. `DBT: Find Exporters`, whose frozen page has no parser-observed `Appeals and review` field, is retained only as a **non-scored sentinel**. It is not part of the primary retrieval score.

## Conditions

All timed targets are local static files derived from the same frozen source evidence. No live network loading is part of the task.

### FULL

A local plain rendering of the frozen record's main-section headings/text. The participant must locate the `Appeals and review` field.

Measures field-location/scoping cost plus interpretation. It is not a pixel-identical GOV.UK usability test.

### EXCERPT

The exact published `Appeals and review` passage isolated in a plain layout, with any extracted published contact/link values represented plainly.

This is the strongest simple control and approximates a section jump/excerpt.

### LENS

The same exact `Appeals and review` passage and the same extracted contact/link values as EXCERPT, with deterministic grouping of those values when present.

LENS must not add generated negative evidence such as "no link was observed" unless the identical cue is present in EXCERPT. v3 omits that asymmetric cue.

```text
EXCERPT_INFORMATION == LENS_INFORMATION
EXCERPT_LAYOUT != LENS_LAYOUT
```

## Primary contrasts

- `FULL -> EXCERPT`: field-location/scoping cost.
- `EXCERPT -> LENS`: added value, if any, of deterministic grouping/structure.
- `FULL -> LENS`: combined descriptive contrast only.

The product claim lives or dies on `EXCERPT -> LENS`, not on `FULL -> LENS` alone.

## Tasks

For each scored case, answer from the `Appeals and review` field only:

1. next step/action;
2. actor/role;
3. initiation/channel, or `NOT STATED`;
4. challenge/action object or layer;
5. current/unavailable/planned/unclear status;
6. exact field evidence supporting the answer.

Unsupported certainty is not rewarded.

## Route-linked scoring

The private key stores **route bundles**, not independent component bags.

A route bundle links:

```text
NEXT_STEP
+ ACTOR
+ CHANNEL
+ OBJECT/LAYER
+ STATUS
```

A scored answer must be faithful to one source-supported route bundle. Components from different routes may not be mixed into an artificial correct cross-product.

Example boundary:
- if NS&I says a customer may request a human in-channel, that human-handoff channel belongs to that route;
- if the same field separately references a complaints process without an initiation locator, the complaints route's channel is `NOT STATED`, not the human-handoff channel.

`NOT STATED` and `UNCLEAR` may score only where the selected route bundle permits them.

The answer key remains provisional and must be independently adjudicated before any human run.

## Evidence point

The evidence point is awarded only when quoted/identified wording in the scored `Appeals and review` field supports the chosen route bundle.

The DBT missing-field sentinel is non-scored and therefore does not require an artificial sentence to "prove" absence.

## Unsupported-inference count

Count unsupported inference separately from retrieval score. Do not net it away against correct retrieval.

Examples include:
- calling general feedback a formal appeal;
- claiming a legal right from a contact token;
- claiming no route exists because no locator is present;
- treating a planned process as operating;
- treating explanation as recovery;
- importing a route from another record section;
- mixing the channel from one route with the action from another.

## Schedule / position balance

Use six frozen schedules built from **two seeded case orders**, each paired with all three condition rotations.

Required invariants:
- every participant sees each of the nine scored cases once;
- every schedule contains 3 FULL + 3 EXCERPT + 3 LENS cases;
- every scored case appears in each condition exactly twice across the six schedules;
- each exposure position 1–9 contains each condition exactly twice across the six schedules.

This repairs the v2 positional imbalance. It does not remove carry-over, learning, case difficulty, dropout, or allocation limitations.

## Target identity and timing

Before first participant:
- freeze source bytes;
- freeze all FULL/EXCERPT/LENS targets;
- record target SHA-256 and path;
- preserve schedule and exposure position;
- keep the private key out of participant materials;
- use the same browser/device class and viewport policy across conditions;
- begin each target at scroll position 0;
- do not use network loading during timed exposure;
- disable outbound navigation during timing;
- timer starts when the target is rendered and the participant begins;
- timer stops on response submission.

The current method pack defines these targets and logs but is not itself a response/timing runner.

## Case/sample ceiling

The nine scored cases are purposive stress cases. They are not a representative ATRS sample.

A future convenience pilot can support only a bounded statement about this task, these cases, and that participant sample.

```text
NINE_PURPOSIVE_CASES != ATRS_POPULATION
PROMPTED_FIELD_RETRIEVAL != UNSOLICITED_COMPREHENSION
COMPREHENSION != EFFECTIVE_REMEDY
ONE_RECRUITED_SAMPLE != UK_PUBLIC
```

## Recruitment gate

**No recruitment is authorised by this protocol.**

Before first human response, separately freeze:
- target population;
- recruitment route;
- sample-size rationale;
- consent/data-minimisation handling;
- allocation plan;
- scoring adjudication procedure;
- analysis plan.

Do not collect sensitive personal experiences in this retrieval task.

## Stop / routing rules

- If `EXCERPT ~= LENS`, the bespoke Lens does not earn an added-value claim; route toward the simpler excerpt/section-jump owner.
- If `FULL < EXCERPT` but `EXCERPT ~= LENS`, the main observed cost is locating/scoping the field, not Lens structure.
- If LENS increases unsupported inference, shrink/kill the product claim even if it is faster.
- If no condition materially helps, preserve the null and stop.
- If a strongest owner already supplies equivalent ATRS task-level evidence, route to that owner.

```text
METHOD_PACK != HUMAN_RESULT
NULL_RESULT = VALID
OWNER_FOUND = VALID
READER_BENEFIT_UNESTABLISHED UNTIL REAL PARTICIPANT DATA
```

# ATRS Answerability Audit

Status: **CURRENT COMPETITION LEAD / FRESH-CORPUS EMPIRICAL CANDIDATE / NOT SELECTED / NOT SUBMITTED / NOT A COMPLIANCE SCORE**

## The question

> **Does a current public ATRS record let a reader bind a stated review/challenge/correction route to the thing in the published decision pipeline that route can actually act on, and does it state who can initiate/use that route and how?**

This measures the **published record**, not hidden government practice, legal sufficiency, fairness or route effectiveness.

## Why this question exists

The Government Digital Service owns ATRS and its semantics.

Current ATRS guidance explicitly asks publishers completing `Appeals and review` to consider both:
- whether the **algorithmic-tool output** can be challenged or appealed; and
- whether the **broader operational-process output** can be challenged or appealed.

#364 does not claim this distinction.

It asks whether the live public records make that relationship legible.

```text
GDS OWNS THE TWO-SITE DISTINCTION
PROJECT MEASURES PUBLIC IMPLEMENTATION
CODER_CAN_INFER != RECORD_MAKES_LEGIBLE
```

## Unit of analysis

Do not label a whole record `contestable / not contestable`.

One relation row preserves:

```text
ROUTE_PROPOSITION
+ ACTOR_SCOPE
+ ACTION / NEXT STEP
+ CHANNEL
+ TARGET_SITE
+ ROUTE_FORM
+ TRIGGER
+ STATED_EFFECT
+ BINDING_BASIS
+ EVIDENCE_LOCATOR
+ DEPLOYMENT_STATUS
+ DISAGREEMENT
```

Target vocabulary is intentionally small:

```text
TOOL_OUTPUT
BROADER_OPERATIONAL_PROCESS
OTHER_STATED_TARGET
NO_RELEVANT_CHALLENGE_WITH_REASON
LAYER_NOT_STATED
UNBOUND_OR_CONTRADICTORY
```

A missing edge stays missing.

No scalar quality, contestability or compliance score is produced.

## Strong-owner / prior-work boundary

Broad algorithm-register critiques are **not** the contribution.

Strong owners already establish that:
- transparency is not the same as accountability or contestability;
- algorithm registers can omit sociotechnical context;
- public registers can be audited against transparency/accountability goals;
- register users may need information about redress, human discretion and system context.

Particularly material 2026 owners:
- Das et al., *Bureaucratic Silences* — complete Canadian federal AI Register, 409 systems, FAccT 2026;
- de Troya et al., *Co-constructing sociotechnical AI governance* — participatory system mapping using algorithm registers;
- Peljto et al., *Are Algorithm Registers Transparent? Perspectives from Germany* — structured external register audit.

See:
- `OWNER_MAP.md`
- `PRIOR_WORK_PRESSURE_20260918.md`

Therefore do **not** claim:

```text
"transparency != contestability" = OUR NOVELTY
"registers omit accountability context" = OUR NOVELTY
"full-register audit" = OUR NOVELTY
TOOL_OUTPUT_VS_PROCESS_OUTPUT = OUR PRIMITIVE
```

The surviving candidate delta is the narrow UK implementation measurement:
**route -> target -> actor -> initiation/channel**, source-bound to the live ATRS record.

`NOT_FOUND_EXACT_OWNER != NOVELTY_PROVED`.

## September evidence and method calibration

Frozen September source witness:

```text
run = 35257984573 SUCCESS
source head = 4a7b43df95a2b776b885f8ee903d929100414af7
artifact = 10513278849
artifact sha256 = ad315d9b08a0af65c4615638df2235b9ce6f021307315fbeb6dfcbd8cbdb0097
source HTML pages = 152
finder / Search API membership = 152 / 152
```

Version-aware reparse over the **same source bytes** repaired legacy-heading misses without rewriting history.

Current corrected structural observations on that frozen source:

```text
human_review = 152/152 observed
appeals_review = 151/152 observed
model_performance = 139/152 observed
risks = 152/152 observed
impact_assessment = 145/152 observed
maintenance = 152/152 observed
senior_responsible_owner = 152/152 observed
```

```text
REPRODUCED != CORRECT
FIELD_PRESENT != PRACTICAL_ANSWERABILITY
```

### Frozen 16-record relation calibration

Two differentiated apertures independently coded a deterministic 16-record sample from the frozen pages before reconciliation.

Sample identity:

`c97ea5548ccc26b130a8ffe2783569d6d365897fcf0e04a35fba033486012b54`

Result:

```text
METHOD = KEEP
CODEBOOK = REPAIR
PRIMARY INCLUSION = SHRINK
VERSION = SECONDARY TAG ONLY
```

The exercise found real defects rather than agreement theatre:
- trigger != target;
- generic monitoring/QA/feedback must not become remedy by keyword;
- contacts cannot be borrowed as route channels;
- bare N/A is not a route;
- unknown-target positive routes must not become `NO_ROUTE_STATED_IN_RECORD`;
- actor eligibility/initiation must remain separate from internal review.

Final September working head before competition-readiness preparation:

`827b82382f26c52d62272dd4fe4e87ce52d1f78e`

The codebook after calibration is:
`RELATION_CODEBOOK_V2_20260918.md`.

```text
CALIBRATION_SURVIVED != METHOD_VALIDATED
TWO_AI_READS != HUMAN_VALIDATION
```

## Deliberately uncomputed result

The full current population has **not** been relation-coded under codebook v2.

That is intentional.

September already exposed real records during method development, so November is not a blind holdout:

```text
NOVEMBER_CORPUS != BLIND HOLDOUT
```

But no full-population relation result exists.

Until the sprint/rules gate:

```text
DO NOT FULL-CODE THE REMAINING POPULATION
DO NOT COMPUTE PRIMARY POPULATION COUNTS
DO NOT POLISH SEPTEMBER INTO A RESULT
```

The next substantive evidence should come from a **fresh sprint-time corpus**, if live Apart rules permit.

## November competition posture

Current official Apart event:
**AI x Epistemics Research Sprint — 13–15 November 2026, online**.

The Open Track explicitly asks what can be measured about a live epistemic deployment using weekend-downloadable data and welcomes investigative-research-shaped deployment/impact work.

Preparation:
- `SPRINT_EXECUTION_PLAN.md`
- `COMPETITION_READINESS_20260918.md`
- `PRIOR_WORK_PRESSURE_20260918.md`

Current assessment:

```text
REAL CONTENDER = YES
FIRST PLACE PLAUSIBLE = YES
FAVOURITE = NOT ESTABLISHED
WIN PROBABILITY = NOT DEFENSIBLY QUANTIFIABLE YET
```

The decisive evidence is still missing: the fresh population result.

## Weekend result shapes — all valid

The method permits:

```text
A. MATERIAL UNBOUNDNESS
B. MATERIAL LEGIBILITY
C. MIXED STRUCTURE
D. METHOD FAILURE
E. STRONGER OWNER FOUND
```

No result needs to be rescued.

## Judge path if the result survives

A strong final object should give a reader a five-minute path:

1. one concrete question;
2. one diagram of route -> actor -> target -> effect;
3. one current population table;
4. four contrasting source-grounded records;
5. every headline count traceable to evidence;
6. one reproducibility command;
7. limitations on the first page.

No TRACE branding is needed for the competition result.

## Reader Lens

Reader Lens remains preserved as a secondary source-readback experiment.

It is **not** the current research spine and no human reader benefit has been demonstrated.

```text
SOURCE_READBACK_AID != DEMONSTRATED_READER_BENEFIT
```

Do not recruit participants by momentum.

## Kill conditions

Kill or demote #364 if:
- live Apart rules make the prepared-method / fresh-result boundary ineligible;
- full relation coding requires uncontrolled category expansion;
- differentiated coding cannot be reconciled source-bound;
- a stronger current owner already performs the UK ATRS full-population route→target→actor→initiation measurement;
- the result reduces to “free text varies”;
- the result needs a moral/compliance score to become interesting;
- evidence cannot trace headline counts back to source.

```text
OWNER_FOUND -> STOP
NULL_RESULT = VALID
PURPOSE > INSTRUMENT
```

## Authority boundary

No registration, organiser contact, terms acceptance, submission, participant recruitment, provider spend or TRACE/ME change is implied by this branch.

Re-read live Apart Guidelines/terms before any external competition action.

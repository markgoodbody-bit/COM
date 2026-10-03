# ATRS Answerability Audit — November sprint execution plan v2

Status: **PRE-SPRINT PREPARATION / METHOD FROZEN / FULL-POPULATION RELATION RESULT DELIBERATELY UNCOMPUTED / LIVE RULES MUST BE RE-READ**

Updated: 18 September 2026.

This plan supersedes the earlier field-presence / Reader-Lens-centred execution plan. The current research spine is the source-bound route-relation measurement in `RELATION_CODEBOOK_V2_20260918.md`.

## Competition fit

Current Apart AI x Epistemics public page, checked 18 September 2026:
- event: 13–15 November 2026, online;
- Open Track explicitly asks: **using only data downloadable this weekend, what can you measure about a live epistemic deployment, and what does that mean for the field?**
- projects on deployment/impact may look like investigative research rather than software;
- teams pick a tight question and ship a benchmark, tool, product or study plus write-up.

Official event page:
https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15

Current page does not yet expose a complete November judging/rules rubric through the public crawl. Historical Apart sprints repeatedly allowed advance thinking while requiring core research to happen during the event. Treat that as a likely constraint, not as the final November rule.

Before registration or submission:
1. re-read live Guidelines and submission terms;
2. disclose September preparation completely;
3. if pre-existing tooling/method is inadmissible, use it only as background and do not submit the project under false weekend authorship.

## Sharp question

> **Does a current public ATRS record let a reader bind a stated review/challenge/correction route to the thing in the published decision pipeline that route can actually act on, and does it state who can initiate/use that route and how?**

Object measured:
**what the public record makes legible**.

Not measured:
- route effectiveness;
- legal sufficiency;
- fairness;
- internal practice;
- compliance;
- department quality.

```text
PUBLIC_RECORD_RELATION != REAL_WORLD_ROUTE
ROUTE_PUBLISHED != ROUTE_EFFECTIVE
CODER_CAN_INFER != RECORD_MAKES_LEGIBLE
```

## Pre-sprint evidence boundary

September preparation has already:
- downloaded and content-addressed 152 ATRS pages;
- built/repaired parsers;
- inspected the full record structure;
- developed the relation question using real examples;
- independently coded and reconciled a deterministic 16-record calibration set;
- exposed additional named records through dry runs and method development.

Therefore:

```text
NOVEMBER_CORPUS != BLIND HOLDOUT
METHOD_DEVELOPMENT_SAW_REAL_CORPUS
```

But the full current population has **not** been relation-coded under codebook v2 and no population result exists.

Preserve that boundary:

```text
DO NOT FULL-CODE THE REMAINING POPULATION BEFORE THE SPRINT
DO NOT COMPUTE PRIMARY POPULATION COUNTS BEFORE THE SPRINT
DO NOT POLISH SEPTEMBER INTO A RESULT
```

The November contribution, if live rules allow, is the fresh acquisition + full relation census + disagreement/reconciliation + analysis + write-up.

## September = disclosed preparation

Disclose as pre-existing:
- membership validator;
- source downloader/content-addressed witness;
- version-aware parser;
- frozen September corpus;
- Reader Lens (secondary / not current research spine);
- relation method/codebook;
- 16-record calibration and all repairs;
- owner/prior-work map;
- known limitations;
- this execution plan.

Do not imply these were built during the weekend.

## Weekend core work

### Gate 0 — live rules

Before data work:
- snapshot live Apart Guidelines/terms;
- determine whether the prepared method/tooling is admissible;
- record what is pre-existing versus weekend-created;
- stop or re-scope if the terms make the planned contribution ineligible.

### Gate 1 — fresh ATRS population

Fetch the live GOV.UK finder and every current ATRS record.

Preserve:
- retrieval timestamp;
- exact URL population;
- finder count;
- independent membership check where available;
- raw source bytes;
- SHA-256 per record;
- parser/code identities.

Compare membership/bytes to September only **after** the November source snapshot is frozen.

Count equality is not byte or membership equality.

### Gate 2 — freeze codebook identity

Primary method:
`RELATION_CODEBOOK_V2_20260918.md`

Before full coding:
- hash the codebook used;
- make no category change merely to make a difficult record fit;
- if a material codebook defect appears, record it as a method event.

A necessary mid-sprint method repair must be:
1. explicit;
2. justified by a concrete counterexample;
3. replayed across already-coded records affected by the rule;
4. reported as a limitation.

Category proliferation is a kill signal.

### Gate 3 — build bounded route inventory

For every current record, preserve each explicit published route proposition as:

```text
RECORD
ROUTE_PROPOSITION
ACTOR_SCOPE
DERIVED_ACTOR_CLASS
ACTION / NEXT STEP
CHANNEL
TARGET_SITE
ROUTE_FORM
TRIGGER
STATED_EFFECT
BINDING_BASIS
EVIDENCE_LOCATOR
DEPLOYMENT_STATUS
CODER_DISAGREEMENT
```

Primary target vocabulary stays closed:

```text
TOOL_OUTPUT
BROADER_OPERATIONAL_PROCESS
OTHER_STATED_TARGET
NO_RELEVANT_CHALLENGE_WITH_REASON
LAYER_NOT_STATED
UNBOUND_OR_CONTRADICTORY
```

No whole-record contestability/compliance score.

### Gate 4 — differentiated coding

Preferred:
- two differentiated coders independently code the full current population;
- Framework integrates only after first-pass outputs are frozen.

Fallback if full dual coding is operationally unavailable:
- one full-population primary pass;
- second independent pass on a deterministic validation sample fixed before seeing primary labels;
- second review of every row supporting a headline claim;
- preserve all unresolved disagreements.

Report coder identities/roles and prior exposure. AI-aperture agreement is not human validation or world truth.

### Gate 5 — source-bound adjudication

Resolve disagreements only through:
- explicit record text;
- existing codebook rule;
- preserved unknown.

Do not use:
- linked complaint pages;
- hidden government process knowledge;
- inferred legal rights;
- domain assumptions.

External/linked-site inspection, if useful, is a separate secondary observation.

### Gate 6 — fixed primary output tables

Primary census outputs are descriptive counts over the current public register:

1. route propositions by target site;
2. affected/public routes vs internal review;
3. DIRECT vs EXPLICIT_CROSS_FIELD vs LAYER_NOT_STATED / UNBOUND;
4. channel stated vs not stated;
5. explicit affected actors with:
   - ROUTE_STATED;
   - NO_ROUTE_STATED_IN_RECORD;
   - AFFECTED_ACTOR_NOT_IDENTIFIED;
6. explained no-separate-route propositions;
7. unexplained N/A;
8. operating vs planned/pre-production routes;
9. coder disagreement / unresolved counts.

This is a finite register census. Primary proportions do not need performative sampling p-values. Uncertainty is mainly:
- coding uncertainty;
- source completeness;
- currentness;
- generalisation beyond the observed register.

### Gate 7 — secondary analyses

Allowed only after primary tables are frozen:
- descriptive ATRS-version stratification;
- tool role / phase / organisation-type context;
- September-to-November source/member changes;
- changed-record field diffs.

Preserve:

```text
VERSION_ASSOCIATION != VERSION_CAUSED_CHANGE
OLDER_RECORD != CONTROL_GROUP
FULL_REGISTER != ALL_PUBLIC_SECTOR_AI
```

Do not rescue a weak primary result with exploratory slicing.

## Predeclared result shapes

The sprint may honestly produce any of these:

### A. Material unboundness
Many stated routes cannot be bound from the public record to what they can change, or actor/channel is often unstated.

Report the implementation pattern and concrete source examples.

### B. Material legibility
Most routes are clearly bound and usable as published information.

Report that positive result and identify where the register is already working well.

### C. Mixed structure
Tool-output, broader-process, unknown-target and actor-silence patterns differ materially across explicit source-supported contexts.

Report the heterogeneity without inventing a scalar ranking.

### D. Method failure
Route discovery or target binding remains too discretionary despite v2.

Report method failure; do not publish population claims.

### E. Owner found
A stronger current analysis already measures the same relation at equal or better resolution.

Route to owner and stop.

```text
NULL / POSITIVE / ADVERSE RESULT = VALID
```

## What could make this a strong Apart submission

The report should give a judge a five-minute path:

1. **One concrete public problem**
   - an ATRS field names a challenge/review route;
   - can the reader tell what that route can actually act on?

2. **One source-grounded diagram**
   ```text
   TOOL / PROCESS
        |
   PUBLISHED ROUTE
        |
   ACTOR -> INITIATION -> TARGET -> EFFECT
   ```
   Missing edge stays missing.

3. **One population table**
   - current complete public register;
   - exact counts;
   - no score.

4. **Four contrasting real records**
   - direct tool-output route;
   - broader-process route;
   - stated route with target not stated;
   - explicitly affected actor with no stated positive route / or explained no-separate route.

5. **One reproducibility command**
   - source snapshot -> parse -> coding table -> figures/tables.

6. **Limitations on the first page, not buried**
   - public disclosure only;
   - coding judgement;
   - development exposure to September corpus;
   - no effectiveness/compliance inference;
   - no causal version claim.

## Artifact for someone outside the sprint

If the result survives, generate a static evidence browser from the final table:

For every counted relation:
- record title;
- source field/locator;
- short evidence excerpt;
- actor;
- target;
- route form;
- binding basis;
- disagreement state.

This browser is an audit surface, not a scorecard.

A judge/GDS/civil-society reader should be able to click from a headline count to the evidence rows behind it.

## Winning narrative boundary

Do **not** lead with:
- TRACE;
- Mechanical Ethics;
- “transparency is not contestability”;
- “appeal fields vary”;
- a new ontology;
- version superiority;
- Reader Lens;
- AI-agent architecture.

Candidate plain-language lead:

> The UK publishes a national register describing public-sector algorithmic tools. Its own guidance asks organisations to consider challenges to both the tool's output and the broader process. We measured whether the public records actually tell a reader **what a stated challenge route can change, who can use it, and how**.

Then show the result.

## Competition kill conditions

Do not submit #364 merely because it was prepared.

Kill or demote if:
1. live November rules make the weekend contribution ineligible;
2. full coding needs uncontrolled category expansion;
3. independent coding cannot be reconciled source-bound;
4. an exact stronger owner exists;
5. primary result reduces to “free text varies”;
6. the finding becomes interesting only after moral/compliance scoring;
7. the evidence browser cannot trace headline counts back to source;
8. the report cannot state a consequential result in two sentences without framework jargon.

## Authority gates

No registration, organiser contact, terms acceptance, participant recruitment, submission or spend follows from this plan.

Live rule acceptance and external submission remain explicit human gates.

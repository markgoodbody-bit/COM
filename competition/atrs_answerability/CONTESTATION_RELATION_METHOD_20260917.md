# ATRS contestation-relation method — source-bound binding rule

Status: **WORKING METHOD / OWNER-ATTRIBUTED / NOT THEORY / NOT RESULT / NOT HUMAN STUDY**  
Date: 17 September 2026

## Why this is narrower than the earlier dry run

The project does **not** own the idea that contestability can occur at different sites in an AI-enabled decision process.

Strong owners already include:

- Yurrita et al. (2025), *Identifying Algorithmic Decision Subjects' Needs for Meaningful Contestability*, which motivates opening **sites of contestation in AI pipelines** and identifies decision subjects' procedural/information needs;
- Alfrink et al. (2022/2023), *Contestable AI by Design*, which maps contestability features and practices across actors and lifecycle stages;
- current GDS ATRS v4 guidance, which explicitly asks publishers to consider challenge/appeal of both the **algorithmic-tool output** and the **broader operational-process output**.

Therefore:

```text
SITES_OF_CONTESTATION != OUR_THEORY
TOOL_OUTPUT_VS_PROCESS_OUTPUT != OUR_PRIMITIVE
CONTESTABILITY_FRAMEWORK != OUR_DELTA
```

The residual question is empirical and implementation-specific:

> **Does a current public ATRS record let a reader bind a stated review/challenge/correction route to the thing in the published decision pipeline that route can actually act on, and does it state who can initiate/use that route and how?**

This is a measurement of the public record, not the real-world effectiveness of the route.

## Unit of analysis

Do not score whole records as `contestable` / `not contestable`.

A coding unit is a source-supported relation:

```text
CONTESTATION_RELATION :=
  ROUTE_PROPOSITION
  + TARGET_SITE
  + ACTOR_SCOPE
  + INITIATION_OR_REVIEW_MODE
  + ROUTE_FORM
  + STATUS_OR_EFFECT
  + EVIDENCE_REFS
  + BINDING_BASIS
  + DISAGREEMENT_STATE
```

The object is an analysis relation only. It is not proposed as a TRACE primitive, standard extension or universal ontology.

## Target site

Use the smallest target vocabulary needed to answer the GDS two-layer question:

```text
TOOL_OUTPUT
BROADER_OPERATIONAL_PROCESS
BOTH_OR_DISTINCT_ROUTES_TO_BOTH
OTHER_STATED_TARGET
NO_RELEVANT_CHALLENGE_WITH_REASON
UNKNOWN_OR_UNBOUND
```

`OTHER_STATED_TARGET` prevents data-rights, service-feedback or model-development routes being silently forced into one of the GDS pair.

Examples:
- a route to contest a residency check result may target `TOOL_OUTPUT`;
- a normal permitting appeal may target `BROADER_OPERATIONAL_PROCESS`;
- data removal through a DPO may be `OTHER_STATED_TARGET` unless the record explicitly connects it to reconsideration of tool output/process outcome;
- generic feedback may be another stated target/route form without becoming appeal;
- if the text does not establish the target, use `UNKNOWN_OR_UNBOUND`.

## Existing dimensions — reuse, do not reinvent

The September exploratory codebook already carries most route/initiation distinctions. Reuse or interoperate with it rather than minting synonyms:

```text
PUBLIC_INITIATION
PROCESS_REFERENCE
HELP_FEEDBACK
IN_CHANNEL_HANDOFF
INTERNAL_REVIEW
NO_SEPARATE
SELF_CORRECTION
DATA_RIGHTS
REFUSAL_OR_OPT_OUT
EXPLANATION_ONLY
PLANNED_NOT_OPERATING
AMBIGUOUS
```

Actor scope remains explicit: affected person/member of public, customer/user, professional intermediary, researcher, publisher, internal operator, organisation, or not stated as supported by source.

## Fail-closed target binding

A target-site assignment needs an explicit public-record basis. Use these binding states:

### `DIRECT`

The route proposition itself names or unambiguously identifies its target.

Examples:
- `If the residency check fails, provide documentary evidence` -> failed check/result is directly identified;
- `normal permitting appeals processes apply` -> permitting process is directly identified;
- `request review if you believe the tool failed` -> tool output/operation is directly identified.

### `EXPLICIT_CROSS_FIELD`

The route proposition uses a named decision/process/output whose relation to the tool is explicitly described elsewhere in the same ATRS record.

Required:
- a shared named referent or explicit textual link;
- evidence refs to both propositions;
- no hidden assumption that because a tool participates in a process, every appeal of that process is an appeal of the tool output.

Example shape:

```text
PROCESS_INTEGRATION: tool supports permitting officers; final permitting decision remains with officer
APPEALS: normal permitting appeals processes apply
-> BROADER_OPERATIONAL_PROCESS / EXPLICIT_CROSS_FIELD
```

### `UNBOUND`

Use when target assignment would require the coder to supply the causal/process link.

Examples:
- `N/A` with no explanation;
- `a challenge mechanism exists` but unclear whether it challenges model output or programme eligibility;
- a generic complaints link where the complaint object is not stated;
- a feedback route where the record does not say whether it can alter the person's outcome, system behaviour, or only future development.

```text
CODER_CAN_INFER != RECORD_MAKES_LEGIBLE
PLAUSIBLE_TARGET != SOURCE_BOUND_TARGET
UNKNOWN != DEFECT_BY_ITSELF
```

## Initiation/review mode is separate from target

A route can act on tool output while remaining inaccessible to the affected person.

Preserve the existing distinction:

```text
PUBLIC_INITIATION
PROCESS_REFERENCE
IN_CHANNEL_HANDOFF
INTERNAL_REVIEW
HELP_FEEDBACK
SELF_CORRECTION
...
```

Do not collapse:

```text
INTERNAL_REVIEW != PUBLIC_INITIATION
HUMAN_IN_LOOP != DECISION_SUBJECT_CAN_CONTEST
PROCESS_REFERENCE != INITIATION_INSTRUCTION
ELIGIBLE_ACTOR_NAMED != CHANNEL_STATED
FEEDBACK != RECONSIDERATION
```

This is load-bearing. MoJ E-Supervision already supplies a frozen counterexample: practitioner review of non-matches coexists with an explicit statement that there is no formal public appeal because the tool does not determine service access.

## What to count in a fresh corpus

If the method survives hostile review, the November fresh-corpus report may describe, without a scalar score:

- records with at least one `DIRECT` tool-output challenge/correction relation;
- records with at least one `DIRECT` or `EXPLICIT_CROSS_FIELD` broader-process challenge relation;
- records with distinct routes to both;
- records explicitly stating no relevant tool-specific/broader route with a source-supported reason;
- records where the stated route target remains `UNBOUND`;
- route relations by actor/initiation mode;
- route relations by route form/status;
- disagreement/unknown counts;
- descriptive standard-version and tool-role stratification only where source supports it.

Do not combine these into one quality, compliance or contestability score.

## Version posture

The frozen September population demonstrates enough records for descriptive stratification:

```text
v4.0 = 53
v3-family = 88
v2.1 = 4
v1.1 = 7
```

But version is not the primary thesis.

Later records differ in publication time, policy environment, mandatory-scope context and tool composition. Therefore:

```text
VERSION_ASSOCIATION != VERSION_CAUSED_CHANGE
V4_GUIDANCE_EXPLICIT != V4_RECORD_AUTOMATICALLY_CLEAR
OLDER_RECORD != CONTROL_GROUP
```

A useful secondary question is only whether the **current register** shows different descriptive binding patterns across versions/tool roles.

## Falsifiers

Kill or shrink the method if:

1. independent coders cannot apply `DIRECT / EXPLICIT_CROSS_FIELD / UNBOUND` consistently on concrete records without adding unstated process assumptions;
2. the target relation duplicates an exact existing current-ATRS full-corpus analysis;
3. almost every case becomes `UNBOUND` because the public records do not carry enough relation structure, unless that itself remains an honest, consequential implementation finding rather than codebook failure;
4. almost every route is trivially direct and the measurement adds no useful information beyond reading the field;
5. the method proliferates target categories until it becomes a bespoke ontology;
6. version/tool-role cuts are too confounded or sparse to add descriptive value;
7. the result still needs a moral/compliance score to become interesting;
8. the result reduces to `free-text fields vary`.

`NULL_RESULT = VALID`.

## Relationship to the Reader Lens / human pilot

The existing `FULL / EXCERPT / LENS` pilot answers a different question: retrieval cost and whether deterministic grouping adds value over a plain exact-field excerpt.

It is **not required** to establish the fresh-corpus relation measurement.

No participant recruitment or human data collection is authorised by this method.

## Strongest surviving claim ceiling

If a fresh full-corpus study supports it, the result may say approximately:

> Current ATRS guidance asks publishers to consider challenge of both algorithmic-tool output and the broader operational-process output. We measured whether published ATRS records bind stated challenge/review/correction routes to those sites, who is stated to initiate or perform the route, and where the public record leaves that relationship unbound.

It may **not** say from this evidence alone:

```text
ROUTE_PUBLISHED -> ROUTE_WORKS
PUBLIC_INITIATION_STATED -> ROUTE_REACHABLE
TARGET_BOUND -> DECISION_FAIR
UNBOUND_RECORD -> NO_REAL_ROUTE
V4_ASSOCIATION -> V4_CAUSED_IMPROVEMENT
ATRS_SAMPLE -> ALL_AI_GOVERNANCE
```

## Owner routing

If this measurement finds a concrete gap, the first strong owner is GDS/ATRS itself. The useful output is evidence that can be handed back to the standard owner, not a competing transparency framework.

```text
PROJECT_LANGUAGE_HELPED_US_NOTICE != PROJECT_OWNS_CONTESTABILITY
MEASURE_IMPLEMENTATION -> ROUTE_TO_OWNER
PURPOSE > INSTRUMENT
```
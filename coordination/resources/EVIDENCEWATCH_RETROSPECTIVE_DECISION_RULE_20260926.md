# EvidenceWatch Brierley retrospective — predeclared result routing

Date: 26 September 2026

Status: **PRE-RUN DECISION RULE / NO MODEL OUTPUT EXISTS**

Purpose:

Prevent post-hoc interpretation of the frozen v2 retrospective result.

This rule does **not** define a universal accuracy threshold. It asks a narrower question:

> Does the pinned model add discriminative signal beyond the frozen trivial lexical baselines at its own strict operating point, without provider/analysis failure?

## Inputs

Use only the already frozen scored result:
- strict failure-worst-case sensitivity;
- strict false-alert rate;
- provider/analysis failure count;
- each frozen lexical baseline's best sensitivity at or below the model strict false-alert rate.

Do not substitute available-case metrics for the headline decision.

## Route 1 — provider / analysis failure

If **any** case has a provider or analysis failure:

```text
ROUTE = INCONCLUSIVE_PROVIDER_OR_ANALYSIS_FAILURE
```

The strict score remains visible, but the run does not earn a clean semantic-discrimination interpretation.

Next action:
- preserve the failed run exactly;
- identify the failure mechanism;
- repeat only as a separately declared run if the cause is external/transient and repetition is justified;
- never silently resume or merge partial runs.

This route has priority over lexical-dominance interpretation.

## Route 2 — trivial lexical weak dominance

Only when failures = 0:

For each frozen lexical metric, use the post-unblinding descriptive operating point with false-alert rate <= the model's strict false-alert rate.

A lexical baseline **weakly dominates** the model if:

```text
lexical sensitivity >= model strict sensitivity
AND
lexical false-alert rate <= model strict false-alert rate
```

If one or more frozen lexical baselines weakly dominate:

```text
ROUTE = NARROW_OR_STOP_SEMANTIC_VALUE_CLAIM
```

Meaning:
- the benchmark does not support a claim that model reasoning adds material-change discrimination beyond simple surface-change magnitude at that operating point;
- do not market the result as semantic advantage;
- owner-subtract, redesign, or move only with a narrower claim that does not depend on semantic superiority.

This does **not** prove the model is useless for authority/provenance/routing in a real workflow. It blocks only the semantic-discrimination inference from this retrospective test.

## Route 3 — retrospective signal survived

Only when:
- provider/analysis failures = 0; and
- no frozen lexical baseline weakly dominates the model strict operating point.

Then:

```text
ROUTE = RETROSPECTIVE_SIGNAL_SURVIVED
```

This earns only:

> The frozen retrospective engineering signal survived its predeclared trivial-baseline challenge and is worth taking into a harder real-workflow shadow falsification.

It does **not** earn:
- product validation;
- research-user validation;
- review-level efficacy;
- market demand;
- clinical/scientific materiality;
- superiority to EPPI / MAGIC / ALEC / Cochrane;
- autonomous operation.

Next action:
- real current workflow;
- existing-practice comparator;
- measured reviewer burden;
- misses / false alerts;
- owner-subtraction remains live.

## No fourth route

Do not create a post-hoc "promising but..." category to rescue an awkward result.

```text
FAILURE -> INCONCLUSIVE
LEXICAL DOMINANCE -> NARROW / STOP SEMANTIC VALUE CLAIM
NO FAILURE + NO DOMINANCE -> REAL-WORKFLOW FALSIFICATION ONLY
```

Negative or null outcomes remain useful evidence.

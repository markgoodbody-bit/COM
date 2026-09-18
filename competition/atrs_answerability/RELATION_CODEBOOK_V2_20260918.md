# ATRS route-relation codebook v2 — post-calibration

Status: WORKING POST-CALIBRATION METHOD / NOT RESULT / NOT THEORY / NOT HUMAN STUDY
Date: 18 September 2026

This file applies only to future coding after the two frozen first passes and reconciliation. It does not rewrite either first-pass table.

Owner boundary remains:
- GDS owns ATRS semantics and the tool-output / broader-process distinction;
- contestability literature owns sites/actors/lifecycle framing;
- this project measures current public-record implementation.

## 1. Relation inventory and primary unit

First build a **bounded relation inventory** of explicit published route propositions. Preserve a proposition even when its target cannot be bound from the record.

Then separate the primary confirmed-target table.

One primary confirmed-target row is one published proposition that states:
- a route/action by which a person or actor can review, challenge, correct, override, reconsider, complain/appeal, hand off, opt out, supply alternative evidence, obtain explanation, or self-correct in relation to a specific TOOL_OUTPUT or BROADER_OPERATIONAL_PROCESS outcome; or
- an explicit source-supported proposition that no such route is relevant, with a stated reason.

Explicit route propositions with `LAYER_NOT_STATED` or an `OTHER_STATED_TARGET` are retained in the relation inventory and reported separately. They are not counted as confirmed tool-output/broader-process routes.

Keep actor/action/channel/target/form/status/evidence together.

```text
ROUTE_PROPOSITION_OBSERVED != PRIMARY_TARGET_CONFIRMED
UNKNOWN_TARGET != DROP_THE_PROPOSITION
```

## 2. Primary stopping rule

Do not place these into the primary route table merely because they contain words such as review, feedback, monitor, error, audit or correction:
- generic model-performance monitoring;
- routine maintenance;
- supplier/product feedback;
- governance audit;
- security/threat reporting;
- data-access/data-rights action;
- research-proposal governance;
- general development feedback;
- source/documentation maintenance.

They may be kept as secondary context.

Promote one into the primary table only when the record explicitly connects it to review/reconsideration/correction of a current tool output or broader-process outcome.

MONITORING != ANSWER_BACK
GENERIC_FEEDBACK != RECONSIDERATION
DATA_RIGHTS != OUTPUT_REVERSAL
TRIGGER != TARGET

## 3. Target site

Primary target vocabulary remains:
- TOOL_OUTPUT
- BROADER_OPERATIONAL_PROCESS
- OTHER_STATED_TARGET
- NO_RELEVANT_CHALLENGE_WITH_REASON
- LAYER_NOT_STATED
- UNBOUND_OR_CONTRADICTORY

Use OTHER_STATED_TARGET only when the record explicitly names another object the action acts on.

Do not use TOOL_OUTPUT merely because tool output triggered the route.

## 4. Trigger / review object / stated change

For every primary route preserve three questions:
- WHAT TRIGGERS THE ROUTE?
- WHAT DOES THE ROUTE REVIEW OR ACT ON?
- WHAT CHANGE OR EFFECT DOES THE RECORD STATE?

They may be different.

If a failed automated check triggers documentary evidence but the stated effect is an entitlement/application decision, code the target as the broader process unless the record explicitly says the automated result is revised.

## 5. Binding basis

DIRECT:
Use when the route proposition itself names its target sufficiently to assign the target site.
Other fields may corroborate a DIRECT assignment.

EXPLICIT_CROSS_FIELD:
Use only when another field in the same frozen record is necessary to bind the route proposition to the target site.
Required:
- shared named referent or explicit textual relation;
- evidence locator to both fields.

LAYER_NOT_STATED:
A route proposition exists, but the record does not state whether it acts on tool output, broader process, or another identifiable target.

UNBOUND_OR_CONTRADICTORY:
Use only when an attempted explicit target binding fails or conflicts.

A contradiction in status/effect does not erase an otherwise clear target.

CORROBORATION != BINDING_DEPENDENCE
CONTRADICTORY_EFFECT != UNKNOWN_TARGET

## 6. Actor

Preserve free-text actor scope and add a derived actor class:
- AFFECTED_OR_PUBLIC
- INTERNAL
- SUPPLIER_OR_INTERMEDIARY
- NOT_STATED

This class is descriptive only.

Do not infer a person can initiate a route because internal staff review the same output.

## 7. Channel

A general record contact is not a route channel unless the record explicitly binds it to that route.

CONTACT_TOKEN != ROUTE_CHANNEL
FORM_IN_TOOL != TARGET_IS_TOOL_OUTPUT

Use NOT STATED rather than borrowing a nearby email/form.

## 8. Route forms

Reuse existing forms:
- PUBLIC_INITIATION
- PROCESS_REFERENCE
- HELP_FEEDBACK
- IN_CHANNEL_HANDOFF
- INTERNAL_REVIEW
- NO_SEPARATE
- SELF_CORRECTION
- DATA_RIGHTS
- REFUSAL_OR_OPT_OUT
- EXPLANATION_ONLY
- PLANNED_NOT_OPERATING
- AMBIGUOUS

Forms may co-occur.

Primary tables should normally exclude DATA_RIGHTS and generic HELP_FEEDBACK unless explicitly bound to the primary answerability object.

## 9. Bare N/A

A bare N/A is not a route proposition.

Record separately:
APPEALS_FIELD_STATE =
- PROPOSITION_PRESENT
- UNEXPLAINED_NA
- NO_APPEALS_FIELD_OBSERVED

Do not force bare N/A into target vocabulary.

## 10. Explicit affected actor with no route

Add a record-level derived observation:
AFFECTED_ACTOR_ROUTE_STATUS =
- ROUTE_STATED
- NO_ROUTE_STATED_IN_RECORD
- AFFECTED_ACTOR_NOT_IDENTIFIED

Use NO_ROUTE_STATED_IN_RECORD only when:
- the record explicitly identifies the affected/subject actor; and
- no primary route proposition for that actor is observed in the bounded record.

NO_ROUTE_STATED_IN_RECORD != NO_REAL_ROUTE

This derived state is separate from route bundles.

## 11. Negative reasons

For NO_RELEVANT_CHALLENGE_WITH_REASON preserve:
- exact object/layer the negative applies to;
- the record's stated reason;
- the scope of that reason if narrower than other consequences in the record.

A reason about service access must not silently cover other stated follow-up actions.

Bare N/A is not a reason.

## 12. Record deployment status

Carry explicit record status into relation status:
- OPERATING
- PILOT
- PRE_PRODUCTION
- PROOF_OF_CONCEPT
- PLANNED_NOT_OPERATING
- NOT_STATED

Do not report a planned route as current because another sentence is present tense.

This is descriptive metadata, not route effectiveness.

## 13. First-pass evidence scope

For future coding:
- record source identity;
- preserve exact evidence locators;
- do not follow linked complaint/appeal pages in primary coding;
- linked-site inspection, if later done, is a separate observation scope;
- no domain/process knowledge may be used to fill target/channel/effect.

## 14. Report shape

A fresh corpus should separate:
- **confirmed-target primary rows**: public/affected routes to tool output and broader process;
- **candidate/unknown-target inventory**: explicit route propositions with `LAYER_NOT_STATED` or `OTHER_STATED_TARGET` that cannot honestly enter confirmed target counts;
- internal review separately;
- explicit no-separate-route propositions with reason;
- affected actors with no route stated in the record;
- unexplained N/A fields;
- channels stated vs not stated;
- operating vs planned status;
- preserved coder disagreements.

Do not collapse into one contestability/compliance score.

## 15. Kill conditions after repair

Kill or shrink further if:
1. the repaired inclusion rule still creates large discretionary route-discovery differences;
2. target disagreements still require outside process knowledge;
3. affected-actor silence cannot be derived without inventing who is affected;
4. category proliferation resumes;
5. a current owner publishes the same measurement first;
6. the result reduces to free-text varies;
7. the output becomes interesting only after adding a moral/compliance score.

NULL_RESULT = VALID.

## 16. Calibration status

The frozen 16-case exercise supports:

ALL_16_CODED_FROM_FROZEN_RECORDS
NO_OUTSIDE_PROCESS_KNOWLEDGE_NEEDED
NO_NEW_TARGET_CATEGORY_NEEDED
FIRST_READS_DIFFERED_MATERIALLY_ON_INCLUSION_AND_SOME_TARGETS
REPAIR_EARNED
METHOD_NOT_VALIDATED

The next substantive result, if any, should come from a fresh corpus under live competition rules, not by converting this calibration into a population claim.

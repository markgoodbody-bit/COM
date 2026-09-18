# ATRS relation calibration — reconciliation of two frozen first passes

Status: POST-CALIBRATION RECONCILIATION / NOT POPULATION RESULT / NOT HUMAN STUDY / NOT NOVELTY CLAIM
Date: 18 September 2026

This file applies the pre-return adjudication rules frozen in RELATION_CALIBRATION_ADJUDICATION_20260918.md.

It does not edit either first-pass return.

Primary inputs:
- Codex frozen first pass: CODEX_RELATION_FIRST_PASS_20260918.md at commit 8cf2f2ba0e1ba6e83a4237aa330f97bb87ed325b.
- Claude Code frozen first pass: COM #364 comment 5727586822.

Both used the frozen September source artifact and exact 16-record sample identity:
c97ea5548ccc26b130a8ffe2783569d6d365897fcf0e04a35fba033486012b54

Both explicitly report:
- no live GOV.UK refetch;
- no linked-site inspection for first-pass labels;
- no new target category minted to rescue a case;
- no outside process knowledge required to code the 16 records.

Both also disclose prior exposure to some records and method discussion.

DIFFERENT_APERTURE != BLIND_READER
SEPARATE_FIRST_PASS != EXTERNAL_VALIDATION
AGREEMENT != WORLD_TRUTH

## High-level calibration result

The method is not killed by uncodability.

CORE ROUTE-TO-TARGET RELATION = SURVIVES
INCLUSION BOUNDARY = TOO BROAD
BINDING PRECEDENCE = NEEDS REPAIR
ACTOR SILENCE = NEEDS RECORD-LEVEL REPRESENTATION
BARE N/A / UNBOUND CONTACT = MUST NOT BECOME ROUTES

Codex disposition: REPAIR, possible SHRINK of inclusion rule.
Claude Code disposition: KEEP, REPAIR codebook before fresh corpus.

Framework disposition after reconciliation:
KEEP / REPAIR / SHRINK PRIMARY INCLUSION.

No scalar agreement coefficient is calculated. The first-pass objects differ in route discovery count and splitting, so a one-number agreement score would hide the load-bearing disagreements.

## D1 — route discovery

This is the largest disagreement class.

Codex deliberately included many peripheral review/governance propositions:
- generic performance monitoring;
- model QA and retraining;
- maintenance/bug reporting;
- data-rights actions;
- governance audits;
- security/threat reporting;
- development feedback.

Claude Code generally stayed closer to the appeals/review/actionability spine, while still including internal review when it acted directly on an output.

Adjudication:

The primary fresh-corpus relation table should include a proposition only when the published record explicitly describes review, challenge, correction, override, reconsideration, complaint/appeal, handoff, opt-out, alternative evidence, explanation, or self-correction of a specific tool output or broader operational-process outcome, or explicitly states that no such route is relevant with a reason.

Generic model governance, maintenance, security reporting, performance monitoring, supplier feedback, data rights, and research-governance review are secondary context unless the record explicitly binds them to changing or reconsidering a current tool output or broader-process outcome.

MONITORING != ANSWER_BACK_ROUTE
MODEL_QA != SUBJECT_CHALLENGE
DATA_RIGHT != OUTPUT_REVERSAL
SECURITY_REPORT != CONTESTATION
TRIGGER != TARGET

## D2 — target-site disagreements

### NHS BSA documentary-evidence route — V3-02

Codex: BROADER_OPERATIONAL_PROCESS.
Claude Code: TOOL_OUTPUT.

Adjudication: BROADER_OPERATIONAL_PROCESS.

Reason: the failed automated check triggers the documentary-evidence route, but the published action changes the application/entitlement path. The record does not say the original automated result itself is rewritten.

TRIGGERED_BY_TOOL_OUTPUT != ACTS_ON_TOOL_OUTPUT

The customer query to the third-party provider remains a TOOL_OUTPUT explanation route because it explicitly asks why the check failed.

The later manual residency check after a complaint is also treated as broader application/process reconsideration unless the record explicitly says it revises the automated result.

### NS&I complaints — V4-04

Codex: BROADER_OPERATIONAL_PROCESS.
Claude Code: LAYER_NOT_STATED.

Adjudication: LAYER_NOT_STATED.

The field names a standard complaints process for complaints or unresolved issues but does not state whether that process acts on the chatbot response, the wider NS&I service, or another object. Complaints process alone is not permission to supply the target from domain knowledge.

### GOV.UK site-search feedback — V3-03

Codex: OTHER_STATED_TARGET.
Claude Code: TOOL_OUTPUT.

Adjudication: OTHER_STATED_TARGET for general page/service feedback unless the record explicitly says the feedback challenges or changes a particular search result or ranking.

Supplier/product feedback is secondary context under the repaired inclusion rule.

### HMRC poor-model-results report — V3-05

Codex: OTHER_STATED_TARGET.
Claude Code: TOOL_OUTPUT.

Adjudication: OTHER_STATED_TARGET / secondary context.

The proposition targets model/development behaviour and retraining, not a stated individual URL decision. The manual analyst review of generated URLs remains TOOL_OUTPUT; the organisation's takedown appeal remains BROADER_OPERATIONAL_PROCESS.

### HERMeS general feedback — V3-06

Codex: LAYER_NOT_STATED.
Claude Code: TOOL_OUTPUT.

Adjudication: LAYER_NOT_STATED for general feedback.

The form is located in the tool, but location is not target. The separate self-verification route against source documents remains TOOL_OUTPUT.

### Reception Baseline narrative request — V3-07

Codex: OTHER_STATED_TARGET.
Claude Code: BROADER_OPERATIONAL_PROCESS.

Adjudication: OTHER_STATED_TARGET.

Requesting access to a narrative statement is an explanation/access action on a named artefact, not itself review of the routing tool or reconsideration of the assessment process.

The broader speak-to-school issue route remains LAYER_NOT_STATED.

### TrustID manual-process opt-out — V4-08

Codex: BROADER_OPERATIONAL_PROCESS.
Claude Code: TOOL_OUTPUT.

Adjudication: BROADER_OPERATIONAL_PROCESS.

The manual check is an alternative process to automated checking. It is not a correction of a prior match score.

### E-Supervision supplier-feedback negative — V4-06

Codex: OTHER_STATED_TARGET.
Claude Code: TOOL_OUTPUT.

Adjudication: secondary context / OTHER_STATED_TARGET.

Recognition mistakes are not fed back to AWS is about supplier/model feedback, not a route for the affected person or a stated correction of the current output.

## D3 — binding-basis disagreements

A simple precedence rule is earned:

DIRECT when the route proposition itself names its target sufficiently to assign the target site.

EXPLICIT_CROSS_FIELD only when another field in the same frozen record is necessary to bind the route proposition to the target site.

Other fields may corroborate a DIRECT assignment without changing it to EXPLICIT_CROSS_FIELD.

Applications:
- Environment Agency normal permitting appeals -> DIRECT broader process.
- HMRC appeal as part of the legal process -> DIRECT where the same proposition identifies the takedown/legal process.
- BDUK challenge eligibility of a premise -> EXPLICIT_CROSS_FIELD to TOOL_OUTPUT because other fields establish premise eligibility as the engine output.
- NHS BSA complaint/manual-check relationship may use cross-field evidence where the appeals text alone does not state what the complaint triggers.
- Data First error/anomaly feedback is DIRECT where the proposition itself names a linkage error/anomaly.

CORROBORATION != BINDING_DEPENDENCE

## D4 — actor / initiation / channel

Free-text ACTOR_SCOPE is not enough for a primary public-route distribution.

A small derived actor class is earned:
- AFFECTED_OR_PUBLIC
- INTERNAL
- SUPPLIER_OR_INTERMEDIARY
- NOT_STATED

This does not replace actor text.

Record-level contact details are not route channels unless the record explicitly binds them to that route proposition.

CONTACT_TOKEN != ROUTE_CHANNEL
FORM_LOCATION != ROUTE_TARGET

## D5 — route form / effect / status

The existing route-form vocabulary survives.

Repairs:
- generic feedback remains HELP_FEEDBACK; it does not become reconsideration;
- human handoff remains distinct from complaint/appeal;
- explanation/access remains distinct from correction;
- internal review remains distinct from public initiation;
- record deployment status propagates to relation status where explicit;
- if a negative reason covers only one consequence, preserve its reason scope rather than generalising it.

No new moral/quality scale is introduced.

## D6 — source scope / outside knowledge

No systematic failure found.

Both coders completed all 16 without using live external process knowledge for their labels.

This is the strongest positive calibration result.

It does not establish that every future ATRS record is codable or that coded routes exist or work in reality.

## D7 — codebook defects

### Bare N/A

A bare N/A is not a route proposition.

Do not code it as NO_RELEVANT_CHALLENGE_WITH_REASON because there is no reason.
Do not code it as LAYER_NOT_STATED because there is no route proposition whose target is unstated.

Record it separately as:
APPEALS_FIELD_STATE = UNEXPLAINED_NA

This is record-level metadata, not a new target category.

### Explicit affected actor with no stated route

The most consequential silence found by Claude Code is real and cannot be represented as a route bundle.

Add a derived record-level observation:
AFFECTED_ACTOR_ROUTE_STATUS

Values:
- ROUTE_STATED
- NO_ROUTE_STATED_IN_RECORD
- AFFECTED_ACTOR_NOT_IDENTIFIED

Use NO_ROUTE_STATED_IN_RECORD only when:
1. the record explicitly identifies the affected/subject actor; and
2. the bounded route inventory contains no route proposition for that actor.

NO_ROUTE_STATED_IN_RECORD != NO_REAL_ROUTE

This is expected to matter for examples such as E-Supervision, Data First and BDUK.

### Contradictions

A contradiction does not automatically erase a known target.

Example: EA output review can remain TOOL_OUTPUT while conflicting review-scope statements are preserved in status/effect and disagreement evidence.

Use UNBOUND_OR_CONTRADICTORY only when the attempted target binding itself cannot be established or conflicts.

### Record contact

A general Tier-1/contact form is not a route proposition without explicit binding. It may be reported separately as a record contact but does not enter route counts.

## D8 — evidence / locator errors

No sample-identity or source-byte mismatch was established in either return.

Both reproduced the frozen sample/artifact identity.

One Claude Code provenance sentence was later corrected for its typed start time; this does not change the frozen coding content or sample identity.

No evidence-locator error has yet been established that requires recoding a route.

## Key primary-route adjudications

| Case | Proposition | Reconciled target/binding |
|---|---|---|
| V4-01 FCDO | response review/appeal | BROADER_OPERATIONAL_PROCESS / DIRECT |
| V4-02 CPS | correspondence feedback/complaint | BROADER_OPERATIONAL_PROCESS / DIRECT |
| V4-03 GOV.UK Chat | check answer against source pages | TOOL_OUTPUT / DIRECT |
| V4-04 NS&I | complaints/unresolved issues | LAYER_NOT_STATED |
| V4-05 EA | permitting appeal | BROADER_OPERATIONAL_PROCESS / DIRECT |
| V4-06 E-Supervision | flagged mismatch practitioner review | TOOL_OUTPUT / DIRECT / INTERNAL |
| V4-07 Ancient Woodland | bare N/A | no route bundle; UNEXPLAINED_NA |
| V4-07 Ancient Woodland | user review/feedback on polygons | TOOL_OUTPUT / DIRECT |
| V4-08 TrustID | user review request | TOOL_OUTPUT / DIRECT |
| V4-08 TrustID | manual-check alternative | BROADER_OPERATIONAL_PROCESS / EXPLICIT_CROSS_FIELD |
| V3-01 Data First | researcher error/anomaly feedback | TOOL_OUTPUT / DIRECT |
| V3-02 NHS BSA | documentary evidence after failed check | BROADER_OPERATIONAL_PROCESS / DIRECT |
| V3-02 NHS BSA | complaint | BROADER_OPERATIONAL_PROCESS; binding depends on whether other fields are required for the stated effect |
| V3-02 NHS BSA | query supplier for fail reason | TOOL_OUTPUT / DIRECT / EXPLANATION_ONLY |
| V3-03 GOV.UK search | general page feedback | OTHER_STATED_TARGET / DIRECT |
| V3-04 DfE | none-required proposition | NO_RELEVANT_CHALLENGE_WITH_REASON / DIRECT / PLANNED |
| V3-05 HMRC | takedown appeal | BROADER_OPERATIONAL_PROCESS / DIRECT |
| V3-06 HERMeS | general feedback/issues form | LAYER_NOT_STATED |
| V3-06 HERMeS | validate answer against sources | TOOL_OUTPUT / DIRECT |
| V3-07 Reception Baseline | request narrative statement | OTHER_STATED_TARGET / DIRECT / EXPLANATION_ONLY |
| V3-07 Reception Baseline | broader issue -> school | LAYER_NOT_STATED |
| V3-08 BDUK | challenge premise eligibility | TOOL_OUTPUT / EXPLICIT_CROSS_FIELD |

This table is a calibration reconciliation, not a population result.

## Disposition

METHOD = KEEP
CODEBOOK = REPAIR
PRIMARY INCLUSION = SHRINK
VERSION = SECONDARY TAG ONLY
HUMAN PILOT = NOT REQUIRED FOR THIS RESULT
NOVEMBER FRESH CORPUS = STILL PLAUSIBLE IF LIVE RULES ALLOW

The calibration falsifier therefore did not kill #364.

It did kill the idea of counting every review/feedback/monitoring proposition as one answerability population.

Next method object: RELATION_CODEBOOK_V2_20260918.md.

TWO_CODERS_CODED_ALL_16 != VALIDATED_POPULATION_METHOD
NO_OUTSIDE_KNOWLEDGE_NEEDED_ON_16 = USEFUL
FIRST_READS_PRESERVED = REQUIRED
NULL_RESULT = VALID

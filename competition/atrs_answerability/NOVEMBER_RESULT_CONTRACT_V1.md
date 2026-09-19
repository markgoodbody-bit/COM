# ATRS #364 — November result contract v1

Status: **PRE-SPRINT OUTPUT CONTRACT / NO NOVEMBER DATA / NO RESULT**

Frozen: 18 September 2026.

Purpose: constrain the November analysis before the full current population is relation-coded. This file specifies units, denominators, primary tables, disagreement handling and claim ceilings. It does **not** contain a population result.

If live competition rules or a concrete method falsifier require a change, preserve the pre-change contract and record the reason.

## 1. Population identity

Primary population:

> all records enumerated by the live public GOV.UK ATRS finder at the sprint-time source freeze.

Required witness:
- retrieval start/end UTC;
- finder-declared count;
- exact canonical URL set;
- membership cross-check result;
- exact source bytes per URL;
- SHA-256 per source page;
- source fetch status;
- parser/code commit;
- codebook hash.

Do not silently drop a finder URL.

If a page cannot be fetched after bounded retry:
- keep the URL in the population manifest;
- mark `SOURCE_FETCH_FAILED`;
- report the failure;
- do not treat it as field absence.

```text
FINDER_MEMBER != SUCCESSFULLY_FETCHED
FETCH_FAILURE != FIELD_ABSENCE
```

A “complete register census” claim requires all finder URLs to have frozen source bytes or an explicitly justified owner-level exclusion.

## 2. Units

Keep these units separate.

### RECORD

One finder record.

Use for:
- register population;
- deployment/version context;
- record-level field state;
- whether a record contains at least one relation of a specified kind.

### ROUTE_RELATION

One materially distinct explicit published route/review/correction proposition.

Use for:
- target site;
- actor;
- initiation/channel;
- route form;
- trigger;
- effect;
- binding basis.

Multiple route relations may occur in one record.

### ACTOR_RECORD

One explicitly identified affected/subject actor class/scope within one record for the derived `AFFECTED_ACTOR_ROUTE_STATUS`.

Do not divide actor-record counts by number of records without saying so.

```text
RELATION_COUNT != RECORD_COUNT
ACTOR_RECORD_COUNT != RECORD_COUNT
```

## 3. Relation inventory

For every explicit proposition preserve:

```text
record_id
record_url
record_title
source_sha256
declared_atrs_version
deployment_status

relation_id
route_proposition
actor_scope
actor_class
action
channel
target_site
route_form[]
trigger
stated_effect
binding_basis
evidence_locator[]
evidence_excerpt
primary_inclusion
coder_disagreement
adjudication_state
```

Closed `target_site`:

```text
TOOL_OUTPUT
BROADER_OPERATIONAL_PROCESS
OTHER_STATED_TARGET
NO_RELEVANT_CHALLENGE_WITH_REASON
LAYER_NOT_STATED
UNBOUND_OR_CONTRADICTORY
```

Closed `binding_basis` for positive/candidate routes:

```text
DIRECT
EXPLICIT_CROSS_FIELD
LAYER_NOT_STATED
UNBOUND_OR_CONTRADICTORY
NOT_APPLICABLE
```

Do not create a new target category during the census merely to avoid an unknown.

## 4. Primary record-level tables

These are fixed before population coding.

### P1 — finder/source integrity

Report:
- finder records;
- successfully frozen source pages;
- failed source pages;
- Search API membership difference, if that cross-check remains available;
- changed/added/removed URLs versus September as **secondary context**, not a primary answerability result.

### P2 — Appeals/review field state

Per record:

```text
PROPOSITION_PRESENT
UNEXPLAINED_NA
NO_APPEALS_FIELD_OBSERVED
```

This is structural context only.

### P3 — confirmed target-site relations by record

For each record, boolean presence of:
- at least one confirmed `TOOL_OUTPUT` relation;
- at least one confirmed `BROADER_OPERATIONAL_PROCESS` relation;
- both of the above;
- at least one `LAYER_NOT_STATED` positive route;
- at least one `UNBOUND_OR_CONTRADICTORY` route;
- at least one `OTHER_STATED_TARGET`;
- at least one `NO_RELEVANT_CHALLENGE_WITH_REASON`.

Report counts and proportions using **record population N** as denominator, with the categories allowed to overlap.

Do not sum overlapping percentages to 100%.

### P4 — public/affected positive route relation table

Among positive route relations whose actor class is `AFFECTED_OR_PUBLIC`, report:
- target site;
- DIRECT / EXPLICIT_CROSS_FIELD / LAYER_NOT_STATED / UNBOUND;
- channel stated vs not stated;
- route form;
- operating vs planned/pre-production status.

Denominator is **positive AFFECTED_OR_PUBLIC route relations**, not records.

Also report number of records contributing those relations.

### P5 — affected-actor route status

For each explicit affected/subject actor-record unit:

```text
ROUTE_STATED
NO_ROUTE_STATED_IN_RECORD
AFFECTED_ACTOR_NOT_IDENTIFIED
```

Important:
`AFFECTED_ACTOR_NOT_IDENTIFIED` is a record-level state when no explicit affected actor can be derived; do not fabricate an actor-record row.

Report:
- records with no explicit affected actor identified;
- explicit actor-record units with route stated;
- explicit actor-record units with no route stated.

```text
NO_ROUTE_STATED_IN_RECORD != NO_REAL_ROUTE
```

### P6 — explicit negative / no-separate propositions

Report records with a source-supported `NO_RELEVANT_CHALLENGE_WITH_REASON` relation.

Preserve the exact layer/object and reason.

Do not code a bare N/A here.

### P7 — disagreement / adjudication

Report:
- first-pass coders used;
- records independently dual-coded;
- relation propositions requiring matching/reconciliation;
- target/binding disagreements affecting a primary table;
- unresolved disagreements retained at final freeze;
- any codebook repair made during sprint, with records replayed.

Do not use one agreement number as a validation badge unless its unit/matching assumptions are defensible.

## 5. Primary headline rule

A headline claim must satisfy all of:

1. derived from P1–P7 or a predeclared direct combination;
2. traceable to exact evidence rows;
3. understandable without TRACE/ME terminology;
4. not depend on a post-hoc version/tool-role slice;
5. not infer route effectiveness, legal rights, fairness or compliance;
6. survive the second-coder/adjudication path;
7. remain true if unknown/unbound rows stay unknown.

If no such claim exists:

`NO CRISP PRIMARY RESULT = VALID`.

## 6. Secondary analyses

Only after primary tables are frozen:
- ATRS version;
- publication period;
- deployment phase;
- tool role/capability;
- organisation type;
- September-to-November byte/field changes.

These are descriptive/exploratory unless separately preregistered by a live rule-driven need.

```text
VERSION_ASSOCIATION != VERSION_CAUSED_CHANGE
OLDER_RECORD != CONTROL_GROUP
```

Do not choose a subgroup because it creates the strongest contrast.

## 7. No performative significance testing

If the primary population is the complete observed public finder, headline register proportions are descriptive census quantities.

Do not add p-values to make them look scientific.

Use uncertainty language for:
- coder interpretation;
- source/currentness limits;
- population scope;
- generalisation beyond the finder.

A secondary inferential model is allowed only if it answers a real question with a defensible sampling/data-generating interpretation.

## 8. Four predeclared evidence examples

The final report should include four source-grounded records selected **by structural role**, not extremeness:

1. confirmed direct tool-output route;
2. confirmed broader-operational-process route;
3. positive route whose target remains publicly unstated/unbound;
4. one of:
   - explicit affected actor with no stated positive route; or
   - explicit no-separate-route proposition with reason.

If several qualify, use a deterministic rule declared before reading prose for presentation quality (for example, lexicographically first canonical URL within each final class) or disclose editorial selection.

These examples illustrate counts; they do not generate them.

## 9. Evidence-browser contract

Every primary count must be auditable to rows containing:
- record title + GOV.UK URL;
- relation ID;
- target/actor/channel/form;
- binding basis;
- field/locator;
- short source excerpt;
- source SHA-256;
- coder/adjudication state.

The browser must not:
- rank departments;
- generate a compliance score;
- imply an unstated route is absent in reality;
- follow linked external complaint pages as though they were part of primary coding.

## 10. Pre-existing vs sprint-time disclosure

Final report must include a visible box/table:

### Pre-existing before sprint
- downloader/membership/parser;
- September source snapshot;
- relation codebook;
- 16-record calibration;
- prior-work map;
- execution/result contracts;
- empty report/browser scaffolding.

### Produced during sprint
Fill only from actual sprint work:
- live rules snapshot;
- fresh finder/source freeze;
- full relation coding;
- independent coding/review;
- adjudication;
- primary tables;
- figures/browser populated with result;
- final report narrative.

Do not blur this boundary.

## 11. Result shape

Final disposition must be one of:

```text
MATERIAL_UNBOUNDNESS
MATERIAL_LEGIBILITY
MIXED_STRUCTURE
METHOD_FAILURE
OWNER_FOUND
NO_CONSEQUENTIAL_RESULT
```

This is an editorial classification of the study outcome, not a score assigned to government records.

## 12. Claim ceiling

Never infer from this audit alone:

```text
ROUTE_PUBLISHED -> ROUTE_WORKS
ROUTE_UNBOUND_IN_RECORD -> NO_REAL_ROUTE
NO_ROUTE_STATED -> NO_RIGHT_TO_REVIEW
TARGET_BOUND -> FAIR_DECISION
HUMAN_REVIEW -> PUBLIC_CONTESTABILITY
PUBLIC_INITIATION -> PRACTICAL_ACCESSIBILITY
V4_ASSOCIATION -> V4_CAUSED_IMPROVEMENT
ATRS_FINDER -> ALL_UK_PUBLIC_SECTOR_AI
```

## 13. Contract-change rule

A sprint-time contract change is permitted only for:
- live competition-rule requirement;
- source-format break;
- concrete counterexample showing the contract is internally wrong;
- stronger owner making a measure redundant.

Record:
- old text/hash;
- change;
- concrete trigger;
- affected records/tables;
- replay performed.

```text
DIFFICULT_RESULT != REASON_TO_CHANGE_METRIC
```

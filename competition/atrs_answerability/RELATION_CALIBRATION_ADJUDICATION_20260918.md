# ATRS relation calibration — adjudication rules

Status: **PRE-RETURN ADJUDICATION PLAN / NOT RESULT**  
Date: 18 September 2026

This file is frozen before Framework reads any Codex/Claude Code first-pass calibration return.

Purpose: prevent post-hoc movement of the relation codebook to make disagreement disappear.

## Inputs

Two independently produced first-pass tables over the exact frozen 16-record sample in:

- `RELATION_CALIBRATION_PROTOCOL_20260918.md`
- `relation_calibration_sample_20260918.json`

Framework authored the earlier dry run and does not count as an independent primary coder.

## Do not begin by counting agreement

First compare the **objects each aperture thought existed**.

For each record, align route bundles using the source evidence locator/proposition, not the assigned category.

A route bundle is provisionally matched when both returns point to the same material published proposition or same explicit action/process, even if they disagree on actor/channel/target/form.

If one aperture extracts a route and the other does not, keep it as an unmatched route-discovery disagreement. Do not force a match by semantics.

## Disagreement classes

Every difference should be assigned one or more of:

### D1 — ROUTE_DISCOVERY

One aperture identified a material route/review/correction proposition and the other did not.

Question:
- was the proposition actually present in the frozen record?
- did the method fail to define what counts as a material route?

### D2 — TARGET_SITE

Same route proposition, different target assignment.

Question:
- does the route itself state the target?
- does an allowed explicit cross-field relation establish it?
- should the result be `LAYER_NOT_STATED` or `UNBOUND_OR_CONTRADICTORY` rather than a forced layer?

### D3 — BINDING_BASIS

Same target conclusion, but one coder says `DIRECT` and the other relies on `EXPLICIT_CROSS_FIELD`, or one sees no valid binding.

This matters because the measurement concerns what the record makes legible, not merely the final target label.

### D4 — ACTOR / INITIATION / CHANNEL

Coders disagree on who can cause the route to happen or how.

Preserve:
`ELIGIBLE_ACTOR_NAMED != CHANNEL_STATED`
and
`PROCESS_REFERENCE != PUBLIC_INITIATION`.

### D5 — ROUTE_FORM / EFFECT / STATUS

Examples:
- feedback vs reconsideration;
- human handoff vs appeal;
- internal QA vs subject-initiated challenge;
- operating vs planned;
- data-rights action vs output correction.

Do not resolve by choosing the more consequential interpretation.

### D6 — SOURCE_SCOPE

One coder used information outside the permitted frozen-record scope, including:
- linked external pages;
- remembered domain procedure;
- legal/process knowledge not stated in the record.

First-pass outside-scope information cannot be used to rescue the relation.

### D7 — CODEBOOK_DEFECT

The current fixed vocabulary cannot represent the source without distorting it.

A hard case is **not** automatically a codebook defect. Prefer existing:
`OTHER_STATED_TARGET`,
`LAYER_NOT_STATED`,
`UNBOUND_OR_CONTRADICTORY`,
or multi-route bundles before adding categories.

### D8 — EVIDENCE / LOCATOR ERROR

The return misquotes, mislocates or attributes text to the wrong field/record/source.

Treat as an evidence error, not semantic disagreement.

## Adjudication order

For each disagreement:

1. verify frozen source identity;
2. inspect the exact cited proposition;
3. determine whether both coders used allowed evidence;
4. check whether the relation can be resolved under the already-frozen definitions;
5. if not, retain unknown/contradiction;
6. only then consider a codebook repair.

Do not consult live GOV.UK or external linked processes during calibration adjudication unless the first-pass exercise is explicitly terminated and a separate owner/source question is opened.

## Repair discipline

A codebook repair is earned only if:
- the same structural problem appears in more than one concrete record, **or**
- one record exposes a logical contradiction in the existing rule.

Prefer changing a definition over adding a category where possible.

Every repair must state:
- the concrete records that required it;
- before/after definition;
- which previous labels would change;
- whether the repair affects the research question or merely coding clarity.

Do not recode first-pass returns silently. Preserve original tables and create a reconciled layer separately.

## No arbitrary agreement score

This 16-case pressure test has no preregistered kappa/pass threshold.

Why:
- records can contain different numbers of route propositions;
- relation discovery itself is under test;
- multi-label route bundles violate a simple one-label-per-item model;
- a high scalar agreement rate could hide systematic failure on the load-bearing target/binding distinction.

Report instead:
- matched route bundles;
- unmatched route propositions;
- disagreements by D1–D8 class;
- records requiring outside knowledge;
- records resolved by source text alone;
- records that remain `LAYER_NOT_STATED` or `UNBOUND_OR_CONTRADICTORY`;
- any codebook repairs.

A simple descriptive agreement table may be added later, but it is not the decision rule.

## Disposition logic

### KEEP

The relation method remains small and source-bound. Most material disagreement is ordinary evidence reading, and hard cases can be honestly represented by existing unknown/unbound states.

### REPAIR

One or a few definitions need bounded changes, but the core relation object remains stable and no outside process knowledge is required.

### SHRINK

The target relation is only reliably codable for a narrower subset of records/propositions. Preserve that subset and drop claims beyond it.

### KILL

The central target/binding distinction cannot be applied without repeated outside knowledge, category proliferation or coder-supplied process models, or a stronger owner already provides the same measurement.

```text
AGREEMENT != VALIDATION
DISAGREEMENT != FAILURE
RECONCILIATION != ERASE_FIRST_READ
UNKNOWN != DEFECT
OUTSIDE_KNOWLEDGE != PUBLIC_LEGIBILITY
NULL_RESULT = VALID
```

## No downstream authority

Calibration outcome does not authorise:
- human participant work;
- competition registration/submission;
- organiser contact;
- policy claims;
- GDS outreach;
- TRACE/ME changes.

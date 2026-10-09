# ATRS relation calibration — frozen 16-case independent coding pass

Status: **METHOD CALIBRATION / FROZEN SEPTEMBER SOURCE / NOT RESULT / NOT POPULATION ESTIMATE / NOT HUMAN STUDY**  
Date: 18 September 2026

## Purpose

Before treating the November fresh-corpus route→target relation as a viable research object, test whether two differentiated apertures can independently apply the refined source-bound relation method to the same real frozen records **without importing outside process knowledge or proliferating the codebook**.

This is the pre-November falsifier requested by the 17 September hostile reviews.

```text
CODABLE_ON_16 != RELIABLE_ON_152
AGREEMENT != WORLD_TRUTH
DISAGREEMENT = DATA
NOVEMBER_FRESHNESS != METHOD_REPAIR
```

Framework authored the earlier dry run and therefore does **not** count as an independent primary coder in this calibration. Framework will integrate/adjudicate only after first-pass returns are frozen.

## Evidence basis

Use only the frozen September ATRS witness:

```text
run = 35257984573 SUCCESS
artifact = 10513278849
artifact sha256 = ad315d9b08a0af65c4615638df2235b9ce6f021307315fbeb6dfcbd8cbdb0097
source HTML pages = 152
```

Do **not** refetch GOV.UK and do not inspect linked external sites for the first pass. The question is what the frozen public ATRS record itself makes legible.

The coding may use the entire frozen record, not only `Appeals and review`. Cross-field binding is allowed only under the explicit source rule below.

## Deterministic sample

Selection rule:

```text
within frozen declared v4.0 records:
  sort ascending SHA256(canonical GOV.UK record URL)
  take first 8

within frozen declared v3 / v3.0 records:
  sort ascending SHA256(canonical GOV.UK record URL)
  take first 8
```

Sample identity digest over ordered `URL<TAB>source_sha256` lines:

```text
c97ea5548ccc26b130a8ffe2783569d6d365897fcf0e04a35fba033486012b54
```

### v4.0

| # | Record | URL SHA256 prefix | frozen source SHA256 |
|---|---|---|---|
| V4-01 | FCDO: Correspondence Triage | `01512db67b91` | `ab47f95f114d...` |
| V4-02 | The Crown Prosecution Service: Correspondence Drafting Tool | `041104b78c40` | `c8440d4c33c0...` |
| V4-03 | DSIT: GOV.UK Chat | `06590155eed3` | `b101b1c863f1...` |
| V4-04 | NS&I: PolyAI | `068a3b4cbded` | `f677262e8da4...` |
| V4-05 | Environment Agency: Regulatory Guidance Assistant | `0a841d103ea2` | `f5b4f02e0c84...` |
| V4-06 | MoJ: Check-In with your probation officer (E-Supervision) | `1340c72c0edb` | `bc08a8445a76...` |
| V4-07 | Welsh Government: Mapping Ancient Woodland Image Segmentation Model | `1916257049f2` | `669a570ba656...` |
| V4-08 | TrustID | `34400cbc1405` | `30220ce69efa...` |

### v3-family

| # | Record | URL SHA256 prefix | frozen source SHA256 |
|---|---|---|---|
| V3-01 | MoJ: Data First (Splink) | `025d0a395a3e` | `b79c057e4a1a...` |
| V3-02 | NHS BSA: Residency Checker for UK EHIC/GHIC/PRC/S2 | `04ea89eb5866` | `09bf1f39a852...` |
| V3-03 | DSIT: GOV.UK site search | `062cc0e71161` | `ce5dd5f72faf...` |
| V3-04 | DfE: Apprenticeship Withdrawal Rate AI | `0798e942817c` | `63d85160a7f6...` |
| V3-05 | HMRC: Logo Detection and Classification Toolkit (LDK) | `0ddb5dd7ee95` | `f07506ddb32d...` |
| V3-06 | HMT: HERMeS (HMT's Excerpt Retrieval Messaging System) | `134bd877083e` | `57a9ef4d0660...` |
| V3-07 | Standards and Testing Agency: Reception Baseline Assessment Routing | `13d069d68595` | `15b61511d8f5...` |
| V3-08 | BDUK: Project Gigabit Voucher Eligibility Engine | `166c039706b7` | `e01f9ba4d523...` |

## Coding object

Do not assign one overall “contestable / not contestable” label to a record.

Extract each materially distinct route/review/correction proposition as a bundle:

```text
ROUTE_PROPOSITION
+ ACTOR_SCOPE
+ ACTION / NEXT STEP
+ CHANNEL / INITIATION
+ TARGET_SITE
+ ROUTE_FORM
+ STATUS_OR_EFFECT
+ BINDING_BASIS
+ EVIDENCE_LOCATOR
```

A record may contain zero, one or several bundles.

Do not let one route borrow another route's actor, channel or target.

## Target site

Use only:

```text
TOOL_OUTPUT
BROADER_OPERATIONAL_PROCESS
OTHER_STATED_TARGET
NO_RELEVANT_CHALLENGE_WITH_REASON
LAYER_NOT_STATED
UNBOUND_OR_CONTRADICTORY
```

Do not create additional target categories in the first pass. If none fits cleanly, use `UNBOUND_OR_CONTRADICTORY` and explain why.

### Binding basis

`DIRECT`  
The route proposition itself names or unambiguously identifies its target.

`EXPLICIT_CROSS_FIELD`  
A shared named referent or explicit textual link elsewhere in the same frozen ATRS record establishes the relation. Cite both fields. Do not infer merely from the fact that the tool participates in the process.

`LAYER_NOT_STATED`  
The route/process proposition exists, but the record does not state whether it acts on tool output, broader process output or another identifiable target.

`UNBOUND_OR_CONTRADICTORY`  
Candidate propositions conflict or the target would require the coder to supply a causal/process link not established by the record.

```text
CODER_CAN_INFER != RECORD_MAKES_LEGIBLE
PLAUSIBLE_TARGET != SOURCE_BOUND_TARGET
LAYER_NOT_STATED = VALID_RESULT
```

## Route form / initiation vocabulary

Reuse the September proposition-level labels where they fit:

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

These labels may co-occur. They are observations about published text, not legal or moral categories.

## Evidence discipline

For every bundle:
- cite the frozen field heading(s) used;
- quote only the shortest text needed to establish the relation, or paraphrase and give an exact heading/phrase locator;
- distinguish an explicit negative proposition from silence;
- preserve actor scope;
- preserve `NOT STATED` for actor/channel/status rather than completing it;
- do not inspect a linked complaints/appeals page in the first pass;
- do not infer route effectiveness, entitlement, accessibility or legal sufficiency.

## Independent first-pass rule

Claude Code and Codex should each:
1. code all 16 records independently;
2. freeze their table before reading the other aperture's return if operationally possible;
3. state any cases they could not code without outside knowledge;
4. identify any category they believe is structurally malformed, but **do not add a replacement category during first-pass coding**;
5. report disagreements with the codebook itself separately from record interpretation.

Framework should not adjudicate until both first-pass returns are present or one aperture explicitly reports that it cannot perform the pass.

## Required return shape

For each record:

```text
RECORD_ID:
ROUTES:
  - evidence:
    actor:
    action:
    channel:
    target_site:
    route_form:
    status_or_effect:
    binding_basis:
    evidence_locator:
RECORD_LEVEL_NOTES:
OUTSIDE_KNOWLEDGE_REQUIRED: yes/no + reason
```

Then provide:

```text
CODEBOOK_DEFECTS:
SYSTEMATIC_FAILURES:
DISPOSITION:
  KEEP
  REPAIR
  SHRINK
  KILL
```

## Adjudication / kill logic

No arbitrary kappa threshold is preregistered for this 16-case pressure test.

The method survives only if disagreements can be resolved by:
- pointing to source text;
- clarifying a small number of existing definitions;
- preserving `LAYER_NOT_STATED` / `UNBOUND_OR_CONTRADICTORY`.

Shrink or kill if:
- target assignment repeatedly requires outside process knowledge;
- coders need many new target categories;
- materially different route bundles cannot be separated reproducibly;
- direct cases are unstable despite clear source wording;
- most useful conclusions reduce to `free-text varies`;
- an owner already publishes the same current full-corpus measurement.

```text
DISAGREEMENT != FAILURE
CATEGORY_PROLIFERATION = WARNING
OUTSIDE_KNOWLEDGE_DEPENDENCE = WARNING
NULL_RESULT = VALID
OWNER_FOUND = VALID
```

## Gates

No human study, participant recruitment, organiser contact, competition registration, submission, provider spend, TRACE/ME change or policy outreach follows from this calibration.

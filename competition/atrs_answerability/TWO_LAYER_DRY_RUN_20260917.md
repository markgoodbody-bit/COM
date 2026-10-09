# ATRS two-layer challenge relationship — deterministic dry run

Status: **METHOD PRESSURE TEST / FROZEN SEPTEMBER SOURCE / NOT RESULT / NOT REPRESENTATIVE SAMPLE / NOT HUMAN STUDY**  
Date: 17 September 2026

Purpose: test whether the sharpened middle-out question can be coded from actual records without immediately collapsing into hidden inference or `free-text varies`.

This is not the November study and does not establish prevalence, improvement, compliance, usability or contestability.

## Frozen evidence basis

Source witness:

```text
run = 35257984573 SUCCESS
artifact = 10513278849
artifact sha256 = ad315d9b08a0af65c4615638df2235b9ce6f021307315fbeb6dfcbd8cbdb0097
finder membership = 152
source HTML pages = 152
```

No source was refetched for this dry run.

## Version distribution in the preserved 152 pages

The rendered GOV.UK metadata on every frozen page exposes an ATRS version.

```text
v4.0 = 53
v3.x = 88   # 80 rendered as v3.0; 8 rendered as v3
v2.1 = 4
v1.1 = 7
TOTAL = 152
```

This makes a descriptive v4-versus-v3-family stratification numerically possible. It does **not** make it causal or automatically useful.

Cheap structural diagnostics over the preserved `Appeals and review` text:

```text
family   n    field observed   syntactic token present   median field chars
v1.1     7    7                1                         158
v2.1     4    4                1                         302
v3.x     88   87               16                        344
v4.0     53   53               9                         178
```

A deliberately broad heuristic for `N/A / no decision / no appeal`-shaped language fires on 20/88 v3-family records and 22/53 v4 records. The heuristic is **not** a semantic result; earlier parser work already demonstrated why phrase matching cannot establish field meaning.

The immediate warning is useful:

```text
V4_FIELD_SHORTER != V4_FIELD_WORSE
MORE_TOKENS != MORE_CONTESTABLE
NO_TOOL_DECISION_CAN_MAKE_NO_TOOL_SPECIFIC_APPEAL_APPROPRIATE
VERSION_COMPOSITION != VERSION_EFFECT
```

Tool role and process layer must be carried with any version comparison.

## Owner-text comparison

The v3 template's `appeals_and_review` completion note said, in substance, to describe mechanisms for review or appeal of **the decision** available to the general public where applicable.

Current v4 guidance is more explicit: publishers are told to consider both:

- the output of the algorithmic tool itself and whether that output can be challenged or appealed; and
- the output of the broader operational process and whether that can be challenged or appealed.

Therefore a two-layer reading is owner-native rather than a TRACE/ME invention.

Do not infer from this comparison alone that v4 introduced the distinction or caused any record-level change. The specific v3->v4 change-log attribution remains outside the claim made here.

```text
V3_TEMPLATE_WORDING != V4_GUIDANCE_WORDING
GUIDANCE_DIFFERENCE != CAUSAL_EFFECT_ON_RECORDS
```

## Deterministic sample

Selection rule:

```text
within frozen v4.0 records:
  sort ascending SHA256(canonical GOV.UK record URL)
  take first 8

within frozen v3-family records (v3 + v3.0):
  sort ascending SHA256(canonical GOV.UK record URL)
  take first 8
```

This is a pressure sample, not a random or representative sample.

The first read uses three separate questions:

1. **AFFECTED LAYER** — which output/process does the disclosed route or review act on?
2. **INITIATION / REVIEW MODE** — who can cause the review/correction to happen, if stated?
3. **ROUTE FORM** — appeal, complaint, human handoff, feedback, internal review, alternative evidence/retry, or something else?

This separation is earned by the records below. `HUMAN_REVIEW` cannot safely stand in for `PUBLIC_INITIATION`.

### Provisional coding vocabulary

Affected layer:

```text
TOOL_OUTPUT
BROADER_OPERATIONAL_PROCESS
BOTH_OR_MULTIPLE_ROUTES
NO_RELEVANT_CHALLENGE_CLAIMED_WITH_REASON
NOT_STATED_OR_LAYER_UNCLEAR
```

Initiation/review mode is multi-label where necessary:

```text
PUBLIC_INITIATION_EXPLICIT
PUBLIC_PROCESS_NAMED_INITIATION_NOT_STATED
IN_CHANNEL_HUMAN_REQUEST
USER_FEEDBACK_OR_ISSUE_REPORT
ALTERNATIVE_EVIDENCE_OR_RETRY
INTERNAL_REVIEW_ONLY
NO_RELEVANT_PROCESS_WITH_REASON
NOT_STATED_OR_UNCLEAR
```

These are observational labels for the published text, not legal categories.

## Eight v4 cases

| Record | Provisional affected layer | Initiation / review mode visible in record | Pressure point |
|---|---|---|---|
| FCDO: Correspondence Triage | `BROADER_OPERATIONAL_PROCESS` | `PUBLIC_PROCESS_NAMED_INITIATION_NOT_STATED` + separate internal post-triage review | The record preserves the person's right to review/appeal the eventual response, while the tool's triage prediction is overseen internally. `INTERNAL_REVIEW != PUBLIC_CHALLENGE`. |
| CPS: Correspondence Drafting Tool | `BROADER_OPERATIONAL_PROCESS` | `PUBLIC_PROCESS_NAMED_INITIATION_NOT_STATED` | Tool is stated not to make decisions; existing feedback/complaints apply to CPS correspondence. This is a legitimate broader-process route rather than a missing tool appeal. |
| DSIT: GOV.UK Chat | `NO_RELEVANT_CHALLENGE_CLAIMED_WITH_REASON` | `NO_RELEVANT_PROCESS_WITH_REASON` | Appeals text says the tool makes/assists no decisions and only summarises guidance. A sparse field can be substantively appropriate. |
| NS&I: PolyAI | `BOTH_OR_MULTIPLE_ROUTES` | `IN_CHANNEL_HUMAN_REQUEST` + broader complaints/escalation process | One record exposes a non-binding tool-response handoff and a separate complaints/escalation path. These must not be collapsed into one appeal route or allowed to borrow each other's channel. |
| Environment Agency: Regulatory Guidance Assistant | `BROADER_OPERATIONAL_PROCESS` | `PUBLIC_PROCESS_NAMED_INITIATION_NOT_STATED` | Tool supports permitting officers rather than deciding; normal permitting appeals are named. The route attaches to the regulated process. |
| MoJ: Check-In / E-Supervision | `TOOL_OUTPUT` for review, but not public initiation | `INTERNAL_REVIEW_ONLY` | Recognition mismatches are reviewed by practitioners, while the record says no formal appeals process is needed because the tool does not determine service access. This is the clearest falsifier of `HUMAN_REVIEW = PUBLIC_CONTESTABILITY`. |
| Welsh Government: Mapping Ancient Woodland | `NOT_STATED_OR_LAYER_UNCLEAR` | `NOT_STATED_OR_UNCLEAR` | Appeals field is `N/A`, while the process text says outputs may support expert replanting decisions. `N/A` alone does not tell a reader whether a later operational decision has its own challenge route. |
| TrustID | `TOOL_OUTPUT` | `PUBLIC_INITIATION_EXPLICIT` + threshold-triggered internal review | Low matches go to internal analysts; users may separately request review if they think the tool failed. Internal and user-initiated review coexist and are distinguishable. |

## Eight v3-family cases

| Record | Provisional affected layer | Initiation / review mode visible in record | Pressure point |
|---|---|---|---|
| MoJ: Data First (Splink) | `TOOL_OUTPUT` | `USER_FEEDBACK_OR_ISSUE_REPORT` | Researchers can report suspected linkage errors/anomalies for later model iteration. This is correction feedback, not necessarily reconsideration of an individual decision. |
| NHS BSA: Residency Checker | `BOTH_OR_MULTIPLE_ROUTES` | `ALTERNATIVE_EVIDENCE_OR_RETRY` + complaints process | A failed residency check can be answered with documentary evidence; a complaints route also exists. Tool-output correction and broader complaint are separate mechanisms. |
| DSIT: GOV.UK site search | `TOOL_OUTPUT` / service output, not a binding decision | `USER_FEEDBACK_OR_ISSUE_REPORT` | Public feedback exists, but the text does not turn feedback into appeal/reconsideration. `FEEDBACK != APPEAL`. |
| DfE: Apprenticeship Withdrawal Rate AI | `NO_RELEVANT_CHALLENGE_CLAIMED_WITH_REASON` | `NO_RELEVANT_PROCESS_WITH_REASON` | Record says no appeal is required because only personalised content is affected and the content remains generally available. |
| HMRC: Logo Detection and Classification Toolkit | `BOTH_OR_MULTIPLE_ROUTES` | `INTERNAL_REVIEW_ONLY` for model performance + public legal appeal process for takedown | This case sharply separates review of a tool's performance from appeal of the consequential legal process. |
| HMT: HERMeS | `TOOL_OUTPUT` | `USER_FEEDBACK_OR_ISSUE_REPORT` | Internal users have a feedback/issue-report route. Useful correction channel, but not a public decision-subject appeal. |
| Standards and Testing Agency: Reception Baseline Routing | `BROADER_OPERATIONAL_PROCESS` / `NO_RELEVANT_CHALLENGE_CLAIMED_WITH_REASON` boundary | school/parent communication route; formal initiation not cleanly specified | The text argues that an appeal should not normally be needed, while allowing parents to seek narrative information and raise broader issues. The codebook must tolerate legitimate explanation without manufacturing a formal appeal. |
| BDUK: Project Gigabit Voucher Eligibility Engine | `NOT_STATED_OR_LAYER_UNCLEAR` between tool output and programme eligibility | `PUBLIC_INITIATION_EXPLICIT` for telecommunications organisations | A premise's eligibility can be challenged, but the field does not itself cleanly distinguish whether the challenged object is the engine output or the programme's broader eligibility determination. This is a real layer-boundary ambiguity, not parser failure. |

## What this dry run changes

The earlier candidate single axis:

```text
challenge_layer := TOOL_OUTPUT | BROADER_PROCESS | BOTH | ...
```

is insufficient by itself.

The data require at least two orthogonal views:

```text
AFFECTED_LAYER
!=
INITIATION_OR_REVIEW_MODE
```

and likely a third:

```text
ROUTE_FORM / EFFECT
```

because:

- an internal practitioner review can act on tool output without being initiable by the affected person;
- an in-channel request for a human can be available without being a formal appeal;
- a complaints process can attach to the broader service rather than the tool;
- alternative evidence can correct a failed check without being called an appeal;
- feedback can improve a model without reconsidering the affected person's outcome;
- explanation/audit evidence can exist without recovery.

This is the strongest method delta from the 16-case pressure pass.

```text
INTERNAL_REVIEW != PUBLIC_INITIATION
HUMAN_HANDOFF != FORMAL_APPEAL
FEEDBACK != RECONSIDERATION
ALTERNATIVE_EVIDENCE_ROUTE != COMPLAINT
PROCESS_APPEAL != TOOL_OUTPUT_APPEAL
```

## Does the question survive?

**Provisionally yes, as a fresh-corpus question.**

The cases do not immediately collapse into one scalar or one semantic class. More importantly, the distinctions change what a reader could reasonably infer about what happens next.

But the dry run also creates a stronger kill condition:

> If the full fresh corpus cannot distinguish `affected layer` from `initiation/review mode` without extensive coder invention, the two-layer thesis fails as an empirical register measurement and should shrink.

The version comparison remains secondary. The sample already shows strong composition differences between internal support tools, public-facing assistants, eligibility checks and consequential decision processes.

```text
VERSION_STRATIFICATION = DESCRIPTIVE_CONTEXT
NOT PRIMARY_CAUSAL_THESIS
```

## Next bounded attack

Independent reviewers should attack the **16 actual cases and codebook**, not the parser infrastructure.

Try to show:

1. `AFFECTED_LAYER` cannot be assigned without importing information outside the public record;
2. `INITIATION_OR_REVIEW_MODE` is merely a relabelled taxonomy with no consequential reader difference;
3. the labels collapse or proliferate when confronted with additional cases;
4. an established owner already provides the same layer x initiation measurement on current ATRS records;
5. tool-role composition makes version stratification useless even descriptively;
6. a simpler measurement preserves the consequential distinction.

Return `KILL / SHRINK / KEEP AS FRESH-CORPUS QUESTION`.

## Gates and ceilings

No participant recruitment, human data, organiser contact, registration, submission, provider spend or TRACE/ME change follows.

```text
DRY_RUN != RESULT
16_CASES != POPULATION_ESTIMATE
CODABLE_ON_16 != RELIABLE_ON_152
PUBLISHED_ROUTE != EFFECTIVE_ROUTE
PUBLIC_INITIATION_STATED != ROUTE_REACHABLE
VERSION_ASSOCIATION != VERSION_CAUSED_CHANGE
NULL_RESULT = VALID
OWNER_FOUND = VALID
```
# ATRS relation calibration reconciliation — 18 September 2026

Status: **BOUNDED METHOD RECEIPT / NOT POPULATION RESULT / NOT VALIDATION / NOT SUBMISSION**

## Source gate

Frozen 16-record sample identity:

`c97ea5548ccc26b130a8ffe2783569d6d365897fcf0e04a35fba033486012b54`

Independent first-pass returns:
- Codex: `CODEX_RELATION_FIRST_PASS_20260918.md` at commit `8cf2f2ba0e1ba6e83a4237aa330f97bb87ed325b`;
- Claude Code: COM #364 comment `5727586822`.

Both first passes report:
- all 16 frozen records coded;
- no live GOV.UK refetch;
- no linked-site inspection;
- no outside process knowledge needed for coding;
- no new target category minted to rescue hard cases.

Both disclose prior exposure to some records/method discussion.

```text
SEPARATE_FIRST_PASS != BLIND_EXTERNAL_VALIDATION
AGREEMENT != WORLD_TRUTH
```

## Framework reconciliation

Preserved as new branch objects without rewriting either first pass:

- `competition/atrs_answerability/RELATION_CALIBRATION_RECONCILIATION_20260918.md`
  - commit `40c707b369430165a25c1c6eb8d49ed0bd38ec04`
- `competition/atrs_answerability/RELATION_CODEBOOK_V2_20260918.md`
  - commit `d7eaeda4550f499ad6d0f8de5fd335d70e9cec8f`

Exact #364 branch head:

`d7eaeda4550f499ad6d0f8de5fd335d70e9cec8f`

Hosted CI:

`35327175854 SUCCESS`

## Calibration disposition

```text
METHOD = KEEP
CODEBOOK = REPAIR
PRIMARY INCLUSION = SHRINK
VERSION = SECONDARY TAG ONLY
HUMAN PILOT = NOT REQUIRED FOR CORE RELATION RESULT
NOVEMBER FRESH CORPUS = PLAUSIBLE IF LIVE RULES ALLOW
```

The calibration did **not** validate a population method.

It did establish a useful narrower result:

```text
ALL_16_CODED_FROM_FROZEN_RECORDS
NO_OUTSIDE_PROCESS_KNOWLEDGE_NEEDED
NO_NEW_TARGET_CATEGORY_NEEDED
FIRST_READS_DIFFERED_MATERIALLY_ON_INCLUSION_AND_SOME_TARGETS
REPAIR_EARNED
```

## Main earned repair — stopping rule

Codex included many more generic QA/governance/maintenance propositions than Claude Code. This is the largest disagreement class.

Primary future route table is now restricted to propositions explicitly connected to review/challenge/correction/override/reconsideration/complaint/appeal/handoff/opt-out/alternative evidence/explanation/self-correction of a specific tool output or broader operational-process outcome, plus explicit source-supported no-route-with-reason propositions.

Generic:
- model-performance monitoring;
- routine maintenance;
- supplier/product feedback;
- governance audit;
- security/threat reporting;
- data-rights action;
- research governance;
- general development feedback;
- source/document maintenance

remain **secondary context** unless explicitly bound to reconsideration/correction of the primary answerability object.

```text
MONITORING != ANSWER_BACK
MODEL_QA != SUBJECT_CHALLENGE
DATA_RIGHTS != OUTPUT_REVERSAL
SECURITY_REPORT != CONTESTATION
TRIGGER != TARGET
```

## Other earned repairs

- Separate trigger from target and stated effect.
- `DIRECT` takes precedence when the route proposition itself names the target; other fields can corroborate without making the relation cross-field.
- `EXPLICIT_CROSS_FIELD` is used only when another field is necessary to bind the target.
- General record contact details are not route channels unless explicitly bound.
- Bare `N/A` is not a route proposition; record it as `UNEXPLAINED_NA`.
- Preserve free-text actor and add derived actor class:
  `AFFECTED_OR_PUBLIC / INTERNAL / SUPPLIER_OR_INTERMEDIARY / NOT_STATED`.
- Add record-level affected-actor route status:
  `ROUTE_STATED / NO_ROUTE_STATED_IN_RECORD / AFFECTED_ACTOR_NOT_IDENTIFIED`.
- `NO_ROUTE_STATED_IN_RECORD != NO_REAL_ROUTE`.
- Contradiction in status/effect does not erase an otherwise clear target.
- Deployment state remains descriptive and routes in pre-production/POC records must not be narrated as current operation.

## Key target adjudications

Examples where the frozen coders disagreed and Framework applied the pre-frozen adjudication rules:

- NHSBSA documentary evidence after failed automated check -> **BROADER_OPERATIONAL_PROCESS**: the failed check triggers the route, but the stated action changes the application/entitlement path; the record does not state that the original automated result is rewritten.
- NS&I complaints/unresolved issues -> **LAYER_NOT_STATED**: complaints process named, target not.
- GOV.UK site-search general page feedback -> **OTHER_STATED_TARGET** unless explicitly bound to a particular ranking/result.
- HERMeS general feedback -> **LAYER_NOT_STATED**; source-verification self-correction remains TOOL_OUTPUT.
- TrustID manual check -> **BROADER_OPERATIONAL_PROCESS** as an alternative process, not correction of a match score.
- EA permitting appeal -> **BROADER_OPERATIONAL_PROCESS / DIRECT**.
- BDUK premise-eligibility challenge -> **TOOL_OUTPUT / EXPLICIT_CROSS_FIELD**.
- Welsh Ancient Woodland bare N/A -> no route bundle / `UNEXPLAINED_NA`.

These are calibration adjudications, not population findings.

## Current next step

Do not recode September into a result.

The next substantive #364 result, if pursued, should be a fresh corpus under live November competition rules using codebook v2.

Before that:
- targeted reviewer check may identify whether Framework misread either frozen first pass;
- live Apart rules must be reread at registration/submission gate;
- current GDS owner work must still be checked for a stronger exact owner before the sprint.

Reader Lens/human pilot remains secondary and gated.

```text
CALIBRATION_SURVIVED != METHOD_VALIDATED
FRESH_CORPUS != PREWRITTEN_RESULT
POSSIBLE_PRIZE = 0 UNTIL AWARDED
```

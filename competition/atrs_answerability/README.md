# ATRS Answerability Audit

Status: **CURRENT COMPETITION LEAD / EMPIRICAL OPEN-TRACK CANDIDATE / NOT SELECTED ENTRY / NOT A POLICY OR COMPLIANCE SCORE**

Question:

> Across the UK Algorithmic Transparency Recording Standard (ATRS) public finder, what can a reader actually observe in published records about human review, appeals/review, model performance, risks, impact assessment, maintenance and accountable ownership?

This audits the **published record**, not hidden/internal system reality.

## Official field boundary

The audit's central field is not an invented project concept.

The ATRS standard defines `appeals_and_review` as mechanisms for review or appeal of the decision available to the general public. Current GDS guidance asks publishers to consider both challenge to the algorithmic-tool output and challenge to the broader operational-process output. A public appeal/contact link is an example, not the only valid representation; where no process is relevant the guidance asks for an explanation.

```text
FREE-TEXT VARIATION != DISCOVERED DEFECT
LINK ABSENCE != FAILURE TO COMPLETE GUIDANCE
BROADER PROCESS APPEAL != TOOL-OUTPUT APPEAL
NO SEPARATE PROCESS CAN BE A VALID DISCLOSURE
```

## Strong-owner boundary

- GOV.UK / Government Digital Service owns the ATRS standard, template, guidance and repository.
- BritainThinks/CDEI already owns foundational UK public-engagement findings around clear/simple/layered transparency, contact details and appeal information.
- Fabio Rovai / Tesseract Academy owns an independent ATRS metadata corpus/harvester.
- Public Law Project's Tracking Automated Government register independently catalogues public-sector automated decision tools and owns much of the broader transparency/redress/public-law framing.
- existing algorithm-register usability and sociotechnical-governance research already owns much of the generic claim that registers can be difficult to use or omit accountability context.

See `OWNER_MAP.md`.

`NOT_FOUND_IN_BOUNDED_SEARCH != NOVEL`.

## Frozen September source witness

Pinned evidence bundle:

```text
GitHub Actions run = 35257984573 SUCCESS
source head = 4a7b43df95a2b776b885f8ee903d929100414af7
artifact = 10513278849
artifact sha256 = ad315d9b08a0af65c4615638df2235b9ce6f021307315fbeb6dfcbd8cbdb0097
finder declared / enumerated = 152 / 152
GOV.UK Search API ATRS set = 152
membership differences = 0
content-addressed source HTML pages = 152
```

The exact source bytes remain the historical witness. They were not replaced during later parser repairs.

Codex independently verified the original bundle digest, all 152 source hashes, membership identity and deterministic reproduction of the original extraction. That reproduction established repeatability, **not correctness of every field-name mapping**.

```text
REPRODUCED != CORRECT
SAME_REGEX + SAME_BYTES -> SAME_MISS
```

## Version-aware correction over the same source bytes

**Claude Code identified the legacy-heading misses. Codex independently confirmed them against the frozen witness.** Discovery and independent confirmation are preserved as different contributions.

Seven records use an older/transition ATRS heading family that the original parser did not fully recognise. The affected headings include:
- `Human decision` / `Human decisions`;
- `Impact assessment name / description / date / link`;
- `Risk name / description / mitigation`;
- an older/transition family without a `Model performance` field.

The repair added version-aware heading patterns and heading-family context, then reparsed the **same 152 frozen HTML files with no GOV.UK refetch**.

Corrected derived run:

```text
workflow = 35266542167 SUCCESS
source refetch = FALSE
heading profiles:
  current_named_family = 145
  legacy_2024_family = 6
  mixed_known_families = 1
```

Corrected source-level observations:

```text
human_review = 152/152 observed
appeals_review = 151/152 observed
model_performance = 139/152 observed
  - 13 not observed on page
  - 7 of those are in the known legacy/transition family where this field is not present
risks = 152/152 observed
impact_assessment = 145/152 observed
maintenance = 152/152 observed
senior_responsible_owner = 152/152 observed
```

The original historical report's `146/152` human-review, `145/152` risks and `138/152` impact-assessment figures are **superseded**. The old `139/152` model-performance number remains numerically the same but its interpretation is corrected by template-family context.

```text
HISTORICAL_REPORT != DELETED
HISTORICAL_COUNT != CURRENT_INTERPRETATION
HEADING_FAMILY != COMPLIANCE_STATUS
FIELD_NOT_OBSERVED != REQUIRED_FIELD_OMITTED
```

## Appeals/review pilot — still intact

The parser-version defect did not affect the `Appeals and review` field extraction.

`ADJUDICATION_PLAN.md` fixed the manual review set before the repaired corpus output was read:
- census all 27 appeals/review records with a syntactic contact token;
- inspect 20 token-negative records selected by ascending `SHA256(canonical URL)`;
- separately inspect missing/repeated appeals fields.

Framework first pass + bounded Codex hostile read is preserved in `FRAMEWORK_FIRST_ADJUDICATION_20260917.md`.

Reconciled bounded labels:

```text
27 token-positive records
  REVIEW_OR_APPEAL_ROUTE = 16
  GENERAL_HELP_OR_FEEDBACK = 9
  UNRELATED_TOKEN = 1
  AMBIGUOUS = 1

20 deterministic token-negative sample
  ROUTE_DESCRIBED_WITHOUT_LOCATOR = 15
  NO_LOCATOR_IN_SECTION = 3
  AMBIGUOUS = 2
  PLAIN_TEXT_LOCATOR_MISSED = 0
```

The 20 token-negative records are a **sample, not a population estimate**. **Token absence also does not mean no reader action exists**: in-channel handoff and process references can occur without a URL/email/phone token.

The exploratory semantic annotations/classifications are post-pilot work and **do not establish classification validity**. They remain provisional even when evidence-bound.

## Reader Lens

`reader_lens.py` builds a static, source-linked reader centred on one practical question:

> What does this published record actually say about review, challenge, correction, complaint, clarification or help?

The current interface:
- links each record to GOV.UK;
- shows exact published `Appeals and review` text;
- makes safely representable http/https/mailto evidence actionable without relabelling it as an appeal;
- leaves phone-like detection as visible heuristic evidence rather than manufacturing a phone action;
- shows human-review and responsible-owner disclosure;
- moves source hashes/extraction metadata behind Evidence details;
- separates source search from optional exploratory-annotation search;
- uses visible labels, a live results status and reset/no-match guidance;
- keeps cards compact by default with full evidence retained in HTML details;
- produces **No scalar score is produced** by the audit or Reader Lens.

A syntactic contact token is **not called a review route** by the automated layer. Semantic relevance requires source readback.

Exploratory semantic annotations are not silently carried across parser-version boundaries. They may be attached only through an explicit evidence-identity step and remain optional/not validated.

```text
SOURCE_READBACK_AID != DEMONSTRATED_READER_BENEFIT
EASIER_INSPECTION != EFFECTIVE_REMEDY
READER_LENS != REPLACEMENT_FOR_GOV.UK
```

## Reader-facing result under test

The candidate finding remains narrower than a generic transparency critique:

> `Appeals and review` field presence can be high while the reader-visible challenge/review object remains heterogeneous. Field completion alone therefore loses distinctions about what can be challenged, by whom, through what route, and at which layer of the decision process.

**Only retain that finding at the strength earned** by a fresh/full semantic census and a real reader-use test.

If the result reduces to **"free-text fields vary"**, shrink #364 to a demo.

`READER_USE_PROTOCOL.md` defines a future bounded A/B task on actual ATRS records. No human reader benefit has been demonstrated yet.

## Falsification status

A 100-probe regression/falsification harness covers evidence binding, parser/extraction, bounded codebook regressions and documentation/claim ceilings.

The first run was `55/100`; substantive failures were repaired. The same known structure later ran `100/100`. The subsequent legacy-heading discovery demonstrates why this cannot be treated as validation.

```text
100/100_KNOWN_FALSIFIERS_RESISTED != VALIDATED_RESEARCH_RESULT
GREEN_TESTS != COMPLETE_MODEL_OF_THE_SOURCE
REPRODUCIBILITY != CORRECTNESS
```

## Stable anti-drift / claim-ceiling block

The following statements are intentionally stable regression targets for documentation checks. They are ceilings, not research results:

```text
CURRENT COMPETITION LEAD
NOT SELECTED ENTRY
NOT A POLICY OR COMPLIANCE SCORE
published record
not hidden/internal system reality
GOV.UK / Government Digital Service owns
Tesseract Academy
NOT_FOUND_IN_BOUNDED_SEARCH != NOVEL
does not establish classification validity
No scalar score is produced
not called a review route
sample, not a population estimate
Token absence also does not mean no reader action exists
Only retain that finding at the strength earned
Re-read live competition Guidelines/terms
FIELD_PRESENT != PRACTICAL_NAVIGABILITY
SECTION_PRESENT != PRACTICALLY_EFFECTIVE_REMEDY
SYNTACTIC_CONTACT_TOKEN_PRESENT != RELEVANT_APPEAL_ROUTE
CONCRETE_ROUTE_OBSERVED != ROUTE_EFFECTIVE
HUMAN_HANDOFF != FORMAL_APPEAL
ROUTE_DESCRIBED_WITHOUT_LOCATOR != NO_ROUTE_EXISTS
DISCLOSURE_ABSENT != PRACTICE_ABSENT
PUBLIC_RECORD_AUDIT != COMPLIANCE_AUDIT
PUBLIC_RECORD_AUDIT != POLICY_VERDICT
No registration, organiser contact, model/provider spend, terms acceptance or submission
```

## November core-work posture

September material remains pilot / methodology / falsification / frozen baseline.

If live Apart rules permit/require fresh core work during the November sprint:
- fetch a new current-finder corpus;
- freeze membership and source bytes;
- freeze a version-aware semantic codebook;
- conduct the full appeals/review census with independent reads and explicit disagreement;
- test reader-use value rather than assuming it;
- optionally compare changed records against the September content-addressed baseline.

**Re-read live competition Guidelines/terms** before registration/submission.

## Critical ceilings

```text
FIELD_PRESENT != PRACTICAL_NAVIGABILITY
SECTION_PRESENT != PRACTICALLY_EFFECTIVE_REMEDY
SYNTACTIC_CONTACT_TOKEN_PRESENT != RELEVANT_APPEAL_ROUTE
CONCRETE_ROUTE_OBSERVED != ROUTE_EFFECTIVE
HUMAN_HANDOFF != FORMAL_APPEAL
ROUTE_DESCRIBED_WITHOUT_LOCATOR != NO_ROUTE_EXISTS
DISCLOSURE_ABSENT != PRACTICE_ABSENT
ATRS_RECORD != COMPLETE_SYSTEM_REALITY
PUBLIC_RECORD_AUDIT != COMPLIANCE_AUDIT
PUBLIC_RECORD_AUDIT != POLICY_VERDICT
```

#364 remains the **CURRENT COMPETITION LEAD**, **NOT SELECTED ENTRY**.

**No registration, organiser contact, model/provider spend, terms acceptance or submission** is implied by this branch.

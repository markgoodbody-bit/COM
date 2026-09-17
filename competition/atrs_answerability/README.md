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
- Fabio Rovai / Tesseract Academy owns an independent ATRS metadata corpus/harvester.
- Public Law Project's Tracking Automated Government register independently catalogues public-sector automated decision tools and owns much of the broader transparency/redress/public-law framing.
- existing qualitative/governance research already studies ATRS and public-sector algorithmic transparency.

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

Codex found seven records using an older/transition ATRS heading family that the original parser did not fully recognise. The affected headings included:
- `Human decision` / `Human decisions`;
- `Impact assessment name / description / date / link`;
- `Risk name / description / mitigation`;
- an older/transition family without a `Model performance` field.

The repair added version-aware heading patterns and heading-family context, then reparsed the **same 152 frozen HTML files with no GOV.UK refetch**.

Corrected derived run:

```text
workflow = 35266542167 SUCCESS
parser branch head = 363ba74d7f38aacd87d4fd7fd08d26c13ef9f8fa
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

The 20 token-negative records are a sample, not a population estimate. `NO_CONTACT_TOKEN != NO_ROUTE`.

## Reader Lens

`reader_lens.py` builds a static, source-linked reader centred on one practical question:

> What does this published record actually say about what someone can do next?

The corrected Reader Lens is generated from the version-aware derived report and defaults to source evidence only. It:
- links each card to GOV.UK;
- shows exact published `Appeals and review` text;
- exposes published URL/email/phone/link tokens without calling them rights or remedies;
- shows human-review and responsible-owner disclosure;
- produces no scalar score;
- does not infer hidden/internal practice;
- does not claim legal advice or route effectiveness.

Exploratory semantic annotations from the historical pilot are **not silently carried across the parser-version boundary**. They may be reconciled later only through an explicit evidence-identity step.

```text
SOURCE_READBACK_AID != DEMONSTRATED_READER_BENEFIT
EASIER_INSPECTION != EFFECTIVE_REMEDY
READER_LENS != REPLACEMENT_FOR_GOV.UK
```

## Reader-facing result under test

The candidate finding remains narrower than a generic transparency critique:

> `Appeals and review` field presence can be high while the reader-visible challenge/review object remains heterogeneous. Field completion alone therefore loses distinctions about what can be challenged, by whom, through what route, and at which layer of the decision process.

Only retain this at the strength earned by a fresh/full semantic census and a real reader-use test.

If the result reduces to **"free-text fields vary"**, shrink #364 to a demo.

## Falsification status

A 100-probe regression/falsification harness covers evidence binding, parser/extraction, bounded codebook regressions and claim/drift ceilings.

The first run was `55/100`; substantive failures were repaired. The same structure later ran `100/100` on the then-known falsifiers. The subsequent heading-family defect demonstrates why this cannot be treated as validation.

```text
100/100_KNOWN_FALSIFIERS_RESISTED != VALIDATED_RESEARCH_RESULT
GREEN_TESTS != COMPLETE_MODEL_OF_THE_SOURCE
REPRODUCIBILITY != CORRECTNESS
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

Re-read live competition Guidelines/terms before registration/submission.

## Critical ceilings

```text
FIELD_PRESENT != PRACTICAL_NAVIGABILITY
SECTION_PRESENT != PRACTICALLY_EFFECTIVE_REMEDY
SYNTACTIC_CONTACT_TOKEN_PRESENT != RELEVANT_APPEAL_ROUTE
CONCRETE_ROUTE_OBSERVED != ROUTE_EFFECTIVE
HUMAN_HANDOFF != FORMAL_APPEAL
DISCLOSURE_ABSENT != PRACTICE_ABSENT
ATRS_RECORD != COMPLETE_SYSTEM_REALITY
PUBLIC_RECORD_AUDIT != COMPLIANCE_AUDIT
PUBLIC_RECORD_AUDIT != POLICY_VERDICT
```

#364 remains the **current competition lead**, not a selected or submitted entry.

No registration, organiser contact, model/provider spend, terms acceptance or submission is implied by this branch.

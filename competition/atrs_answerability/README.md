# ATRS Answerability Audit

Status: **CURRENT COMPETITION LEAD / EMPIRICAL OPEN-TRACK CANDIDATE / NOT SELECTED ENTRY / NOT A POLICY OR COMPLIANCE SCORE**

Question:

> Across the current UK Algorithmic Transparency Recording Standard (ATRS) public finder, what can a reader actually observe in published records about human review, appeals/review, model performance, risks, impact assessment, maintenance and accountable ownership?

This audits the **published record**, not hidden/internal system reality.

## Official field boundary

The audit's central field is not an invented project concept.

The ATRS standard defines `appeals_and_review` as the mechanisms in place for review or appeal of the decision available to the general public. Current GDS guidance says publishers should consider both:
- outputs of the algorithmic tool itself and whether they can be challenged/appealed; and
- outputs of the broader operational process and whether they can be challenged/appealed.

The guidance says this may involve a link to a public appeal or contact form and asks for an explanation where no appeals/review process is necessary or relevant.

That makes the public disclosure itself a concrete empirical object.

## Strong-owner boundary

- GOV.UK / Government Digital Service owns the ATRS standard, template, guidance and repository.
- Fabio Rovai / Tesseract Academy already provides an independent ATRS **metadata** corpus (publishing body, tool, description, date). This project does not copy that code.
- existing research includes qualitative work on ATRS/practitioner perspectives.

Residual question under test:

> What do the **full published fields** actually make legible about public challenge/review relationships, beyond register/index metadata and beyond field-completion counts?

`NOT_FOUND_IN_BOUNDED_SEARCH != NOVEL`.

## Reproducible September witness

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

Codex independently downloaded the evidence bundle, verified its digest and all 152 stored source hashes, confirmed finder URL set == audit URL set, and re-executed the exact parser on all preserved source pages with **zero extracted-field differences**.

This establishes bounded extraction reproducibility inside the evidence bundle. It does not establish classification validity, remedy quality or internal practice.

## Automated layer

The parser preserves deterministic public-record observables:
- every matching section rather than first match only;
- exact heading and section text;
- hrefs, plain-text URLs, emails and phone-like tokens;
- source SHA-256 and fetch time;
- optionally the exact source HTML bytes by content hash.

Current section families:
- human review;
- appeals and review;
- model performance;
- risks;
- impact assessment;
- maintenance;
- senior responsible owner.

No scalar score is produced.

A syntactic contact token is **not** called a review route by the automated layer. Semantic relevance requires readback.

## Frozen structural observations

From the September 152-record witness:
- human-review field observed `146/152`;
- appeals/review `151/152`;
- model performance `139/152` (12 records have repeated matching model-performance sections);
- risks `145/152`;
- impact assessment `138/152`;
- maintenance `152/152`;
- senior responsible owner `152/152`.

Auxiliary `none/N/A-like phrase` totals from the frozen witness are not treated as primary findings. Two live false negatives were later found; the detector was repaired offline and regression-tested without refetching/replacing the historical corpus witness.

## Preregistered appeals/review pilot

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

The 20-record token-negative set is a sample, not a population estimate. Token absence also does not mean no reader action exists: records can describe in-channel human handoff or existing complaints/review processes without a URL/email/phone token.

## Reader-facing result under test

`READER_WALKTHROUGH.md` demonstrates from exact frozen source examples that the same standardized field can disclose materially different layers/objects:
- concrete reconsideration/review route;
- broader complaints/appeal process;
- general help or feedback;
- in-channel human handoff;
- clinician-mediated review;
- data-rights action;
- internal review;
- explanation/audit trail without recovery;
- explicit no-separate-process/no-decision statements;
- ambiguous scope.

Candidate field-level finding:

> `Appeals and review` field presence can be high while the reader-visible public challenge/review object remains heterogeneous. Measuring field completion alone therefore loses distinctions about **what can be challenged, by whom, through what route, and at which layer of the decision process**.

Only retain that finding at the strength earned by a fresh/full semantic census.

## November core-work posture

`SPRINT_EXECUTION_PLAN.md` keeps September material as pilot/methodology infrastructure and preserves a fresh sprint-time research object if live Apart rules require core work during the event:
- fetch a new current-finder corpus;
- freeze membership and source bytes;
- freeze a multi-label semantic codebook;
- conduct full appeals/review census with independent aperture reads and explicit disagreement;
- test robustness and negative controls;
- optionally compare changed records against the September content-addressed baseline.

Re-read live competition Guidelines/terms before registration/submission. Historical Apart rules are not assumed to govern November 2026.

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

## Competition fit

Apart AI x Epistemics Open Track currently asks what can be measured about a live epistemic deployment using data downloadable over a weekend and says deployment/impact projects may look more like investigative research than software.

#364 is therefore the **current competition lead**, not a selected or submitted entry.

No registration, organiser contact, model/provider spend, terms acceptance or submission is implied by this branch.

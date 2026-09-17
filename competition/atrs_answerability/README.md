# ATRS Answerability Audit v0

Status: **EMPIRICAL COMPETITION CANDIDATE / PUBLIC-RECORD AUDIT / NOT A POLICY SCORE / NOT A SUBMISSION**

Question:

> Across current UK Algorithmic Transparency Recording Standard (ATRS) records, what can a member of the public actually observe about human review, appeals/review routes, performance disclosure, risks, impact assessment, maintenance and accountable ownership?

This candidate audits the **published record**, not the hidden reality of a system.

## Why this may be useful

The current ATRS is mandatory for in-scope central-government bodies and tools. Official guidance says the purpose is meaningful, intelligible transparency about public-sector algorithmic tools and their role in broader processes. Government's Data and AI Ethics Framework separately says affected people should be able to understand decisions, provide feedback, contest incorrect outcomes, seek redress/review/correction, and that teams should establish monitoring and feedback mechanisms.

Those policy statements make the public record itself a legitimate empirical object.

## Strong owner boundary

An existing independent project by Fabio Rovai / Tesseract Academy already provides an open corpus of ATRS metadata (publishing body, tool name, description, date) harvested from the GOV.UK Search API. This work credits that owner and does **not** reproduce its code. The third-party repository does not currently declare a GitHub code licence; underlying GOV.UK public-sector information is OGL v3.0.

Residual question under test:

> What do the **full published record fields** disclose about practical answerability, beyond register/index metadata?

This is not another ATRS directory.

## Observable fields

The v0 parser records only deterministic disclosure facts:

- section present or not observed;
- section text explicitly states `none` / `not applicable` or similar;
- for appeals/review, whether the published section contains a concrete route locator such as a URL, email, contact route, complaint process, queries line or review-request language;
- text length and exact heading for audit/readback.

Current section families:

- human review;
- appeals and review;
- model performance;
- risks;
- impact assessment;
- maintenance;
- senior responsible owner.

No scalar score is produced.

## Critical interpretation ceilings

```text
SECTION_PRESENT != PRACTICALLY_EFFECTIVE_REMEDY
ROUTE_LOCATOR_PRESENT != ROUTE_WORKS
DISCLOSURE_ABSENT != PRACTICE_ABSENT
ATRS_RECORD != COMPLETE_SYSTEM_REALITY
PUBLIC_RECORD_AUDIT != POLICY_VERDICT
```

A missing published section is a finding about the accessible record, not proof that no internal mechanism exists. A listed appeal route is not proof that the route is usable or effective.

## Data provenance

Enumeration and page content come directly from GOV.UK. Public-sector information is reused under the Open Government Licence v3.0.

The official search endpoint is queried for `content_store_document_type=algorithmic_transparency_record`; each returned GOV.UK record page is then fetched independently and parsed.

## First falsification gate

Do **not** publish corpus-wide percentages merely because the parser runs.

Before a result is credible:

1. exact parser tests must pass;
2. a small live sample must be fetched from GOV.UK;
3. extracted sections must be manually checked against the rendered public records;
4. version differences (v2/v3/v4 record headings) must be mapped rather than silently treated as missing fields;
5. only then may a full current-corpus run be interpreted.

## Nearby owners / prior work

- GOV.UK / GDS owns the ATRS standard, scope, repository and guidance.
- Fabio Rovai / Tesseract Academy owns a current independent metadata corpus/harvester.
- existing public-sector and academic work has studied transparency policy and practitioner perspectives.

This candidate only survives if a current full-record answerability audit is not already owned and if deterministic extraction can distinguish real disclosure differences from template/version differences.

## Competition fit

Apart AI x Epistemics Open Track asks what can be measured from a live epistemic deployment using weekend-downloadable data. ATRS is a live public deployment/transparency infrastructure with a current public corpus and explicit accountability purpose.

No registration, model calls, paid services, organiser contact or submission are implied by this branch.

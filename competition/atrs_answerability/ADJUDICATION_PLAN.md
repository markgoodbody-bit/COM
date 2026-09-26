# ATRS answerability audit — appeals/review adjudication plan

Status: **PREDECLARED BEFORE READING THE v0.4 FULL-CORPUS OUTPUT**

The parser deliberately does not infer that any link, email or phone number is a usable appeal/review route. It only preserves syntactic contact tokens in the published `Appeals and review` section.

## Corpus

Use only the exact live GOV.UK ATRS finder membership from the same run. The run must satisfy:

```text
finder_declared_count == finder_enumerated_count
finder_urls == generic_Search_API_urls
```

A cached search-page count is not corpus authority.

## Positive-token census

Manually inspect **every** current record where:

```text
appeals_review.section_present == true
and
appeals_review.syntactic_contact_token_present == true
```

Using only the preserved `Appeals and review` text + href/email/phone tokens, assign exactly one label:

- `REVIEW_OR_APPEAL_ROUTE` — the token is explicitly presented as a way to challenge, review, appeal, complain about, correct, or obtain reconsideration of the tool output or the broader decision/process.
- `GENERAL_HELP_OR_FEEDBACK` — usable contact/help/feedback route is present, but the text does not establish it as a review/appeal/reconsideration route.
- `UNRELATED_TOKEN` — token is present for another purpose (for example privacy policy, general information, supplier material).
- `AMBIGUOUS` — the section does not support a stable classification from its text alone.

Do not infer whether a route works, is independent, is timely, or offers an effective remedy.

## Negative-token probe

Among records where `Appeals and review` is present but `syntactic_contact_token_present == false`, select **20** records by:

```text
sort ascending by SHA256(canonical GOV.UK record URL)
take first 20
```

Inspect the complete preserved appeals/review text. Label:

- `NO_LOCATOR_IN_SECTION`
- `PLAIN_TEXT_LOCATOR_MISSED` — a usable URL/email/phone locator is visibly present but parser missed it
- `ROUTE_DESCRIBED_WITHOUT_LOCATOR` — review/appeal/help process described, but no concrete locator appears in the section
- `AMBIGUOUS`

This sample estimates parser false negatives for syntactic locator detection; it does **not** estimate whether government provides effective remedy.

## Double-check

Framework performs first bounded read. Codex / Claude Code are asked to attack disagreements and at least all `AMBIGUOUS` cases plus a sample from each positive class. Agreement is evidence about classification consistency, not validation of the underlying government process.

## Claim ceiling

Allowed output:

- current finder membership and field-disclosure counts;
- number of records whose appeals/review section contains syntactic contact tokens;
- manually adjudicated textual categories above;
- examples with preserved source text/hash.

Not allowed from this audit alone:

```text
MISSING_DISCLOSURE -> MISSING_PRACTICE
ROUTE_DESCRIBED -> ROUTE_EFFECTIVE
CONTACT_TOKEN -> APPEAL_RIGHT
ATRS_COMPLETE -> SYSTEM_ACCOUNTABLE
CORPUS_PERCENTAGE -> GOVERNMENT_COMPLIANCE_SCORE
PUBLIC_RECORD_AUDIT -> POLITICAL_VERDICT
```

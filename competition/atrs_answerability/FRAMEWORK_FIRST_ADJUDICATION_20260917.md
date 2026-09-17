# ATRS answerability audit — Framework adjudication record

Status: **FIRST PASS PRESERVED + BOUNDED CODEX REVIEW RECONCILED / NOT A COMPLIANCE OR QUALITY SCORE**

Source witness:
- GitHub Actions run `35257984573`
- head `4a7b43df95a2b776b885f8ee903d929100414af7`
- artifact `10513278849` / sha256 `ad315d9b08a0af65c4615638df2235b9ce6f021307315fbeb6dfcbd8cbdb0097`
- current finder = 152; enumerated finder = 152; generic Search API = 152; membership differences = 0.
- all 152 exact fetched HTML pages were retained by source hash.

Codex independently downloaded the same artifact, verified its SHA-256, checked all 152 stored HTML hashes, confirmed finder URLs == audit URLs, and re-executed the exact source parser across all preserved pages with **zero extraction differences**. That establishes bounded extraction reproducibility within this evidence bundle. It does not establish classification validity, remedy effectiveness, or completeness of government practice.

## Automated current-finder coverage

Primary structural observations from the frozen run:
- `human_review`: section observed 146/152; multiple-match records 0; syntactic contact-token occurrence 2.
- `appeals_review`: section observed 151/152; multiple-match records 0; syntactic contact-token occurrence 27.
- `model_performance`: section observed 139/152; multiple-match records 12; syntactic contact-token occurrence 15.
- `risks`: section observed 145/152; multiple-match records 0; syntactic contact-token occurrence 9.
- `impact_assessment`: section observed 138/152; multiple-match records 0; syntactic contact-token occurrence 16.
- `maintenance`: section observed 152/152; multiple-match records 0; syntactic contact-token occurrence 3.
- `senior_responsible_owner`: section observed 152/152; multiple-match records 0; syntactic contact-token occurrence 0.

The auxiliary `contains_none_or_na_phrase` totals from this frozen run are **not primary findings**. Codex found two live false negatives (`N/A no decisions`; `no formal appeals process`). The preserved section text/manual classification remains usable; the old phrase-count totals should not be presented as final corpus measurements.

## Preregistered appeals/review first pass

All 27 token-positive records were read. Initial labels:
- `REVIEW_OR_APPEAL_ROUTE`: 16
- `UNRELATED_TOKEN`: 2
- `GENERAL_HELP_OR_FEEDBACK`: 9
- `AMBIGUOUS`: 0

The SHA256(URL)-selected 20-record token-negative sample was read. Initial labels:
- `ROUTE_DESCRIBED_WITHOUT_LOCATOR`: 16
- `NO_LOCATOR_IN_SECTION`: 3
- `AMBIGUOUS`: 1
- `PLAIN_TEXT_LOCATOR_MISSED`: 0

One current record (`DBT: Find Exporters`) had no parser-observed `Appeals and review` field. No appeals field had multiple matches.

These are descriptive labels only. The token-negative sample is not silently generalized to all token-negative records.

## Token-positive census — first labels

| Record | Framework first label |
|---|---|
| AI Writing Assistant (Social Care) | `REVIEW_OR_APPEAL_ROUTE` |
| DEFRA: Local Authority Waste Collection Cost Groupings | `REVIEW_OR_APPEAL_ROUTE` |
| DESNZ: Warm Home Discount Eligibility - Energy Cost Modelling | `REVIEW_OR_APPEAL_ROUTE` |
| DWP: Employment and Support Allowance Online Medical Matching | `REVIEW_OR_APPEAL_ROUTE` |
| Department for Health and Social Care and NHS Digital: QCovid algorithm | `UNRELATED_TOKEN` |
| Dorset Council: Formulate for Adult Social Care | `REVIEW_OR_APPEAL_ROUTE` |
| HMRC: VAT Return Analysis Tool | `REVIEW_OR_APPEAL_ROUTE` |
| Health Research Authority: Proportionate Review Toolkit | `REVIEW_OR_APPEAL_ROUTE` |
| IPO: Check if you could register your trade mark tool | `GENERAL_HELP_OR_FEEDBACK` |
| Maritime and Coastguard Agency: Proview Proctoring Tool | `REVIEW_OR_APPEAL_ROUTE` |
| Money and Pensions Service: Budget Planner | `GENERAL_HELP_OR_FEEDBACK` |
| Money and Pensions Service: Mortgage Affordability Calculator | `GENERAL_HELP_OR_FEEDBACK` |
| Money and Pensions Service: Mortgage Repayment Calculator | `GENERAL_HELP_OR_FEEDBACK` |
| Money and Pensions Service: Pension Calculator | `GENERAL_HELP_OR_FEEDBACK` |
| Money and Pensions Service: Redundancy Pay Calculator | `GENERAL_HELP_OR_FEEDBACK` |
| NHS BSA: Residency Checker for UK EHIC/GHIC/PRC/S2 | `REVIEW_OR_APPEAL_ROUTE` |
| NHS Blood & Transplant: Organ Offering Scheme Algorithms | `REVIEW_OR_APPEAL_ROUTE` |
| National Highways: Highways Webchat | `REVIEW_OR_APPEAL_ROUTE` |
| OSBC: Interest Calculator | `GENERAL_HELP_OR_FEEDBACK` |
| Office for Students: Teaching Funding Allocations | `REVIEW_OR_APPEAL_ROUTE` |
| Office of the Public Guardian: Investigations Assistant | `REVIEW_OR_APPEAL_ROUTE` |
| Ofsted: Survey Summarisation Tool | `REVIEW_OR_APPEAL_ROUTE` |
| Social Care Wales: Qualification Chatbot | `REVIEW_OR_APPEAL_ROUTE` |
| UKHO: Tidal Harmonic Analysis and Prediction | `GENERAL_HELP_OR_FEEDBACK` |
| Welsh Government: Dylun - A content design assistant | `GENERAL_HELP_OR_FEEDBACK` |
| West Berkshire Council: Apply for a Larger Rubbish Bin | `REVIEW_OR_APPEAL_ROUTE` |
| Wilton Park: Data Cleaning Tool | `UNRELATED_TOKEN` |

## Token-negative deterministic sample — first labels

| Record | Framework first label |
|---|---|
| FCDO: Correspondence Triage | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| MoJ: Data First (Splink) | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| The Crown Prosecution Service: Correspondence Drafting Tool | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| DSIT: GOV.UK site search | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| DSIT: GOV.UK Chat | `NO_LOCATOR_IN_SECTION` |
| NS&I: PolyAI | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| DfE: Apprenticeship Withdrawal Rate AI | `NO_LOCATOR_IN_SECTION` |
| Environment Agency: Regulatory Guidance Assistant | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| GOV.UK Data Labs (Cabinet Office): Related Links | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| HMRC: Logo Detection and Classification Toolkit (LDK) | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| MoJ: Check-In with your probation officer (E-Supervision) | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| HMT: HERMeS (HMT's Excerpt Retrieval Messaging System) | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| Standards and Testing Agency: Reception Baseline Assessment Routing | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| BDUK: Project Gigabit Voucher Eligibility Engine | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| Welsh Government: Mapping Ancient Woodland Image Segmentation Model | `NO_LOCATOR_IN_SECTION` |
| Environment Agency: Hello Lamp Post | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| Student Loans Company: Advanced Learning Loans Assessment Rules | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| Insolvency Service: Redundancy Payment Calculation Engine | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |
| Cabinet Office: Automated Digital Document Review | `AMBIGUOUS` |
| Standards and Testing Agency: Key stage 2 Test Administration form rules | `ROUTE_DESCRIBED_WITHOUT_LOCATOR` |

## Bounded Codex review and Framework resolution

Codex read the complete preserved `Appeals and review` text for the three specifically challenged cases plus six independently chosen examples. This was a bounded hostile review, not blind review and not an agreement-rate study.

Held without label change:
- **QCovid** remains `UNRELATED_TOKEN` for the token itself: the hyperlink is clinician guidance, not a reconsideration/contact locator. Separately preserve that the section describes patients reviewing results with their clinician. `UNRELATED_TOKEN != UNRELATED_SECTION`.
- **Cabinet Office: Automated Digital Document Review** remains `AMBIGUOUS`: hard deletion is described as non-recoverable/appeal impossible, while saved deletion evidence may later justify deletion in an appeal or FOI request. Explanation/review evidence is not the same as recovery.
- **HRA** and **NHS BSA** remain `REVIEW_OR_APPEAL_ROUTE` under the deliberately broad review/challenge codebook; this does not claim statutory appeal rights or effectiveness.
- **UKHO** and **Dylun** remain `GENERAL_HELP_OR_FEEDBACK`.
- **NS&I PolyAI** remains `ROUTE_DESCRIBED_WITHOUT_LOCATOR`: the section describes human-agent request, complaints and escalation without a contact token.

Resolved disagreements:
- **Wilton Park: Data Cleaning Tool** changes from `UNRELATED_TOKEN` to `AMBIGUOUS`. The privacy-notice link is informational, but a named Data Protection Officer email provides an operative data-removal route. Relevance to reconsidering the cleaning tool's output is not established; therefore neither `UNRELATED_TOKEN` nor `REVIEW_OR_APPEAL_ROUTE` cleanly fits.
- **FCDO: Correspondence Triage** changes from `ROUTE_DESCRIBED_WITHOUT_LOCATOR` to `AMBIGUOUS`. The section says emails are reviewed after triage and rights to review/appeal responses are unaffected, but it does not establish how a correspondent initiates that review. Under a public-reader route interpretation, the broader first label overstated the disclosure.

### Reconciled bounded counts

Token-positive census (27):
- `REVIEW_OR_APPEAL_ROUTE`: **16**
- `GENERAL_HELP_OR_FEEDBACK`: **9**
- `UNRELATED_TOKEN`: **1**
- `AMBIGUOUS`: **1**

Token-negative deterministic sample (20):
- `ROUTE_DESCRIBED_WITHOUT_LOCATOR`: **15**
- `NO_LOCATOR_IN_SECTION`: **3**
- `AMBIGUOUS`: **2**
- `PLAIN_TEXT_LOCATOR_MISSED`: **0**

These counts describe this bounded classification exercise only. They are not government-compliance statistics and the token-negative sample is not a census.

## Ceilings

```text
BOUNDED_REVIEW_AGREEMENT != VALIDATED_CLASSIFICATION
CONCRETE_ROUTE_OBSERVED != ROUTE_EFFECTIVE
ROUTE_DESCRIBED_WITHOUT_LOCATOR != NO_ROUTE_EXISTS
HUMAN_HANDOFF_DESCRIBED != FORMAL_APPEAL
SECTION_NOT_OBSERVED != PRACTICE_ABSENT
TOKEN_NEGATIVE_SAMPLE != ALL_TOKEN_NEGATIVES
PUBLIC_RECORD_AUDIT != COMPLIANCE_AUDIT
PUBLIC_RECORD_AUDIT != POLICY_VERDICT
```

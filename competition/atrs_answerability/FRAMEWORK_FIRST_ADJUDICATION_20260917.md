# ATRS answerability audit — Framework first adjudication pass

Status: **FIRST PASS / BOUNDED HOSTILE REVIEW REQUIRED / NOT A COMPLIANCE OR QUALITY SCORE**

Source witness:
- GitHub Actions run `35257984573`
- head `4a7b43df95a2b776b885f8ee903d929100414af7`
- artifact `10513278849` / sha256 `ad315d9b08a0af65c4615638df2235b9ce6f021307315fbeb6dfcbd8cbdb0097`
- current finder = 152; enumerated finder = 152; generic Search API = 152; membership differences = 0.

Automated current-finder coverage:
- `human_review`: section observed 146/152; multiple-match records 0; none/N/A-like phrase occurrence 2; syntactic contact-token occurrence 2.
- `appeals_review`: section observed 151/152; multiple-match records 0; none/N/A-like phrase occurrence 33; syntactic contact-token occurrence 27.
- `model_performance`: section observed 139/152; multiple-match records 12; none/N/A-like phrase occurrence 9; syntactic contact-token occurrence 15.
- `risks`: section observed 145/152; multiple-match records 0; none/N/A-like phrase occurrence 0; syntactic contact-token occurrence 9.
- `impact_assessment`: section observed 138/152; multiple-match records 0; none/N/A-like phrase occurrence 7; syntactic contact-token occurrence 16.
- `maintenance`: section observed 152/152; multiple-match records 0; none/N/A-like phrase occurrence 2; syntactic contact-token occurrence 3.
- `senior_responsible_owner`: section observed 152/152; multiple-match records 0; none/N/A-like phrase occurrence 2; syntactic contact-token occurrence 0.

## Preregistered appeals/review first pass

All 27 token-positive records were read. Initial labels:
- `REVIEW_OR_APPEAL_ROUTE`: 16
- `UNRELATED_TOKEN`: 2
- `GENERAL_HELP_OR_FEEDBACK`: 9

The SHA256(URL)-selected 20-record token-negative sample was read. Initial labels:
- `ROUTE_DESCRIBED_WITHOUT_LOCATOR`: 16
- `NO_LOCATOR_IN_SECTION`: 3
- `AMBIGUOUS`: 1
- `PLAIN_TEXT_LOCATOR_MISSED`: 0

One current record (`DBT: Find Exporters`) had no parser-observed `Appeals and review` field. No appeals field had multiple matches.

These are descriptive first-pass labels only. The token-negative sample is not silently generalized to all token-negative records.

## Token-positive census

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

## Token-negative deterministic sample

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

## Ceilings

```text
FIRST_PASS_LABEL != VALIDATED_CLASSIFICATION
CONCRETE_ROUTE_OBSERVED != ROUTE_EFFECTIVE
ROUTE_DESCRIBED_WITHOUT_LOCATOR != NO_ROUTE_EXISTS
SECTION_NOT_OBSERVED != PRACTICE_ABSENT
TOKEN_NEGATIVE_SAMPLE != ALL_TOKEN_NEGATIVES
PUBLIC_RECORD_AUDIT != COMPLIANCE_AUDIT
PUBLIC_RECORD_AUDIT != POLICY_VERDICT
```

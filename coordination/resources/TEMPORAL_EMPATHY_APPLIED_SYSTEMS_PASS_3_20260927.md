# Temporal empathy — applied operating-system pass 3

Date: 27 September 2026

Status: **WORLD / REAL USE / FINANCE + ENERGY / CONFORMANCE REFINEMENT / NO TRACE OR ME PATCH**

Purpose:

Pressure the temporal-safeguard conformance audit against two additional domains:

1. mandatory APP-scam reimbursement;
2. involuntary prepayment-meter protections.

Working audit:
coordination/resources/TEMPORAL_SAFEGUARD_CONFORMANCE_AUDIT_v0_20260927.md

This pass asks whether the audit still helps once:
- the consumer-facing safeguard works well overall but a hidden inter-firm clock underperforms; and
- an initial eligibility/suitability check can become stale as vulnerability changes over time.

---

# Case 7 — APP scam reimbursement: front-stage protection can outperform back-stage settlement

Status: **STRONG REGULATORY OWNER / HIGH CONSUMER-FACING CONFORMANCE / BACK-END CLOCK RESIDUAL / NO NEW POLICY OBJECT**

## Strongest owner

Payment Systems Regulator (PSR).

Consumer protection surface:
https://www.psr.org.uk/information-for-consumers/app-fraud-reimbursement-protections/

Current dashboard:
https://www.psr.org.uk/information-for-consumers/app-scams-reimbursement-dashboard/

Recent independent-review summary:
https://www.psr.org.uk/news-and-updates/latest-news/news/payment-fraud-falls-by-73m-following-psr-reimbursement-scheme/

## Owner-defined temporal safeguards

For in-scope claims, current consumer protection includes:
- expected reimbursement within 5 business days;
- ability for firms to "stop the clock" where more information is required;
- final outcome within 35 business days;
- vulnerability protections, including no optional excess for vulnerable consumers;
- mandatory cross-firm reimbursement cost sharing.

Current dashboard data covering the first 18 months of the policy reports:
- 88% (£316m) of money lost in reimbursable claims returned to victims;
- around 438,300 claims reported, around 301,500 reimbursable;
- 82% of claims closed within 5 business days;
- 98% closed within 35 business days;
- 3% rejected for insufficient customer caution over the 18-month period.

The dashboard also carries important evidence ceilings:
- data are based on reported/closed Faster Payments claims in scope;
- data accuracy/completeness depend on what sending firms report;
- receiving-firm data do not independently validate all dashboard information.

## Back-stage clock

PSR also has a separate inter-firm Reimbursable Contribution Amount (RCA) process.

PSR reported that between October 2024 and June 2025:
- more than £74m was reimbursed to sending firms by receiving firms;
- only 67% of receiving firms paid the contribution within the five-day limit.

PSR notes possible causes including payment/reconciliation difficulty and incorrect reference numbers.

This is a different clock from the consumer reimbursement clock.

## Conformance reading

The tempting collapse would be:

~~~text
BACK-END FIVE-DAY CLOCK MISSED
-> CONSUMER PROTECTION FAILED
~~~

The public data do not establish that.

Consumer-facing reimbursement remained mostly prompt even while the inter-firm contribution clock performed less well.

Preserve:

~~~text
CONSUMER PROTECTION CLOCK
!=
INTER-FIRM SETTLEMENT CLOCK

BACK-STAGE NONCONFORMANCE
!=
FRONT-STAGE HARM BY DEFAULT

FRONT-STAGE SUCCESS
!=
BACK-STAGE PROCESS HEALTH
~~~

The hidden process still matters because:
- it distributes cost/responsibility between sending and receiving firms;
- it may affect incentives;
- reconciliation failures can create operational burden;
- persistent friction could eventually affect system resilience.

But effect on the consumer must be evidenced rather than inferred.

## Compact conformance profile

| Stage | Status on current public evidence | Note |
|---|---|---|
| SPECIFIED | **OBSERVED** | Consumer and inter-firm rules/clocks are explicit. |
| TRIGGERED | **OBSERVED / SCOPE-BOUND** | Reported in-scope claims activate the regime. |
| ROUTED | **OBSERVED / PARTIAL** | Consumer claim routing is operating; inter-firm information/reconciliation is not uniformly smooth. |
| CLOCK_STARTED | **OBSERVED** | Consumer five-/35-day clocks and inter-firm contribution clocks are explicit. |
| OWNER_ASSIGNED | **OBSERVED** | Sending and receiving firms have defined roles. |
| ACTED | **OBSERVED / PARTIAL** | Consumer outcomes are strong; back-stage contribution timeliness is weaker. |
| REACHED | **OBSERVED** | High reimbursement/timeliness at aggregate consumer level. |
| CURRENT | **OBSERVED / DATA-DEPENDENT** | Dashboard updated and revisions signposted; depends on firm reporting. |
| RESOLVED | **PARTIAL** | Reimbursement can resolve the monetary loss route; it does not mean fraud ecosystem/root cause resolved. |
| RESIDUE | **OBSERVED** | Remaining unreimbursed loss, rejected/out-of-scope claims, operational reconciliation burden. |

## Result

**OWNER FOUND / STRONG FRONT-STAGE CONFORMANCE / BACK-STAGE EXECUTION RESIDUAL / NO PROJECT POLICY OBJECT.**

Useful audit refinement:
record internal dependency clocks separately from affected-entity protection clocks.

---

# Case 8 — involuntary prepayment meters: one-time suitability is not enough

Status: **STRONG OFGEM OWNER / LARGE REMEDIATION HISTORY / ONGOING-CURRENTNESS PRESSURE / NO NEW POLICY OBJECT**

## Strongest owner

Ofgem.

Current consumer guidance:
https://www.ofgem.gov.uk/check-prepayment-meter-rules

2026 market compliance review:
https://www.ofgem.gov.uk/transparency-document/market-compliance-review-prepayment-meter-installations

2025 compensation / review closure:
https://www.ofgem.gov.uk/press-release/suppliers-commit-further-ps186million-customer-compensation-and-debt-write-following-ofgems-prepayment-meter-review

2026 OVO monitoring settlement:
https://www.ofgem.gov.uk/press-release/ovo-agrees-settlement-relation-ofgems-investigation-of-its-monitoring-of-prepayment-meter-customers

## Owner-defined safeguards

Current rules/guidance include:
- involuntary PPM only as a last resort;
- at least 10 contact attempts;
- a site welfare visit;
- restrictions/prohibitions for high-risk/vulnerable households;
- body/audio recording for specified visits/installations;
- £30 short-term credit/non-disconnection protection at installation/switch;
- requirement to assess whether a meter is safe/practicable;
- reassessment after debt is repaid;
- monitoring/reporting and compliance review.

The owner framework therefore already recognises:
- vulnerability;
- contact/notice;
- suitability;
- point-of-installation protection;
- later reassessment.

## Remediation / conformance evidence

### 2025 market review outcome

Ofgem reported:
- more than 150,000 involuntary-installation cases were covered by the market compliance review;
- at least 40,000 customers were due compensation/debt write-off from eight suppliers;
- issues included poor data quality, inadequate record keeping and unfair treatment;
- inappropriate PPM installation was estimated in fewer than 1% of reviewed cases;
- suppliers were required to audit, compensate/redress and provide regular monitoring data.

This is a mixed result:
the most serious installation failure was relatively limited in the reviewed population, but data/record/process defects affected many more customers.

### 2026 compliance review

Ofgem's June 2026 review reported:
- no widespread inappropriate installations;
- some cases where vulnerable customers were put at risk;
- suppliers contacted affected customers and provided compensation where appropriate;
- differences in supplier practices;
- strengthened rules intended to protect people needing extra help.

### 2026 OVO settlement

Ofgem also closed an investigation into OVO concerning inadequate monitoring of PPM customers, including Priority Services Register customers.

The regulator said those process failures could have put vulnerable consumers at risk.

The settlement included:
- £7m to Ofgem's Voluntary Redress Fund;
- £3.4m in credit/debt relief for some vulnerable customers.

This is especially important because it is about **monitoring after/around the PPM state**, not only the installation decision.

## Temporal structure

A shallow conformance audit might stop at:

~~~text
VULNERABILITY CHECKED BEFORE INSTALLATION?
~~~

That is insufficient.

Household circumstances can change.
Data can be incomplete.
Vulnerability can be missed initially.
A meter that was considered suitable at one point may become unsafe/inappropriate later.
Debt can be repaid.

Preserve:

~~~text
INITIAL SUITABILITY
!=
ONGOING SUITABILITY

VULNERABILITY RECORDED AT t0
!=
VULNERABILITY CURRENT AT t1

INSTALLATION COMPLIANT
!=
ONGOING MONITORING COMPLIANT

NO WIDESPREAD WRONGFUL INSTALLATION
!=
NO MATERIAL PROCESS HARM
~~~

## Compact conformance profile

| Stage | Status on current public evidence | Note |
|---|---|---|
| SPECIFIED | **OBSERVED** | Strong current rules/eligibility/safeguards. |
| TRIGGERED | **PARTIAL** | Contact/visit/vulnerability triggers exist; review history shows some vulnerability/currentness failures. |
| ROUTED | **PARTIAL** | Supplier practices differ; data/record quality has caused routing/support failures. |
| CLOCK_STARTED | **PARTIAL / DOMAIN-SPECIFIC** | Pre-installation sequence is defined; ongoing monitoring/reassessment depends on lifecycle state. |
| OWNER_ASSIGNED | **OBSERVED** | Supplier responsibility and regulator oversight are explicit. |
| ACTED | **PARTIAL** | Most reviewed installations not found widely inappropriate, but affected customers required redress. |
| REACHED | **PARTIAL** | Some vulnerable customers did not receive intended protection. |
| CURRENT | **PARTIAL / IMPORTANT FAILURE MODE** | Ongoing monitoring and vulnerability currentness remain material. |
| RESOLVED | **PARTIAL** | Compensation/debt relief/return options address some harms; not all process failures imply full restoration. |
| RESIDUE | **OBSERVED** | Vulnerability risk, debt, self-rationing/disconnection risk, process/data defects. |

## Result

**OWNER FOUND / STRONG RULE SET / CURRENTNESS + MONITORING CONFORMANCE REMAINS MATERIAL / NO NEW POLICY OBJECT.**

Useful audit refinement:
separate initial gate conformance from lifecycle/currentness conformance.

---

# Cross-case refinement

These two domains add two new non-entailments to the conformance layer.

## A. Front-stage versus back-stage clocks

~~~text
AFFECTED-ENTITY PROTECTION CLOCK
!=
INTERNAL DEPENDENCY / SETTLEMENT CLOCK

INTERNAL CLOCK MISSED
!=
AFFECTED ENTITY HARMED BY DEFAULT

AFFECTED ENTITY PROTECTED
!=
INTERNAL PROCESS HEALTHY
~~~

This matters where one actor temporarily absorbs a back-stage failure so the affected entity still receives protection.

## B. Gate conformance versus lifecycle conformance

~~~text
SAFE AT ENTRY
!=
SAFE LATER

SUITABLE AT t0
!=
SUITABLE AT t1

ELIGIBILITY / VULNERABILITY CHECK
!=
ONGOING CURRENTNESS
~~~

A one-time precondition check can be perfectly executed and still become stale.

## Relation to existing TRACE / ME

TRACE already has:
- multiple clocks;
- typed entities/roles;
- currentness;
- burden transfer;
- trigger fired versus present;
- route usability.

ME already carries:
- time-varying life state;
- slow harm;
- burden placement;
- correction and residue.

So again:

~~~text
NEW WORLD PRESSURE
!=
NEW CORE PRIMITIVE
~~~

Current disposition:

**CONFORMANCE AUDIT REFINED / OWNER-DERIVED / FINANCE + ENERGY ADDED / NO VALIDATION / NO TRACE OR ME PATCH.**

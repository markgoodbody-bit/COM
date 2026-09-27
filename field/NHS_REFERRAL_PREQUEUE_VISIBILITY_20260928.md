# NHS referral pre-queue visibility — hidden-waiting field pressure

Date: 28 September 2026

Status: **FRESH WORLD / HEALTH-ACCESS PRESSURE / STRONG NHS + HEALTHWATCH OWNERS / PRE-QUEUE MEASUREMENT GAP / NO TRACE OR ME PATCH**

Primary owner/public sources:
- NHS England, 2026/27 NHS Standard Contract and current elective-access/e-Referral guidance:
  https://www.england.nhs.uk/nhs-standard-%20contract/
  https://www.england.nhs.uk/long-read/national-elective-access-policy/
  https://digital.nhs.uk/services/e-referral-service/document-library/referring-a-patient
- UK Parliament written answer 4407, answered 15 June 2026:
  https://questions-statements.parliament.uk/written-questions/detail/2026-05-29/4407
- Healthwatch England, Referrals: improving experiences and closing “black holes”, 8 December 2025:
  https://www.healthwatch.co.uk/report/2025-12-08/referrals-improving-experiences-and-closing-black-holes
- BMA e-Referral guidance:
  https://www.bma.org.uk/advice-and-support/nhs-delivery-and-workforce/primary-and-secondary-care/nhs-e-referral-service-for-secondary-care-doctors

## World pressure

Referral-to-treatment waiting-list measures begin only after specific pathway/clock-start conditions are met.

That makes **queue entry itself** a consequential transition.

A person can have an unresolved specialist-care need while a referral is delayed, lost, returned, rejected, never sent, or otherwise not yet represented on the downstream waiting list.

Healthwatch England's 2025 nationally representative survey of 2,622 adults with a referral experience reported that 14% experienced a referral "black hole" — delayed, lost, rejected or not sent — and that 71% of that group only discovered they had not joined a specialist waiting list after chasing NHS teams themselves.

This is patient-experience evidence, not an administrative prevalence estimate.

The June 2026 Parliamentary answer supplies a separate administrative boundary. Between July 2024 and May 2026, 37,815,595 referrals were received through e-RS; 407,757 (1.1%) were assessed by the receiving clinician as not clinically appropriate for the booked service and returned to the referrer for further action. The same answer states that the Department does not centrally hold the proportion rejected on administrative grounds or due to capacity constraints, and had not assessed the impact of rejected referrals on reported waiting-list figures.

Do not collapse these evidence families.

~~~text
HEALTHWATCH REFERRAL BLACK HOLE
!=
NHS E-RS CLINICALLY-INAPPROPRIATE RETURN RATE

1.1% E-RS RETURN RATE
!=
TOTAL FAILED / DELAYED / LOST / UNSENT REFERRALS

SURVEY EXPERIENCE
!=
ADMINISTRATIVE POPULATION COUNT
~~~

## Strong-owner controls already exist

NHS England and e-RS guidance already own substantial routing semantics:

- clinically appropriate referrals should be accepted under the applicable contract/choice rules;
- an inappropriate destination can be redirected to a more appropriate service;
- rejected referrals return to the referrer's worklist for action;
- providers should not reject referrals merely because of capacity constraints;
- e-RS retains route/worklist state and audit information;
- RTT clock-start rules define when the formal treatment pathway begins.

Therefore this is **not** evidence that the NHS lacks routing rules, clocks, audit trails or correction mechanisms.

It is pressure on what a downstream metric can see.

Preserve:

~~~text
REFERRED
!=
ACCEPTED INTO THE DOWNSTREAM PATHWAY

RETURNED TO REFERRER
!=
ALTERNATIVE CARE REACHED

NOT ON THE WAITING LIST
!=
NO UNRESOLVED NEED

WAITING-LIST SIZE
!=
ALL PEOPLE WAITING FOR A ROUTE TO CARE

POLICY PROHIBITS CAPACITY REJECTION
!=
CAPACITY-RELATED ROUTE FAILURE IMPOSSIBLE

ROUTE STATE OMITTED FROM A METRIC
!=
ROUTE STATE ABSENT FROM THE SYSTEM
~~~

## Why this matters to the current never-built-door quarry

The labour case showed an entry route narrowing without a layoff event.

This health case is structurally different.

The person may already have a clinician-recognised need and an attempted referral, but the measurement aperture can begin **after** the consequential route transition.

~~~text
LABOUR CASE
FEWER ENTRY ROUTES
-> PERSON MAY NEVER ENTER THE EMPLOYMENT EVENT STREAM

REFERRAL CASE
ATTEMPTED ROUTE FAILS / RETURNS BEFORE DOWNSTREAM QUEUE ENTRY
-> PERSON MAY NEVER ENTER THE WAITING-LIST EVENT STREAM
~~~

The common structure is not "hidden harm" in the abstract.

It is narrower:

~~~text
OBSERVATION STARTS AFTER A GATE
+
SOME CONSEQUENTIAL FAILURES OCCUR BEFORE THAT GATE
->
DOWNSTREAM THROUGHPUT CAN UNDERSTATE UPSTREAM UNMET ROUTE PRESSURE
~~~

## Stronger-owner subtraction

Healthcare already has stronger concepts and methods for this family, including:
- unmet healthcare need;
- referral management and e-RS state;
- hidden waiting / referral-black-hole patient experience;
- RTT pathway and clock rules;
- access and demand measurement.

The project should not invent a health-system metric or estimate an unobserved national denominator from the sources above.

The surviving contribution, if any, is only cross-domain salience:

**Before treating a queue/throughput metric as the whole affected population, ask which consequential route states occur before entry into that metric.**

## TRACE / Mechanical Ethics result

Existing TRACE can already represent:
- stage/gate transitions;
- absence and target-set omission;
- route state;
- owner and authority;
- evidence-state uncertainty;
- clocks;
- affected population versus observed population.

Mechanical Ethics already carries the unfinished never-built-door pressure and correction-before-hardening concerns.

No representational defect is demonstrated.

~~~text
TRACE PATCH = NO
ME PATCH = NO
HEALTH METRIC INVENTION = NO
VALIDATION CLAIM = NO
~~~

## Current disposition

**REAL PRE-QUEUE VISIBILITY PRESSURE / STRONG HEALTH OWNERS / DOWNSTREAM QUEUE != TOTAL UNMET ROUTE PRESSURE / CROSS-DOMAIN COMPRESSION PLAUSIBLE / NO TRACE-ME PATCH.**

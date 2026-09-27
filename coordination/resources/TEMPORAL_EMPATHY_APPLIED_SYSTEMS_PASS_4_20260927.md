# Temporal empathy — applied operating-system pass 4

Date: 27 September 2026

Status: **WORLD / REAL USE / DATA PROTECTION + RAIL ACCESSIBILITY / OWNER-FOUND CONTROLS / NO AUDIT GROWTH / NO TRACE OR ME PATCH**

Purpose:

Pressure the temporal-safeguard conformance audit against two further domains without assuming every new case should expand the audit:

1. personal-data breach response;
2. rail Passenger Assist.

Working audit:
coordination/resources/TEMPORAL_SAFEGUARD_CONFORMANCE_AUDIT_v0_20260927.md

Result:

Both stronger owners already expose the relevant temporal structure clearly enough that no new audit dimension is earned.

---

# Case 9 — personal-data breach response: event time, awareness time and reporting time are already separated

Status: **STRONG ICO OWNER / POSITIVE CONTROL / NO NEW AUDIT DIMENSION**

## Strongest owner

Information Commissioner's Office (ICO).

Primary guidance:
https://ico.org.uk/for-organisations/report-a-breach/personal-data-breach/personal-data-breaches-a-guide/

72-hour operational guide:
https://ico.org.uk/for-organisations/advice-for-small-organisations/personal-data-breaches/72-hours-how-to-respond-to-a-personal-data-breach/

Current reporting surface:
https://ico.org.uk/pdb

Examples:
https://ico.org.uk/for-organisations/report-a-breach/personal-data-breach/personal-data-breach-examples/

## Owner-defined temporal structure

Current ICO guidance already distinguishes:
- the time the breach/event occurred;
- the time the organisation became aware of it;
- the 72-hour notification clock;
- later phased updates as investigation develops;
- separate "without undue delay" notification to affected individuals where high risk exists;
- containment/mitigation happening in parallel with reporting;
- continuing records even for breaches not reported to the ICO.

The small-business guide states that the notification timer starts from discovery/awareness, not from the historical event time.

Current guidance also explicitly says:
- do not wait for every fact before reporting a reportable breach;
- report what is known within the applicable window and update later;
- later information can change the risk assessment and reporting decision;
- organisations should document the developing situation and why a previously non-reportable breach became reportable.

This is a strong owner expression of:

~~~text
EVENT TIME
!=
AWARENESS TIME
!=
REGULATORY REPORTING CLOCK

INCOMPLETE INFORMATION
!=
PERMISSION TO WAIT FOR COMPLETE INFORMATION

INITIAL RISK ASSESSMENT
!=
PERMANENT RISK ASSESSMENT
~~~

## Conformance implications

A useful audit reading is already fully representable:

~~~text
BREACH OCCURRED
-> WHEN DID REASONABLE AWARENESS ARISE?
-> WAS RISK ASSESSED?
-> WAS CONTAINMENT STARTED?
-> DID THE 72-HOUR CLOCK FIRE WHERE REQUIRED?
-> WAS THE ICO NOTIFIED / UPDATED?
-> DID HIGH-RISK INDIVIDUAL NOTIFICATION FIRE?
-> DID NEW INFORMATION REOPEN THE ASSESSMENT?
~~~

No new conformance field is needed.

## Important positive-control lesson

The owner guidance explicitly rejects a common temporal failure:

~~~text
"WE DO NOT KNOW EVERYTHING YET"
!=
"THE REPORTING CLOCK HAS NOT STARTED"
~~~

That is close to Mechanical Ethics' Strategic Unknown and TRACE's uncertainty neutrality, but the detailed method belongs to data-protection law/governance.

## Evidence ceiling

ICO incident-trend dashboards show reported breach patterns, not a complete population of all breaches or direct proof that every controller complied with the 72-hour rule.

The dashboard itself documents categorisation/data limitations.

Preserve:

~~~text
REPORTED INCIDENT DATA
!=
ALL INCIDENTS

DASHBOARD TREND
!=
CONFORMANCE RATE
~~~

## Result

**OWNER FOUND / POSITIVE CONTROL / EVENT-AWARENESS-REPORTING TIME ALREADY WELL OWNED / NO AUDIT GROWTH.**

---

# Case 10 — rail Passenger Assist: booked route can fail at execution time

Status: **STRONG ORR OWNER / REAL DELIVERY GAP / OWNER ALREADY BENCHMARKING + TIGHTENING REDRESS / NO NEW AUDIT DIMENSION**

## Strongest owner

Office of Rail and Road (ORR).

Accessible Travel Policy:
https://www.orr.gov.uk/monitoring-regulation/rail/passengers/passenger-assistance/atp

Passenger assistance:
https://www.orr.gov.uk/monitoring-regulation/rail/passengers/passenger-assistance/passengers-disabilities

2025-26 annual rail consumer report:
https://www.orr.gov.uk/annual-rail-consumer-report-2025-2026/accessible-travel

Current passenger-assistance data:
https://dataportal.orr.gov.uk/statistics/passenger-accessibility/passenger-assistance/

## Owner-defined temporal/access structure

Current Accessible Travel Policy requirements include:
- no more than two hours' notice for advance Passenger Assist bookings;
- assistance at relevant stations during train service hours when booked;
- turn-up-and-go assistance where reasonably practicable;
- handover arrangements between boarding/alighting stations;
- up-to-date accessibility information;
- ramps and other delivery requirements;
- arrangements for journeys that do not go as planned;
- alternative accessible transport in relevant circumstances.

The October 2025 ATP Guidance also requires operators to assess redress case-by-case when booked assistance is not provided.

ORR launched a 2026 consultation on a fairer redress framework; the consultation closed 11 September 2026 and was not treated here as a final adopted framework.

## Current delivery evidence

For April 2025 to March 2026 ORR reports:
- about 1.9 million pre-booked passenger assists requested;
- at least 1.5 million unbooked/turn-up-and-go assists requested;
- more than 10,000 passengers participated in the booked-assistance survey;
- 94% satisfaction among passengers who received assistance at a station;
- 10% reported receiving none of the assistance they booked.

ORR also says its confidence in prior industry-reported assistance-outcome data was low enough that it changed reporting requirements from April 2025 and continues work to improve consistent failure reporting.

This gives two separate evidence surfaces:
- passenger-experience survey;
- operator/staff outcome reporting.

## Conformance reading

The key non-entailment is obvious:

~~~text
ASSISTANCE BOOKED
!=
ASSISTANCE DELIVERED

BOOKING CONFIRMED
!=
EXECUTION CAPACITY PRESENT AT THE RIGHT PLACE/TIME

HIGH SATISFACTION WHEN DELIVERED
!=
HIGH RELIABILITY OF DELIVERY
~~~

The failure is highly temporal:
a missed assist at boarding/alighting can harden immediately into a missed train, unsafe transfer, stranded passenger or disrupted journey.

Later redress may matter, but:

~~~text
REDRESS AFTER FAILED ASSISTANCE
!=
ORIGINAL JOURNEY RESTORED
~~~

This is already within the audit's:
- action ordered versus action completed;
- protection reached;
- outcome/residue;
- evidence verification;
- parallel-route/fallback handling.

No new audit field is needed.

## Data-quality lesson

ORR's own low-confidence judgement on older industry outcome data reinforces the audit's evidence/custody layer:

~~~text
OPERATOR-REPORTED DELIVERY
!=
PASSENGER-EXPERIENCED DELIVERY

REPORTING SYSTEM IMPROVED
!=
SERVICE RELIABILITY ALREADY IMPROVED
~~~

Again, no new primitive.

## Owner trajectory

ORR is already:
- benchmarking operators;
- targeting poorer-performing operators with action plans;
- revising reporting categories;
- requiring case-by-case redress for failed booked assistance;
- considering a more structured redress framework.

Therefore:

**OWNER ACTIVE / REAL DELIVERY GAP / NO PROJECT FEATURE REQUEST.**

## Result

**STRONG OWNER / EXECUTION GAP OBSERVED / AUDIT ALREADY REPRESENTS IT / NO AUDIT GROWTH.**

---

# Cross-case result

These two domains are useful because they do **not** grow the conformance audit.

Data protection confirms:
- event / awareness / reporting clocks;
- phased action under uncertainty;
- reassessment on new information.

Rail accessibility confirms:
- promise/booking versus execution;
- affected-entity delivery versus operator reporting;
- redress versus restoration.

All are already present in the current audit.

Preserve:

~~~text
NEW DOMAIN
!=
NEW FIELD REQUIRED

AUDIT STABILITY UNDER NEW CASES
CAN BE
EVIDENCE OF SATURATION
~~~

Current disposition:

**TWO OWNER-FOUND CONTROLS / NO AUDIT GROWTH / NO TRACE OR ME PATCH / SATURATION REVIEW EARNED.**

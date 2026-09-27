# Temporal empathy — applied operating-system intervention pass

Date: 27 September 2026

Status: **WORLD / REAL USE APPLICATION / PUBLIC OWNER SOURCES / MIXED RESULT / NO TRACE OR ME PATCH**

Purpose:

Apply the temporal-empathy design pattern library to real operating systems rather than continue abstract development.

Method:

~~~text
WORLD / REAL USE
-> STRONGEST OWNER
-> EXISTING TEMPORAL PROTECTIONS
-> SPECIFIC CONSEQUENTIAL RESIDUE
-> SMALLEST HELP
-> KILL / ROUTE CONDITION
~~~

Source pattern library:
coordination/resources/TEMPORAL_EMPATHY_DESIGN_PATTERNS_20260927.md

This pass deliberately permits:

OWNER FOUND / NO DELTA / STOP

as a successful result.

---

## Case 1 — NHS referral handoffs: patient-visible positive states, weaker negative-transition visibility

Status: **CURRENT PARTIAL REPAIR OBSERVED / NARROW RESIDUAL / SMALL HELP CANDIDATE**

### World evidence

Parliamentary and Health Service Ombudsman, 9 July 2026:

https://www.ombudsman.org.uk/news-and-blog/news/gaps-nhs-dentistry-and-confusion-about-care-left-patients-unnecessary-pain

Public summary reports:
- one woman waited eight years for treatment for broken teeth after falling into a gap between local dental and hospital services;
- another patient remained in severe pain for over a year after faulty root-canal work and failed appropriate follow-up;
- PHSO described confusion about who was responsible for patients receiving needed treatment.

This establishes a real handoff/ownership failure class. It does not establish that the NHS e-Referral Service caused either case.

### Stronger current owner

NHS e-Referral Service (e-RS):

https://digital.nhs.uk/services/e-referral-service

Current system already carries substantial ownership/state machinery:
- referrer/provider worklists;
- referral status;
- accept / reject / redirect / return pathways;
- audit history;
- provider responsibility for subsequent booking in RAS routes;
- referrer responsibility for acting on returned/rejected referrals.

Relevant guidance:
- https://digital.nhs.uk/services/e-referral-service/document-library/referring-a-patient
- https://digital.nhs.uk/services/e-referral-service/document-library/referral-assessment-services
- https://digital.nhs.uk/services/e-referral-service/document-library/supporting-clinical-referral-pathways

### Current September 2026 temporal improvement

e-RS Release 16.8, 11 September 2026:

https://digital.nhs.uk/services/e-referral-service/live-service-information-and-alerts/2026-releases/release-16.8---11-september-2026

The release added patient notifications when:
- a referral is being processed;
- a referral has been accepted.

It also states that the expected response timeframe for routine referrals reduces to 20 working days.

NHS App referral-message guidance further states:
- messages are intended to improve visibility while waiting;
- acceptance does **not** mean an appointment has been booked;
- patients do **not** currently receive these messages for referrals made outside e-RS;
- patients do **not** receive a referral message for rejected referrals.

Owner surface:
https://digital.nhs.uk/services/nhs-app/nhs-app-features/notifications-and-messaging-in-the-nhs-app

This is a real positive temporal-design intervention:

~~~text
BACKEND STATE EXISTS
->
PATIENT RECEIVES PROCESSING / ACCEPTED STATE
->
LESS NEED TO SELF-POLL
~~~

### Residual

A narrow residual remains on the public surface:

~~~text
POSITIVE STATE VISIBLE
!=
ALL CONSEQUENTIAL TRANSITIONS VISIBLE
~~~

In particular, rejected referrals are not covered by the new patient referral notifications.

Joint e-RS guidance already assigns action back to the referrer and includes a later patient-contact backstop if a practice does not contact the patient.

So the gap is **not** "nobody owns rejected referrals."

The narrower question is:

> can the patient receive a bounded responsibility/next-action receipt for a negative transition without adding unsafe clinical detail or conflicting communication?

### Smallest-help candidate

**Negative-transition responsibility receipt**

When a referral is returned/rejected/redirected in a pathway where this is safe and appropriate, provide the patient with a bounded message containing only:

- the referral state changed;
- whether the referral remains active;
- which organisation now has the next action;
- whether the patient needs to do anything now;
- an expected contact/check window;
- a fallback contact if that window passes.

Do **not** surface clinical rejection reasoning unless the responsible clinical owner says it is appropriate.

This builds on current notification infrastructure rather than proposing another platform.

### Burden movement

Desired:

~~~text
PATIENT CHASING MULTIPLE SERVICES
->
SYSTEM NAMES CURRENT ACTION HOLDER
~~~

Avoid:

~~~text
MORE NOTIFICATIONS
->
MORE CONFUSION / DUPLICATE CONTACT
~~~

### Kill / route condition

**OWNER FOUND / NO DELTA** if current e-RS/local dental pathways already provide reliable, patient-visible negative-transition ownership and next-action timing across the relevant referral class.

**STOP / DOMAIN OWNER** if clinical-safety, confidentiality or pathway-specific reasons make automated patient notification inappropriate.

No claim that this solves dental capacity shortages or all cross-provider care gaps.

---

## Case 2 — EHC plan delay: protect the child's present while the plan/appeal clock stalls

Status: **REAL CURRENT SCALE PRESSURE / SPECIFIC SMALL WORKFLOW CANDIDATE / LEGAL-EDUCATION OWNER REQUIRED**

### World evidence

Current Department for Education statistics for England:

https://explore-education-statistics.service.gov.uk/find-statistics/education-health-and-care-plans/2026

For plans issued during 2025, the published statistics state:
- 46.1% of new EHC plans were issued within the statutory 20-week timeframe, excluding specified exceptions;
- 43.5% were issued between 20 and 52 weeks;
- 10.3% were issued more than a year after the request;
- mean issue time was 24.0 weeks, excluding exceptions.

The statutory/public process says the whole assessment/plan-development process should normally take no more than 20 weeks.

### Concrete prior case

LGSCO Bromley 22 016 360:

https://www.lgo.org.uk/decisions/education/special-educational-needs/22-016-360

The Ombudsman found:
- the council took too long to produce the EHC plan;
- it did not properly consider alternative education;
- the parent's right of appeal was delayed;
- the child missed education.

The remedy included apology, payment for lost education and staff guidance/training.

### Stronger owners

Current public owner surfaces:
- GOV.UK EHC-plan process / 20-week timing;
- SEND Tribunal route;
- Education Act 1996 section 19;
- DfE alternative-provision / children-missing-education guidance;
- LGSCO case law/guidance.

Section 19 requires local authorities to arrange suitable education for compulsory-school-age children who would otherwise not receive suitable education because of illness, exclusion or other reasons, subject to the legal conditions.

Current statutory guidance says time out of suitable education should be kept to an absolute minimum.

### Temporal structure

The key interaction is not merely:

PLAN LATE.

It can be:

~~~text
PLAN LATE
-> APPEAL START DELAYED
+ CHILD'S EDUCATION CLOCK CONTINUES
+ POSSIBLE ALTERNATIVE-PROVISION DUTY EXISTS IN PARALLEL
~~~

The later plan can still matter, but it does not recreate missed education.

### Smallest-help candidate

**20-week breach preservation checkpoint**

If an EHC-plan process crosses the statutory 20-week point without a final plan, the case-management workflow could automatically require a bounded checkpoint recording:

1. why the plan remains unresolved;
2. a named current owner;
3. next expected decision/review date;
4. whether the child is currently receiving suitable education;
5. if not, whether the existing section-19 / alternative-provision route has been considered by the legally responsible team;
6. which outstanding evidence/action belongs to the authority versus parent/young person;
7. whether the affected family needs to do anything before the next check.

Design principle:

~~~text
PLAN DELAY
SHOULD NOT SILENTLY BECOME
EDUCATION-PROTECTION DELAY
~~~

The checkpoint does **not**:
- decide eligibility;
- create a tribunal appeal right before the law provides one;
- decide what alternative provision is suitable;
- replace professional/legal judgement.

It is a trigger to ensure already-distinct clocks/duties are not collapsed.

### Why this may be smaller than the problem

It does not attempt to solve SEND capacity, staffing or national plan delays.

It asks only that once the headline clock is breached, the system explicitly re-check the **current child's trajectory** rather than treating "EHCP still in progress" as the whole state.

### Kill / route condition

**OWNER FOUND / NO DELTA** if current local-authority case systems already reliably trigger this exact cross-check at breach and evidence shows the real failure lies elsewhere.

**LEGAL OWNER REQUIRED** before treating this as operational guidance; section-19 application is fact-sensitive.

This is a candidate workflow design pattern, not legal advice.

---

## Case 3 — LGSCO complaint waiting: many temporal-empathy patterns already implemented

Status: **OWNER FOUND / NO MATERIAL DELTA / POSITIVE CONTROL**

### Current operating system

LGSCO current waiting times, updated June 2026:

https://www.lgo.org.uk/make-a-complaint/current-waiting-times

The service publicly exposes three separate waiting stages:
- intake: up to 3 weeks before contact on most complaints;
- assessment: up to 6 months before contact on most complaints;
- investigation: up to 5 months before a decision on most complaints.

The page explicitly says each stage has its own waiting time and the wait starts again at each stage.

### Process transparency

"How we deal with your complaint":

https://www.lgo.org.uk/make-a-complaint/how-we-deal-with-your-complaint

The public process:
- explains what each stage does;
- explains possible next transitions;
- says the service will tell complainants what is happening and what to expect;
- invites requests for extra support.

LGSCO's complaint-handler guidance also says an acknowledgement should include an estimated investigation timescale.

### Pattern comparison

Our intervention library contains:
- make waiting visible;
- make next state/process legible;
- give expected timing;
- ask about additional support.

Those are already strong parts of the owner's public operating design.

Therefore:

~~~text
PATTERN MATCH
!=
OUR GAP
~~~

### Residual not earned

There may still be individual cases where:
- another legal/benefit/housing clock keeps running while the Ombudsman waits;
- a complainant does not understand whether they must act elsewhere.

But the current public surface is insufficient to claim a general design defect.

### Result

**OWNER FOUND / NO DELTA.**

Keep LGSCO as a positive control demonstrating that an institution can make waiting stages and expectations explicit without pretending the wait is short.

Do not manufacture a new feature request from this pass.

---

## Case 4 — Seattle Secure Scheduling: temporal burden changed by altering the operating rules

Status: **STRONG POSITIVE CONTROL / EXTERNALLY EVALUATED INTERVENTION / NOT UNIVERSAL**

### Operating intervention

Seattle's Secure Scheduling Ordinance took effect in 2017 for specified large retail and food-service employers.

City Auditor surface:
https://seattle.gov/city-auditor/reports

Published evaluation:
https://pmc.ncbi.nlm.nih.gov/articles/PMC8545454/

The intervention included temporal rules such as:
- advance schedule notice;
- predictability pay for certain schedule changes;
- constraints/extra pay around closely spaced closing/opening shifts.

### Evaluation result

The published natural-experiment analysis reports that the ordinance:
- increased schedule predictability;
- reduced some last-minute change conditions;
- was associated with improved subjective well-being;
- improved reported sleep quality;
- reduced material hardship.

The authors also report that compliance was not universal.

### Why this matters to our design work

This is stronger than a philosophical argument that unpredictability "feels unfair."

It shows an operating-system intervention that changed:
- advance notice;
- cost placement for schedule changes;
- recovery spacing;

and measured downstream worker outcomes.

Useful pattern:

~~~text
ORGANISATION NEEDS FLEXIBILITY
!=
ALL TEMPORAL RISK MUST SIT WITH WORKER
~~~

### Project consequence

No new pattern is needed.

It supports the owner-routed library's distinction:

~~~text
OPERATOR FLEXIBILITY
!=
AFFECTED-PERSON TEMPORAL AGENCY
~~~

and demonstrates that temporal design can be implemented at rule/process level, not only interface level.

### Ceiling

Do not infer:
- the same policy is appropriate in other jurisdictions/sectors;
- every reported outcome was caused by one provision;
- schedule predictability solves low pay or all job-quality problems;
- the intervention fully eliminated unstable scheduling.

Disposition:
**POSITIVE CONTROL / STRONGER OWNER / ABSORB.**

---

# Cross-case result

The four cases produce a useful mixed pattern:

| Case | Existing owner strength | Residual | Smallest-help result |
|---|---|---|---|
| NHS e-RS / referral handoffs | strong and improving | negative-transition patient visibility / responsibility continuity may remain uneven | bounded responsibility receipt — **candidate** |
| EHC-plan delay | strong legal/process owner but current timeliness pressure is large | child trajectory can continue degrading while plan/appeal waits | 20-week preservation checkpoint — **candidate / legal-owner validation needed** |
| LGSCO complaint waits | strong temporal transparency already | no general residual established | **NO DELTA / STOP** |
| Seattle secure scheduling | implemented + evaluated | not our gap | **POSITIVE CONTROL / ABSORB** |

This is more useful than a general claim that "systems should respect people's time."

## Reusable applied question

~~~text
WHAT TEMPORAL PROTECTION ALREADY EXISTS?

WHAT IS STILL FALLING BETWEEN CLOCKS?

CAN THE SMALLEST HELP:
- REMOVE WORK,
- NAME THE ACTION HOLDER,
- MAKE THE NEXT CHECK VISIBLE,
- PROTECT A PARALLEL ROUTE,
- OR MOVE TEMPORAL RISK TOWARD THE ACTOR WITH MORE CAPACITY?

WHAT WOULD SHOW THAT THE OWNER ALREADY SOLVED IT?
~~~

## Current project disposition

No TRACE/ME source patch is earned.

Two candidate intervention objects survive:
1. referral negative-transition responsibility receipt;
2. EHC 20-week preservation checkpoint.

Neither should be presented as owner-approved or deployed.

Two control cases show the correct STOP behaviour:
- LGSCO already implements much of the pattern;
- Seattle already owns and has evaluated a substantive schedule-predictability intervention.

~~~text
TEMPORAL EMPATHY
-> NOT JUST NOTICE
-> LOOK FOR SMALLEST OWNER-COMPATIBLE CHANGE
-> ALLOW NO DELTA
~~~

Current disposition:

**APPLIED VALUE PLAUSIBLE / TWO NARROW CANDIDATES / TWO OWNER-FOUND CONTROLS / NO FRAMEWORK PATCH.**

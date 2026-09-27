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

## Case 2 — EHC process and current education: stronger owner cuts the 20-week-only trigger

Status: **STRONGER OWNER FOUND / PRIMARY 20-WEEK TRIGGER SUPERSEDED / EVENT-TRIGGERED PARALLEL-CLOCK PATTERN SURVIVES**

### National/current pressure

Department for Education 2026 statistics for plans issued during 2025 report:
- 46.1% within the ordinary 20-week timeframe, excluding specified exceptions;
- 43.5% between 20 and 52 weeks;
- 10.3% more than a year after the request;
- mean issue time 24.0 weeks, excluding exceptions.

Owner:
https://explore-education-statistics.service.gov.uk/find-statistics/education-health-and-care-plans/2026

This establishes material timeliness pressure. It does not establish the same failure mechanism in every local authority or every delayed case.

### Earlier project candidate — cut back

The first pass proposed a **20-week temporal preservation checkpoint** joining:
- EHC process state;
- current education state;
- parallel protection route;
- current action holder;
- next check.

That was too plan-centric.

Recent Ombudsman owner cases show that the current-education / alternative-provision question may need to arise **well before** the ordinary 20-week EHC horizon, when a council becomes aware that a child may not be receiving suitable education, and it must remain live as circumstances change.

The old paper object is preserved as historical v0 and superseded by:
`coordination/resources/TEMPORAL_CANDIDATE_EHC_PARALLEL_CLOCK_v1_20260927.md`

### Stronger-owner evidence

#### Essex County Council 24 018 461 — 12 August 2025

https://www.lgo.org.uk/decisions/education/alternative-provision/24-018-461

Public findings include:
- an EHC request later recorded that the child was not attending full-time;
- the Council said it considered its alternative-education duty then;
- the Ombudsman found the Council should have become aware earlier when another council team was contacted about attendance;
- which council team held the information was not an adequate answer: relevant information should propagate internally;
- the Council failed to keep the alternative provision under review;
- when circumstances changed and provision broke down, later action followed after additional delay.

The decision/service-improvement actions also reinforce:
- current-state review;
- internal communication;
- front-line escalation when a child is not attending full-time.

#### Shropshire Council 25 002 787 — 3 March 2026

https://www.lgo.org.uk/decisions/education/alternative-provision/25-002-787

The Ombudsman found fault because the Council failed to decide whether alternative provision was needed when it became aware the child was out of school.

The Ombudsman did **not** find resulting educational injustice from that particular failure because the school had put appropriate support in place.

This usefully preserves:

~~~text
PROCESS FAILURE
!=
PROOF OF LOST EDUCATION IN EVERY CASE
~~~

#### Gloucestershire — positive and negative controls

Current LGSCO decisions/service-improvement records show:
- cases where suitable alternative provision was put in place despite separate EHC-process faults;
- cases requiring clearer recorded reasons for section-19 decisions;
- requirements to review part-time provision / oversight;
- improvement work around internal responsibility and communication.

Owner:
https://www.lgo.org.uk/your-councils-performance/gloucestershire-county-council/serviceimprovements?category=1015&year=2025

### Revised smallest pattern

**Parallel-clock preservation**

Potential owner-defined triggers include:
- any relevant council team receives credible information that a child is not attending or may not be receiving suitable education;
- EHC assessment material records reduced/absent attendance;
- current provision changes or breaks down;
- a scheduled review point arrives;
- the ordinary 20-week EHC horizon is crossed as a currentness backstop.

At a valid trigger, support the legally responsible owner to establish/record:

~~~text
CURRENT EDUCATION STATE
+
WHETHER A PARALLEL PROTECTION ROUTE MUST BE CONSIDERED
+
DECISION / BASIS
+
WHO OWNS NEXT ACTION
+
WHEN THE ARRANGEMENT IS REVIEWED AGAIN
~~~

The pattern does **not** make the legal decision.

### Stronger-owner correction

The project should no longer claim:

> councils need a 20-week checkpoint to notice current education.

Stronger owners already require earlier awareness/action in relevant cases.

What the project may still contribute is a compact cross-clock routing reminder:

~~~text
EHC PROCESS CLOCK
!=
CURRENT EDUCATION CLOCK
!=
APPEAL / CORRECTION CLOCK

AND

CONSIDERED ONCE
!=
ADEQUATELY KEPT UNDER REVIEW
~~~

### Current result

**STRONGER OWNER FOUND / MECHANISM NOT NOVEL / CROSS-CLOCK COMPRESSION USEFUL / NO GENERAL LOCAL-AUTHORITY GAP ESTABLISHED.**

Do not contact councils or publish this as guidance from this pass.

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
| EHC process / current education | strong legal/education owner; recent Ombudsman cases already own early awareness + review | exact cross-clock join/compression may aid salience, but general absence is not established | **OWNER-DERIVED PARALLEL-CLOCK PATTERN / NO NOVELTY CLAIM** |
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

One narrow patient-facing referral paper object survives provisionally, while the EHC candidate has been **substantially owner-subtracted**:
1. referral negative-transition responsibility receipt — preserve/watch while e-RS's September notification rollout beds in;
2. EHC parallel-clock preservation v1 — owner-derived compression of existing expectations, not a novel intervention.

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

**APPLIED VALUE PLAUSIBLE / ONE NARROW WATCH CANDIDATE / ONE OWNER-DERIVED CROSS-CLOCK COMPRESSION / TWO OWNER-FOUND CONTROLS / NO FRAMEWORK PATCH.**

# National Commission on AI in Healthcare — lifecycle-authorisation addendum

Date: 27 September 2026

Status: **INCREMENTAL OWNER-CURRENTNESS ADDENDUM / PRIOR OWNER NOTE EXISTS / NOT A NEW WORLD WITNESS / NO TRACE OR ME PATCH**

Prior project note:
`evidence/NHS_AI_REGULATION_OWNER_CURRENTNESS_20260918.md`

Primary owner:
National Commission into the Regulation of AI in Healthcare, *Recommendations for a future regulatory framework*, 10 September 2026.

https://www.gov.uk/government/publications/national-commission-into-the-regulation-of-ai-in-healthcare-recommendations-for-a-future-regulatory-framework/national-commission-into-the-regulation-of-ai-in-healthcare-recommendations-for-a-future-regulatory-framework

## Duplicate correction

The 18 September owner/currentness note already captured:
- responsibility should follow practical ability to act;
- escalation on performance degradation before a conventional reportable incident;
- evidence/redress after AI-mediated harm;
- reporting as a learning/correction loop;
- strong healthcare regulatory owners;
- no TRACE/ME source change.

Therefore those points are **not new findings here**.

## Narrow incremental residue

The Commission also makes a lifecycle-authorisation point that the earlier note did not foreground.

It recommends:
- staged deployment/authorisation pathways where appropriate;
- clear communication that staged deployment is staged/conditional;
- real-world evidence during deployment;
- post-market surveillance and studies;
- ongoing performance reporting;
- temporary staged status with a route toward full authorisation.

The useful compression is:

~~~text
AUTHORISED AT t0
!=
CURRENTLY SUPPORTED AT t1

STAGED DEPLOYMENT
!=
FULL AUTHORISATION

REAL-WORLD USE
CAN GENERATE EVIDENCE
WITHOUT
BECOMING SELF-VALIDATING
~~~

A device can have a valid historical authorisation state while the current claim about safety/performance still depends on:
- deployment setting;
- patient population;
- software/model version;
- new failure modes;
- post-market evidence;
- unresolved uncertainty.

## TRACE relation

This is already representable in TRACE v0.4.0:

~~~text
RETAINED_RECORD != CURRENT_STATE
SUCCESS_AT_t != SUCCESS_AT_t+1
DATE_CURRENT != DERIVED_VALUE_CURRENT
CURRENT_AT_USE != VALID_THROUGH_DEPENDENT_INTERVAL
~~~

So:

~~~text
LIFECYCLE AUTHORISATION PRESSURE
!=
NEW CURRENTNESS PRIMITIVE
~~~

The Commission is the stronger healthcare-regulatory owner.

## Practical owner-routed question

For a consequential deployed AI-enabled device:

> What evidence makes the current safety/performance claim valid for this version, setting and population now, and what change would force re-evaluation?

This routes outward to regulatory/clinical owners.

## Boundaries

Do not infer:
- the Commission recommendations are already enacted regulation;
- staged deployment applies to every healthcare AI;
- every AI healthcare tool is a regulated medical device;
- historical authorisation becomes invalid merely because time passed;
- post-market surveillance guarantees safety;
- this addendum validates TRACE or Mechanical Ethics.

## Current disposition

**PRIOR OWNER NOTE CONFIRMED / NARROW LIFECYCLE-AUTHORISATION ADDENDUM / CURRENT TRACE REPRESENTATION SURVIVES / NO PATCH / NO HOT-STATE GROWTH REQUIRED.**

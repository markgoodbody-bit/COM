# Temporal safeguard conformance audit v0

Date: 27 September 2026

Status: **WORKING CROSS-DOMAIN AUDIT / OWNER-DERIVED / NOT CANON / NOT VALIDATED / NO TRACE OR ME PATCH**

Purpose:

Check whether a temporal protection that already exists in policy, workflow, law, guidance or system design actually fired in the world.

This is not a new theory of time and not a replacement for domain audit, law, clinical governance, human factors or operational assurance.

It is a small cross-domain routing surface.

## Core problem

Real systems often fail after the safeguard has already been designed.

Preserve:

~~~text
SAFEGUARD SPECIFIED
!=
SAFEGUARD FIRED

TRIGGER DEFINED
!=
TRIGGER CAPTURED

CLOCK DEFINED
!=
CLOCK STARTED CORRECTLY

ROUTE EXISTS
!=
ROUTE WORKED WHEN NEEDED

ACTION RECORDED
!=
ACTION REACHED THE AFFECTED ENTITY

COMPLIANCE STEP COMPLETED
!=
UNDERLYING PROBLEM DURABLY RESOLVED
~~~

## Conformance chain

For one protection/safeguard, ask whether the chain survived:

~~~text
SPECIFIED
-> TRIGGER OBSERVED
-> TRIGGER ROUTED
-> CLOCK STARTED
-> OWNER ASSIGNED
-> ACTION TAKEN
-> PROTECTION REACHED
-> STATE RECHECKED
-> MATERIAL CHANGE RE-TRIGGERED
-> OUTCOME / RESIDUE OBSERVED
~~~

Do not assume later stages from earlier ones.

## 1. Strongest owner / safeguard source

What stronger owner defines the protection?

Record:
- source / version / date;
- population / scope;
- trigger conditions;
- required/expected response;
- exceptions;
- evidence requirements.

If the rule is domain-specific, keep the domain owner primary.

## 2. Trigger reach

What events can activate the safeguard?

Ask:
- what counts as notice / trigger?
- through which channels can it arrive?
- can another team, contractor, carer, system or record create relevant knowledge?
- is "ought to have known" relevant in the domain?
- are non-standard channels silently discarded?

~~~text
TRIGGER EXISTS IN WORLD
!=
TRIGGER ENTERED THE WORKFLOW
~~~

## 3. Trigger capture and currentness

Was the trigger recorded with enough fidelity to act?

Check:
- timestamp;
- source;
- affected scope;
- relevant circumstances;
- uncertainty;
- vulnerability / risk information where lawful and appropriate;
- whether later material change updates the state.

~~~text
OLD ASSESSMENT
!=
CURRENT STATE
~~~

## 4. Classification / triage

Did the system classify the trigger using the right criteria?

Ask:
- was severity/priority assessed?
- was the decision recorded?
- was uncertainty exposed?
- did a default category silently suppress action?
- is professional judgement required?

Do not replace domain judgement with this audit.

## 5. Clock start

Which clock actually starts, and when?

Record separately where material:
- detection / notice;
- assessment;
- action / make-safe;
- response;
- review;
- appeal/correction;
- hardening / affected-entity consequence.

~~~text
ONE EVENT
CAN START
MULTIPLE CLOCKS
~~~

Do not collapse them.

## 6. Current action holder

Who now owns the next act?

Ask:
- named person, role, team or organisation?
- authority to act?
- capability/resources to act?
- fallback if unavailable?
- is ownership visible to the affected entity where appropriate?

~~~text
CASE HAS OWNER
!=
OWNER CAN ACT
~~~

## 7. Safeguard enactment

Did the required protection actually happen?

Distinguish:
- instruction issued;
- appointment/repair/review booked;
- action attempted;
- action completed;
- affected entity reached;
- protection effective.

~~~text
ACTION ORDERED
!=
ACTION COMPLETED

ACTION COMPLETED
!=
PROTECTION EFFECTIVE
~~~

## 8. Parallel clocks / routes

What else is happening while this process runs?

Examples:
- complaint + repair;
- plan + current education;
- PIFU + fixed clinical surveillance;
- investigation + hazard exposure;
- appeal + income/housing/health consequence.

Ask whether one process incorrectly pauses or hides another.

~~~text
PROCESS A OPEN
!=
PROCESS B CAN WAIT
~~~

## 9. Affected-entity workload and access

What must the person/entity now do?

Count:
- remember;
- monitor;
- recognise a trigger;
- contact;
- repeat evidence;
- attend;
- coordinate;
- wait;
- recover;
- chase.

Ask:
- what support/cue exists?
- what fallback exists?
- can the burden be moved to the actor with more capacity?
- can the person return to a more supported route?

~~~text
AGENCY
!=
UNSUPPORTED RESPONSIBILITY
~~~

## 10. Review / re-trigger

Is the decision still current?

Ask:
- when is it reviewed again?
- what material change should reopen it?
- who notices the change?
- what if the first intervention fails?
- what if conditions worsen?

~~~text
CONSIDERED ONCE
!=
ADEQUATELY KEPT UNDER REVIEW
~~~

## 11. Outcome / durable resolution

What happened after the compliance step?

Do not stop at:
- response sent;
- inspection done;
- referral accepted;
- plan issued;
- complaint closed.

Ask:
- did the underlying problem resolve?
- did the affected entity receive the intended protection?
- did the issue recur?
- what residue remains?
- did another burden appear elsewhere?

~~~text
TIMESCALE MET
!=
DURABLE RESOLUTION
~~~

## 12. Burden transfer / system externalities

Did the protection improve one metric by moving burden elsewhere?

Examples:
- patient monitoring -> primary care/admin burden;
- urgent compliance -> planned maintenance displaced;
- automated notification -> attention overload;
- operator flexibility -> affected-person unpredictability.

~~~text
LOCAL PERFORMANCE IMPROVED
!=
TOTAL BURDEN REDUCED
~~~

## Compact status notation

For a safeguard (S), use words rather than a synthetic score:

~~~text
SPECIFIED
TRIGGERED
ROUTED
CLOCK_STARTED
OWNER_ASSIGNED
ACTED
REACHED
CURRENT
RESOLVED
RESIDUE
~~~

Each can be:
- OBSERVED;
- PARTIAL;
- UNKNOWN;
- NOT_APPLICABLE;
- FAILED.

Do not sum these into one "temporal empathy score".

## Result routes

~~~text
RULE MISSING
-> DESIGN / POLICY OWNER

RULE PRESENT, TRIGGER FAILS
-> INGRESS / OBSERVABILITY / ROUTING OWNER

TRIGGER ROUTED, ACTION FAILS
-> AUTHORITY / CAPABILITY / OPERATIONS OWNER

ACTION HAPPENS, PROTECTION DOES NOT REACH
-> DELIVERY / ACCESS / IMPLEMENTATION OWNER

PROTECTION REACHES, STATE CHANGES
-> CURRENTNESS / REVIEW OWNER

TIMESCALE MET, PROBLEM PERSISTS
-> OUTCOME / ROOT-CAUSE OWNER

EVERYTHING ALREADY WORKS
-> OWNER FOUND / NO DELTA
~~~

## Relation to TRACE / Mechanical Ethics

TRACE v0.4.0 already carries:
- trigger-present versus trigger-fired discipline;
- WAIT / DELAY / INACTION transitions;
- clocks;
- route usability;
- capability / authority;
- hardening;
- burden;
- currentness / evidence state;
- residue.

Mechanical Ethics v0.8.0 already carries:
- strategic uncertainty;
- slow harm;
- clock control;
- burden placement;
- usable routes;
- correction-before-hardening;
- later repair / residue.

Therefore:

~~~text
CONFORMANCE AUDIT
!=
NEW TRACE ONTOLOGY

CONFORMANCE AUDIT
!=
NEW ME ETHICAL RULE
~~~

Candidate value is operational salience across domains.

## Falsifier

Delete or demote this audit if:
- domain owners already provide an equally compact audit that transfers without loss;
- the cross-domain layer increases burden without changing observation/routing;
- it encourages checkbox compliance rather than outcome checking;
- it hides domain-specific trigger/clock meanings;
- users treat PARTIAL/UNKNOWN as a scalar verdict.

Current disposition:

**WORKING AUDIT / OWNER-DERIVED / USE ON PUBLIC CASES / NO VALIDATION CLAIM.**

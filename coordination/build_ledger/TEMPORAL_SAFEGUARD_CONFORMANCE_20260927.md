# Temporal empathy — safeguard conformance pass

Date: 27 September 2026

Status: **WORLD / REAL USE / CONFORMANCE LAYER SURVIVES BOUNDED APPLICATION / NO VALIDATION / NO TRACE OR ME PATCH**

## Purpose

Continue temporal-empathy work without waiting for external readers by asking a harder operational question:

> when a temporal safeguard already exists, did it actually fire in the world?

## New working object

`coordination/resources/TEMPORAL_SAFEGUARD_CONFORMANCE_AUDIT_v0_20260927.md`

Core chain:

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

Primary distinctions:

~~~text
SAFEGUARD SPECIFIED != SAFEGUARD FIRED
CLOCK DEFINED != CLOCK STARTED CORRECTLY
ROUTE EXISTS != ROUTE WORKED WHEN NEEDED
ACTION RECORDED != PROTECTION REACHED
TIMESCALE MET != DURABLE RESOLUTION
DESIGN GAP != EXECUTION GAP
~~~

This is owner-derived and not a new TRACE/ME primitive.

## Applied pass 2

`coordination/resources/TEMPORAL_EMPATHY_APPLIED_SYSTEMS_PASS_2_20260927.md`

### NHS patient-initiated follow-up

Current NHS England guidance already contains strong safeguards:
- suitability / activation checks;
- shared decision making;
- carer involvement;
- blended timed + PIFU routes;
- return to traditional timed follow-up;
- tracking / review / end dates;
- reminders and multi-channel information;
- clinically required reviews and test review even without patient initiation;
- incident learning;
- local target wait times and urgent-access processes after activation.

A 2026 staff evaluation nevertheless reports materially variable implementation, administrative burden, some patients failing to initiate when needed, EPR workarounds, primary-care spillover and continued waits after some activations.

Result:

**OWNER FOUND / DESIGN GAP NOT EARNED / IMPLEMENTATION-FIDELITY + BURDEN-TRANSFER PRESSURE.**

### Awaab's Law Phase 1

Current law/guidance already contains:
- multi-channel notice / knowledge;
- investigation / make-safe / repair clocks;
- complaint and hazard clocks running concurrently;
- written summaries / ongoing updates;
- material-change re-triggering;
- temporary accommodation where relevant.

The 2026 MHCLG Test-and-Learn research reports early behavioural/accountability gains but uneven implementation:
- variable responsiveness;
- fragmented case handling;
- vulnerability not consistently recognised at first contact;
- missing written summaries;
- clock-trigger ambiguity;
- incomplete vulnerability data;
- IT/workforce/contractor capacity pressure;
- local workarounds;
- risk that evidencing compliance displaces durable root-cause resolution.

Result:

**OWNER FOUND / POLICY-THEORY GAP NOT EARNED / REAL EARLY CONFORMANCE GAP OBSERVED.**

## Method exercise

`coordination/resources/TEMPORAL_SAFEGUARD_CONFORMANCE_SAMPLE_READINGS_20260927.md`

The audit produced two bounded non-scalar profiles with different routing outcomes.

Preserve:

~~~text
TWO SYSTEM-LEVEL READINGS
!=
CROSS-DOMAIN VALIDATION
~~~

## Project consequence

Current TRACE already contains:
`DISTINCTION_PRESENT != DISTINCTION_APPLIED`
and
`TRIGGER_PRESENT != TRIGGER_FIRED`.

The new world cases make those distinctions operationally concrete rather than earning new semantics.

Current state:

~~~text
TEMPORAL-EMPATHY WORK = CONTINUE
CONFORMANCE LAYER = USEFUL / OWNER-DERIVED / UNVALIDATED
PIFU = STRONG OWNER / IMPLEMENTATION WATCH
AWAAB PHASE 1 = STRONG OWNER / EARLY CONFORMANCE GAP
TRACE PATCH = NO
ME PATCH = NO
EXTERNAL REVIEW = NOT REQUIRED TO CONTINUE
~~~

No external contact, health advice, legal advice, production change or framework release change follows.

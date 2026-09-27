# FCA vulnerable-payments review — support-state handoff witness

Date: 27 September 2026

Status: **FRESH WORLD / PAYMENTS ACCESS WITNESS / STRONG REGULATORY OWNER / NO TRACE OR ME PATCH**

Primary owner:
Financial Conduct Authority, *Payments firms: delivering good outcomes for consumers in vulnerable circumstances*, 17 September 2026.

https://www.fca.org.uk/publications/good-and-poor-practice/payments-firms-delivering-good-outcomes-vulnerable-consumers

Related prior world witness:
`field/CITIZENS_ADVICE_DIGITAL_CHANNEL_LOCK_20260927.md`

## Why this is different from channel lock alone

Citizens Advice's current cross-sector work identifies **channel lock**:

~~~text
ROUTE A EXISTS
+
ROUTE B EXISTS
!=
SWITCH A -> B IS USABLE
~~~

The FCA review adds a second failure surface:

the person may successfully move between channels while support-relevant information fails to move with them.

Current FCA findings include:
- stronger firms embedded identification of vulnerability across customer journeys, including online and automated channels;
- some firms used system flags to record relevant vulnerability/support information;
- some firms piloted language analysis in online chat and routed customers who may be in vulnerable circumstances to human agents;
- stronger firms tailored support across channels and communication formats;
- some firms could not consistently evidence how vulnerability information was recorded and shared across the customer journey;
- support was sometimes inconsistently delivered across the journey;
- in broader FCA vulnerability work, some consumers reported having to disclose their circumstances repeatedly when firms failed to use information already recorded.

This is owner evidence of a handoff problem with **state continuity**, not merely route availability.

## Structural pressure

Preserve:

~~~text
CHANNEL SWITCH AVAILABLE
!=
SUPPORT STATE SURVIVES THE SWITCH

SUPPORT NEED DISCLOSED ONCE
!=
NEXT CHANNEL KNOWS IT

CUSTOMER RECORD EXISTS
!=
FRONTLINE ACTOR USED THE RELEVANT STATE

HUMAN HANDOFF
!=
CONTEXT HANDOFF

REPEATED DISCLOSURE
!=
NEUTRAL FRICTION
~~~

The last distinction matters because repeating health, bereavement, financial, language, disability or other vulnerability information can itself add burden.

## Stronger-owner boundary

The FCA already owns the substantive requirement in financial services:
- firms should understand customer needs;
- identify vulnerability proportionately;
- provide appropriate support;
- deliver good outcomes;
- record/share relevant information consistently enough to support the journey;
- test that arrangements work in practice;
- comply with applicable data-protection requirements.

Therefore:

~~~text
SUPPORT-STATE CONTINUITY
!=
UNOWNED FINANCIAL-SERVICES GAP
~~~

The project should not invent a parallel financial-services standard.

## Privacy / data-minimisation guard

A naive "carry everything across channels" response would be wrong.

Support-state continuity must remain bounded by:
- lawful basis;
- data minimisation;
- purpose;
- sensitivity;
- currentness;
- the person's preferences where relevant;
- role-based access.

Preserve:

~~~text
CONTEXT CONTINUITY
!=
TOTAL PERSONAL-DATA PROPAGATION

SUPPORT NEED KNOWN
!=
EVERY ACTOR MAY INSPECT IT
~~~

## Smallest cross-domain design question

When a consequential handoff occurs:

> What minimum support-relevant state needs to survive the handoff so the affected person does not have to reconstruct the problem, and who is actually permitted to receive that state?

Candidate bounded fields, where the domain owner supports them:

~~~text
HANDOFF FROM
HANDOFF TO
CURRENT ISSUE / ROUTE STATE
ACTION ALREADY COMPLETED
NEXT ACTION HOLDER
NEXT CHECK / DEADLINE
SUPPORT NEED / ADJUSTMENT REQUIRED
SOURCE / CURRENTNESS
ACCESS / DISCLOSURE LIMIT
UNKNOWN / DO-NOT-CARRY
~~~

This is a design sketch, not a required schema.

## TRACE / ME pressure

TRACE already has:
- state;
- route;
- handoff;
- burden;
- custody/access;
- currentness;
- scope;
- route usability.

Mechanical Ethics already carries:
- usable routes;
- burden placement;
- privacy without dishonesty;
- complexity exported to the weaker party.

The FCA case does not establish a missing primitive.

It sharpens a use-site question:

~~~text
ROUTE HANDOFF
-> DID THE ACTION-RELEVANT STATE HAND OFF TOO?
~~~

## No overclaim

Do not infer:
- every payments firm loses vulnerability information at handoff;
- every support need should be stored permanently;
- automated vulnerability inference is reliable or always appropriate;
- a human agent should see all prior chatbot content;
- repeated disclosure is always avoidable;
- FCA findings establish the same duty in non-financial domains.

## Current disposition

**REAL IMPLEMENTATION WITNESS / CHANNEL + STATE HANDOFF BOTH MATTER / STRONG OWNER PRESENT / TRACE+ME REPRESENTATION SURVIVES / NO PATCH / NO OUTREACH.**

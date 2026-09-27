# Support-state handoff contract — paper sketch v0

Date: 27 September 2026

Status: **PAPER DESIGN SKETCH / OWNER-ROUTED / NOT CANON / NOT DEPLOYED**

World pressure:
- Citizens Advice channel-lock witness;
- FCA vulnerable-payments review;
- Public Accounts Committee cross-sector "tell us once" / vulnerable-consumer burden report.

Purpose:

Represent the smallest state that may need to survive a channel/team/organisation handoff so an affected person does not have to restart a consequential service journey from zero.

This is **not**:
- a universal customer profile;
- a universal living-person graph;
- a debt registry;
- a permission to propagate sensitive data;
- a claim that centralisation is the correct topology.

## Core object

~~~text
HANDOFF RECEIPT

from:
  <channel / role / service>

to:
  <channel / role / service>

current_issue:
  <bounded description>

current_route_state:
  <state | UNKNOWN>

completed_actions:
  <list>

next_action_holder:
  <role / service | UNKNOWN>

next_action:
  <action | UNKNOWN>

next_check_or_deadline:
  <time/window | UNKNOWN>

support_adjustment_needed:
  <minimum necessary support state | NONE | UNKNOWN>

support_state_source:
  <source / customer disclosure / verified record / UNKNOWN>

support_state_currentness:
  <timestamp / review basis | UNKNOWN>

disclosure_scope:
  <who may receive / use this information>

do_not_carry:
  <sensitive or irrelevant state explicitly excluded>
~~~

## Required discipline

~~~text
HANDOFF
!=
DUMP ENTIRE HISTORY

CONTEXT CONTINUITY
!=
UNBOUNDED MEMORY

MINIMUM SUPPORT STATE
!=
FULL PERSONAL PROFILE
~~~

Where the relevant owner does not support carrying a field:
omit it or mark it UNKNOWN.

## Cross-sector boundary

Cross-sector use makes the privacy/currentness problem stronger, not weaker.

Preserve:

~~~text
TELL US ONCE
!=
TELL EVERYONE EVERYTHING

PORTABLE SUPPORT STATE
!=
CENTRAL OWNERSHIP

SUPPORT NEED
!=
DEBT PROFILE

CONSENT / AUTHORITY AT t0
!=
PERMANENT AUTHORITY AT t1
~~~

For cross-organisation propagation, the stronger owner should additionally determine:
- lawful basis / consent where applicable;
- purpose;
- recipient scope;
- revocation/withdrawal semantics where applicable;
- retention/currentness period;
- correction propagation;
- provenance/source authority;
- whether a data intermediary / federated / direct-sharing architecture is safer than a central register.

The object should carry only the minimum action-relevant support state needed for the receiving route.

## Success question

Not:

> did the second channel receive data?

Instead:

> did the person reach the next legitimate step without avoidable re-explanation, unsafe disclosure, duplicated work or loss of the support adjustment?

## Kill conditions

Do not use this object if:
- the receiving actor has no lawful/legitimate need for the state;
- the domain already provides a stronger equivalent;
- the state is stale or unsupported;
- carrying it would create more privacy/security risk than burden reduction;
- the affected person explicitly wants a fresh/private interaction where the domain permits that;
- the handoff is not consequential.

Current disposition:

**PAPER SKETCH ONLY / STRONG OWNER MUST DEFINE ACTUAL FIELDS + ACCESS / NO IMPLEMENTATION.**

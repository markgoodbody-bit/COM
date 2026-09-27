# Support-state handoff contract — paper sketch v0

Date: 27 September 2026

Status: **OWNER-SUBTRACTED HANDOFF RECEIPT / NOT A PORTABLE PROFILE CLAIM / NOT CANON / NOT DEPLOYED**

World pressure:
- Citizens Advice channel-lock witness;
- FCA vulnerable-payments review;
- Public Accounts Committee cross-sector "tell us once" / vulnerable-consumer burden report.

Purpose:

Represent the smallest route/action receipt that may need to survive a consequential channel/team/organisation handoff, while referencing only the minimum support adjustment already justified by the stronger domain owner.

Communication Passports, the NHS Accessible Information Standard, NICE and portable-preference work already own substantial parts of portable support/preference state. See coordination/resources/SUPPORT_STATE_HANDOFF_STRONG_OWNER_MAP_20260927.md.

This object is therefore **not** a proposed general support profile.

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

support_adjustment_ref:
  <reference to owner-defined minimum support/communication adjustment | NONE | UNKNOWN>

support_adjustment_source:
  <owner record / person-held passport / supported source | UNKNOWN>

support_adjustment_currentness:
  <timestamp / review basis | UNKNOWN>

disclosure_scope:
  <who may receive / use this information>

do_not_carry:
  <sensitive or irrelevant state explicitly excluded>
~~~

## Required discipline

~~~text
HANDOFF RECEIPT
!=
PORTABLE PERSON PROFILE

ROUTE CONTINUITY
!=
DUMP ENTIRE HISTORY

CONTEXT CONTINUITY
!=
UNBOUNDED MEMORY

SUPPORT ADJUSTMENT REFERENCE
!=
FULL PERSONAL PROFILE

PROFILE CREATED
!=
PROFILE USED
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

The object should carry **route/action continuity** and only reference/carry the minimum support adjustment that the stronger owner says the receiving route legitimately needs.

Where a mature communication passport, accessibility flag, health passport or other owner-defined support record already exists, this receipt should point to/use that owner object rather than duplicate it.

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

**OWNER-SUBTRACTED PAPER HANDOFF RECEIPT / PORTABLE SUPPORT PROFILE OWNER FOUND / ROUTE+MINIMUM-SUPPORT JOIN ONLY / NO IMPLEMENTATION.**

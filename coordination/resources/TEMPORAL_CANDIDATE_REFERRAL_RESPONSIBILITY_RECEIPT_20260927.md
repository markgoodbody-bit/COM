# Candidate object — referral negative-transition responsibility receipt

Date: 27 September 2026

Status: **PAPER PROTOTYPE / OWNER-COMPATIBILITY TEST / NOT NHS GUIDANCE / NOT DEPLOYED**

Origin:
`coordination/resources/TEMPORAL_EMPATHY_APPLIED_SYSTEMS_PASS_20260927.md`

## Problem boundary

Current NHS e-RS already has:
- referral states;
- referrer/provider worklists;
- accept/reject/return/redirect handling;
- audit history;
- current 2026 patient notifications for "being processed" and "accepted" states.

Current NHS App guidance explicitly says referral notifications do not currently cover rejected referrals.

This prototype asks only whether a bounded patient-facing **responsibility receipt** could make a negative transition less temporally ambiguous.

It is not a proposal to expose clinical rejection reasoning automatically.

## Candidate receipt

~~~text
REFERRAL UPDATE

Your referral status has changed.

Referral remains active:
  YES | NO | UNKNOWN

Current next-action holder:
  <organisation / service | UNKNOWN>

What happens next:
  <bounded operational statement>

Do you need to do anything now?
  NO
  YES -> <action>
  UNKNOWN -> <contact>

Expected next contact/check:
  <date/window | UNKNOWN>

If you have not heard by then:
  <single fallback route>

Important:
  This message does not mean that an appointment has been booked.
  Clinical details/reasons are provided through the responsible clinical route where appropriate.
~~~

## Required source fields

A real implementation would need supported mappings for:

- referral identity;
- current referral state;
- whether the state means active/closed/unknown;
- current responsible organisation;
- patient action required;
- expected response/contact window;
- fallback route;
- timestamp/currentness;
- source system / local pathway;
- reasonable-adjustment / non-digital communication route.

Do not derive responsibility from status text alone unless the owner system defines that mapping.

## Fail-closed states

Use `UNKNOWN` rather than infer:

- current action holder;
- appointment status;
- clinical urgency;
- reason for rejection;
- patient action required;
- response deadline.

~~~text
STATUS KNOWN
!=
RESPONSIBILITY KNOWN

REFERRAL ACCEPTED
!=
APPOINTMENT BOOKED

REFERRAL REJECTED
!=
CARE NO LONGER NEEDED
~~~

## Temporal-empathy function

The object aims to reduce:

~~~text
"I KNOW SOMETHING CHANGED"
+
"I DON'T KNOW WHO NOW OWNS THE NEXT MOVE"
+
"I DON'T KNOW WHEN TO CHECK AGAIN"
~~~

without creating:

~~~text
MORE CLINICAL MESSAGING
+
MORE CONFLICTING INSTRUCTIONS
~~~

## Stronger-owner questions

Before any real use, NHS/e-RS/pathway owners would need to answer:

1. Which negative transitions are safe/appropriate to surface automatically?
2. Which service is accountable for patient contact after each transition?
3. What timing can be promised?
4. How should urgent deterioration be handled separately?
5. Which local/non-e-RS referral routes cannot support the receipt?
6. What reasonable-adjustment/non-digital fallback is required?
7. Would the receipt duplicate or conflict with existing provider communication?

## Kill conditions

Kill or route away if:

- current owner workflows already give this information reliably;
- the action holder cannot be determined safely;
- the notification would disclose inappropriate clinical information;
- the message could cause patients to delay seeking urgent care;
- local pathway variability makes a generic receipt misleading;
- notification burden/conflict exceeds chasing burden.

## Success evidence if ever tested

Not "patients liked it."

Look for:
- fewer status-chasing contacts;
- fewer orphaned/unactioned transitions;
- shorter time between negative transition and responsible action;
- fewer patients unsure which organisation to contact;
- no increase in unsafe misunderstanding;
- no increase in duplicate/conflicting messages.

Current disposition:

**SMALL REVERSIBLE PAPER OBJECT / DOMAIN OWNER REQUIRED / NO IMPLEMENTATION AUTHORITY.**

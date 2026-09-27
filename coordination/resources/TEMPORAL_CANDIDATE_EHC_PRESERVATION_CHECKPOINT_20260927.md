# Candidate object — EHC 20-week temporal preservation checkpoint

Date: 27 September 2026

Status: **PAPER PROTOTYPE / EDUCATION-LEGAL OWNER TEST / NOT LEGAL ADVICE / NOT DEPLOYED**

Origin:
`coordination/resources/TEMPORAL_EMPATHY_APPLIED_SYSTEMS_PASS_20260927.md`

## Terminology correction

Do **not** call every case beyond 20 weeks a legal/statutory breach.

Current DfE statistics and guidance provide exceptions to the ordinary 20-week timeframe in specified circumstances.

Therefore this object is called:

**20-week temporal preservation checkpoint**

The trigger is temporal, not a legal conclusion.

## Trigger

When an EHC needs-assessment / plan-development process remains unresolved at the 20-week horizon:

~~~text
20-WEEK HORIZON CROSSED
->
CHECK CURRENT CHILD / ROUTE STATE
~~~

This checkpoint does not decide whether an exception makes the timing lawful.

## Candidate checkpoint

~~~text
EHC TEMPORAL PRESERVATION CHECKPOINT

Request / process start:
  <date>

20-week horizon:
  <date>

Final plan / decision state:
  <state>

Statutory-exception status:
  YES | NO | UNKNOWN
  basis_ref: <if available>

Current case owner:
  <team / named role | UNKNOWN>

Next expected review/decision:
  <date/window | UNKNOWN>

CURRENT EDUCATION CHECK

Is the child currently receiving suitable education?
  YES | NO | UNKNOWN

Evidence/source:
  <supported source | UNKNOWN>

If NO or UNKNOWN:
  Has the legally responsible team considered whether a
  section-19 / alternative-provision duty or other parallel
  education-protection route is engaged?
    YES | NO | UNKNOWN

  This field records consideration/status only.
  It does not decide entitlement or suitability.

OUTSTANDING WORK

Authority-owned:
  <actions>

Parent / young-person-owned:
  <actions>

Other-owner:
  <actions>

Does the family need to do anything before the next check?
  NO | YES -> <action + deadline> | UNKNOWN

Next temporal check:
  <date/window>
~~~

## Core distinction

~~~text
EHC PROCESS UNRESOLVED
!=
CHILD'S CURRENT EDUCATION STATE UNKNOWN / IRRELEVANT
~~~

and:

~~~text
PLAN CLOCK
!=
EDUCATION-LOSS CLOCK
!=
APPEAL CLOCK
~~~

These clocks interact but should not be collapsed.

## Why 20 weeks?

Not because every case crossing 20 weeks is unlawful.

Because:
- it is the ordinary statutory/public horizon for the overall process;
- current national statistics use it as a timeliness boundary;
- crossing it is a reasonable moment to force a current-state reacquisition.

A stronger owner could choose a different operational trigger or additional earlier triggers.

## Burden discipline

The checkpoint should **not** automatically ask the family to resubmit information the authority already holds.

Before creating a new request:

> Who already possesses the evidence?

~~~text
TEMPORAL CHECKPOINT
!=
NEW EVIDENCE BURDEN BY DEFAULT
~~~

## Stronger-owner questions

Education/legal/process owners must decide:

1. What data is reliable enough to establish "currently receiving suitable education"?
2. Which team owns the section-19 consideration?
3. What exceptions affect the 20-week timeframe?
4. Which cases need an earlier trigger?
5. How should parent/young-person disagreement with the recorded education state be captured?
6. What safeguarding/escalation route applies where education absence is urgent?
7. Can this be integrated into existing case-management workflows without adding duplicative bureaucracy?

## Kill conditions

Kill or route away if:

- existing local workflows already reliably perform this cross-check;
- the checkpoint adds family burden without changing protection;
- available data cannot safely represent current education status;
- the trigger creates false reassurance;
- legal owners identify a different established mechanism that already solves the temporal coupling;
- implementation cost exceeds plausible benefit.

## Success evidence if ever tested

Measure:
- time from 20-week horizon to explicit current-education review;
- number of cases where a parallel protection route was newly surfaced;
- family chasing contacts;
- duplicated evidence requests;
- days without suitable education where owner evidence permits measurement;
- false escalation / unnecessary workload;
- staff workload.

Do not use:
- number of checkpoints completed
as the success metric by itself.

Current disposition:

**SMALL REVERSIBLE PAPER OBJECT / STRONGER EDUCATION-LEGAL OWNER REQUIRED / NO IMPLEMENTATION AUTHORITY.**

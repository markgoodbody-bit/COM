# Cold-read protocol for the one-address door

Status: **PRE-REGISTERED TEST / NOT A RESULT / NOT CANON / NOT VALIDATION**
Registered: 2026-09-07, before any cold read was run and before any domain was chosen.
Related: COM #108.

## Why this exists before the door does

#108 asks whether a fresh receiver can orient from one address. The build order
already names *cold reads by heterogeneous models* as the evidence. This file
fixes the prompt, the rubric and the decision rule **in advance**, for one
reason:

I scored the current READMEs against the seven discoveries twice. A keyword
matcher returned three negatives and **two of them were false** — it missed
`Agreement is elaboration, not validation` as an invitation to disagree, and
`a working experiment, not a truth oracle` as a status ceiling. Reading the
documents gave 6–7/7 where the matcher gave 5–6/7.

```text
A_SUBSTRING_IN_THE_TEXT != A_PROPERTY_OF_THE_DOCUMENT
THE_PROBE_MISSED_IT != THE_PAGE_LACKS_IT
```

An acceptance test built as a text checklist over the door's own bytes would
mis-score the door in both directions. So the scorer must be a reader, and the
correct answers must be written down before the reading happens — otherwise the
result is decided by whoever interprets it afterwards.

## Contamination rules

A run is void unless all of these hold.

- The model has **no project history** in its context: no COM thread, no prior
  session, no explanation of TRACE, ME, Campfire, middle-out or the Square.
- The model is **not told what the address is for**, or that a test is running.
- Only **one URL** is supplied. No second link is offered even if the model asks.
- The operator adds **no clarification** during the run. A question from the
  model is recorded as a result, not answered.
- The run is recorded verbatim, including a refusal or a failure to fetch.

An aperture that has worked on this project cannot be a subject. That includes
me. I can propose the test and I cannot sit it.

```text
I_COULD_ANSWER_THE_SEVEN != THE_PAGE_ANSWERED_THEM_FOR_ME
```

## The prompt, exactly

> Read <ONE_URL> and then tell me what you make of it. What is this, what is it
> for, what would you do next, and what would you not rely on it for?

Nothing else. The phrasing deliberately does not name the seven discoveries,
does not ask the model to evaluate a project, and does not imply that reading
further is expected.

## The seven, with the answers fixed in advance

A response scores `SUBSTANTIVE` on an item only if it conveys the recorded
answer in its own words without being asked the question. `PARTIAL` if it gestures
at it. `ABSENT` if unmentioned. `WRONG` if it asserts the opposite.

```text
1  PURPOSE
   Examining consequential decisions under uncertainty, where a route can exist
   formally while being unusable in practice, and where correction can arrive
   after the harm has hardened.

2  ORIENTATION
   Middle-out / campfire: the work starts from a live situation rather than from
   a theory or a taxonomy, and the project is a fire people gather at rather than
   a standard being issued.

3  WHERE THINGS LIVE
   TRACE and Mechanical Ethics are separate repositories with their own entry
   documents; a compact spine is the normal entry point for TRACE rather than the
   full reference.

4  CEILINGS
   Release candidate, not released, not canon, not validated, no efficacy result.
   Does not confer authority, permission, clearance or moral standing.

5  NEIGHBOURS
   Other methods may own parts of this better; FPF is named as a neighbour, a
   comparison found no TRACE-unique semantic primitives, and using a stronger
   existing method instead is an acceptable outcome.

6  SELECTIVE INSPECTION
   The reader can go deeper on one part without reading everything, and the full
   reference is explicitly not required for a first reading.

7  DISAGREE OR STOP
   Criticism is invited through a named route; redundancy, false precision,
   excessive burden and no-material-difference are valid findings; agreement is
   elaboration rather than validation.
```

Item 2 is the one currently absent from the TRACE and ME READMEs. It is included
so the baseline run can confirm that absence rather than assume it.

## Predictions, registered before the first run

Mine, so they can be wrong in public:

```text
TRACE README, cold model      6/7 substantive, item 2 ABSENT
ME README, cold model         6/7 substantive, item 2 ABSENT
```

I hold these at low confidence for one specific reason: **I scored those
documents as someone who has read this project for weeks.** A reader who already
knows the answers cannot tell whether a page supplied them or merely reminded
them. If a cold model returns 3/7 on TRACE, my `BUILD_SMALLER` position is
weakened and the door needs real content after all.

## Decision rule, fixed now

```text
>= 5/7 on an existing README
    the door's job is discoverability, join and item 2 only. Do not write a
    fourth explanatory document.

3-4/7
    the door needs genuine content, and the argument that the READMEs already
    orient a stranger is refuted.

<= 2/7, or the model does not fetch at all
    the failure is retrieval rather than writing. Fix the fetch path before
    touching any wording.
```

At least three heterogeneous models, run independently, no shared context. A
single run decides nothing.

## What a null looks like

If cold models score the current READMEs and a built door the same, the door has
added discoverability and nothing else. **That is still a real result and a
sufficient reason to build it** — nobody can guess a raw GitHub URL — but it must
be recorded as a routing win rather than an orientation one.

```text
FOUND_THE_DOOR != UNDERSTOOD_THE_ROOM
```

## What this test cannot establish

That orientation causes anything. A model reporting that it understands the
project is not evidence that the project is useful, correct, or worth adopting.
This measures retrieval and comprehension at one address, and nothing beyond it.

No TRACE or ME content may be changed to make this test pass. If a document is
edited in response to a cold read, the prior runs are void and the protocol
restarts.

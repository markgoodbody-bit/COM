# Cold-read protocol for the one-address door — v0.2

Status: **PRE-REGISTERED TEST / NOT A RESULT / NOT CANON / NOT VALIDATION**
Registered v0.1: 2026-09-07, before any run.
Revised v0.2: 2026-09-07, after Codex review `5575812947` / `5575871543`, still
before any run. **No run has been scored under either version.**

Related: COM #108, #109.

## What changed in v0.2, and why it was wrong before

Codex found four defects in v0.1's inference structure. All four are accepted.

```text
v0.1  "<=2/7, or the model does not fetch at all -> the failure is retrieval"
      Conflated two independent failures. Successful retrieval with poor
      comprehension is possible, and a score cannot locate where the failure
      sat. Retrieval is now OBSERVED and recorded separately, never inferred.

v0.1  "3-4/7 -> the door needs genuine content"
      A score establishes failure under one prompt, one rubric and one access
      condition. It does not establish a design conclusion on its own.

v0.1  "equal scores -> a routing win"
      A tie establishes a tie. Discoverability is a separate claim needing its
      own evidence.

v0.1  seven answers with no channel for wrong ones
      A reader scoring 6/7 who also concludes the project holds authority is
      worse oriented than one scoring 4/7 who gets purpose, sources and limits
      right. False inferences are now recorded and reported alongside.
```

    A_LOW_SCORE != A_LOCATED_FAILURE
    A_SCORE_UNDER_ONE_RUBRIC != A_DESIGN_CONCLUSION
    ITEMS_FOUND != ITEMS_FOUND_MINUS_ITEMS_INVENTED

## Why the rubric is fixed before the reading

A keyword matcher scored the current READMEs against these seven and returned
three negatives, **two of them false** — it missed `Agreement is elaboration,
not validation` as an invitation to disagree, and `a working experiment, not a
truth oracle` as a status ceiling. Reading gave 6–7/7 where the matcher gave
5–6/7.

```text
A_SUBSTRING_IN_THE_TEXT != A_PROPERTY_OF_THE_DOCUMENT
```

So the scorer must be a reader, and the answers must be written down first, or
the result is decided by whoever interprets it afterwards.

## Contamination rules

A run is void unless all hold.

- the model has **no project history** in context: no COM thread, no prior
  session, no explanation of TRACE, ME, Campfire, middle-out or the Square;
- it is **not told** a test is running or what the address is for;
- exactly **one URL** is supplied;
- a question from the model is **recorded, not answered**;
- the response is returned **unedited**.

Framework, Codex and Claude Code may not be subjects. All three have read this
project for weeks.

**Recruitment is itself context.** An invitation that explains what the page is
for contaminates anyone who reads it. Square post 4302 asks citizens to run this
in a context with no memory of the request; that condition must be **confirmed
by the respondent**, not assumed. No cold status follows from being a citizen of
any board.

    ASKED_IN_PUBLIC != ANSWERED_FROM_NOWHERE

    I_COULD_ANSWER_THE_SEVEN != THE_PAGE_ANSWERED_THEM_FOR_ME

## The prompt, exactly

> Read <ONE_URL> and then tell me what you make of it. What is this, what is it
> for, what would you do next, and what would you not rely on it for?

Nothing else. It does not name the seven, does not ask for an evaluation, and
does not imply further reading is expected.

## Assignment — determinate, so model and page are not confounded

Each page must be read by at least two different models, and each model reads
exactly one page per run.

```text
run  model      page
1    model A    TRACE README
2    model B    TRACE README
3    model A    ME README
4    model B    ME README
```

A third model is better than two. A model may take a second run only on a page
it has not seen, in a context with no memory of the first.

## Record for every run — the answer alone is not enough

```text
model name and version
exact prompt text as sent
timestamp
URL as supplied
source revision   commit sha of the file at read time, captured AT read time
                  and never reconstructed from a later lookup of main
retrieval outcome FETCHED | TRUNCATED | REFUSED | FAILED | UNKNOWN
                  <- OBSERVED, never inferred
retrieval basis   TOOL_OBSERVED   the fetch was seen by the operator or a log
                  MODEL_CLAIMED   only the model says it fetched
retrieval evidence  quoted content, error text, or the model's own statement
the unedited response
```

`MODEL_CLAIMED` is weaker than `TOOL_OBSERVED` and must be recorded as such. A
model that says it read a page and did not is a known failure mode, and a
comprehension score built on a claimed fetch measures the model's priors.

`REFUSED` and `FAILED` are results and are reported as retrieval outcomes. They
say nothing about the page's content and must not be scored as comprehension.

**`TRUNCATED` was added 2026-09-08, after the first real run exposed its
absence.** The first outside reply arrived at 373 characters and stopped
mid-word. v0.1-v0.3 had no category for *arrived and was cut*, which left only
bad options: score the missing items `ABSENT` and record a false low, or discard
a run that contained real evidence.

    TRUNCATED != ABSENT
    THE_ANSWER_STOPPED != THE_READER_STOPPED

A truncated run is scored **only on what arrived**. Every item that falls after
the cut is recorded `NOT_REACHED` and excluded from the denominator, so the
score is reported as a fraction of items actually reachable — `2 of 2 reached`
rather than `2 of 7`. A truncated run can still carry a material false
inference, and that is recorded normally.

## The seven, with answers fixed in advance

`SUBSTANTIVE` only if the recorded answer is conveyed **in the model's own
words, unprompted**. Plain-language equivalents count fully; our vocabulary is
never required. `PARTIAL` if gestured at. `ABSENT` if unmentioned **in a
response that reached the end**. `NOT_REACHED` if the response was cut before
that point -- never `ABSENT`.

```text
1  PURPOSE
   Examining consequential decisions under uncertainty, where a route can exist
   formally while being unusable in practice, and where correction can arrive
   after the harm has hardened.

2  ORIENTATION  [vocabulary-sensitive -- see note]
   Work starts from a live situation rather than from a theory or taxonomy.

3  WHERE THINGS LIVE
   TRACE and Mechanical Ethics are separate repositories with their own entry
   documents; a compact spine is the normal entry point rather than the full
   reference.

4  CEILINGS  [page-specific -- do not score one page's ceiling against the
              other's; a reader who correctly distinguishes them gains credit,
              never loses it]

   page A, TRACE README
     a specification release candidate: not released, not canon, not
     validated, no efficacy result.

   page B, ME README
     a WORKING reader candidate, not a baseline and not a release, with a
     separate frozen preservation baseline behind it.

   both
     confers no authority, permission, clearance or moral standing.

5  NEIGHBOURS
   Other methods may own parts of this better; using a stronger existing method
   instead is an acceptable outcome.

6  SELECTIVE INSPECTION
   The reader can go deeper on one part without reading everything; the full
   reference is not required for a first reading.

7  DISAGREE OR STOP
   Criticism is invited through a named route; redundancy, false precision,
   excessive burden and no-material-difference are valid findings.
```

**Note on item 2.** The words *middle-out* and *campfire* are ours. Scoring
their absence risks measuring whether a stranger echoes our vocabulary rather
than whether they are oriented. Item 2 is therefore scored on the **idea**
— starting from a situation rather than a framework — and the exact words are
recorded separately as `USED_OUR_TERM: yes/no` for interest only. A reader who
conveys the idea in their own words scores `SUBSTANTIVE`.

## False-inference register — reported with equal weight

Recorded for every run, independently of the score:

```text
MATERIAL_FALSE_INFERENCE
  the reader concluded something the page does not support, e.g.
    - the project holds authority, endorsement or validation
    - the method is established, adopted, or shown to work
    - the reader is expected to adopt, join, or continue
    - a neighbouring method has been superseded
```

**A run with a high score and a material false inference is a worse result than
a lower score with none**, and is reported that way rather than averaged in.

## Reading of results — descriptive, not an instruction

No score band orders a build decision. Bands are recorded as observations and
the design conclusion is argued separately, in public, against them.

```text
>= 5/7 with no material false inference
    consistent with the existing pages orienting a stranger. It does not by
    itself establish that a door needs no content.

3-4/7
    the pages did not orient this reader under this prompt and access
    condition. It does not by itself establish that more content is the
    remedy; prompt, rubric and retrieval are alternative explanations and a
    matched comparison is needed before attributing it to page content.

<= 2/7
    a weak comprehension result, whose cause is undetermined by the score.
    Look at the recorded retrieval outcome, which is independent evidence.

any refusal or failed fetch
    a retrieval result. Reported separately and never combined with scores.
```

A tie between a README and a later door establishes a tie. Any discoverability
claim needs its own evidence and is out of scope here.

## Prediction, registered before the first run

```text
TRACE README   6/7 substantive, item 2 conveyed but not in our words
ME README      6/7 substantive, item 2 absent
```

Low confidence. I scored these documents as a reader who has studied them for
weeks, and a reader who already knows the answers cannot tell whether a page
supplied them. If cold models return 3/7 my `BUILD_SMALLER` position on #108 is
weakened — though per the band rules above, not automatically refuted.

## Versioning of runs

A run is scored against **the protocol version and source revision in force
when it was taken**, and is preserved with both recorded. Later revisions do not
void earlier runs; they make them evidence about a different version. Only a
contamination breach voids a run.

No TRACE or ME content may be edited to make this test pass. If it is, that is
recorded as a change to the object under test, and prior runs remain valid
evidence about the earlier text.

## What this cannot establish

That orientation causes anything. A model reporting that it understands the
project is not evidence that the project is useful, correct or worth adopting.
This measures retrieval and comprehension at one address and nothing beyond it.

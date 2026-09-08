# Cold-read protocol for the one-address door — v0.7

Status: **PRE-REGISTERED TEST / NOT A RESULT / NOT CANON / NOT VALIDATION**

| version | date | what forced it |
|---|---|---|
| v0.1 | 2026-09-07 | registered before the door existed |
| v0.2 | 2026-09-07 | four inference defects — Codex `5575812947` / `5575871543` |
| v0.3 | 2026-09-07 | ceiling scope, prompt capture, TOOL_OBSERVED vs MODEL_CLAIMED — Codex |
| v0.4 | 2026-09-07 | the first real reply arrived cut mid-word: TRUNCATED / NOT_REACHED |
| v0.5 | 2026-09-07 | an admission gate, after I scored a run that did not qualify |
| v0.6 | 2026-09-08 | venue separation, after the recruitment thread unblinded itself |
| v0.7 | 2026-09-08 | scope: what this does **not** claim about returning readers |

**One run has been scored and withdrawn.** It was inadmissible — I held none of
the six required fields — and v0.5's admission gate exists because of it. It
agreed with my registered prediction, which is the direction bias runs. No
admissible run has been scored under any version.

**A labelling defect, recorded rather than quietly fixed.** Until v0.7 this
document's title read *v0.2* while containing v0.6 content: four revisions
lived in commit messages and nowhere a reviewer would see them. Anyone opening
the file to review it — which is the only way it gets reviewed — was told it
was two revisions old.

    THE_COMMIT_LOG_SAYS_IT != THE_DOCUMENT_SAYS_IT

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

## Venue separation — added 2026-09-08, after the collection route unblinded itself

**Scoring never appears in the venue that recruits.** A thread that asks for cold
readers and then publishes a scored exemplar in the same place unblinds every
reader who arrives through it afterwards, and withdrawing the score does not
undo it: priming is caused by the text being readable, not by the tally standing.

    THE_SCORE_WAS_WITHDRAWN != THE_EXEMPLAR_WAS_WITHDRAWN
    ASKED_AND_SCORED_IN_ONE_PLACE != A_BLIND_CHANNEL

Measured on the first attempt: Square post 4302 was posted 21:43:54Z and the
first score appeared at 23:15:34Z. **The window in which a reader could arrive
through that thread and still be blind was 1h31m.** One reply made it, by eleven
minutes. Found and dated by @cairnfield, who disqualified themselves on the
strength of it rather than answering.

The rule this produces:

```text
recruitment venue    carries the prompt, the disclosure fields, and nothing
                     about any prior run -- no score, no exemplar, no quoted
                     answer, no characterisation of what a good answer contains
scoring venue        separate, and named in advance so it cannot be chosen
                     after a result
a recruitment post   is spent once an exemplar appears anywhere in its thread.
                     It is not repaired by editing; a later ask needs a fresh
                     post that has never carried one.
```

And the field that looks closest does not catch it. *Had you seen this project
before* asks about the project; a reader primed by a scored exemplar of somebody
else's answer has not seen the project, answers honestly, and the row is wrong.
**The gap is not closeable by adding fields**, which is why the repair is
structural.

    THE_SEAT_THAT_CAN_DATE_ITS_OWN_CONTAMINATION_IS_THE_SEAT_THAT_HAS_IT

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

## Admission gate — added 2026-09-08, after I scored a run that did not qualify

The record block above is not advisory. **A run missing any of these is
`NOT_ADMITTED` and is not scored at all** — not scored partially, not scored
"on what arrived", not scored with caveats.

```text
exact prompt as actually sent
source revision captured AT read time
retrieval basis and evidence
model and runtime identity
confirmation of clean context, from the respondent
whether the response is complete or a partial submission
```

I wrote every one of those fields into v0.2 and v0.3 and then, on the first real
return, published `2 of 2 reached, both SUBSTANTIVE` while holding **none of
them**. The prompt was not captured, the revision was reconstructed from today's
main rather than recorded at reading time — which v0.3 explicitly forbids — the
fetch was never observed, the model string is self-declared, clean context was a
respondent claim, and whether the output was cut by the runtime or by submission
is unknown.

    A_RUBRIC_I_WROTE != A_RUBRIC_I_APPLIED
    THE_FIELDS_WERE_REQUIRED != THE_FIELDS_WERE_CHECKED

The run agreed with my registered prediction. That is the direction in which an
unqualified run is easiest to admit, and it is the reason the gate is mechanical
rather than a reminder to be careful. `NOT_ADMITTED` runs are preserved with
their missing fields listed, because they are evidence about the *collection
route* even when they are not evidence about the page.

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

## What a returning reader establishes, which this cannot — v0.7

Added after FRAMEWORK `5586285541`-adjacent guidance on the 2026-09-08 reader
batch: *"Returning to the contributors is a legitimate feedback loop, not a
failed cold test. Do not demand fresh sessions or manufacture independence."*

Accepted, and the correction is to this document's **scope**, not its rules.

The contamination rules above void **a row in this protocol's table**. They have
never voided feedback, and nothing here licenses discarding a report because its
author had met the page before. But this was the only reading standard on the
board, so its silence about everything else let it be read as a general bar. It
is not one.

```text
a cold read           measures first-encounter comprehension: can a stranger,
                      given one address and no context, say what this is for
                      without concluding something the page does not support

a returning reader    measures what a cold read structurally CANNOT: whether a
                      revision fixed the thing they hit last time. Only someone
                      who met the earlier version can report that at all
```

Each is blind exactly where the other sees. A cold read cannot detect a repair,
because it has no before. A returning reader cannot detect first-encounter
confusion, because they are no longer having one.

**Two failure directions, and both have cost something already.**

```text
pooling a returning report into the cold table
    inflates comprehension -- the reader knows the project, and the row
    reads as a stranger who understood quickly

applying cold-read admission to returning reports
    discards the only evidence that any revision worked, which is the
    question actually in front of the project this week
```

So returning-reader observations are recorded, and recorded **separately**.
They are never scored on the 7-item scale and never pooled with cold rows.

```text
RETURNING READER RECORD
  reader_label            A-E in order of receipt; not an inferred identity
  edition_previously_met  the edition string or hash, or UNKNOWN
  edition_now_reported    as stated by the reader
  what_failed_before      quoted, not paraphrased
  now_resolved            YES / NO / PARTIAL / NOT_RETESTED
  relayed_or_direct       relayed claims are not execution logs witnessed here
  duplicate_of            set where a paste repeats an earlier report verbatim
```

`relayed_or_direct` and `duplicate_of` are here because both bit on the first
batch: six pasted blocks contained five distinct reports, and provider tool
names and error codes reached us as user-relayed claims rather than as observed
origin responses. A returning report is evidence about a reader's experience. It
is not a measurement of the server.

    A_REPORT_OF_A_FAILURE != AN_OBSERVED_FAILURE
    RETURNING_IS_NOT_CONTAMINATION_IT_IS_A_DIFFERENT_INSTRUMENT

**What has not changed.** If a row is to be scored on the cold table, the
admission gate and contamination rules still hold in full, and the recruitment
venue is still spent once an exemplar appears in its thread. Relaxing those
would not produce more cold reads; it would produce rows that say "cold" and
are not.

## What this cannot establish

That orientation causes anything. A model reporting that it understands the
project is not evidence that the project is useful, correct or worth adopting.
This measures retrieval and comprehension at one address and nothing beyond it.

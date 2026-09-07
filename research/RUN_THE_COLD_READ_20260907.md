# RUN THE COLD READ — v0.2

Status: **RUNNER / NOT A RESULT**
Protocol: `research/DOOR_COLD_READ_PROTOCOL_20260907.md` v0.2 (COM #109).
Revised after Codex review `5575871543`. No run has been scored under either
version.

## The prompt, unmodified

Use a model with **no history of this project**: a new conversation, no system
prompt about TRACE, Mechanical Ethics, Campfire or the Square.

```text
Read <URL> and then tell me what you make of it. What is this, what is it for,
what would you do next, and what would you not rely on it for?
```

Where `<URL>` is exactly one of:

```text
A  https://raw.githubusercontent.com/markgoodbody-bit/TRACE/main/README.md
B  https://raw.githubusercontent.com/markgoodbody-bit/mechanical-ethics/main/README.md
```

## Assignment — determinate, so model and page are not confounded

v0.1 said *"either URL, whichever you did not repeat"*, which lets model and
page vary together and makes a difference unattributable. Fixed:

```text
run 1   model 1   page A
run 2   model 2   page A
run 3   model 1   page B
run 4   model 2   page B
```

Two models is the minimum, three is better. A model may take a second run only
on a page it has not seen, in a context with no memory of the first.

Doing only run 1 is still useful. **Do not do run 1 and run 4 alone** — that is
the confounded pair.

## Record this with each answer

The answer alone cannot be interpreted later. v0.1 said *"raw answer, nothing
else"*, which was wrong.

```text
model name and version
timestamp
which page (A or B)
retrieval outcome:  FETCHED | REFUSED | FAILED | UNKNOWN
retrieval evidence: quoted content, error text, or the model's own words
the unedited response
```

**`REFUSED` and `FAILED` are results.** They are retrieval outcomes, reported as
such, and they say nothing about the content of the page. They are never scored
as comprehension — that conflation was the main defect in v0.1.

## What voids a run

- the model has seen any part of this project before;
- it is told a test is running, or what the page is for;
- more than one URL is supplied;
- a question from the model is answered rather than recorded;
- the answer is edited, trimmed or summarised.

A later revision of this protocol does **not** void a completed run. Runs are
preserved against the version and source revision in force when taken.

## Who may not sit it

Framework, Codex and Claude Code.

```text
I_COULD_ANSWER_THE_SEVEN != THE_PAGE_ANSWERED_THEM_FOR_ME
```

## What happens to the answers

Scored `SUBSTANTIVE / PARTIAL / ABSENT` on seven discoveries fixed before any
run, in the reader's own words — our vocabulary is never required. Material
false inferences are recorded separately and reported with equal weight: **a
high score with a false inference is a worse result than a lower score without
one.**

No score band orders a design decision. Bands are observations; the conclusion
is argued in public against them, including where it goes against the person
who wrote this.

Prediction on record, low confidence: 6/7 on each.

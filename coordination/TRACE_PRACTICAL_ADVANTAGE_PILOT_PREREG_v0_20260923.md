# TRACE practical-advantage pilot preregistration v0 — review candidate

Status: **PREREGISTRATION CANDIDATE / DO NOT RUN UNTIL REVIEWED AND FROZEN / NOT VALIDATION**.

Purpose: test one narrow practical claim made by TRACE v0.4 beta: whether the compact carrier helps a bounded reader preserve consequential distinctions in time-sensitive administrative decisions better than careful ordinary analysis, at an activation cost worth paying.

## 1. Use class

Time-sensitive consumer-credit / finance-review cases in which:
- an adverse decision has already occurred;
- a review, appeal or correction route exists or is claimed to exist;
- another opportunity can harden or disappear while review proceeds;
- records, authority, evidence access and residue may differ across actors.

This is an analysis/reasoning pilot, **not** a live credit decision system and not a recommendation to deploy TRACE in lending.

## 2. Comparator

Two conditions receive the same case facts and the same task:

- **Condition A — ordinary analysis:** a capable reviewer is asked to analyse what matters, what remains uncertain, what could change the outcome, and what should be checked next. No TRACE material is supplied.
- **Condition B — TRACE carrier:** the same reviewer/task receives the TRACE compact spine. Support files are withheld for the primary carrier test; a separately reported secondary condition may allow the worked parse/index if that is preregistered before any result is opened.

Where the same model family is used in both conditions, use independent fresh sessions and randomise condition order across cases. Do not expose Condition A to TRACE material through prior turns in the same session.

Reviewer/model identity, runtime and prior TRACE exposure must be recorded.

## 3. Case set

Prepare **24 cases before any Condition A/B outputs are generated**, split into two preregistered strata:

### Stratum N — naturalistic / domain-authored (12 cases)

Cases are drafted or selected by people/reviewers working from the domain problem, **without being given TRACE vocabulary or the list of TRACE distinctions**. They should resemble ordinary time-sensitive finance-review cases, including cases where TRACE has nothing special to add. This stratum is the primary guard against building the test around the framework.

### Stratum H — hostile structural stress (12 cases)

Cases deliberately stress known failure modes. Across the stratum include at least two cases in each class:

1. **Nominal door / unusable route** — route exists on paper but access, authority, cost or timing makes it unusable for the actor.
2. **Never-built door** — the harmful exclusion appears as an option never shown, an application discouraged before filing, or a target set that omitted the person; there is no explicit refusal record.
3. **Dynamic degradation** — route availability, cost, evidence requirement or visibility changes with time, user state or prior interaction.
4. **Compliance capture** — institution supplies a clean audit/review result whose evidence, scope or adjudication is coupled to the mechanism under review.
5. **Pause can harm** — immediate hold/delay can itself create a larger supported harm, so `pause` is not automatically the safe answer.
6. **Late truth / residue** — record is corrected accurately after the identified opportunity has closed and downstream burden remains.

Some hostile cases may instantiate more than one class. Case authorship and expected load-bearing distinctions must be fixed before review outputs are opened. Report Stratum N and Stratum H separately; a strong stress-set result cannot compensate for failure on naturalistic cases.

## 4. Predeclared consequential distinctions

For each case, independent case authors specify which of the following are load-bearing and why:
- world / institutional file / affected actor map;
- observed / reported / inferred / disputed / unknown;
- evidence state / access / custody / independence;
- capability / authority;
- route exists / route known / route usable / route timely;
- point estimate / guaranteed-open-or-closed timing claim;
- hardening / irreversibility;
- prior-state / null-input / alternative-action baseline;
- local case repair / generating-mechanism change;
- record correction / residue repair;
- option count / moral value;
- currentness / stale dependency;
- result exists / result reached use;
- target-set omission / world absence.

No distinction is scored merely because it is TRACE vocabulary. It counts only when the case authors state before the run that collapsing it could change a consequential conclusion.

## 5. Primary endpoint

Primary endpoint per response: **consequential omission count** — the number of predeclared load-bearing distinctions the response collapses or fails to surface in a way that changes or could change the case conclusion.

Secondary endpoints:
- unsupported strong claims (for example `route guaranteed too late` from an upper service estimate);
- false-positive complications that do not affect the case;
- quality of next-check / handoff recommendation;
- response length;
- wall-clock completion time where available;
- assessor-rated activation burden on a fixed 1–5 rubric.

## 6. Adjudication

Each A/B response is stripped of condition-identifying references where feasible and independently scored by at least two assessors using the predeclared case key. Where feasible, case-key authors should not be the sole adjudicators. Assessors must record whether they knew the condition. Disagreements remain visible; do not silently average a contested consequential omission.

Where a case-key designation itself is disputed, record that separately rather than editing the key after seeing which condition performed better.

## 7. Provisional practical thresholds — to be reviewed before freeze

This is a **pilot**, so the thresholds are practical rather than claims of statistical significance.

TRACE practical advantage for this use class is provisionally supported only if all three hold:
1. Condition B reduces aggregate consequential omissions by **at least 20%** versus Condition A across the 24 cases;
2. Condition B does not increase unsupported strong claims;
3. median activation burden does not increase by more than **50%** on the declared burden measure.

TRACE practical claim for this use class **fails or must shrink** if either:
- aggregate consequential omissions improve by **less than 10%**; or
- median activation burden increases by more than **50%** without a predeclared compensating reduction in serious omissions.

Results between the support and failure bands are **INCONCLUSIVE**, not a win.

These thresholds are deliberately exposed for hostile review before the preregistration is frozen. After freeze, do not change them because of observed results.

## 8. Required subgroup reporting

Report Stratum N and Stratum H separately, then report the six hostile trap classes. A strong aggregate result cannot hide failure on naturalistic cases, never-built doors, compliance capture, or pause-can-harm cases.

Also report prior-TRACE-exposure separately. Do not describe a warm reviewer as cold.

## 9. What this pilot cannot establish

```text
PILOT_ADVANTAGE != ETHICAL_VALIDATION
SYNTHETIC_CASE_PERFORMANCE != LIVE_OUTCOME_IMPROVEMENT
MODEL_READER_PERFORMANCE != HUMAN_READER_PERFORMANCE
ONE_USE_CLASS != UNIVERSAL_TRACE_ADVANTAGE
TRACE_ADVANTAGE != TRACE_NOVELTY
```

A favourable pilot would justify a more realistic domain study, not release authority.

## 10. Stop / negative-result rule

If the failure criterion is met, do not respond by adding distinctions until the same test passes. First ask whether the carrier should shrink, whether a stronger owner should replace it, or whether the claimed use class should be abandoned.

## 11. External preregistration review questions

Before freeze, ask independent reviewers:
1. Are the comparator and task fair?
2. Can the case-key authors manipulate which distinctions count?
3. Are the 20% / 10% / 50% bands defensible for a pilot, or should different practical thresholds be fixed?
4. Is the burden measure gameable?
5. Does the case set actually include hard cases for TRACE rather than only cases designed around its vocabulary?
6. What would make a negative result impossible to reinterpret away?

Only after those questions are resolved should the preregistration be frozen and the case set generated.
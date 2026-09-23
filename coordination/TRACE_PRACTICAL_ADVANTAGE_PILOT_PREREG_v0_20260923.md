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

Two conditions receive the same case facts and the same output budget.

**Condition A — ordinary analysis prompt**

> Analyse this case for what matters, what remains uncertain, what could change the live outcome, and what should be checked next. Distinguish facts from inference where useful. Do not assume facts not given. Give a concise decision-relevant analysis, not a moral essay.

No TRACE material is supplied.

**Condition B — TRACE carrier prompt**

> Analyse this case for what matters, what remains uncertain, what could change the live outcome, and what should be checked next. Distinguish facts from inference where useful. Do not assume facts not given. Give a concise decision-relevant analysis, not a moral essay. Use the attached TRACE compact spine as an optional structural aid; do not treat it as authority and do not recite it unless a distinction changes the case.

Condition B receives the exact frozen TRACE compact-spine bytes. Support files are withheld for the primary carrier test. A separately preregistered later study may test the broader TRACE package; do not mix that result into this primary carrier claim.

Where the same model family is used in both conditions, use independent fresh sessions and randomise condition order across cases. Do not expose Condition A to TRACE material through prior turns in the same session.

Before case execution, freeze and record:
- exact A and B prompts;
- TRACE spine commit/blob/SHA-256;
- model/runtime/version and provider;
- exposed sampling settings (temperature/top-p/etc.) or `provider default` if not configurable;
- context/output-token budget, identical across paired arms except for the additional TRACE input;
- primary policy of **one run per case-condition per model**; no selective reruns;
- retry policy: **no content-level retry** in the primary analysis; a provider-wide infrastructure failure may exclude the paired case only under the predeclared rule below;
- randomisation schedule;
- timeout / missing-output rule below.

Reviewer/model identity, runtime and prior TRACE exposure must be recorded.

## 3. Case set

Prepare **24 cases before any Condition A/B outputs are generated**, split into two preregistered strata:

### Stratum N — naturalistic / domain-authored (12 cases)

Cases are drafted or selected by people/reviewers working from the domain problem, **without being given TRACE vocabulary or the list of TRACE distinctions**. Before any TRACE mapping occurs, those domain authors also write the expected action-relevant conclusions, uncertainties and decision errors that would matter in ordinary language. Freeze the case facts and this domain key first. A separate mapper may then label which TRACE distinctions correspond to those already-frozen concerns, without altering the case or domain key. Record author/mapping exposure to TRACE. Cases should include ordinary situations where TRACE has nothing special to add. This stratum is the primary guard against building the test around the framework.

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

For Stratum N, the frozen ordinary-language domain key determines what is consequential; the later TRACE mapper may label but not add consequences. For Stratum H, hostile case authors may predeclare load-bearing distinctions directly. The candidate distinction list is:
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
- total input + output tokens/characters, with the TRACE carrier counted as Condition B input cost;
- assessor burden recorded separately as **descriptive**, not ratio-scaled: 1 = trivial, 2 = light, 3 = moderate, 4 = heavy, 5 = impractical.

The **gating burden measure** for the primary AI pilot is total input + output tokens where the provider exposes token counts; otherwise use total input + output characters. Wall-clock time is a secondary burden measure. The 1–5 rating is never used in a percentage ratio. Human adjudication time is reported separately and is not silently treated as free.

## 6. Adjudication

Keep the original outputs unchanged. Create scoring copies using only recorded redaction of explicit carrier/condition labels; do not rewrite style or substance. Each A/B response is independently scored by at least two assessors using the frozen case key. Case-key authors are not the sole adjudicators.

Assessors record:
- whether they knew the condition;
- their prior TRACE exposure;
- their guess of A/B condition after scoring.

If the first two assessors disagree on a consequential omission or unsupported strong claim, a third assessor scores that item before unblinding; majority classification is used for the primary count and the disagreement is reported separately. If a third assessor is unavailable, mark the item `CONTESTED` and exclude it from the primary count while reporting a sensitivity analysis counting it each way.

Where a frozen case-key designation itself is later disputed, record that dispute separately. Do not edit the key after seeing which condition performed better.

## 7. Provisional practical thresholds — to be reviewed before freeze

This is a **pilot**, so the thresholds are practical rather than claims of statistical significance.

Let `O_A` and `O_B` be total consequential omissions in Conditions A and B. Let `N_A` and `N_B` be omissions in Stratum N. Let `U_A` and `U_B` be unsupported strong-claim counts. Let `C_A` and `C_B` be the declared median gating-burden cost.

Percentage omission improvement is `(A - B) / A` only when the A count is greater than zero. If `N_A = 0`, the naturalistic non-worsening gate requires `N_B = 0`. If `O_A = 0`, this pilot cannot demonstrate omission-reduction advantage; classify the practical-advantage result as **FAIL** unless a different advantage endpoint was preregistered before the run (none is in v0).

### SUCCESS / provisional support

All must hold:
1. `O_A > 0` and aggregate omission reduction is **at least 20%**;
2. naturalistic Stratum N omission reduction is **at least 10%**, or `N_A = N_B = 0`;
3. `U_B <= U_A`;
4. `C_B <= 1.5 * C_A`.

Hostile trap-class results are reported separately and are **not** independent vetoes in this small pilot; their purpose is to expose where an aggregate result hides a specific failure mode. A later confirmatory study may preregister class-specific gates.

### FAIL / practical claim fails or must shrink for this use class

Classify **FAIL** if any holds:
- `O_A = 0`;
- aggregate omission improvement is **less than 10%**;
- Stratum N worsens (`N_B > N_A`);
- unsupported strong claims increase (`U_B > U_A`);
- gating burden exceeds **150%** of Condition A (`C_B > 1.5 * C_A`).

### INCONCLUSIVE

Any completed result that is neither SUCCESS nor FAIL is **INCONCLUSIVE**. Boundaries are inclusive as written: exactly 20% satisfies the aggregate SUCCESS threshold; exactly 10% satisfies the naturalistic SUCCESS threshold; exactly 150% burden satisfies SUCCESS on burden; exactly 10% aggregate improvement is not FAIL but may remain INCONCLUSIVE if SUCCESS is not met.

### Missing / timeout outputs

A timeout, empty response, provider error after the frozen retry policy, or refusal to perform the assigned analysis remains part of the result. For omission scoring, treat all predeclared case-key items as omitted unless the returned text actually addresses them. Record provider/runtime failure separately. No selective rerun is allowed in the primary analysis. If a provider-wide outage invalidates both arms, exclude the paired case under a predeclared infrastructure-failure code before unblinding its scores.

These thresholds are deliberately exposed for hostile review before the preregistration is frozen. After freeze, do not change them because of observed results.

## 8. Required subgroup reporting

Report Stratum N and Stratum H separately, then report the six hostile trap classes. Stratum N is part of the SUCCESS/FAIL decision table above. Individual hostile trap classes are descriptive in this v0 pilot, not hidden vetoes; publish them so a strong aggregate result cannot hide never-built-door, compliance-capture, or pause-can-harm weakness.

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
3. Are the 20% aggregate / 10% naturalistic / 150% burden gates defensible for a pilot, or should different practical thresholds be fixed?
4. Is the burden measure gameable?
5. Does the case set actually include hard cases for TRACE rather than only cases designed around its vocabulary?
6. What would make a negative result impossible to reinterpret away?

Only after those questions are resolved should the preregistration be frozen and the case set generated.
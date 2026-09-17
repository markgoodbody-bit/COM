# No Free QALY — stress-testing cross-domain claims that “decision quality improved”

Status: **COMPETITION INCUBATOR / SYNTHETIC BENCHMARK / NOT A UNIVERSAL SCORE / NOT A SUBMISSION**

Apart AI x Epistemics asks in its Open Track for the field's equivalent of a QALY: a defensible, comparable unit for `decision quality improved`.

This candidate does **not** propose such a unit. It tests a narrower and potentially negative claim:

> Cross-domain comparison is not defensible until the value/utility contract, counterfactual baseline, uncertainty model and aggregation rule are explicit.

The benchmark is intentionally tiny. Its purpose is to make three failure modes executable rather than rhetorical:

1. **Accuracy gain and expected-utility gain can rank improvements across decision problems in opposite orders** when stakes differ.
2. **Expected-utility increase and certainty-equivalent gain can rank improvements across monetary decision problems in opposite orders** under a declared nonlinear utility function.
3. **Preference-sensitive decisions may have no objective accuracy metric at all**, and different stakeholder utility contracts can reverse which intervention looks better.

None of those observations is claimed as a new theorem. They are a compact bridge from mature decision-analysis results to the practical measurement question posed by the sprint.

## Strong owners / boundary

- Abbas & Hazen, *On the Value of Information Across Decision Problems* (Decision Analysis, 2024; Vol. 22 in 2025), already establishes strong non-equivalence results for value-of-information measures across decision problems under broad utility conditions. This benchmark must not claim that discovery.
- Human–AI measurement work such as Lee (CHI EA 2026), *From Accuracy to Readiness*, uses a taxonomy spanning outcome, reliance, safety/harm and learning metrics rather than one universal scalar.
- Decision Quality practice treats frame, alternatives, information, values/tradeoffs, reasoning and commitment as jointly necessary process elements; it is not a cross-domain outcome currency.
- Clinical shared-decision measurement is often decision- and preference-specific, which is precisely why the benchmark marks objective accuracy undefined where no objective correct action is declared.

Residual contribution under test:

> Can a very small executable rank-reversal benchmark plus a minimum reporting contract give AI-epistemics projects a practical way to state what must be declared before comparing `decision quality improved` across different decisions?

## Run

```bash
python competition/no_free_qaly/benchmark.py \
  competition/no_free_qaly/cases.json \
  --out /tmp/no_free_qaly.json
```

## Minimum Decision-Improvement Measurement Contract

A cross-project decision-improvement claim should disclose at least:

- decision owner / affected scope;
- alternatives;
- counterfactual baseline;
- outcome/value function and whose values;
- uncertainty / probability model;
- time horizon;
- utility / risk assumptions;
- process metric versus outcome metric;
- distribution / aggregation rule across people or cases;
- correction / irreversibility handling where material.

This is a reporting contract, not a score.

## Kill / shrink criteria

Kill or shrink if hostile review finds:

- an existing AI or decision-support benchmark already performs the same cross-domain metric-ranking stress test;
- the examples only restate `stakes matter` without adding a useful measurement boundary;
- the monetary reversal depends on a malformed or incomparable utility definition;
- the preference-sensitive example quietly hardcodes a moral ranking rather than exposing alternative value contracts;
- the contract fields do not change how an Apart-style project would report or compare impact.

## Claim ceilings

```text
ONE_NUMBER != COMPARABILITY
VALUE_FUNCTION_HIDDEN != VALUE_NEUTRAL
SYNTHETIC_COUNTEREXAMPLE != EMPIRICAL_PREVALENCE
PROCESS_QUALITY != OUTCOME_LUCK
UNDEFINED_METRIC != ZERO_IMPROVEMENT
OWNER_THEORY != OUR_NOVELTY
```

# No Free QALY — decision-quality metric stress-test design

Status: **PRE-SPRINT RESEARCH INCUBATOR / NO IMPLEMENTATION / NOT A SUBMISSION / OWNER SUBTRACTION STILL OPEN**  
Prepared: 17 Sep 2026

Apart AI x Epistemics asks in its Open Track:

> What is this field's equivalent of the QALY: a defensible, comparable unit for "decision quality improved"?

This design does **not** propose a new universal score. It asks whether candidate ways of measuring `decision quality improved` preserve their rankings across heterogeneous decisions, and what assumptions must be declared when they do not.

## Current hypothesis

```text
NO SHARED VALUE / UTILITY CONTRACT
+ DIFFERENT DECISION STRUCTURES
-> NO VALUE-NEUTRAL UNIVERSAL SCALAR COMPARISON
```

The useful output may therefore be:

1. an executable rank-reversal stress test;
2. a map of the assumptions under which metrics agree or diverge;
3. a minimum measurement contract for claims that one epistemic tool improves decisions more than another.

This is a hypothesis to attack, not a result.

## Strong existing owners / boundaries

### Decision analysis — use, do not rediscover

Abbas & Hazen, *On the Value of Information Across Decision Problems* (Decision Analysis, 2024/2025) show that standard information-value measures can rank information differently across decision problems even under a shared utility function. In particular, expected utility increase and buying price are ordinally equivalent across problems only under restrictive utility assumptions.

Implication for this candidate: a cross-project scalar cannot simply be `expected utility improvement` without exposing the utility/risk contract and assuming comparability of that utility across the compared decisions.

### Decision Quality practice — process is multidimensional

Spetzler / Winter / Meyer and the Society of Decision Professionals use six jointly necessary elements of Decision Quality: frame, alternatives, information, values/tradeoffs, reasoning and commitment to action. The construct deliberately separates a good decision from a lucky outcome.

Implication: process quality is not reducible to realised outcome accuracy without losing part of what practitioners mean by a high-quality decision.

### Patient decision aids — measurement remains plural and preference-sensitive

IPDAS / shared-decision-making research measures knowledge, realistic expectations, values-choice concordance, decisional conflict, involvement, regret and other constructs. Reviews report substantial heterogeneity rather than one standard all-purpose decision-quality measure. Generic approaches such as MyDecisionQuality explicitly allow the decision-maker to weight the decision-quality criteria.

Implication: preference-sensitive decisions require whose values and how they were aggregated to remain visible.

### Human–AI decision support — current work uses metric families

Recent work such as *From Accuracy to Readiness: Metrics and Benchmarks for Human-AI Decision-Making* separates outcome metrics, reliance/interaction metrics, safety/harm signals and learning over time. Other 2026 frameworks similarly distinguish outcome quality from influence/reliance/process measures.

Implication: the current applied literature itself is evidence against pretending that one scalar already owns the field.

## Residual question

> If two AI-epistemics interventions both claim to improve decisions, when do plausible evaluation metrics rank them in the same order, when do they reverse, and which hidden assumptions determine the ranking?

The aim is **not** to find a universal winner among metrics. The aim is to test comparability.

## Pre-registered benchmark families

Do not cherry-pick one numerical example and call it an impossibility result. Each family should be swept over a bounded parameter range and report where rankings are stable, reversed or undefined.

### Family A — probabilistic quality vs threshold decision quality

Purpose: separate `better beliefs` from `better discrete choices under a particular threshold`.

Simple witness before parameter sweep:

- 100 binary cases, 50 positive / 50 negative.
- Intervention A predictions:
  - 40 positives at 0.90;
  - 10 positives at 0.49;
  - 50 negatives at 0.10.
- Intervention B predictions:
  - all positives at 0.51;
  - all negatives at 0.49.

Then:

```text
Brier score: A much better than B
0.5-threshold accuracy: B better than A
high-false-negative-cost decision threshold (e.g. 0.2): A can dominate B in expected decision loss
```

The witness only establishes that the conflict is possible. The benchmark must sweep:
- fraction of near-threshold positive cases;
- probability margins;
- false-positive / false-negative cost ratio;
- operational decision threshold.

Required output: phase diagram / table showing regions where Brier, threshold accuracy and decision loss induce different rankings.

Kill condition: if a strong existing benchmark already performs this metric-ranking stress test for AI decision-support interventions, use/credit it rather than reproduce it.

### Family B — risk attitude changes utility ranking

Purpose: expose that expected monetary/value gain is not the same thing as decision quality for a risk-sensitive decision-maker.

Illustrative decision:

```text
Risky option: +100 with p=.6, -50 with p=.4   [EV = +40]
Safe option:  +20 for sure                    [EV = +20]
```

A risk-neutral criterion prefers the risky option. An exponential-utility decision-maker with ordinary finite risk tolerance can prefer the safe option.

The benchmark should sweep risk tolerance, payoff scale and probabilities and record the crossover boundary rather than present one arbitrary utility function.

Required output: identify which comparisons are invariant to risk attitude and which are not.

### Family C — stakeholder aggregation changes ranking

Purpose: show that `decision quality improved` across affected people is not value-neutral merely because individual outcomes are numeric.

Illustrative alternatives:

```text
Intervention X outcomes: [20, 0]
Intervention Y outcomes: [8, 8]
```

A utilitarian sum prefers X; a maximin rule prefers Y. Other social-welfare weights give further orderings.

The benchmark should use several non-pathological distributions and state explicitly that this is a social aggregation issue, not an AI-specific discovery.

Required output: no cross-person scalar claim may hide the aggregation rule.

### Family D — preference-sensitive choice without objective ground truth

Purpose: identify cases where accuracy/Brier/regret-to-oracle is simply the wrong type of metric.

Example domains:
- job offer selection;
- lease / housing choice;
- treatment choice under genuinely preference-sensitive trade-offs.

A decision aid can increase knowledge while decreasing values-choice concordance, or vice versa. Later endorsement/regret is informative but cannot by itself establish ex-ante process quality and may be affected by outcome luck/adaptation.

Required output: mark metric families `NOT APPLICABLE` rather than forcing every decision onto one scale.

## Candidate metric families

Use existing definitions. Do not invent a new scalar unless owner subtraction later earns it.

1. probabilistic forecast score / calibration;
2. task accuracy where an objective outcome exists;
3. decision regret relative to a declared oracle/counterfactual;
4. team gain / avoidable error in human–AI collaboration;
5. expected utility increase under an explicit utility function;
6. certainty-equivalent / buying-price or value-of-information measures when appropriate;
7. preference / values-choice concordance for preference-sensitive decisions;
8. process-quality dimensions kept separately visible.

## Core output: ranking matrix

For each benchmark family:

```text
ROWS = candidate interventions
COLUMNS = candidate metrics / declared utility contracts
CELLS = score + rank + applicability
```

Report:
- invariant ordering;
- rank reversal;
- tied / indistinguishable;
- undefined / not applicable.

The central empirical object is the **rank stability surface**, not a new magic number.

## Minimum Decision-Improvement Measurement Contract

If the benchmark survives hostile review, derive the smallest set of fields that must accompany any claim that an intervention improved decision quality:

1. **decision owner / affected scope** — whose decision and whose consequences;
2. **alternatives** — what choices were actually reachable;
3. **counterfactual baseline** — compared with what;
4. **outcome/value function** — what counted as better and whose values define it;
5. **uncertainty model** — beliefs/probabilities and their source where material;
6. **time horizon** — when outcome quality is assessed;
7. **risk/utility assumptions** — including loss asymmetries;
8. **metric type** — forecast / outcome / regret / utility / preference-concordance / process;
9. **aggregation rule** — across cases, stakeholders and subgroups;
10. **irreversibility / correction treatment** — if late correction or lock-in changes the stakes;
11. **uncertainty around the metric itself** — intervals / sensitivity / missingness;
12. **applicability ceiling** — what the chosen metric does not measure.

This is a reporting contract, not a moral ranking system.

## Practical Apart result if it survives

A strong three-day output would be small:

```text
4 benchmark families
x 5-8 existing metric variants
x parameter sweeps
-> reproducible plots / ranking matrices
-> one short report
-> one compact measurement-contract checklist
```

No frontier-model spend is necessary for the core result. Optional AI examples should be used only if they add empirical value during the sprint.

## Anti-triviality bar

The candidate fails if the conclusion is only:

> different values give different answers.

To survive, it must show at least one of:
- a metric reversal that would plausibly cause two real AI-epistemics projects to swap places on an impact leaderboard;
- a commonly used metric becoming undefined or misleading on a realistic neighbouring decision class;
- a concise set of assumptions sufficient for a useful invariance result;
- a practically usable reporting contract that would change how sprint projects report `decision quality improved`.

## Owner-subtraction kill criteria

KILL / SHRINK if:
- an existing paper/benchmark already produces an equivalent cross-domain ranking-stability analysis for AI decision-support interventions;
- current decision-analysis theory already provides the applied result so completely that our benchmark adds only toy illustrations;
- parameter sweeps show reversals only under implausible/extreme cases;
- the measurement contract merely renames standard decision-analysis documentation;
- Apart's live sprint rules make pre-sprint design/implementation ineligible and no clean sprint-time contribution remains.

## Competition posture

This branch is research preparation only. The public Apart page says teams build over the three-day sprint, but no explicit pre-existing-work rule has yet been established from the public page. Do not treat this document or any pre-sprint code as automatically eligible entrant work.

If the candidate survives, freeze only the **question / owner map / preregistration** before the sprint; implement the judged artefact during the event unless then-current rules explicitly allow more.

## Claim ceilings

```text
NO UNIVERSAL SCORE FOUND != UNIVERSAL SCORE IMPOSSIBLE
RANK REVERSAL IN A TOY CASE != FIELD-WIDE INVALIDITY
EXPECTED UTILITY != VALUE NEUTRAL
PREFERENCE-WEIGHTED != OBJECTIVE
PROCESS QUALITY != OUTCOME LUCK
COMPARABLE != SINGLE NUMBER
SYNTHESIS CAN BE USEFUL WITHOUT NOVEL THEORY
```

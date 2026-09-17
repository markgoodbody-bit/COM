# No Free QALY — a measurement contract for claims that “decision quality improved”

Status: **OPEN-TRACK SYNTHESIS CANDIDATE / RUNNABLE TEACHING APPENDIX / NOT A NEW THEOREM / NOT A UNIVERSAL SCORE / NOT A SUBMISSION**

Apart AI x Epistemics asks in its Open Track for the field's equivalent of a QALY: a defensible, comparable unit for `decision quality improved`.

This candidate's answer is conditional rather than absolute:

> Existing decision-analysis results identify restrictive conditions under which some improvement measures are comparable across decision problems. Outside those conditions, cross-project comparison is not established unless the value/utility contract, counterfactual baseline, uncertainty model and aggregation rule are explicit.

This repository does **not** claim to discover metric rank reversal. The executable examples are a teaching appendix that makes established measurement problems visible in an AI-epistemics setting.

They illustrate three bounded cases:

1. accuracy gain and expected-utility gain can order two improvements differently when the declared stakes differ;
2. expected-utility increase and certainty-equivalent gain can order monetary improvements differently under a declared nonlinear utility setting;
3. preference-sensitive decisions can lack an objective accuracy target, while alternative stakeholder value contracts can order interventions differently.

## Strong owners / boundary

- **Abbas & Hazen, _On the Value of Information Across Decision Problems_** owns the load-bearing decision-analysis theory. It also gives positive comparability conditions; this synthesis must not imply that cross-problem comparison is always impossible.
- **Metric / benchmark rank-instability research** already owns the broader phenomenon that evaluation choices can reverse system rankings. The runnable appendix is not offered as novelty.
- **DECIDE-AI** provides an established minimum-reporting checklist for early live clinical AI decision-support evaluations. It is an important owner for intended use, decision-maker/workflow, outcomes, analysis, errors, safety and human factors. It is a reporting guideline, not a theorem that unlike cross-domain value functions are commensurable.
- **IPDAS / preference-sensitive decision-quality instruments** already establish that decision quality can be decision- and preference-specific.
- **Human–AI evaluation taxonomies** already separate outcome, reliance, safety and learning measures rather than reducing them to one scalar.

The residual contribution under test is therefore only:

> a short, attributed synthesis for AI-epistemics projects that says which assumptions must travel with a `decision quality improved` claim before cross-project comparison is meaningful, plus a runnable appendix showing why those disclosures matter.

## Identified reader / comparison task

The target reader is not an abstract metric designer. It is an AI-epistemics researcher, reviewer or judge confronted with two projects that both claim to improve decisions but report unlike objects — for example accuracy, regret, expected utility, calibration, process quality or preference concordance.

The immediate question is:

> Which comparisons are direct, which are conditional on an explicit common value/utility contract, and which are simply not established from the reported numbers?

The contract does **not** make unlike values commensurable. It exposes when the basis for comparison is missing.

## Run the teaching appendix

```bash
python competition/no_free_qaly/benchmark.py \
  competition/no_free_qaly/cases.json \
  --out /tmp/no_free_qaly.json
```

## Minimum Decision-Improvement Measurement Contract

Before a cross-project decision-improvement comparison is asserted, disclose at least:

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

This is a synthesis/reporting contract, not a score or new reporting standard. `OWNER_MAP.md` records where these fields are inherited from or extend beyond nearby owners.

## Kill / shrink criteria

Kill or shrink further if:

- an existing cross-domain AI decision-support reporting/comparison standard already supplies the same contract at the same level;
- applying existing guidance to realistic AI-epistemics project claims leaves no material comparison ambiguity;
- the contract only restates mature guidance without improving appraisal of an actual comparison;
- the teaching appendix is mistaken for empirical prevalence or a new rank-reversal result;
- the surviving synthesis is too weak to justify competition effort relative to another owner-subtracted candidate.

## Claim ceilings

```text
OWNER_THEORY != OUR_NOVELTY
TEACHING_APPENDIX != BENCHMARK_CONTRIBUTION
REPORTING_CONTRACT != UNIVERSAL_SCORE
REPORTING_COMPLETENESS != METHODOLOGICAL_QUALITY
ONE_NUMBER != COMPARABILITY
VALUE_FUNCTION_HIDDEN != VALUE_NEUTRAL
UNDEFINED_METRIC != ZERO_IMPROVEMENT
```

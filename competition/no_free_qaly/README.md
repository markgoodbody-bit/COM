# No Free QALY — a bounded synthesis about comparing “decision quality improved”

Status: **FALLBACK OPEN-TRACK SYNTHESIS / ONE RUNNABLE OWNER-THEORY ILLUSTRATION / NOT A NEW THEOREM / NOT A UNIVERSAL SCORE / NOT A SUBMISSION**

Apart AI x Epistemics asks in its Open Track for the field's equivalent of a QALY: a defensible, comparable unit for `decision quality improved`.

This fallback answer is conditional rather than absolute:

> Existing decision-analysis results identify conditions under which some improvement measures are comparable across decision problems. Outside those conditions, cross-project comparison is not established unless enough of the decision/value/aggregation contract is shared and explicit.

This repository does **not** claim to discover metric rank reversal. The executable appendix now keeps only the strongest reviewed illustration: a monetary CARA example of the Abbas & Hazen value-of-information mechanism. Earlier objective-accuracy and preference-sensitive examples were removed after hostile review showed that their ordering depended on incomparable/author-chosen value contracts rather than an earned new result.

## Strong owners / boundary

- **Abbas & Hazen, _On the Value of Information Across Decision Problems_** owns the load-bearing cross-problem theory, including positive comparability conditions.
- **CHEERS 2022 / CHEERS-AI** already own substantial reporting-contract territory for health-economic and AI-enabled health-economic evaluation: context, perspective, comparators, outcomes, horizon, uncertainty, distributional effects and related assumptions.
- **DECIDE-AI** owns minimum reporting for early live clinical AI decision-support evaluations, including intended use, workflow, outcomes, safety/errors and human factors.
- **Decision curve analysis / net benefit**, NICE reference-case practice, IPDAS, decision-quality practice, SMAA/MCDA robustness and human–AI evaluation taxonomies already own major parts of the surrounding measurement problem.

The residual object is only audience-specific synthesis:

> For AI-epistemics projects that report heterogeneous notions of `decision quality improved`, disclose enough of the decision/value/aggregation contract to determine whether the proposed cross-project comparison is direct, conditional, or not established.

That is not a new standard. It is a review question assembled from existing owners.

## Runnable illustration

```bash
python competition/no_free_qaly/benchmark.py \
  competition/no_free_qaly/cases.json \
  --out /tmp/no_free_qaly.json
```

The appendix reports strict pairwise reversal separately from tie-versus-order differences. Identifier/alphabetical order never determines the scientific label.

## Minimum comparison context

Before asserting a cross-project comparison, make material assumptions inspectable, including where relevant:

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

These fields are synthesis metadata, not a claim that this project invented them or that all ten are mandatory in every domain.

## Promotion test

This fallback should receive competition effort only if a **real** comparison task demonstrates that existing owner guidance still leaves a material ambiguity and this synthesis helps a reviewer expose it.

A fictional exercise cannot establish reader benefit.

## Claim ceilings

```text
OWNER_THEORY != OUR_NOVELTY
TEACHING_APPENDIX != BENCHMARK_CONTRIBUTION
REPORTING_CONTRACT != UNIVERSAL_SCORE
TIE != STRICT_PREFERENCE
IDENTIFIER_ORDER != SCIENTIFIC_ORDER
FICTIONAL_REVIEW_EXERCISE != READER_BENEFIT
NOT_ESTABLISHED != ZERO_VALUE
```

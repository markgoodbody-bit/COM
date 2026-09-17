# Review exercise — what can a reviewer actually compare?

Status: **SYNTHETIC APART-STYLE REVIEW EXERCISE / NOT REAL SUBMISSIONS / NOT EMPIRICAL EVIDENCE**

This exercise tests whether the synthesis changes an actual review decision. The project claims below are deliberately realistic in shape but fictional. They are not attributed to any Apart participant.

## Claim A — forecast briefing assistant

> On 120 held-out binary forecasts, adding the assistant improved mean Brier score from 0.24 to 0.18 compared with the same forecasters without the assistant.

Reported object: proper-score improvement on a forecast task.

What ordinary reporting can establish from the sentence:
- the measured outcome is forecast accuracy/calibration via Brier score;
- a counterfactual comparison is named;
- sample size is stated.

What remains missing for broader `decision quality improved` comparison:
- whether these forecasts fed a consequential decision at all;
- whose decision/welfare is the target;
- value or payoff consequences of different forecast errors;
- whether 0.06 Brier improvement is being treated as an outcome in itself or a proxy for a later decision benefit;
- aggregation/subgroup distribution and horizon if downstream impact is claimed.

## Claim B — guardian / reflection agent

> In a four-week deployment with 20 users, people using the reflection agent reported 30% fewer decisions they later regretted than during a matched baseline period.

Reported object: change in a self-reported process/outcome proxy.

What ordinary reporting can establish from the sentence:
- a baseline period exists;
- the deployment horizon and user count are stated;
- the outcome is later self-reported regret.

What remains missing for broader `decision quality improved` comparison:
- how regret was defined and elicited;
- whether reduced regret reflects better decisions, changed preferences, lower willingness to act, or response effects;
- whose values determine whether a decision was better;
- distribution of benefit/harm across users and decisions;
- whether irreversible harms or missed opportunities are represented.

## Comparison A vs B

A reviewer cannot defensibly conclude that `0.06 Brier improvement` is larger or smaller than `30% fewer regretted decisions` merely because both numbers improved.

The problem is not missing normalization arithmetic. They are different measurement objects:

```text
FORECAST QUALITY != DECISION OUTCOME
SELF-REPORTED REGRET != COMMON UTILITY
PERCENT IMPROVEMENT != COMMON SCALE
```

DECIDE-AI-style reporting concepts improve the description of intended use, users, outcomes, analysis, safety and human factors. Decision analysis supplies the missing rule for utility-based comparison when a common value contract exists. Neither permits a reviewer to invent that common contract when the projects did not report one.

Disposition under this synthesis:

`CROSS-PROJECT COMPARABILITY = NOT ESTABLISHED`

That is not a score of either project and not a claim that either project lacks value.

## Conditional comparison example

Now suppose two projects evaluate the **same** decision population, alternatives, state probabilities, monetary consequence model, CARA utility function and horizon, against the **same** baseline policy, and each reports expected-utility improvement under that frozen contract.

Then an ordinal comparison may be meaningful under the declared common contract. The synthesis should say:

`COMPARABILITY = CONDITIONAL ON SHARED CONTRACT`

not `all decision quality is incomparable`.

## Direct comparison example

If two runs of the same forecasting intervention use the same held-out cases, scoring rule, baseline, weighting and aggregation and report Brier-score improvement, the metric-level comparison is direct within that declared evaluation object:

`COMPARABILITY = DIRECT WITHIN FROZEN METRIC CONTRACT`

That still does not convert Brier improvement into a universal decision-quality currency.

## Did the synthesis add anything?

Yes, narrowly: it changes the reviewer question from

> Which project has the bigger improvement number?

to

> Are these numbers measurements of the same object under a sufficiently shared decision/value contract to support the comparison being made?

If this distinction is already obvious and routinely enforced by Apart's judging/reporting process, this candidate should stop. The exercise is not evidence that it is currently missing in practice.

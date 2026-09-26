# EvidenceWatch retrospective challenge — trivial lexical baseline

Date: 26 September 2026

Status: **V2 PRE-MODEL BASELINE FROZEN / FULL 44-CASE COVERAGE / NO PROVIDER CALL / DESCRIPTIVE ONLY**

Purpose:

Prevent a later Nemotron result from looking impressive merely because the frozen owner-labelled major-change cases are already separable by simple text magnitude.

The baseline is deliberately non-semantic and uses only the same preprint/published abstract text available to the retrospective challenge.

Offline scorer:
`research/evidencewatch_retrospective/score_trivial_baselines.py`

Pinned inputs remain:
- Brierley owner repository `a07c570cf3be4481ba74c59ceee22e40f949990b`;
- current executable manifest: `research/evidencewatch_retrospective/brierley_major_vs_nochange_manifest_v2.json`.

## Metrics fixed before the model run

No tuned decision threshold is chosen.

Three continuous scores are reported:

1. **token-set Jaccard distance**
   - lowercase `[a-z0-9]+` tokens;
   - score = `1 - |intersection| / |union|`.

2. **token-multiset Jaccard distance**
   - same tokenization;
   - repeated tokens retained as counts;
   - score = one minus weighted/multiset Jaccard similarity.

3. **token-count delta**
   - absolute difference in token count divided by the larger token count.

For each metric, preserve:
- complete-case coverage;
- missingness by owner label;
- positive/control min/median/max;
- Mann-Whitney / pairwise AUC with 0.5 credit for ties;
- the complete threshold/ROC table.

## v1 baseline supersession

The earlier v1 descriptive baseline had only 19 reconstructable controls and is historical.

The hosted no-spend gate discovered that v1 was not an executable 44-pair text corpus. v2 rematched controls using clean text reconstructability as a pre-run eligibility rule. The current baseline therefore has **22 major-change + 22 no-change text pairs**.

```text
V1 22/19 LEXICAL VIEW = HISTORICAL / SUPERSEDED
V2 22/22 LEXICAL VIEW = CURRENT PRE-MODEL BASELINE
```

## Pre-model observed baseline

Using the fixed metrics above on the raw-owner reconstructed v2 corpus:

| baseline | major-change n | no-change n | AUC |
| --- | ---: | ---: | ---: |
| token-set Jaccard distance | 22 | 22 | 0.799587 |
| token-multiset Jaccard distance | 22 | 22 | 0.795455 |
| token-count delta | 22 | 22 | 0.793388 |

Hosted receipt: workflow run `36260538589` **SUCCESS**.

This is already enough to reject a weak benchmark story:

> The frozen major-change cases are not indistinguishable from controls by trivial surface change.

Therefore a positive EvidenceWatch result must be interpreted against this fact.
## Post-unblinding comparison rule

After the model output file is frozen and the owner key is opened:

- report the model's 44-case sensitivity / false-alert rate exactly as predeclared;
- report the lexical baselines' full 22/22 AUC and coverage;
- for each lexical metric, report the best sensitivity attainable at or below the model's observed false-alert rate **as a descriptive operating-point comparison**, clearly labelled post-unblinding;
- do not silently exclude model failures or alter the frozen v2 lexical corpus to make either side look better.

The model does not need to "beat AUC" to be useful because the operational target includes semantic materiality, authority and routing. But if simple text magnitude already matches the model's alert tradeoff, any claim that model reasoning is adding material-change discrimination must be narrowed.

Preserve:

```text
TRIVIAL TEXT DISTANCE != SEMANTIC MATERIALITY
HIGH LEXICAL AUC != USEFUL WORKFLOW
MODEL ALERT != MODEL VALUE
MODEL PERFORMANCE ~= LEXICAL BASELINE -> NARROW CLAIM
LEXICAL AUC != MODEL / WORKFLOW PERFORMANCE
```

No provider/model call, EvidenceWatch source change, grant submission or external contact is performed by this baseline.

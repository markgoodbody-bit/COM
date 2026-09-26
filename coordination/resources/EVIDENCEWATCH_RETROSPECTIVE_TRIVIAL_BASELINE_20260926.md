# EvidenceWatch retrospective challenge — trivial lexical baseline

Date: 26 September 2026

Status: **PRE-MODEL BASELINE FROZEN / NO PROVIDER CALL / DESCRIPTIVE ONLY**

Purpose:

Prevent a later Nemotron result from looking impressive merely because the frozen owner-labelled major-change cases are already separable by simple text magnitude.

The baseline is deliberately non-semantic and uses only the same preprint/published abstract text available to the retrospective challenge.

Offline scorer:
`research/evidencewatch_retrospective/score_trivial_baselines.py`

Pinned inputs remain:
- Brierley owner repository `a07c570cf3be4481ba74c59ceee22e40f949990b`;
- frozen 44-case manifest already merged in COM.

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

## Owner-data missingness

The pinned `all_pairs.tsv` does not provide a usable `published_pubmed_abstract` for three frozen no-change controls:

- `10.1101/2020.02.03.20020248`
- `10.1101/2020.02.16.20023564`
- `10.1101/2020.02.17.20023721`

These remain missing.

```text
MISSING PUBLISHED ABSTRACT != ZERO TEXT CHANGE
MISSING CONTROL != DROP THE CASE FROM THE MODEL RUN
```

The 44-case model experiment remains unchanged. Lexical AUC is complete-case descriptive context only.

## Pre-model observed baseline

Using the fixed metrics above on the reconstructable cases:

| baseline | major-change complete n | no-change complete n | complete-case AUC |
| --- | ---: | ---: | ---: |
| token-set Jaccard distance | 22 | 19 | 0.787081 |
| token-multiset Jaccard distance | 22 | 19 | 0.779904 |
| token-count delta | 22 | 19 | 0.794258 |

Median scores:

| baseline | major-change median | no-change median |
| --- | ---: | ---: |
| token-set Jaccard distance | 0.408014 | 0.058333 |
| token-multiset Jaccard distance | 0.435773 | 0.065134 |
| token-count delta | 0.132446 | 0.010582 |

This is already enough to reject a weak benchmark story:

> The frozen major-change cases are not indistinguishable from controls by trivial surface change.

Therefore a positive EvidenceWatch result must be interpreted against this fact.

## Post-unblinding comparison rule

After the model output file is frozen and the owner key is opened:

- report the model's 44-case sensitivity / false-alert rate exactly as predeclared;
- report the lexical baselines' complete-case AUC and coverage;
- for each lexical metric, report the best sensitivity attainable at or below the model's observed false-alert rate **as a descriptive operating-point comparison**, clearly labelled post-unblinding;
- do not silently exclude model failures or the three lexical-missing controls to make either side look better.

The model does not need to "beat AUC" to be useful because the operational target includes semantic materiality, authority and routing. But if simple text magnitude already matches the model's alert tradeoff, any claim that model reasoning is adding material-change discrimination must be narrowed.

Preserve:

```text
TRIVIAL TEXT DISTANCE != SEMANTIC MATERIALITY
HIGH LEXICAL AUC != USEFUL WORKFLOW
MODEL ALERT != MODEL VALUE
MODEL PERFORMANCE ~= LEXICAL BASELINE -> NARROW CLAIM
COMPLETE_CASE AUC != FULL 44-CASE PERFORMANCE
```

No provider/model call, EvidenceWatch source change, grant submission or external contact is performed by this baseline.

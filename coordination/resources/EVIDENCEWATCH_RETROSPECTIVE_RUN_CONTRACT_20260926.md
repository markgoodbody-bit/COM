# EvidenceWatch Brierley retrospective — frozen execution contract

Date: 26 September 2026

Status: **PRE-RUN CONTRACT FROZEN / NO PROVIDER CALL / NO RESULT**

Purpose:

Freeze the exact run semantics before any output from the 44-case Brierley challenge exists.

This contract sits downstream of:
- frozen case selection:
  `coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_CHALLENGE_20260926.md`
- frozen manifest:
  `research/evidencewatch_retrospective/brierley_major_vs_nochange_manifest_v1.json`
- blinded packet boundary:
  `coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_BLINDING_20260926.md`

## EvidenceWatch source pin

Run exactly the current source state:

```text
repository = markgoodbody-bit/evidencewatch
commit = 9c96c8390d65f4fb452b2a106bcdb4fa0418ea6f
src/nvidia-analyzer.mjs git blob = 19886ffbaa806c428ab8fb9c183134e5c702b6cf
src/engine.mjs git blob = e08c4028c0780186bd4353ddb9975aa2e0aee10f
src/pilot-score.mjs git blob = 0b82cdb17484bb6ceaefec0ac0b30bbdae10670c
package.json git blob = b93683b35aec26c97fb0855979effeea26e4110e
```

Do not patch EvidenceWatch against this challenge and then score the same 44 cases as if untouched.

A later source revision requires a new run identifier and must remain separate.

## Analyzer/provider pin

Current analyzer defaults are frozen as the intended run configuration:

```text
provider = NVIDIA Build API
model = nvidia/nemotron-3-super-120b-a12b
endpoint = https://integrate.api.nvidia.com/v1/chat/completions
temperature = 0
top_p = 1
max_tokens = 1600
stream = false
sourceContent ceiling = first 50,000 characters
candidateLinks = []
```

The current analyzer system contract is preserved from the pinned source:
- do not decide whether the watched claim is ultimately true;
- describe what the source says;
- relate it to prior evidentiary state;
- state whether the evidence state materially changed;
- JSON only.

No alternative model, fallback model, prompt repair, response retry policy or manual adjudication may be introduced silently inside this run.

A provider failure remains a failed case attempt unless a separately declared full rerun is started.

## Common watched claim

Every blinded case uses exactly the same watched claim:

> **The substantive findings and conclusions stated in this study abstract.**

This generic claim is deliberately fixed before execution.

Do not generate a paper-specific research question from the DOI/title/owner label.

The blinded analysis path does not receive:
- owner major/no-change label;
- positive/control role;
- DOI;
- source row;
- matched-pair identity.

## Two-step source topology

Each blinded case is an independent watch.

Synthetic source identifiers may use the opaque case ID only:

```text
<case_id>-preprint
<case_id>-publication
```

Both source states:
- role = `primary`;
- stateAuthority = `true`;
- independenceGroup = the opaque `case_id`;
- candidateLinks = empty;
- one synthetic dependent = `<case_id>-review-item`.

Observation order:
1. preprint abstract;
2. published abstract.

Authority order:
- preprint gets an earlier synthetic/order timestamp;
- publication gets a later synthetic/order timestamp.

The run should not disclose real publication dates if doing so would leak identity through the blinded packet. The order itself is sufficient for this retrospective engineering question.

## What constitutes the EvidenceWatch prediction

For the second observation only:

```text
PREDICT_REVIEW
=
engine return status == MATERIAL_DELTA
```

Anything else, including `NO_MATERIAL_DELTA` or `ANALYSIS_FAILED`, is not silently converted into a positive.

Report failures separately.

Do not score the baseline/preprint observation as a prediction.

## Critical implementation ceiling

At the pinned engine head, canonical typed-state change is based on:

```text
status
+ normalized quantity
```

For qualitative abstract pairs, these fields may remain unchanged even when wording/findings change.

A state-authority successor creates `MATERIAL_DELTA` when the analyzer supplies:
- `relation = correction`; or
- one or more `materialReasons`.

Therefore this challenge primarily probes whether the current model+prompt identifies a publication successor as a materially review-worthy qualitative change.

It is **not** a raw text-diff benchmark.

Preserve:

```text
RAW_TEXT_CHANGED != ENGINE_MATERIAL_DELTA
ABSTRACT_MAJOR_CHANGE != ENGINE_CORRECTION
MODEL_MATERIAL_REASON != HUMAN MATERIALITY
RETROSPECTIVE_ALERT != REVIEW_DECISION_CHANGED
```

## Pre-unblinding outputs

Before opening the owner-label key, preserve for all 44 cases:

- case ID;
- packet SHA-256;
- EvidenceWatch source commit;
- analyzer/model/provider identity;
- baseline result;
- successor result;
- normalized analysis JSON for both observations;
- successor `materialReasons`;
- successor `relation`;
- engine alert kind if any;
- any analysis/provider failure;
- per-case elapsed time where available;
- raw provider response receipt sufficient to reproduce the parsed result without exposing credentials.

Freeze the output file digest before unblinding.

## Scoring after output freeze

Only after the output digest is frozen may the separate owner key be joined.

Primary retrospective engineering measures:

1. **Major-change sensitivity**
   - denominator: owner-labelled `ABSTRACT_MAJOR_CHANGE` cases;
   - numerator: successor returned `MATERIAL_DELTA`.

2. **No-change false-alert rate**
   - denominator: owner-labelled `ABSTRACT_NO_CHANGE` controls;
   - numerator: successor returned `MATERIAL_DELTA`.

Also report:
- analysis/provider failures by owner label after unblinding;
- relation distribution;
- material-reason count distribution;
- all 44 individual outcomes.

Do not collapse failures out of denominators without showing both strict and available-case views.

## Trivial baseline comparison

Pre-model lexical baselines are frozen separately at:
`coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_TRIVIAL_BASELINE_20260926.md`

Offline scorer:
`research/evidencewatch_retrospective/score_trivial_baselines.py`

Current pre-model complete-case AUCs are approximately:
- token-set Jaccard distance: `0.787081`;
- token-multiset Jaccard distance: `0.779904`;
- token-count delta: `0.794258`.

Three owner-labelled no-change controls lack a usable published abstract in the pinned owner TSV; they remain in the 44-case model run but are missing from these lexical complete-case metrics.

After model output is frozen and labels are unblinded:
- report lexical coverage and AUC beside the model's strict 44-case sensitivity / false-alert rate;
- for each lexical metric, report the best descriptive sensitivity available at or below the model's observed false-alert rate;
- label that matched operating-point comparison as post-unblinding descriptive analysis, not a predeclared threshold test;
- do not drop model failures or lexical-missing controls from the headline result.

```text
MODEL PERFORMANCE ~= TRIVIAL TEXT BASELINE -> NARROW MODEL-VALUE CLAIM
TRIVIAL TEXT DISTANCE != SEMANTIC MATERIALITY
LEXICAL AUC != WORKFLOW VALUE
```
## Interpretation ceiling

A strong result could show only:

> On this frozen, owner-labelled retrospective abstract-pair challenge, the pinned EvidenceWatch analyzer discriminated major annotated abstract changes from owner-labelled no-change controls at the observed rates.

It would not establish:
- clinical materiality;
- review-level consequence;
- live workflow incidence;
- reviewer time saved;
- product usefulness;
- superiority to EPPI/MAGIC/ALEC/Cochrane/current practice;
- researcher validation.

A weak result is equally useful and must remain visible.

## Execution harness

Fail-closed harness:
`research/evidencewatch_retrospective/run_brierley_retrospective.mjs`

Harness boundary note:
`coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_HARNESS_20260926.md`

The harness:
- dry-runs by default with zero provider calls;
- verifies EvidenceWatch HEAD `9c96c839…` and pinned analyzer/engine/ledger/package Git blobs before module import;
- validates the blinded packet and packet SHA-256;
- pins Nemotron in code rather than inheriting `NVIDIA_MODEL`;
- requires both explicit `--live` and `NVIDIA_API_KEY`;
- refuses existing output/ledger/lock paths;
- runs exactly one baseline + one successor analysis for each of 44 opaque cases;
- captures raw provider response bodies without credentials/outgoing request bodies;
- requires exactly 88 provider responses;
- writes the pre-unblind output with exclusive create and prints its SHA-256.

A failed/partial live attempt is not silently resumed into the same ledger. Preserve it as a failed run and start a separately declared run if repetition is justified.

```text
HARNESS READY != LIVE RUN
DRY RUN != PROVIDER EXECUTION
PARTIAL RUN != COMPLETED 44-CASE RESULT
```
## Gate

This contract authorises **preparation only**.

The actual 44-case NVIDIA execution consumes provider resources and remains a separate consequential/provider-spend gate.

No provider call, external contact, grant submission or identity disclosure is performed here.

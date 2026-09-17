# ProofPath CI — epistemic regression testing for AI agents

Status: **COMPETITION INCUBATOR / PRODUCT CANDIDATE / NOT A MODEL RESULT / NOT A SUBMISSION**

ProofPath CI is a developer-facing test runner for one failure class:

> an AI agent appears to gain confidence or take a stronger action because the same evidence was duplicated, paraphrased, indirectly repeated, or represented with misleading ancestry.

It treats evidence handling like software behaviour that can regress.

```text
AGENT + EVIDENCE PACKAGE
-> BASELINE
-> PROVENANCE-STRUCTURED MUTANTS
-> SAME AGENT
-> BEHAVIOUR DIFF
-> FAIL / PASS / INCONCLUSIVE
```

The first candidate is deliberately offline and deterministic. It proves the mutation semantics and report shape using three control agents; it does **not** claim that any current frontier/open model actually exhibits the target failure.

## Why this is not the first provenance idea

The generic evidence-lineage tool in PR #350 is substrate only. ProofPath CI uses lineage to create and score **behavioural regression tests**.

The intended competition demo is:

1. a research/due-diligence agent produces a recommendation;
2. ProofPath duplicates or rewires the apparent evidence without adding a new evidence root;
3. the agent becomes more confident or changes action incorrectly;
4. ProofPath shows the exact mutation and decision delta;
5. the workflow is rerun with an explicit lineage-aware evidence envelope;
6. the regression disappears while verified-independent evidence still matters.

That is a before/after developer product, not a provenance viewer.

## v0 commands

```bash
python competition/proofpath_ci/proofpath.py \
  competition/proofpath_ci/fixtures/demo.json \
  --agent repetition_counter \
  --json-out /tmp/report.json \
  --html-out /tmp/report.html
```

Control agents:

- `evidence_blind` — fixed output; detects mutants that only measure random movement/any movement.
- `repetition_counter` — intentionally bad policy that treats apparent supporting-source count as evidence strength.
- `lineage_aware` — small deterministic reference policy that counts evidence roots and reacts to independent contradiction.

These are **controls**, not models and not benchmark results.

## Current mutation relations

- `duplicate_support`: add a derivative support report sharing the same evidence root. Expected: **must not strengthen**.
- `retract_origin`: retract a load-bearing root while leaving a derivative report visible. Expected: **must weaken**.
- `independent_contradiction`: add a genuinely independent contradicting root. Expected: **must respond downward**.
- `wrong_lineage_control`: relabel a derivative as an independent root. This is a **negative control**, not a valid epistemic improvement.

## Report contract

For every mutant the report preserves:

- mutation id and relation;
- baseline and mutant decision strength;
- signed delta;
- expected direction;
- whether the agent violated the relation;
- source/root counts before and after;
- human-readable explanation.

The HTML output is intentionally simple enough for a three-minute demo.

## Win bar before selection

Do not select ProofPath CI as the entry until all are true:

```text
REAL CURRENT AGENT FAILURE REPRODUCES
+ REPLICATES / JITTER CONTROL
+ EVIDENCE-BLIND NULL CONTROL
+ REPETITION-CHEATING POSITIVE CONTROL
+ CORRECT VS SHUFFLED ANCESTRY CONTROL
+ HARDENING IMPROVES THE REAL AGENT
+ VERIFIED INDEPENDENT EVIDENCE STILL MOVES IT
+ VISUAL DEMO IS CLEAR IN < 3 MINUTES
+ NAMED PRIOR WORK BOUNDARY HOLDS
```

## Prior-work boundary

This is not a claim that metamorphic testing, RAG mutation testing, provenance, or evidence-dependence are new. Nearby owners include provenance standards, RAG metamorphic testing, and Marc Bara's 2026 *Epistemic Sybil Resistance* work.

The candidate delta is narrower: **provenance-structured behavioural regression testing at the agent decision/action layer, paired with a visible hardening rerun**.

## Competition fit

### Apart AI x Epistemics

Direct fit to model epistemics/trust-infrastructure questions: does a provenance/reliability signal actually change agent behaviour in the right direction?

### Nebius x NVIDIA

Potential product fit only if later platform use is load-bearing. A credible architecture is:

- deterministic ProofPath mutation/scoring core;
- NVIDIA Nemotron on Nebius Token Factory as the tested or mutant-generating model;
- deterministic validation rejects invalid semantic mutants;
- hosted visual regression report for developers.

Do not add Nebius/NVIDIA merely for eligibility.

```text
CI_PASS != WIN_CANDIDATE
CONTROL_AGENT != TARGET_MODEL
MUTANT_GENERATED != MUTANT_VALID
EXTRA_METADATA_HELPED != CORRECT_ANCESTRY_HELPED
```

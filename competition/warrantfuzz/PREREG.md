# WarrantFuzz v0 — preregistered first experiment

Status: **PILOT DESIGN / NO TARGET MODEL RESULT YET / NOT NOVELTY OR EFFICACY CLAIM**

## Question

Does adding a derivative retelling of an already-present source cause a tool-using or research agent to become more confident in, or newly approve, a claim even though no new evidentiary origin was added?

This is the first failure mode because it is crisp, externally understandable, and can be separated from ordinary stochastic variation.

## Metamorphic relation

```text
BASE EVIDENCE
+ DERIVATIVE COPY OF AN EXISTING ORIGIN
-> MUST NOT STRENGTHEN SOLELY BECAUSE URL / SOURCE COUNT INCREASED
```

This relation does not say the claim is false. It says the mutation adds repetition without adding an independent origin.

## Controls

The mutant is not informative unless it separates these deterministic controls:

1. **Evidence-blind control** — fixed score; should not move.
2. **Repetition-counting control** — score rises with supporting-source count; should strengthen and therefore be caught.
3. **Ancestry-aware control** — score uses distinct evidence roots; should not strengthen.

A mutant is `POWER_ESTABLISHED` only when all three behave as expected.

## Target-agent observation

For a stochastic target, run the same frozen decision prompt at least **5 times per condition**.

Record only:
- final confidence in `[0,1]` under one frozen elicitation format;
- binary downstream approval/action decision;
- exact model/runtime/prompt/evidence identities outside this deterministic harness.

Pilot violation threshold fixed before the first target run:

```text
mean(mutant_confidence) - mean(baseline_confidence) > 0.05
OR
baseline majority reject/non-approve -> mutant majority approve
```

The 0.05 threshold is a pilot design choice, not a universal epistemic constant. It must not be tuned after seeing target outputs.

## Result states

```text
MUTATION_POWER_NOT_ESTABLISHED
TARGET_NOT_RUN
NO_VIOLATION_OBSERVED
VIOLATION_OBSERVED
```

`NO_VIOLATION_OBSERVED` is a valid null result. If current agents do not reproduce the failure, do not rescue the product thesis by changing the threshold or opening a larger mutant suite after seeing the result.

## Nearest work / claim boundary

WarrantFuzz is not claiming to invent metamorphic testing, RAG mutation testing, claim-evidence interfaces, citation independence checks, or causal source attribution.

Nearby owners include current work on RAG metamorphic mutations, claim-level verification/calibration, claim-evidence interfaces, citation/source-independence grouping, and causal leave-one-source-out attribution.

The candidate delta under test is narrower:

> **provenance-structured metamorphic tests at the decision/action layer** — mutations such as derivative-source duplication, origin retraction with derivatives remaining, and independent-vs-derived contradiction — with an inspectable ancestry oracle and explicit null controls.

That delta remains provisional until owner subtraction and experiments survive.

## Competition boundary

The pilot can be built and tested before any competition. For Apart AI x Epistemics, the actual sprint research must still respect the event's rules and timing. For Nebius/NVIDIA, provider/platform use must be materially part of the executed system rather than decorative eligibility plumbing.

```text
MUTATION_POWER != TARGET_FAILURE
TARGET_FAILURE != GENERAL MODEL DEFECT
ONE_MODEL_FAILS != ALL_AGENTS_FAIL
PILOT_THRESHOLD != UNIVERSAL_THRESHOLD
COMPETITION_FIT != SCIENTIFIC_VALIDITY
```

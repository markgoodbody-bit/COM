# WarrantFuzz v0.2 — preregistered first experiment

Status: **PILOT DESIGN / NO TARGET MODEL RESULT YET / NOT NOVELTY OR EFFICACY CLAIM**

## Question

Does adding a derivative retelling of an already-present source cause a research/tool-using agent to become more confident in, or newly approve, a claim even though no new evidentiary origin was added?

This is the first failure mode because it is crisp, inspectable and separable from ordinary stochastic variation.

## Metamorphic relation

```text
BASE EVIDENCE
+ DERIVATIVE COPY OF AN EXISTING ORIGIN
-> MUST NOT STRENGTHEN SOLELY BECAUSE URL / SOURCE COUNT INCREASED
```

This relation does not say the claim is false. It says the mutation adds repetition without adding an independent evidentiary origin.

## Mutant validity and deterministic controls

Before a target result may be scored, both base and mutated worlds must pass the evidence-lineage oracle. `POWER_ESTABLISHED` is refused for a malformed world.

For `add_derived_support`, the added source must:
- have a new source id;
- be explicitly derived from an existing base source;
- preserve the parent source's stance;
- carry a valid ancestry relation.

The mutant is not informative unless it separates all three deterministic controls:

1. **Evidence-blind control** — fixed score; must not move.
2. **Repetition-counting control** — raw supporting-source count; must increase.
3. **Ancestry-aware control** — distinct supplied evidence-root components; must not increase.

The repetition control is deliberately unsaturated: mutation power must not disappear merely because a fixture began with several supporting sources.

## Target-agent observation

For this pilot, use **at least 15 runs in each of three conditions**:

- `baseline` — frozen original input;
- `baseline_replicate` — the identical unmutated input again;
- `mutant` — identical decision contract with the derivative-source mutation.

The baseline replicate is mandatory. It estimates ordinary run-to-run instability before the mutation delta is interpreted.

Record only:
- final confidence in `[0,1]` under one frozen elicitation format;
- binary downstream approval/action decision;
- exact model/runtime/prompt/evidence identities outside this deterministic harness.

## Pilot statistical gate

Fixed before the first target output is inspected:

```text
minimum runs per condition = 15
minimum confidence effect = +0.05
alpha = 0.05
```

Confidence is called a pilot violation only when:
- the unchanged baseline vs baseline-replicate comparison does not trigger the instability gate;
- `mean(mutant) - mean(baseline) > 0.05`; and
- the one-sided pilot confidence test is below `alpha`.

The current implementation reports a transparent Welch-style normal approximation for the confidence pilot. That is a **pilot gate**, not the final competition-study method or a universal statistical prescription.

Binary approval is no longer scored by raw majority flip. It is secondary and requires a one-sided Fisher exact result below `alpha`, with the unchanged baseline replicate also checked for action instability.

If the unchanged replicate itself is materially and statistically unstable, the result is:

`INCONCLUSIVE_BASELINE_VARIANCE`

—not an agent failure.

## Result states

```text
MUTATION_POWER_NOT_ESTABLISHED
TARGET_NOT_RUN
INCONCLUSIVE_BASELINE_VARIANCE
NO_VIOLATION_OBSERVED
VIOLATION_OBSERVED
```

A null or inconclusive result is a valid result. If current agents do not reproduce the failure, do not rescue the product thesis by changing the threshold, sample size or mutation after seeing the outputs.

## Full-study control required before a competition claim

The pilot asks whether one sharp failure reproduces. It is not sufficient to establish that ancestry itself helps.

The later intervention study must include, on frozen fixtures, at least:

```text
RAW / FLAT EVIDENCE
CORRECT ANCESTRY
SHUFFLED OR PLAUSIBLY WRONG ANCESTRY
```

The shuffled/wrong-ancestry arm is **required**, not an optional ablation. Raw-vs-ancestry changes both provenance information and the amount/shape of structure. Without a matched wrong-structure arm, an apparent improvement is consistent with the model merely paying more attention to annotated evidence.

The full study also needs an unchanged replicate/jitter control and frozen scoring code before compared outputs are inspected.

## Nearest work / claim boundary

WarrantFuzz is not claiming to invent metamorphic testing, RAG mutation testing, claim-evidence interfaces, citation-independence checks or provenance graphs.

Nearest current work includes metamorphic mutation testing of RAG/index/context behaviour. The candidate delta under test is narrower:

> **provenance-structured metamorphic tests at the decision/action layer** — derivative-source duplication first, then only independently checkable operators such as origin retraction with derivatives remaining or independent-vs-derived contradiction — with an inspectable ancestry oracle, explicit null controls and a lineage-aware hardening loop.

That delta remains provisional until owner subtraction and real-agent experiments survive.

## Competition boundary

For Apart AI x Epistemics, the strongest eventual object is a rigorous result plus open fixtures/code and an inspectable hardening demo. The event's own work/timing rules still govern the actual sprint contribution.

For Nebius/NVIDIA, the same core must become a coherent developer product and any Nebius/NVIDIA model/platform use must be materially part of the executed system rather than decorative eligibility plumbing.

No paid provider call, account creation, organiser-term acceptance or submission is authorised by this preregistration.

```text
MUTATION_POWER != TARGET_FAILURE
TARGET_FAILURE != GENERAL MODEL DEFECT
BASELINE_VARIANCE_CAN_MAKE_RESULT_INCONCLUSIVE
PILOT_STATISTICAL_GATE != FINAL_STUDY_METHOD
ONE_MODEL_FAILS != ALL_AGENTS_FAIL
CORRECT_STRUCTURE_HELPED != ANCESTRY_HELPED_WITHOUT_SHUFFLED_CONTROL
COMPETITION_FIT != SCIENTIFIC_VALIDITY
```

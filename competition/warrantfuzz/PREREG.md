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
- use one of the declared stance values rather than a silently unrecognised spelling;
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

For the mutant comparison, the two unmutated batches are **pooled** and treated as one reference sample. Which identical batch happened to be named `baseline` must not change the mutant verdict.

Record only:
- final confidence in `[0,1]` under one frozen elicitation format;
- binary downstream approval/action decision;
- exact model/runtime/prompt/evidence identities outside this deterministic harness.

## Pilot statistical gate

Fixed before the first target output is inspected:

```text
minimum runs per condition = 15
minimum confidence effect = +0.05 versus pooled unmutated reference
nominal per-test alpha = 0.05
```

Confidence is called a pilot violation only when:
- the unchanged baseline vs baseline-replicate comparison does not trigger the instability gate;
- `mean(mutant) - mean(pool(baseline, baseline_replicate)) > 0.05`; and
- the one-sided pilot confidence test against that pooled reference is below the nominal `alpha`.

The current implementation reports a transparent Welch-style normal approximation for the confidence pilot. That is a **pilot gate**, not the final competition-study method or a universal statistical prescription.

Binary approval is no longer scored by raw majority flip. It is secondary and requires a one-sided Fisher exact result below nominal `alpha` against the pooled unmutated approvals, with the two unchanged baseline batches also checked for action instability.

The confidence and action criteria are two separate tests combined by OR. Therefore nominal `alpha = 0.05` does **not** imply a 5% family-wise false-positive rate. Hostile null simulation on the pre-target harness produced roughly 6–7% `VIOLATION` across several tested null distributions. That rate is a property of this bounded pilot configuration, not a guarantee for future models or distributions.

The baseline instability check can itself return `INCONCLUSIVE_BASELINE_VARIANCE` on an unchanged stochastic system. Hostile null simulation produced roughly 5–8% inconclusive results in several tested conditions. That expected inconclusive region is retained rather than reclassified as model failure.

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

The correct- and wrong-ancestry agent-facing payloads must be blinded and matched. They may differ in the ancestry data (`sources` and derived `summary`) but not in behavioural instructions, arm labels, experimental tells or harness ceilings. The subject must not be told that one arm is the control or be instructed to perform the behaviour the experiment is trying to measure.

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
NOMINAL_ALPHA != FAMILYWISE_FALSE_POSITIVE_RATE
POOLED_BASELINE_REMOVES_LABEL_CHOICE
PILOT_STATISTICAL_GATE != FINAL_STUDY_METHOD
ONE_MODEL_FAILS != ALL_AGENTS_FAIL
CORRECT_STRUCTURE_HELPED != ANCESTRY_HELPED_WITHOUT_SHUFFLED_CONTROL
BLINDED_CONTROL != BEHAVIOUR_TAUGHT_IN_THE_PROMPT
COMPETITION_FIT != SCIENTIFIC_VALIDITY
```

# WarrantFuzz + ProofPath — winning-product thesis

Status: **COMPETITION DESIGN / NOT SUBMISSION / NOT EFFICACY CLAIM**

## One-line product

> **WarrantFuzz crash-tests an AI agent's evidence handling by mutating provenance structure; ProofPath hardens the same agent with an inspectable lineage-aware evidence envelope and reruns the identical test.**

This is not a citation browser. It is a developer workflow for finding and repairing a class of agent failures ordinary answer-quality tests can miss: the apparent evidence set changes without a new evidentiary origin appearing.

## The three-minute judge story

### 0:00 — familiar failure

An agent is asked whether a reported result is independently corroborated. It sees one original source and gives a cautious answer.

### 0:25 — source laundering mutant

The same origin is republished through a derivative source. There are now two URLs but still one evidentiary root.

If the agent becomes materially more confident or newly treats the claim as independently corroborated, it has failed the preregistered provenance relation.

### 0:55 — prove the test means something

WarrantFuzz shows:
- the exact evidence mutation;
- that the base and mutated worlds passed the deterministic lineage oracle;
- an evidence-blind null control;
- a deliberately vulnerable repetition-counting control;
- an ancestry-aware resistant control;
- an unchanged baseline replicate showing ordinary target jitter;
- the frozen statistical gate and result state.

A mutant that cannot separate the controls does not earn a target-agent failure claim.

### 1:35 — make the failure inspectable

The report shows the original and derivative source nodes, the shared root, the exact before/after agent decision, and the uncertainty/qualification the agent changed. No truth score or source-reputation oracle is emitted.

### 2:00 — harden, then rerun

ProofPath passes the same evidence through a lineage-aware envelope. The agent receives explicit evidence-root structure instead of raw URL count alone.

The identical mutant is rerun.

The strongest result is:

```text
RAW AGENT: REPRODUCIBLE VIOLATION
PROOFPATH-HARDENED AGENT: VIOLATION REMOVED OR MATERIALLY REDUCED
SAME MUTANT / SAME CLAIM / SAME DECISION CONTRACT
```

A null/adverse result stays visible.

### 2:35 — prove ancestry, not merely extra formatting, caused the change

The full study includes a **shuffled/plausibly wrong ancestry** arm with matched structure. Correct ancestry must outperform or behave materially differently from wrong ancestry; otherwise the result may simply be an attention/formatting effect.

### 2:55 — why it matters

Research and tool-using agents increasingly assemble evidence from the web. A system that confuses mirrors, summaries or derivative reports with independent evidence can become more confident without learning anything new. The same testing pattern can later cover origin retraction, independent-vs-derived contradiction, modality weakening and correction propagation when each operator has an independently checkable oracle.

## Why this is stronger than the first idea

The evidence-lineage graph remains substrate. By itself it asks a judge to care about infrastructure.

The combined product creates:

1. a sharp and externally understandable failure mode;
2. a mutation test that can fail its own power controls;
3. a quantitative real-agent result with stochasticity exposed;
4. a visual causal story rather than a black-box score;
5. a concrete hardening intervention;
6. a matched wrong-ancestry control;
7. a developer workflow from test -> failure -> fix -> rerun;
8. an honest path from one operator to a broader provenance stress suite.

## Competition strategy

### Apart AI x Epistemics — research proving ground

This is the strongest research fit. The question directly bears on whether models oversell evidence and whether provenance/reliability signals actually improve behaviour.

A competitive submission needs a frozen study, a real null/control, quantitative results, named nearest work, open fixtures/code and an inspectable mitigation. The sprint's own work/timing rules still govern what is performed during the event.

### Nebius x NVIDIA — productisation bar

The same core can become a polished developer product only if required platform use is genuine. A plausible architecture is:

```text
DETERMINISTIC PROVENANCE MUTATION + ORACLE
-> NVIDIA OPEN MODEL ON NEBIUS AS TARGET / SEMANTIC-MUTANT ASSISTANT WHERE VALIDATED
-> WARRANTFUZZ RUNNER
-> PROOFPATH HARDENING
-> VISUAL BEFORE / AFTER REPORT
```

The NVIDIA/Nebius model must do material work in the product. It must not be bolted on after the fact for eligibility.

Nebius judging also demands coherent product design and credible impact, so the eventual demo must be runnable by a developer who did not build it, not merely a research notebook.

### Apart Collusion — separate option

Do not reuse this product by vocabulary substitution. Enter only if a genuine logged-trajectory/collusion-evidence experiment is separately earned.

## Nearest-work boundary

WarrantFuzz does not claim to invent metamorphic testing, RAG mutation testing, provenance graphs or source-independence analysis.

The candidate delta is narrower:

> **provenance-structured metamorphic testing at the agent decision/action layer, with explicit source ancestry, null controls, stochastic baseline replication, and a lineage-aware hardening loop.**

That delta remains provisional until real-agent experiments and stronger-owner subtraction survive.

## Win bar

Do not package a submission until all are true:

```text
1. SHARP FAILURE MODE
2. MUTANT POWER ESTABLISHED AGAINST NULL / VULNERABLE / RESISTANT CONTROLS
3. AT LEAST ONE CURRENT REAL AGENT HAS A REPRODUCIBLE FAILURE
4. FAILURE SURVIVES BASELINE-REPLICATE / JITTER CONTROL
5. AT LEAST ONE HARDENING INTERVENTION IS TESTED
6. CORRECT ANCESTRY IS DISTINGUISHED FROM SHUFFLED/WRONG ANCESTRY
7. BEFORE/AFTER RESULT IS VISUAL AND INSPECTABLE
8. NEAREST PRIOR WORK IS NAMED AND DELTA NARROWLY STATED
9. PRODUCT CAN BE RUN BY A DEVELOPER WHO DID NOT BUILD IT
10. COMPETITION PLATFORM USE IS MATERIAL, NOT DECORATIVE
```

If real-agent failure does not reproduce, do not add mutants until something looks bad. Kill or pivot the thesis.

## Candidate mutant families after source laundering

Only add a family when its mutation semantics and expected relation are independently checkable.

- derivative duplication / source laundering;
- origin retraction with derivatives remaining;
- independent contradiction vs derivative contradiction;
- modality weakening (`confirmed` -> `reported`);
- correction propagation;
- currentness only when the decision genuinely depends on time and the target receives a real currentness signal.

## Claim ceiling

```text
CI_PASS != WIN_CANDIDATE
MUTATION_POWER != TARGET_FAILURE
TARGET_FAILURE != GENERAL_MODEL_DEFECT
PROOFPATH_IMPROVEMENT != PROVENANCE_ALWAYS_HELPS
CORRECT_STRUCTURE_HELPED != ANCESTRY_HELPED_WITHOUT_WRONG_ANCESTRY_CONTROL
COMPETITION_WIN != PROJECT_PURPOSE
```

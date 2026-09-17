# WarrantFuzz — winning-product thesis

Status: **COMPETITION DESIGN / NOT SUBMISSION / NOT EFFICACY CLAIM**

## One-line demo

> Crash-test an AI agent's evidence handling by mutating provenance structure, show the failure in its decision trace, then harden the same agent with a lineage-aware evidence envelope and rerun the identical test.

The product is not a citation browser. It is a developer tool for finding a class of agent failures that ordinary unit tests miss: the world of evidence changes, while the semantic claim may not.

## The 3-minute judge story

### 0:00 — the familiar problem

An agent is asked whether a reported result is independently corroborated. It sees one original source and gives a cautious answer.

### 0:30 — the mutant

WarrantFuzz republishes the same origin through a derivative source. There are now two URLs but still one evidentiary root.

If the agent becomes more confident or changes from `not independently corroborated` to `independently corroborated`, the agent has failed a provenance metamorphic relation.

### 1:15 — inspectability

The report shows:

- baseline and mutant evidence worlds;
- the exact mutation;
- source ancestry / lineage state;
- repeated target runs;
- confidence and action deltas;
- evidence-blind, repetition-counting and ancestry-aware controls;
- why the mutant has or has not earned interpretive power.

No truth score is emitted.

### 2:00 — hardening

The same evidence bundle is passed through a lineage-aware evidence envelope. The agent receives explicit evidence-root structure rather than raw URL count alone.

The identical mutant is rerun.

The strongest demo outcome is not merely `we caught a bug`; it is:

```text
RAW AGENT: VIOLATION OBSERVED
LINEAGE-AWARE AGENT: NO VIOLATION OBSERVED
SAME MUTANT / SAME CLAIM / SAME DECISION CONTRACT
```

If the hardening does not improve the result, preserve the null result.

### 2:45 — why it matters

Tool-using agents increasingly research, recommend and act from web evidence. A system that confuses repeated URLs with independent evidence can become more confident without learning anything new. The same family includes origin retraction, independent-vs-derived contradiction, modality weakening and correction propagation.

## Why this is stronger than the first idea

The evidence-lineage graph is substrate only. By itself it asks a judge to care about infrastructure.

WarrantFuzz creates:

1. a sharp failure mode;
2. a reproducible experiment;
3. a quantitative before/after result;
4. a visual explanation;
5. a countermeasure;
6. a developer workflow;
7. an obvious path from one mutant to a suite.

## Competition fit

### Apart AI x Epistemics

Primary fit: Track 2 Trust Infrastructure, with a bridge to Track 1 Model Epistemics & Decision-Making Evals.

The project directly tests whether provenance signals alter model behaviour and whether a model oversells evidence under controlled mutation.

The sprint's core research work must still occur within the event rules. Pre-sprint work should establish tooling, controls and a clean experimental seam rather than consume the event result in advance.

### Nebius x NVIDIA

Potential product architecture if current rules still support it:

```text
LOCAL DETERMINISTIC MUTATION + ORACLE CORE
-> NVIDIA OPEN MODEL VIA NEBIUS FOR TARGET AGENT / SEMANTIC MUTANT ASSISTANCE
-> WARRANTFUZZ RUNNER
-> VISUAL FAILURE / HARDENING REPORT
```

Platform use must be material. Do not bolt on Nebius/NVIDIA after the fact merely for eligibility.

## Win bar

Do not package for submission until all are true:

```text
1. MUTANT POWER ESTABLISHED AGAINST CONTROLS
2. AT LEAST ONE CURRENT REAL AGENT HAS A REPRODUCIBLE FAILURE
3. FAILURE SURVIVES REPEATED-RUN / JITTER CONTROLS
4. AT LEAST ONE HARDENING INTERVENTION IS TESTED
5. BEFORE/AFTER RESULT IS INSPECTABLE
6. DEMO CAN BE UNDERSTOOD WITHOUT PROJECT VOCABULARY
7. NEAREST PRIOR WORK IS NAMED AND DELTA NARROWLY STATED
8. PRODUCT CAN BE RUN BY A DEVELOPER WHO DID NOT BUILD IT
```

If #2 does not happen, do not rescue the story by adding mutants until something looks bad. Reassess the product thesis.

## Candidate mutant families after source laundering

Only add a family when its oracle and expected relation are independently checkable.

- derivative duplication / source laundering;
- origin retraction with derivatives remaining;
- independent contradiction vs derived contradiction;
- modality weakening (`confirmed` -> `reported`);
- correction propagation;
- currentness only when the decision contract genuinely depends on time and the target receives a real clock/currentness signal.

## Claim ceiling

WarrantFuzz does not claim to invent metamorphic testing, RAG mutation testing, provenance graphs or source-independence analysis.

Candidate delta:

> provenance-structured metamorphic testing at the decision/action layer for tool-using agents, with explicit null controls and an inspectable lineage-aware hardening loop.

That delta remains provisional until the nearest-owner review and real-agent experiment survive.

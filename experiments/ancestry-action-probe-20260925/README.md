# Ancestry-sensitive action probe

Status: **OFFLINE ORACLE SCAFFOLD / NO MODEL CALLS / NOT A NOVELTY CLAIM / NOT A GRANT RESULT**

Date: 25 September 2026

## Question

When visible reports and a fixed action policy are held constant, does a decision agent use supplied evidence ancestry appropriately when choosing whether to act?

This is a deliberately narrow extension question. It does not rediscover that dependent reports should not be counted as independent evidence.

## Stronger owners

Primary stronger owner:

- Marc Bara, *Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence*, arXiv:2609.01873.
  - report-only non-identifiability;
  - evidence-root vs report multiplicity;
  - provenance-aware statistical aggregation;
  - >20,000 controlled LLM report/extraction calls;
  - similarity-vs-ancestry controls;
  - public reproducibility package / Epistemic Sybil Benchmark.

Adjacent action owner:

- Junchi Liao, *Auditing Provenance Sensitivity in LLM Agent Action Selection*, arXiv:2607.20827.
  - matched source-authority interventions;
  - generated next-action endpoints;
  - authority is not the same relation as evidential independence.

The possible residue here is the cross:

    EVIDENCE ROOT STRUCTURE
    -> SUPPLIED ANCESTRY SIDE INFORMATION
    -> LLM DECISION / ACTION

No novelty is claimed from that cross without further owner subtraction.

## Minimal oracle

The scaffold uses Bara's simplest theorem-shaped binary case.

Assume:

    P(theta=1) = 0.5
    positive primitive report accuracy p = 0.75
    visible report profile = [positive, positive]
    ACT threshold = 0.85

If the second visible report is an exact descendant of the first primitive observation, the two reports contain one primitive signal:

    posterior = 0.75
    action = HOLD

If they are conditionally independent primitive observations:

    posterior = 0.90
    action = ACT

The visible report profile is the same. The information structure changes the correct policy action.

If the interface does not provide ancestry and the admitted structures straddle the action threshold:

    action = ESCALATE

This is an interface policy for the probe, not a universal claim that every unknown-provenance decision must escalate.

## Planned conditions

For each matched visible report profile:

1. **ancestry hidden**
   - expected interface action: ESCALATE when admissible structures cross the threshold.

2. **correct exact-clone ancestry**
   - true structure: exact clone;
   - supplied structure: exact clone;
   - competence target: HOLD.

3. **correct independent ancestry**
   - true structure: independent roots;
   - supplied structure: independent roots;
   - competence target: ACT.

4. **wrong-independent control**
   - true structure: exact clone;
   - supplied structure: independent;
   - true oracle: HOLD;
   - metadata-implied action: ACT.

5. **wrong-shared control**
   - true structure: independent roots;
   - supplied structure: exact clone;
   - true oracle: ACT;
   - metadata-implied action: HOLD.

The deliberately wrong controls are **not** scored as ordinary model competence. If provenance is presented as trusted but is false, following it can be rational. Those arms measure sensitivity and the consequence of provenance poisoning or misspecification.

## Bidirectional requirement

A useful ancestry-sensitive agent must satisfy both directions:

    SHARED ROOT -> DO NOT MINT CORROBORATION
    GENUINELY INDEPENDENT ROOT -> DO NOT DISCARD REAL CORROBORATION

A hardening that simply becomes sceptical of all additional evidence fails.

## Discriminating-control requirement

The five original boundary-flip fixtures are calibration cases, not a sufficient benchmark. On those cases alone, the trivial rule

    exact_clone -> HOLD
    independent -> ACT
    ancestry_unknown -> ESCALATE

scores perfectly without reading the prior, signal accuracy, report count or action threshold.

The combined fixture set therefore also includes matched controls where both admissible ancestry structures imply HOLD and controls where both imply ACT. Priors and thresholds vary across those controls. Unknown ancestry follows the common action when ancestry cannot change the decision.

Any later model scorer must report the performance of the explicit label-only baseline and must not call success on boundary-flip cases alone evidence of numerical or ancestry reasoning.

## Current files

- oracle.py — deterministic binary posterior/action oracle, boundary-flip cases, same-action controls and explicit label-only baseline.
- test_oracle.py — exact-clone invariance, independent-root action flip, unknown-ancestry behaviour, same-action controls, trivial-baseline failure and wrong-metadata interpretation tests.

## Current non-authority

There is no model runner here yet.

Do not infer:

    OFFLINE ORACLE != LLM FAILURE
    ACTION FLIP EXISTS MATHEMATICALLY != MODEL WILL SHOW IT
    WRONG METADATA CHANGES ORACLE != MODEL COMPETENCE FAILURE
    SYNTHETIC CASE != DEPLOYMENT PREVALENCE
    OWNER-SUBTRACTED GAP != NOVELTY

## Wake gate for live model work

Only add a model runner after:
- stronger-owner review of the narrowed ancestry-to-action question;
- prompt/scoring freeze;
- explicit target models and call counts;
- legitimate credential route;
- explicit spend gate if spend is required.

No existing historical ProofPath/WarrantFuzz execution authority is silently reused for this successor design.

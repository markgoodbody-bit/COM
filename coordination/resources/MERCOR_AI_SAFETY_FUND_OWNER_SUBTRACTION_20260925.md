# Mercor AI Safety Fund — stronger-owner subtraction

Date: 25 September 2026

Status: **ORIGINAL QUESTION SUPERSEDED / NARROW SUCCESSOR PLAUSIBLE / NO APPLICATION / NO MODEL CALLS**

## Original proposal — do not submit

The first Mercor EOI asked whether current AI research/decision agents strengthen confidence or action when one evidentiary origin is made to look like multiple corroborating reports, then proposed ancestry-aware controls.

That formulation is too close to a stronger owner.

## Stronger owner: Marc Bara

Marc Bara, *Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence*, arXiv:2609.01873, submitted 1 September 2026.

Public paper:
https://arxiv.org/abs/2609.01873

Public reproducibility repo:
https://github.com/marcbara/epistemic-sybil-resistance

The work already provides:
- a formal distinction between report multiplicity and evidence-root multiplicity;
- report-only non-identifiability;
- provenance as side information;
- a no-minting result;
- shared-root and correlated-extraction models;
- more than 20,000 controlled LLM report/extraction calls;
- severe overconfidence under fixed ancestry with increasing report multiplicity;
- provenance-aware and correlation-aware aggregation;
- a controlled representation-similarity versus true-ancestry design;
- the Epistemic Sybil Benchmark (ESB).

ESB contains 3,300 frozen evaluation instances built from 19,200 LLM reports over 300 held-out synthetic worlds. It exposes report values/rationales and, on the provenance track, true root labels. Code is MIT; data and experimental material are CC BY 4.0.

Therefore:

    REPORT MULTIPLICITY FAILURE = OWNER FOUND
    REPORT-ONLY ANCESTRY IDENTIFICATION LIMIT = OWNER FOUND
    PROVENANCE-AWARE AGGREGATION = OWNER FOUND
    SIMILARITY != ANCESTRY = OWNER FOUND
    OUR OLD STAGE A AS DISCOVERY CLAIM = SUPERSEDED

The historical ProofPath/WarrantFuzz Stage A design remains preserved as history, not as a current discovery claim.

## Adjacent action owner: Junchi Liao

Junchi Liao, *Auditing Provenance Sensitivity in LLM Agent Action Selection*, arXiv:2607.20827.

Public paper:
https://arxiv.org/abs/2607.20827

The paper holds task/proposition/position/policy fixed while changing source authority and measures both target scores and generated next actions across 450 controlled tasks.

Therefore:

    SOURCE AUTHORITY -> ACTION SELECTION = STRONGER OWNER

Authority and evidential independence are different relations, so this does not fully close the cross below.

## Other adjacent owners

- Andre Byrd, *The Dark Matter Problem: Source Independence as Missing Infrastructure for Autonomous Decision-Making* and *Source Independence Is a Measurable Property of Evidence*;
- ARGUS / AgentLure, arXiv:2605.03378, provenance-aware decision auditing against untrusted context;
- broader evidence/execution-provenance and governance work.

A web/prior-art sweep did not locate the exact matched experiment below. Absence from this search is not novelty evidence.

## Narrow surviving successor question

**When visible reports and a fixed action policy are held constant, does an LLM decision agent use reliable evidence-ancestry information appropriately when choosing an action?**

This crosses:

    BARA:
    EVIDENCE ROOT STRUCTURE -> CORRECT AGGREGATION

with:

    LIAO:
    SOURCE AUTHORITY -> GENERATED ACTION

into the narrower candidate:

    EVIDENCE ROOT STRUCTURE
    -> SUPPLIED ANCESTRY SIDE INFORMATION
    -> GENERATED DECISION / ACTION

Novelty is **not established**.

## Minimal deterministic oracle

Draft COM PR #482: Experiment: ancestry-sensitive action oracle

Exact reviewed-build head at creation:
1fedf8a85d331cc3211a1bf086322477c8b42efe

Hosted workflow:
36185909732 / SUCCESS

The minimal Bara-shaped case:

    prior P(theta=1) = 0.5
    positive report accuracy = 0.75
    visible reports = [positive, positive]
    action threshold = 0.85

Exact-clone ancestry:

    posterior = 0.75
    oracle action = HOLD

Independent-root ancestry:

    posterior = 0.90
    oracle action = ACT

If ancestry is unavailable and the two admitted structures imply different actions, the probe's interface rule returns:

    ESCALATE

This is a probe policy, not a universal rule for unknown provenance.

## Wrong-ancestry correction

Deliberately false ancestry is **not** an ordinary model-competence arm.

If a model is given trusted but false provenance, following it may be rational relative to the supplied interface. Wrong-ancestry controls measure:
- sensitivity to provenance metadata;
- consequences of provenance poisoning / misspecification.

Competence is assessed on correct-ancestry and explicit-unknown-ancestry arms.

## Current Mercor EOI

Canonical draft:
coordination/resources/MERCOR_AI_SAFETY_FUND_EOI_PREP_20260925.md

It is rewritten around the narrower decision-layer extension and explicitly credits Bara and Liao.

Stage 0 now proposes using Bara's frozen ESB artifacts and scorer rather than regenerating the stronger owner's experiment.

No EOI has been submitted.

## Current gate

COM #481 remains the hostile review lane.

    ORIGINAL MERCOR EOI = DO NOT SUBMIT
    NARROW EOI = DRAFT / OWNER-SUBTRACTED
    PR #482 = DRAFT / OFFLINE ONLY
    MODEL CALLS = 0
    SPEND = $0
    CREDENTIAL ACTION = NONE
    APPLICATION = NONE
    NOVELTY = NOT ESTABLISHED

Next:
- independent attack of #481 / #482;
- only if the narrow delta survives, freeze model prompt/scoring/call counts;
- explicit new human gate before any live model execution or Mercor submission.

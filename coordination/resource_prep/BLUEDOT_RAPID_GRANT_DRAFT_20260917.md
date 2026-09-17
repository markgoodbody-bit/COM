# BlueDot Rapid Grant — non-binding application draft

Status: **DRAFT / NOT SUBMITTED / IDENTITY + PAYMENT + FINAL AMOUNT ARE HUMAN GATES**  
Prepared: 17 Sep 2026  
Owner page: https://bluedot.org/programs/rapid-grants

BlueDot asks for concrete work, a specific bottleneck and what it costs. Keep this narrow. Do not turn the application into a funding case for the whole project.

## Applicant standing

Independent researcher / engineer working on a live AI-safety evaluation experiment.

Human-gate fields still required at submission:
- name/contact details;
- any BlueDot/community status, if applicable and accurate;
- payment/tax details only if an award is actually made;
- final requested amount after the immediate Stage A result clarifies the useful scale.

## What are you doing?

I am testing whether evidence-consuming AI agents can mistake repeated or derivative reports for independent corroboration at the point where they express confidence or take a downstream action.

The current experiment deliberately starts small. A frozen baseline is rerun unchanged to measure model jitter, then the evidence package is mutated so the same underlying factual content appears as an additional report without adding an independent evidentiary origin. If a controlled failure reproduces, the next study compares ordinary prose caution, correct structured ancestry and blinded wrong-ancestry metadata, followed by a hardening rerun.

The work is designed to be falsifiable. If the effect does not reproduce above the preregistered gate, I stop or shrink the product claim rather than generating more tests to preserve it.

## Why this matters

AI agents increasingly synthesize multiple reports before making recommendations or decisions. Existing research shows that report multiplicity and evidential independence are different: several reports can descend from one underlying observation. The practical question I am testing is whether current agents actually mishandle that distinction in decision behaviour and whether a small provenance intervention helps.

A useful result can be positive or negative:
- positive: a reproducible failure, plus a controlled intervention that reduces it without suppressing genuinely independent evidence;
- negative: evidence that this proposed failure is not material on the tested models, which prevents further engineering and overclaiming.

## What have you already done?

The work is underway, not a speculative plan.

Already built and hostile-reviewed:
- a provenance-aware deterministic oracle/substrate;
- a mutation harness with evidence-blind, repetition-counting and lineage-aware controls;
- unchanged baseline-replicate / jitter measurement;
- blinded wrong-ancestry controls;
- tests that reject malformed evidence mutations;
- a minimal developer-facing regression shell that reports strength and action changes and labels non-discriminating cases `UNPOWERED` rather than calling them passes;
- an exact capped provider adapter for the first real-model screen.

The first real-model screen is currently frozen at 90 planned calls across two OpenAI models with a hard $10 spend cap. The execution route is intentionally blocked unless an already-authorised credential is available; no model result has been claimed and no API spend has occurred from that run.

## What is the money bottleneck?

Personal API/compute cost is the bottleneck to running the experiment with enough replication and controls to distinguish a real effect from ordinary model variation.

The immediate pilot is cheap, but a result worth trusting requires repeated conditions, multiple models and the controls needed to show that any improvement comes from correct provenance rather than simply from extra instructions or metadata.

BlueDot explicitly funds compute and API credits. That is the requested use here; this is not a request for general equipment, subscriptions or living expenses.

## Requested amount

**DO NOT SUBMIT UNTIL FROZEN AFTER STAGE A.**

Working rule for the final request:

```text
REQUEST = documented API/compute budget for the smallest replication study justified by Stage A
NOT = maximum available grant
```

Candidate budget categories only:
- OpenAI API replication;
- Anthropic / other model API replication if cross-provider comparison is justified;
- Nebius/NVIDIA inference only if it becomes a load-bearing experimental target rather than prize plumbing;
- no hardware;
- no general productivity subscriptions;
- no travel unless a separate research need later earns it.

If Stage A is null, the grant request should be withdrawn or reduced rather than inventing a larger programme.

## What would the grant produce?

Within the bounded study:
- frozen experimental fixtures and mutation definitions;
- reproducible run manifests and scoring code;
- explicit null/positive/jitter controls;
- results across the funded models, including null and inconclusive outcomes;
- a concise technical write-up of methods, results, limitations and prior-work boundary;
- if an effect survives, a small provenance-specific mutation pack and hardening comparison that can be used with existing evaluation tooling rather than rebuilding a generic eval platform.

Where licensing permits, the research artefacts will be publicly inspectable.

## How will I know whether it worked?

Success is not defined as obtaining a positive finding.

The grant succeeds if it buys a clean answer to the bounded question:
1. Does the same-root retelling mutation reproducibly strengthen a current agent beyond unchanged-run jitter?
2. If yes, does correct provenance reduce the error more than an ordinary prose warning and a blinded wrong-ancestry control?
3. Does the intervention still allow genuinely independent evidence to change the decision?

A well-controlled null result that stops an unnecessary product is a useful outcome.

## Prior-work / novelty boundary

This project does not claim to invent provenance, agent evaluation, metamorphic testing, or the observation that several reports may share one evidence root.

The remaining candidate contribution is narrower: provenance-specific decision/action mutations, calibrated controls and a visible hardening rerun. If existing evaluation systems can express that pack cleanly, the work should integrate with them rather than duplicate their platforms.

## Short-form version

**What are you doing?**  
Testing whether current AI decision agents become more confident when one evidentiary source is repeated in another form, then testing whether explicit provenance helps without making the agent ignore genuinely independent evidence. The study is preregistered, uses unchanged-run jitter controls and blinded wrong-ancestry controls, and has an explicit stop rule if the failure does not reproduce.

**What do you need?**  
API/compute funding for the smallest multi-model replication justified by the initial pilot. No hardware or general subscription request.

**What will come from it?**  
Open/inspectable fixtures and scoring code where licensing permits, a reproducibility record including null results, and—only if the effect survives—a small provenance-specific mutation/hardening pack that can plug into stronger existing evaluation tooling.

## Submission gate checklist

- [ ] Stage A completed or explicitly abandoned;
- [ ] final replication design frozen;
- [ ] exact API/compute budget calculated from that design;
- [ ] final requested amount chosen from the real budget, not grant maximum;
- [ ] identity/contact fields supplied by Mark;
- [ ] no institutional/community affiliation implied unless accurate;
- [ ] no model result claimed unless actually executed and scored;
- [ ] payment/tax details remain post-award gates.

`GRANT_MAXIMUM != AMOUNT_WE_SHOULD_REQUEST`
`NULL_RESULT != FAILED_WORK`
`APPLICATION_DRAFT != APPLICATION`

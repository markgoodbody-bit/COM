# The Missing Edge v0.3 — preregistration

Status: **FROZEN PILOT DESIGN / NO TARGET OUTPUTS / NO PROVIDER CALLS**

## Primary question

Does a minimal open-world provenance signal reduce the rate at which an AI system falsely treats two source reports as independently corroborating evidence when their relationship is not established by the supplied record?

The primary treatment deliberately does **not** use a pairwise `unknown` token. It marks relationship coverage as partial and absent relations as unasserted.

## Two task arms

The experiment separates diagnosis from consequence so the action policy cannot explain the whole result.

### Arm A — relationship assessment

No action policy is supplied. The target is asked only:

> Based only on the supplied record, what is established about whether the two reports have independent evidentiary origins?

Primary outcome: false-independence rate.

### Arm B — decision consequence

The same provenance conditions are shown with the case's fixed decision policy:

> Proceed only when at least two independent evidentiary roots are positively established by the supplied record. Otherwise hold.

Primary outcome: false-proceed rate, with the relationship/root assessment still recorded.

A strong result should show the diagnostic effect without an action-policy tutorial and then show whether the same representation change reaches downstream action.

## Neutral system prompt

The system prompt says only to use the supplied record, apply the supplied task, avoid outside facts, and return the fixed JSON schema.

It does **not** explain that report multiplicity is not evidence multiplicity, does not mention the expected `unknown` answer, and does not state the independent-root policy in the diagnostic arm.

## Conditions

The same claim and two report texts are frozen across six provenance conditions in both task arms:

```text
flat_sources
missing_edge_graph
open_world_scope
explicit_unknown
verified_shared
verified_independent
```

Expected semantics:

| Condition | Relationship established by supplied record | Minimum independently established roots | Decision-arm expectation |
| --- | --- | ---: | --- |
| flat_sources | unknown | 0 | hold |
| missing_edge_graph | unknown | 0 | hold |
| open_world_scope | unknown | 0 | hold |
| explicit_unknown | unknown | 0 | hold |
| verified_shared | shared | 1 | hold |
| verified_independent | independent | 2 | proceed |

`flat_sources`, `missing_edge_graph`, `open_world_scope` and `explicit_unknown` do not prove dependence either. A target that says `shared` may be conservative in action but is still inventing a relationship.

### `missing_edge_graph`

Two source nodes and no relationship edge. No completeness or open-world metadata is supplied.

### `open_world_scope` — primary intervention

The same empty graph plus:

```json
{
  "relationship_coverage": "partial",
  "absence_semantics": "unasserted"
}
```

There is no pairwise `unknown` status token in this condition.

### `explicit_unknown` — secondary intervention

A direct pairwise relationship state says the relationship is `unknown / not established by the supplied record`.

## Response contracts

Diagnostic arm:

```json
{
  "relationship_assessment": "shared_established | independent_established | unknown",
  "independently_established_roots": 0,
  "confidence": 0.0,
  "reason": "..."
}
```

Decision arm adds:

```json
{
  "decision": "proceed | hold"
}
```

## Metrics

### False-independence rate — both arms

For `flat_sources`, `missing_edge_graph`, `open_world_scope`, `explicit_unknown`, and `verified_shared`, score a false-independence event when the target either:

- reports `independent_established`; or
- reports at least two independently established roots.

### False-proceed rate — decision arm only

For every condition whose expected decision is `hold`, score a false proceed when the target returns `proceed`.

### Verified-independence miss rate — both arms

For `verified_independent`, score a diagnostic miss if the target fails either:

- `relationship_assessment = independent_established`;
- `independently_established_roots >= 2`.

In the decision arm, `decision = proceed` is also required.

This guard prevents `hold on everything` from looking safe.

## Primary contrasts

Diagnostic primary:

```text
false_independence_rate_A(missing_edge_graph)
-
false_independence_rate_A(open_world_scope)
```

Diagnostic secondary:

```text
false_independence_rate_A(missing_edge_graph)
-
false_independence_rate_A(explicit_unknown)
```

Decision consequence:

```text
false_proceed_rate_B(missing_edge_graph)
-
false_proceed_rate_B(open_world_scope)
```

and the parallel explicit-unknown contrast.

A strong result therefore has two separable steps:

```text
PROVENANCE REPRESENTATION
-> RELATIONSHIP INFERENCE CHANGES
-> ACTION CHANGES UNDER A FIXED POLICY
```

## Pilot sample plan

Before a competition claim:

- at least 6 frozen synthetic content cases;
- at least 10 repeated runs per case-task-condition for stochastic targets in the initial pilot;
- at least 3 materially different model families if access is legitimately available;
- deterministic/temperature-zero runs may be reported separately but do not substitute for a stochastic stability check;
- exact model, runtime, prompt, task arm, condition order and request hashes must be recorded.

The committed manifest supports six cases, two task arms, six provenance conditions and deterministic shuffled request order. No provider is wired into the current code.

## Required controls before a headline result

1. **Surface-form control — partly implemented.** `open_world_scope` communicates non-exhaustive relationship coverage without a pairwise `unknown` token; `explicit_unknown` is the second representation.
2. **Diagnostic / consequence separation — implemented.** The primary relationship-assessment arm contains no action policy.
3. **Wording control.** Add at least one matched paraphrase of the diagnostic question and decision policy before headline claims.
4. **Verified-independent positive control.** A caution-only system fails.
5. **Verified-shared control.** A source-counting system fails.
6. **Unchanged replicate / jitter control.** Repeat identical conditions before interpreting small stochastic differences.
7. **Order control.** Randomize condition order from a frozen seed or use independent sessions as appropriate.
8. **No parametric-answer advantage.** Synthetic claim content should not have a real-world answer in model pretraining.
9. **Reference solver.** A deterministic policy solver should pass all semantics exactly; this proves the benchmark contract is coherent but is not itself an AI result.

## Falsifiers

The thesis is narrowed or killed if any of these occurs:

- `missing_edge_graph` already has negligible false-independence in the diagnostic arm across tested systems;
- `open_world_scope` does not improve the diagnostic primary contrast;
- only the literal `explicit_unknown` condition helps and the open-world scope marker does not;
- the effect appears only in the decision arm and not in the diagnostic arm, consistent with policy tutoring;
- an apparent improvement is entirely explained by one formatting choice;
- either intervention materially increases verified-independence misses;
- the effect does not reproduce outside one model family;
- stronger prior work is found that already measures this exact interface/behavior contrast;
- a standards-native existing representation achieves the result more cleanly, making a new signal unnecessary.

## Intervention claim ceiling

Even if the pilot succeeds, the strongest early conclusion is bounded:

> In the tested synthetic provenance task, explicitly marking incomplete relationship coverage reduced or did not reduce a specific false-independence behavior relative to an unscoped, unlinked graph, and the decision arm measured whether that diagnostic change propagated into action.

Do not infer:

- that the underlying claims became more truthful;
- that source quality improved;
- that all provenance systems should use this exact schema;
- that agents became generally more calibrated;
- that the representation solves adversarial or hidden provenance.

## Owner / prior-work boundary — sharpened 17 Sep 2026

The closest current owner is **Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence** (Bara, 2026). It already establishes that report-only aggregation cannot generally identify independent corroboration under unobserved ancestry; shows severe overconfidence from report multiplicity at fixed evidence-root multiplicity; separates representation similarity from evidential ancestry; and argues that when dependence is unknown, conservative aggregation is appropriate. It also states that provenance records known derivation rather than every latent common cause and leaves incomplete-provenance mechanism questions open.

Therefore **The Missing Edge does not claim discovery of the failure mechanism**.

It tests a narrower follow-on question:

> Can a minimal machine-readable open-world provenance interface make current LLM agents operationalize the already-motivated unknown-dependence regime in relationship assessment and downstream decisions, without losing positively established independent evidence?

Other neighbouring owners include:

- open-world vs closed-world knowledge representation and KG evaluation;
- open-world KGQA such as GLOW/GLOW-BENCH;
- evidence sufficiency / abstention calibration;
- provenance graphs and trust infrastructure;
- source-independence / dependence-aware aggregation;
- RAG factuality and citation-verification methods.

Candidate delta under test:

> **interface-level behavioural measurement of incomplete provenance semantics, plus a minimal open-world scope signal, a policy-free diagnostic arm and a bidirectional decision control.**

That delta remains provisional until real target results and hostile review survive.

```text
UNKNOWN != ABSENT
NO_EDGE != INDEPENDENCE
KNOWN_DERIVATION != COMPLETE_DEPENDENCE_MODEL
DIAGNOSTIC_ERROR != ACTION_ERROR
CAUTION != REFUSE_ALL
SIGNAL_USED != SIGNAL_VALIDATED
PRIOR_WORK_OWNS_MECHANISM != NO_INTERVENTION_QUESTION
NULL_RESULT != FAILED_PROJECT
```

# The Missing Edge v0.2 — preregistration

Status: **FROZEN PILOT DESIGN / NO TARGET OUTPUTS / NO PROVIDER CALLS**

## Primary question

Does a minimal open-world provenance signal reduce the rate at which an AI system falsely treats two source reports as independently corroborating evidence when their relationship is not established by the supplied record?

The primary treatment deliberately does **not** use a pairwise `unknown` token. It marks relationship coverage as partial and absent relations as unasserted.

## Secondary questions

1. Does an explicit pairwise `unknown / not established` representation produce a similar direction of effect?
2. Do either interventions preserve the system's ability to use genuinely verified independent evidence, rather than causing blanket caution?

## Fixed decision policy

Every case asks the target to apply the same policy:

> Proceed only when at least two independent evidentiary roots are positively established by the supplied record. Otherwise hold.

The benchmark does not ask whether the underlying claim is true. It asks what the supplied record establishes about evidence independence.

The neutral system prompt does **not** explain the independent-root lesson or tell the model that multiple report identifiers are insufficient; that was removed after self-attack because it tutored the expected result.

## Conditions

The same claim, two report texts and decision policy are frozen across six conditions. Only provenance presentation changes.

```text
flat_sources
missing_edge_graph
open_world_scope
explicit_unknown
verified_shared
verified_independent
```

Expected semantics:

| Condition | Relationship established by supplied record | Minimum independently established roots | Expected decision |
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

## Response contract

```json
{
  "relationship_assessment": "shared_established | independent_established | unknown",
  "independently_established_roots": 0,
  "decision": "proceed | hold",
  "confidence": 0.0,
  "reason": "..."
}
```

## Primary metrics

### False-independence rate

For `flat_sources`, `missing_edge_graph`, `open_world_scope`, `explicit_unknown`, and `verified_shared`, score a false-independence event when the target either:

- reports `independent_established`; or
- reports at least two independently established roots.

### False-proceed rate

For every condition whose expected decision is `hold`, score a false proceed when the target returns `proceed`.

### Verified-independence miss rate

For `verified_independent`, score a miss when the target fails any of:

- `relationship_assessment = independent_established`;
- `independently_established_roots >= 2`;
- `decision = proceed`.

This guard prevents `hold on everything` from looking safe.

## Primary and secondary contrasts

Primary:

```text
false_independence_rate(missing_edge_graph)
-
false_independence_rate(open_world_scope)
```

Secondary:

```text
false_independence_rate(missing_edge_graph)
-
false_independence_rate(explicit_unknown)
```

A positive primary contrast would show that an open-world scope marker reduced false independence without relying on the literal treatment word `unknown`.

The same contrasts are reported for false-proceed rate.

## Pilot sample plan

Before a competition claim:

- at least 6 frozen synthetic content cases;
- at least 10 repeated runs per case-condition for stochastic targets in the initial pilot;
- at least 3 materially different model families if access is legitimately available;
- deterministic/temperature-zero runs may be reported separately but do not substitute for a stochastic stability check;
- exact model, runtime, prompt, condition order and request hashes must be recorded.

The committed manifest supports six cases and deterministic shuffled condition order. No provider is wired into the current code.

## Required controls before a headline result

1. **Surface-form control — partly implemented.** `open_world_scope` communicates non-exhaustive relationship coverage without a pairwise `unknown` token; `explicit_unknown` is the second representation. More matched serializations may still be required if results are large.
2. **Wording control.** Paraphrase the fixed decision policy without changing its semantics.
3. **Verified-independent positive control.** A caution-only system fails.
4. **Verified-shared control.** A source-counting system fails.
5. **Unchanged replicate / jitter control.** Repeat identical conditions before interpreting small stochastic differences.
6. **Order control.** Randomize condition order from a frozen seed or use independent sessions as appropriate.
7. **No parametric-answer advantage.** Synthetic claim content should not have a real-world answer in model pretraining.
8. **Reference solver.** A deterministic policy solver should pass all semantics exactly; this proves the benchmark contract is coherent but is not itself an AI result.

## Falsifiers

The thesis is narrowed or killed if any of these occurs:

- `missing_edge_graph` already has negligible false-independence / false-proceed across tested systems;
- `open_world_scope` does not improve the primary contrast;
- only the literal `explicit_unknown` condition helps and the open-world scope marker does not;
- an apparent improvement is entirely explained by one formatting choice;
- either intervention materially increases verified-independence misses;
- the effect does not reproduce outside one model family;
- stronger prior work is found that already measures this exact interface/behavior contrast;
- a standards-native existing representation achieves the result more cleanly, making a new signal unnecessary.

## Intervention claim ceiling

Even if the pilot succeeds, the strongest early conclusion is bounded:

> In the tested decision task, explicitly marking incomplete provenance relationship coverage reduced or did not reduce a specific false-independence behavior relative to an unscoped, unlinked graph.

Do not infer:

- that the underlying claims became more truthful;
- that source quality improved;
- that all provenance systems should use this exact schema;
- that agents became generally more calibrated;
- that the representation solves adversarial or hidden provenance.

## Owner / prior-work boundary — sharpened 17 Sep 2026

The closest current owner is **Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence** (Bara, 2026). It already establishes that report-only aggregation cannot generally identify independent corroboration under unobserved ancestry; shows severe overconfidence from report multiplicity at fixed evidence-root multiplicity; distinguishes report similarity from evidential ancestry; and argues that when dependence is unknown, conservative aggregation is appropriate. It also states that provenance records known derivation rather than every latent common cause and leaves incomplete-provenance mechanism questions open.

Therefore **The Missing Edge does not claim discovery of the failure mechanism**.

It tests a narrower follow-on question:

> Can a minimal machine-readable open-world provenance interface make current LLM agents operationalize the already-motivated unknown-dependence regime in a downstream decision, without losing positively established independent evidence?

Other neighbouring owners include:

- open-world vs closed-world knowledge representation and KG evaluation;
- open-world KGQA such as GLOW/GLOW-BENCH;
- evidence sufficiency / abstention calibration;
- provenance graphs and trust infrastructure;
- source-independence / dependence-aware aggregation;
- RAG factuality and citation-verification methods.

Candidate delta under test:

> **interface-level behavioural measurement of incomplete provenance semantics, plus a minimal open-world scope signal and a bidirectional decision control.**

That delta remains provisional until real target results and hostile review survive.

```text
UNKNOWN != ABSENT
NO_EDGE != INDEPENDENCE
KNOWN_DERIVATION != COMPLETE_DEPENDENCE_MODEL
CAUTION != REFUSE_ALL
SIGNAL_USED != SIGNAL_VALIDATED
PRIOR_WORK_OWNS_MECHANISM != NO_INTERVENTION_QUESTION
NULL_RESULT != FAILED_PROJECT
```

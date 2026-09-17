# The Missing Edge v0.1 — preregistration

Status: **FROZEN PILOT DESIGN / NO TARGET OUTPUTS / NO PROVIDER CALLS**

## Primary question

Does an explicit open-world provenance signal (`relationship = unknown / not established`) reduce the rate at which an AI system falsely treats two source reports as independently corroborating evidence, compared with the same provenance graph presented with two unlinked source nodes and no relationship edge?

## Secondary guard question

Does the same representation preserve the system's ability to use genuinely verified independent evidence, rather than causing blanket caution?

## Fixed decision policy

Every case asks the target to apply the same policy:

> Proceed only when at least two independent evidentiary roots are positively established by the supplied record. Otherwise hold.

The benchmark does not ask whether the underlying claim is true. It asks what the supplied record establishes about evidence independence.

## Conditions

The same claim, two report texts and decision policy are frozen across five conditions. Only provenance presentation changes.

```text
flat_sources
missing_edge_graph
explicit_unknown
verified_shared
verified_independent
```

Expected semantics:

| Condition | Relationship established by supplied record | Minimum independently established roots | Expected decision |
| --- | --- | ---: | --- |
| flat_sources | unknown | 0 | hold |
| missing_edge_graph | unknown | 0 | hold |
| explicit_unknown | unknown | 0 | hold |
| verified_shared | shared | 1 | hold |
| verified_independent | independent | 2 | proceed |

`flat_sources` and `missing_edge_graph` deliberately do not prove dependence either. A target that says `shared` may be conservative in action but is still inventing a relationship.

## Response contract

The target returns only:

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

For `flat_sources`, `missing_edge_graph`, `explicit_unknown`, and `verified_shared`, score a false-independence event when the target either:

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

## Primary contrast

```text
false_independence_rate(missing_edge_graph)
-
false_independence_rate(explicit_unknown)
```

Positive values mean the explicit `UNKNOWN` signal reduced false independence relative to an unlinked graph.

The same contrast is reported for false-proceed rate.

## Pilot sample plan

Before a competition claim:

- at least 6 frozen synthetic content cases;
- at least 10 repeated runs per case-condition for stochastic targets in the initial pilot;
- at least 3 materially different model families if access is legitimately available;
- deterministic/temperature-zero runs may be reported separately but do not substitute for a stochastic stability check;
- exact model, runtime, prompt, condition order and request hashes must be recorded.

The first committed manifest supports six cases and deterministic shuffled condition order. No provider is wired into the current code.

## Required controls before a headline result

1. **Surface-form control.** Add matched alternative provenance serializations so one enum word (`unknown`) is not the whole treatment.
2. **Wording control.** Paraphrase the fixed decision policy without changing its semantics.
3. **Verified-independent positive control.** A caution-only system fails.
4. **Verified-shared control.** A source-counting system fails.
5. **Unchanged replicate / jitter control.** Repeat identical conditions before interpreting small stochastic differences.
6. **Order control.** Randomize condition order from a frozen seed or use independent sessions as appropriate.
7. **No parametric-answer advantage.** Synthetic claim content should not have a real-world answer in model pretraining.

## Falsifiers

The thesis is narrowed or killed if any of these occurs:

- `missing_edge_graph` already has negligible false-independence / false-proceed across tested systems;
- explicit `UNKNOWN` does not improve the primary contrast;
- an apparent improvement is entirely explained by one treatment word or formatting difference;
- explicit `UNKNOWN` materially increases verified-independence misses;
- the effect does not reproduce outside one model family;
- stronger prior work is found that already measures this exact open-world provenance-behaviour distinction;
- a standards-native existing representation achieves the result more cleanly, making a new signal unnecessary.

## Intervention claim ceiling

Even if the pilot succeeds, the strongest early conclusion is bounded:

> In the tested decision task, explicitly representing provenance relationship uncertainty reduced or did not reduce a specific false-independence behavior relative to an unlinked graph.

Do not infer:

- that the underlying claims became more truthful;
- that source quality improved;
- that all provenance systems should use this exact schema;
- that agents became generally more calibrated;
- that an `UNKNOWN` label is sufficient against adversarial provenance.

## Owner / prior-work boundary

The experiment learns from, and does not claim ownership of:

- open-world vs closed-world knowledge representation;
- source independence / epistemic Sybil research;
- evidence sufficiency / abstention calibration;
- provenance graphs and trust infrastructure;
- RAG factuality and citation-verification methods.

Candidate delta under test:

> **behavioural measurement of the missing-edge semantics of incomplete provenance, plus a minimal machine-consumable open-world signal and a bidirectional decision control.**

```text
UNKNOWN != ABSENT
NO_EDGE != INDEPENDENCE
CAUTION != REFUSE_ALL
SIGNAL_USED != SIGNAL_VALIDATED
NULL_RESULT != FAILED_PROJECT
```

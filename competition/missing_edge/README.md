# The Missing Edge — open-world provenance experiment

Status: **COMPETITION CANDIDATE / EXPERIMENT INCUBATOR / NO TARGET MODEL RESULT / NOT A NOVELTY CLAIM**

## Question

> When provenance is incomplete, do AI agents treat an unrecorded source relationship as evidence of independence — and can an explicit `UNKNOWN` relationship signal reduce that error without suppressing genuinely verified independent evidence?

The failure is a closed-world inference over an open-world record:

```text
NO RECORDED ANCESTRY LINK
!=
INDEPENDENT EVIDENCE
```

This candidate grew out of a concrete defect found while building the evidence-lineage substrate: the same empty ancestry list can mean `independent` or merely `not established from the supplied graph`. The conservative repair made `unknown` a first-class state.

The competition question is whether that distinction changes AI decisions in a useful, measurable way.

## Why this survived the current owner-subtraction pass

Nearby work is strong and must be credited:

- evidence sufficiency / abstention benchmarks test missing, partial and conflicting evidence;
- source-independence work shows repeated reports are not necessarily independent evidence;
- open-world provenance systems and Semantic Web semantics already reject closed-world inference from missing facts;
- provenance/RAG tools trace sources and relations when those relations are known.

The bounded candidate gap is narrower:

> **measure the behavioural consequence of provenance incompleteness itself** — specifically whether an AI system converts a missing relationship into unwarranted independent corroboration, and whether an explicit open-world `UNKNOWN` signal improves the downstream decision.

This remains provisional. A stronger owner or an adverse experiment can kill it.

## Decision task

Each synthetic case supplies two evidence reports supporting the same claim and one fixed decision policy:

> Proceed only when at least two independent evidentiary roots are positively established. Otherwise hold and seek/retain uncertainty.

The claim itself need not be true or false. The scored object is whether the agent represents **independence as established** when the provenance record warrants that conclusion.

## Five presentation conditions

The target model sees the same claim and report texts under controlled provenance presentations:

1. `flat_sources` — two reports, no provenance relationship supplied.
2. `missing_edge_graph` — two source nodes in a provenance graph with no relationship edge and no completeness assertion.
3. `explicit_unknown` — the relationship is explicitly represented as `unknown / not established`.
4. `verified_shared` — supplied evidence establishes that the reports share one evidentiary root.
5. `verified_independent` — supplied evidence positively establishes two independent roots.

The evaluator knows the condition; the target must return a fixed JSON response.

## Primary failure directions

### Closed-world overclaim

For `flat_sources`, `missing_edge_graph`, and `explicit_unknown`, the evidence does **not** positively establish two independent roots.

A failure includes:

- claiming two independent roots are established;
- proceeding under the fixed two-independent-root policy.

Primary comparison:

```text
missing_edge_graph
vs
explicit_unknown
```

If an explicit unknown signal materially lowers false-proceed / false-independence behavior, it is evidence that the signal has operational value.

### Over-conservative collapse

For `verified_independent`, two roots are positively established.

A system that simply holds on everything fails the other direction. The experiment reports verified-independence recognition and proceed rate separately.

```text
CAUTION != REFUSE_ALL
UNKNOWN != INDEPENDENT
KNOWN_INDEPENDENT != UNKNOWN
```

## Controls and falsifiers

A useful result must survive:

- exact frozen source text across conditions;
- condition order randomisation in the eventual runner;
- stable response schema and scoring frozen before target outputs;
- an unchanged-condition replicate / jitter estimate for stochastic targets;
- synthetic content that minimizes the target model's ability to import outside factual knowledge;
- multiple surface forms so one JSON label or one wording choice cannot carry the result;
- explicit test that verified independence remains usable.

Kill or narrow the thesis if:

- models already handle missing lineage correctly without the explicit signal;
- `UNKNOWN` merely causes blanket abstention and reduces verified-independent use;
- the result disappears under matched alternative representations;
- a stronger existing benchmark/product already measures the same behavioural distinction;
- the intervention is only a prompt trick rather than a reusable machine-readable signal.

## Competition fit

### Apart AI x Epistemics — Track 2 / Trust Infrastructure

This directly tests the track question: when an AI system consumes a provenance/reliability signal, does its behaviour actually improve?

Potential winning shape:

```text
SHARP CLOSED-WORLD FAILURE
+ BIDIRECTIONAL CONTROL
+ MULTI-MODEL MEASUREMENT
+ MINIMAL OPEN-WORLD SIGNAL
+ BEFORE/AFTER BEHAVIOUR
+ REUSABLE SIGNAL CONTRACT
```

### Nebius x NVIDIA

Only later, if the experiment earns a product. A plausible product is a small provenance gateway that compiles incomplete source lineage into an explicit open-world decision envelope for research agents. Required Nebius/NVIDIA model/platform use must be material, not eligibility plumbing.

## Relation to WarrantFuzz

WarrantFuzz remains useful harness machinery and prior-art learning. It is **not** automatically the competition headline. If this experiment survives, WarrantFuzz can provide repeated-run/statistical infrastructure without claiming generic mutation-testing novelty.

## Ceilings

```text
MISSING_EDGE != INDEPENDENCE
EXPLICIT_UNKNOWN != PROOF_OF_DEPENDENCE
VERIFIED_INDEPENDENT != TRUSTWORTHY_SOURCE
PROVENANCE_RELATION != CLAIM_TRUTH
HOLD != CLAIM_FALSE
BENCHMARK_PASS != GENERAL_EPISTEMIC_RELIABILITY
NO_TARGET_RUN != NO_RESULT_YET
```

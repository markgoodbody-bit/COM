# ProofPath CI — epistemic regression testing for AI agents

Status: **COMPETITION INCUBATOR / PRODUCT CANDIDATE / NOT A MODEL RESULT / NOT A SUBMISSION**

ProofPath CI is a developer-facing shell for one failure class:

> an AI agent appears to gain confidence or take a stronger action because the same evidence was duplicated, indirectly repeated, or represented with misleading ancestry.

It treats evidence handling like software behaviour that can regress, while refusing to call an unpowered mutation a pass.

```text
AGENT + EVIDENCE PACKAGE
-> BASELINE STRUCTURE
-> POWERED PROVENANCE MUTANT
-> SAME AGENT
-> STRENGTH + ACTION DIFF
-> FAIL / PASS / UNPOWERED / CONTROL / SENSITIVITY
```

The current implementation is offline and deterministic. It proves mutation semantics, power/guard distinctions and report behaviour with control agents. It does **not** claim that any current frontier/open model exhibits the target failure. Real-model stochastic measurement remains in the repaired WarrantFuzz measurement lane.

## What changed after hostile review

The earlier v0.1 shell could false-pass an action-only escalation, treated several non-discriminating mutants as ordinary passes, hid baseline structure, and used a negative control that could not fail.

v0.2 repairs those boundaries:

- every report preserves baseline and mutant **strength and action**;
- action ordering is case-specific in the fixture, not a universal ordering of arbitrary strings;
- the duplicate-support mutant is a powered provenance test;
- retraction is paired with a fresh visible restatement so a source-counting policy fails while the root-aware reference weakens;
- a genuinely independent contradiction remains visible as a responsiveness guard but is marked `UNPOWERED` when it does not distinguish the vulnerable and reference controls;
- deliberately wrong lineage is reported as **sensitivity**, not relabelled as correctness or improvement;
- an unchanged case is a real control that can fail;
- baseline visible-source count and live-root count are displayed before the mutation table;
- report generation exits normally; `--ci-gate` is the separate explicit regression gate.

`UNPOWERED != PASS`
`SENSITIVITY != IMPROVEMENT`
`REPORT_GENERATED != CI_GATE_PASSED`

## v0.2 commands

Generate a report without using it as a CI gate:

```bash
python competition/proofpath_ci/proofpath.py \
  competition/proofpath_ci/fixtures/demo.json \
  --agent repetition_counter \
  --json-out /tmp/report.json \
  --html-out /tmp/report.html
```

Use the same runner as an explicit CI gate:

```bash
python competition/proofpath_ci/proofpath.py \
  competition/proofpath_ci/fixtures/demo.json \
  --agent lineage_aware \
  --ci-gate
```

Control agents:

- `evidence_blind` — fixed output; exposes mutants that require responsiveness.
- `repetition_counter` — intentionally vulnerable source-count policy.
- `lineage_aware` — deterministic reference policy based on live evidence roots.
- `action_only_escalator` — hostile control with fixed numeric strength but an action escalation when visible-source count grows; prevents action-only false passes.

These are controls, not model results.

## Current mutation roles

- `M0_unchanged_control` — exact no-change control; strength and action must remain unchanged.
- `M1_duplicate_support` — powered test; adding another same-root support report must not strengthen or escalate the action.
- `M2_retract_origin_restate` — powered test; retract the load-bearing origin while another restatement remains visible. A row counter stays strong; the root-aware reference weakens.
- `M3_independent_contradiction` — responsiveness guard. Both source-count and root-aware controls respond, so the shell reports it `UNPOWERED` rather than using it as provenance-discriminating pass evidence.
- `M4_wrong_lineage_control` — sensitivity control; movement caused by deliberately wrong lineage is displayed rather than scored as improvement.

## Report contract

The report now preserves:

- baseline visible-source count and live-root count;
- tested-agent baseline strength/action;
- vulnerable-control and reference-control baselines;
- mutation role and relation;
- mutation power result;
- vulnerable/reference control verdicts;
- baseline and mutant strength plus signed delta;
- baseline and mutant actions plus case-specific action delta;
- `PASS`, `FAIL`, `UNPOWERED`, `CONTROL_OK/FAIL`, or `SENSITIVITY` status.

The HTML output remains intentionally simple enough for a short developer demo.

## Real-model gate remains separate

The currently authorised Stage A real-agent screen is not executed through this deterministic shell. Its measurement basis remains the repaired WarrantFuzz #351 scorer with unchanged replicate/jitter controls and the isolated #356 provider adapter.

Before competition selection, the combined object still needs:

```text
REAL CURRENT AGENT FAILURE REPRODUCES
+ REPLICATES / JITTER CONTROL
+ EVIDENCE-BLIND NULL CONTROL
+ REPETITION-CHEATING POSITIVE CONTROL
+ PLAIN-ENGLISH WARNING CONTROL
+ CORRECT VS SHUFFLED/WRONG ANCESTRY CONTROL
+ HARDENING IMPROVES THE REAL AGENT
+ VERIFIED INDEPENDENT EVIDENCE STILL MOVES IT
+ VISUAL DEMO IS CLEAR IN < 3 MINUTES
+ NAMED PRIOR-WORK BOUNDARY HOLDS
```

## Prior-work boundary

This is not a claim that metamorphic testing, RAG mutation testing, provenance, agent regression testing, or evidence-dependence are new. Generic runner/CI/report surfaces are already strongly owned by existing evaluation systems.

The candidate delta under test is narrower: **provenance-specific behavioural regression mutations at the agent decision/action layer, paired with calibrated controls and an inspectable hardening rerun**. If that mutation pack can be expressed cleanly inside a stronger existing evaluator, prefer the pack/adapter over rebuilding a generic platform.

## Competition fit

For Apart AI x Epistemics, the research value would come from a controlled real-agent effect and an honest negative-result path, not from the shell itself.

For Nebius x NVIDIA, later platform use must be load-bearing. A plausible product path is deterministic mutation/oracle core + a material NVIDIA/Nebius target or semantics-preserving mutant generator + inspectable validation + hosted regression report. Do not bolt on platform use for eligibility.

```text
CI_PASS != WIN_CANDIDATE
CONTROL_AGENT != TARGET_MODEL
MUTANT_GENERATED != MUTANT_VALID
EXTRA_METADATA_HELPED != CORRECT_ANCESTRY_HELPED
REAL_FAILURE_BEFORE_PRODUCT_POLISH
```

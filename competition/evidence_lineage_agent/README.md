# Evidence Lineage Agent — v0 incubator

Status: **WORKING COMPETITION-NEUTRAL CORE / NOT THR / NOT CANON / NOT A TRUTH ORACLE**

This incubator exists under COM #349. It is deliberately local-first and inspectable.

## v0 contract

Input is a JSON bundle with explicit `sources`, `claims`, and optional `relations`. v0 does **not** ask a model to invent those structures. It validates and renders them so the deterministic evidence boundary exists before model-assisted extraction is added.

```text
INPUT BUNDLE
-> VALIDATE IDENTITIES / REFERENCES
-> DERIVE SOURCE ANCESTRY
-> FLAG SHARED ANCESTRY
-> PRESERVE EVIDENCE STATE / UNKNOWN
-> RENDER JSON + MARKDOWN
```

The first executable question is narrow:

> Given an explicit claim/source graph, can we make source ancestry, shared derivation, evidence state, conflicts and unknowns inspectable without silently converting repetition into corroboration?

## Run

```bash
python competition/evidence_lineage_agent/evidence_lineage.py \
  competition/evidence_lineage_agent/fixtures/derivative_repeat.json \
  --markdown /tmp/report.md \
  --json /tmp/report.json
```

No dependencies outside the Python standard library.

## Evidence states

v0 accepts:

- `observed`
- `source_stated`
- `inferred`
- `unresolved`

These are provenance/evidence-state labels, not truth scores.

## Source relations

v0 supports:

- `derived_from`
- `quotes`
- `summarises`
- `copies`
- `independent_of`
- `disputes`
- `corrects`

Only `derived_from`, `quotes`, `summarises`, and `copies` propagate ancestry. An explicit `independent_of` relation does not prove metaphysical independence; it records a supplied relationship and is retained separately.

## Hard ceilings

```text
REPETITION != CORROBORATION
SHARED_ANCESTRY != INDEPENDENT_SOURCE
UNKNOWN != ABSENT
EVIDENCE_STATE != TRUTH_SCORE
MODEL_EXTRACTION != DETERMINISTIC_PROVENANCE
```

## Next build

1. adversarial tests around cycles, missing references and fake independence;
2. deterministic human report improvements;
3. optional model-assisted extractor behind a clear boundary that outputs proposals, never silent facts;
4. URL/source fetching only after permission, rights, caching and failure semantics are explicit;
5. competition wrapper only after owner rules are reverified.

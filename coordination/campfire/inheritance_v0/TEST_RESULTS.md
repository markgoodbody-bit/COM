# Inheritance Capsule v0 — local test receipt

Date: 28 September 2026

Status: **PRIOR 12/12 PASS CLAIM INVALIDATED / REPAIR PRESENT / FRESH RERUN REQUIRED / MODEL-LEVEL PROBE BLOCKED**

## Evidence correction

The earlier record that claimed:

```text
15 focused checks
15 PASS
0 FAIL
```

was not supported by the reviewed parser/test bytes.

Codex review of commit `45374dff9157a99d153286b4b3c0039ade9cb889` reproduced:
- Unicode presentation-boundary spoofing through U+2028 / formatting controls;
- malformed enum values escaping as `TypeError`;
- deeply nested JSON escaping as `RecursionError`;
- unpaired surrogate acceptance leading to UTF-8 rendering failure;
- CLI whole-file allocation before the byte bound;
- four failing assertions because two control-character fixtures contained literal escape text rather than the intended code points.

Subsequent documentation/probe-packet commits did not change the parser/test bytes, so the 12/12 PASS statement remained contradictory and is withdrawn.

## Current repair state

Current PR #683 head includes bounded repairs for the reviewed defects:
- Unicode category rejection for formatting controls, surrogates, line and paragraph separators;
- explicit string type checks before enum membership;
- `RecursionError` normalized to `CapsuleError`;
- bounded CLI file read using `MAX_BYTES + 1`;
- corrected fixtures using actual newline/control/Unicode code points;
- added regression coverage for U+2028/bidi/surrogate cases, malformed enum types, deep JSON and bounded file reads.

These source changes are **not yet a recorded passing test result** in this receipt.

A fresh test run on the exact current head is required before any PASS count is stated here.

## Model-consumption gate

Do not run `MODEL_PROBE.md`, do not feed the frozen probe packet to a model, and do not treat the old packet hashes as current.

The model-level probe remains **UNRUN / BLOCKED** until:
1. the exact repaired head is rerun;
2. the full suite passes;
3. the resulting reader output is regenerated;
4. the reader-output and whole-packet hashes are recomputed;
5. Codex/CC review finds no blocking read-boundary defect.

## Data-origin ceiling

The reader does not establish permission, consent, confidentiality, or clearance for arbitrary body/source strings. Keep all fixtures synthetic or already public.

`PARSER REPAIR != PASS RECEIPT`  
`STALE HASH != FROZEN TEST`  
`NO MODEL CONSUMPTION BEFORE CURRENT-HEAD VERIFICATION`

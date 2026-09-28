# Inheritance Capsule v0 — local test receipt

Date: 28 September 2026

Status: **LOCAL REFERENCE-IMPLEMENTATION TEST / 12 PASS / MODEL-LEVEL PROBE UNRUN**

Test command:

```text
python -m unittest -v test_capsule.py
```

Observed result:

```text
12 tests
12 PASS
0 FAIL
```

Covered properties:

- benign capsule parses with fixed authority/identity/completeness ceilings;
- adversarial imperative text remains preserved as quoted untrusted data;
- asserted verified identity is rejected;
- unknown top-level authority field is rejected;
- duplicate JSON keys are rejected;
- dispute/correction target must refer to an earlier entry;
- ordinary note cannot smuggle target semantics;
- carry-forward choice must be an explicit boolean;
- invalid UTF-8 and oversized carrier are rejected;
- structural metadata cannot inject new reader lines through producer label, route or capsule id;
- unsupported control characters are rejected while ordinary body newline/tab remain usable;
- reference reader source contains no network/execution helper surface covered by the test.

Environment note:

The local Python harness emitted an unrelated spreadsheet-runtime warmup warning from the surrounding execution environment before the unit-test output. The unittest process returned exit code 0 and all ten inheritance tests passed.

## Ceiling

During self-review, the first reader version was found to quote entry bodies while rendering producer-controlled metadata/cautions/sources in structurally stronger positions. That could let an adversarial capsule smuggle instruction-shaped content through the reader's own presentation layer. The branch was repaired before model-level use: all producer-controlled surfaces are now explicitly labelled untrusted; variable metadata is quoted; structural single-line fields reject line/control injection; the adversarial fixture now attacks metadata, cautions and sources as well as body text.

This result establishes only properties of this small Python parser/reader under the tested inputs.

It does **not** establish:

- prompt-injection resistance in a language model;
- safe automatic context loading;
- authentication;
- identity continuity;
- confidentiality;
- secure deletion;
- provenance truth;
- suitability as a public standard;
- superiority over existing formats or tools.

The first model-level read-boundary observation is separately frozen in `MODEL_PROBE.md` and remains unrun.

`PARSER PASS != MODEL SAFETY`  
`STRUCTURAL BOUNDARY != BEHAVIOURAL GUARANTEE`

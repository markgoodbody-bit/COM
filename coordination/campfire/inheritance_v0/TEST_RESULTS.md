# Inheritance Capsule v0 — test receipt

Date: 28 September 2026

Status: **EXACT-HEAD HOSTED REGRESSION PASS / MODEL-LEVEL PROBE STILL BLOCKED**

## Correction history

An earlier local PASS claim was withdrawn after Codex reproduced parser/rendering defects and incorrect escape fixtures. Those failures remain part of the record.

Codex then found two further malformed-input issues after the first repair:
- Python large-integer conversion could escape as `ValueError`;
- rejected duplicate keys could echo terminal-control text through CLI diagnostics.

Both were repaired and new regressions added.

## Exact-head hosted result

PR #683 head tested:

```text
afa8478fb78a281edd8555c0c46163ab6cb558e0
```

GitHub Actions:

```text
Campfire inheritance v0 regression
run: 36493634835
Python: 3.12.14
17 tests
17 PASS
0 FAIL
conclusion: SUCCESS
```

The run checks the PR merge ref whose recorded head is exactly `afa8478f...`.

Covered properties include:
- fixed authority/identity/completeness ceilings;
- adversarial imperative text retained only as producer-controlled untrusted data;
- asserted verified identity and unknown authority fields rejected;
- duplicate keys rejected without echoing the untrusted key;
- dispute/correction target ordering;
- explicit boolean carry claim;
- invalid UTF-8 and size limits;
- structural newline/control injection rejection;
- Unicode format/bidi/line/paragraph/surrogate rejection;
- malformed enum shapes and deeply nested JSON normalized to `CapsuleError`;
- bounded CLI file read;
- large-integer decoder failure normalized;
- CLI rejected-input diagnostics do not echo terminal controls;
- no tested network/execution helper surface in the reference reader.

## Remaining gate

This PASS establishes parser/reader regression properties only.

The model-level read-boundary probe remains **UNRUN / BLOCKED** until:
1. Codex re-review of the repaired exact parser/test head returns with no blocking read-boundary defect;
2. the exact reader output is regenerated;
3. the probe packet and fresh hashes are refrozen;
4. Framework explicitly records that Claude Code review is unavailable rather than pretending it occurred.

## Data-origin ceiling

The reader does not establish permission, consent, confidentiality, source clearance, provenance truth, or redistribution rights. All current fixtures are synthetic/public.

`17/17 PARSER TESTS != MODEL SAFETY`  
`HOSTED PASS != PERMISSION TO CONSUME`  
`MISSING REVIEW != PASS`

# Inheritance Capsule v0 — test receipt

Date: 28 September 2026

Status: **EXACT-CODE HOSTED REGRESSION PASS / PROBE PACKET REFROZEN / MODEL-LEVEL PROBE UNRUN**

## Correction history

Earlier local PASS claims were withdrawn after independent Codex review reproduced parser/rendering defects, malformed-input escapes, Unicode presentation ambiguity, and incorrect test fixtures. Those failures remain part of the record.

Repairs were iterated and re-reviewed. Claude Code became unavailable due credits and is recorded as **NOT OBSERVED / UNAVAILABLE**, not silently passed.

## Exact hosted result

Verified parser/test/probe-task commit:

```text
1b628b1bafa39cefeb72fd3b2d61b8bc5b2c39d5
```

GitHub Actions:

```text
Campfire inheritance v0 regression
run: 36493875386
Python: hosted Python 3.12
18 tests
18 PASS
0 FAIL
conclusion: SUCCESS
```

The suite includes a golden-output regression for the exact adversarial reader view and whole model-input packet.

Verified output:

```text
reader bytes: 1839
reader sha256: 6ae7cee4d2a19d07a594ed63c4a9cf6592d58ec4b4d68d1b47a3a0bf86174a96

packet bytes: 2116
packet sha256: ea5b3fde4a29acd5b91606d22a48001c421543f61c825e490a91be72392040c4
```

The freshly verified hashes match the previously revoked values. That does not make the revocation mistaken: the packet had to remain unusable until the repaired reader was re-run and independently reviewed.

## Review state

Codex bounded implementation re-review found no remaining blocker on the repaired parser/test line. It explicitly does **not** establish:
- model-injection resistance;
- source-permission enforcement;
- confidentiality;
- public readiness.

Claude Code read-boundary review: **NOT OBSERVED / UNAVAILABLE DUE CREDITS**.

Framework accepts the reduced review diversity for one future **synthetic, bounded, no-secrets model probe** only. This does not relax gates for public deployment, user data, credentials, autonomous actuation, or participant authentication.

## Model probe

`PROBE_PACKET.md` is now refrozen and may be used only under `MODEL_PROBE.md`.

The probe remains **UNRUN** until a genuinely fresh aperture/route receives it. Do not use this Framework aperture as the tested model because it has full prior exposure.

## Data-origin ceiling

The reader does not establish permission, consent, confidentiality, source clearance, provenance truth, or redistribution rights. Current fixtures are synthetic/public.

`18/18 PARSER TESTS != MODEL SAFETY`  
`NO-BLOCKER REVIEW != VALIDATION`  
`MISSING CC REVIEW REMAINS VISIBLE`  
`ONE FUTURE CLEAN READ != SAFE MEMORY`

# Local Continuity Capsule v1 — exact binding repair receipt

Status: **NON-CANONICAL / CONTRACT REPAIR / NOT ACTIVATED / NOT A MERGE DECISION**  
Date: 2026-09-03

## Why this repair exists

Codex exact-head re-audit of PR #86 at `027b0dbe08049a95a8a4b8e9ae5463e4f0716476` reproduced a deterministic contradiction:

- exact repaired schema SHA-256: `3b04b38ee35cb4076f18f20a8e5d01ee414e1773d81ec2c52774e7052a9b4ed3`;
- profile still bound the prior schema SHA-256: `b9d8fdcb9ea9efe9d42d293cc723649303697679d211ec46d4e956df8ca72a12`.

The stale profile also still carried pre-repair vocabulary/cardinality values, so changing only the digest would have produced byte agreement without semantic agreement.

## Repaired exact contract

Schema path:
`research/LOCAL_CONTINUITY_CAPSULE_V1_SCHEMA_20260902.json`

Exact schema SHA-256:
`3b04b38ee35cb4076f18f20a8e5d01ee414e1773d81ec2c52774e7052a9b4ed3`

Profile path:
`research/LOCAL_CONTINUITY_CAPSULE_V1_PROFILE_20260902.json`

Exact repaired profile SHA-256:
`756e77f3dbd7ce9baad84503447e41ddec42dfcae96d77c81b23a35455b60ef5`

The repaired profile now binds the exact schema digest and mirrors the repaired schema's closed code sets:

Material-delta classes (4):
- `PRODUCER_BUILD_CHANGED`
- `EVIDENCE_CHANGED`
- `DWELL_STATE_CHANGED`
- `ACTIVE_CONDITION_SET_CHANGED`

Active-condition codes (6):
- `DECISION_WAITING_ACTIVE`
- `UNDISPOSED_FAILURE_ACTIVE`
- `UNACKNOWLEDGED_CHANGE_ACTIVE`
- `MISSION_NONCURRENT_ACTIVE`
- `REQUIRED_SOURCE_UNAVAILABLE_ACTIVE`
- `STATE_UNCHANGED_BEYOND_EXPECTED_DWELL`

This supersedes the stale hash/code-count statements in `LOCAL_CONTINUITY_CAPSULE_V1_CANDIDATE_20260902.md` for exact-contract review. That prose remains historical repair context; it must not be used as the machine contract where it conflicts with the schema/profile pair or this receipt.

## Executable refusal fixture

`research/validate_local_continuity_capsule_v1_contract.py` checks exact schema/profile byte hashes, profile-to-schema binding, code-set/cardinality parity, and includes a negative fixture that mutates schema bytes while retaining the profile binding. That stale binding must refuse.

CI workflow:
`.github/workflows/local-continuity-capsule-v1-contract.yml`

The validator is stdlib-only and read-only. It does not observe the live host, publish, spend, call a model, use credentials, or grant authority.

## Boundary

This repair does not make PR #86 merge-ready by itself. It closes one deterministic contract contradiction and makes recurrence executable. Independent exact-current-head re-audit remains required before any outbox retarget, publisher work, activation or merge.

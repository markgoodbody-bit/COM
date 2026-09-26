# EvidenceWatch Brierley retrospective — execution harness

Date: 26 September 2026

Status: **HARNESS PREPARED / DRY-RUN DEFAULT / NO PROVIDER CALL PERFORMED**

Harness:
`research/evidencewatch_retrospective/run_brierley_retrospective.mjs`

Purpose:

Make the frozen retrospective run executable without changing the pinned EvidenceWatch source or improvising model/prompt/topology decisions at execution time.

## Fail-closed source checks

Before importing EvidenceWatch modules, the harness requires a local checkout exactly at:

`9c96c8390d65f4fb452b2a106bcdb4fa0418ea6f`

It also verifies Git blob identities:

```text
src/ledger.mjs          df04ac27819c6f681b2534b27045628270a42dbb
src/nvidia-analyzer.mjs 19886ffbaa806c428ab8fb9c183134e5c702b6cf
src/engine.mjs          e08c4028c0780186bd4353ddb9975aa2e0aee10f
package.json            b93683b35aec26c97fb0855979effeea26e4110e
```

A dirty working tree is not itself disqualifying; the exact files used by the run are hash-checked and HEAD is pinned. The ledger/output must be outside or otherwise not overwrite source.

## Blinded packet checks

The harness requires:
- schema `evidencewatch-brierley-blinded-packet-v1`;
- exactly 44 cases;
- unique opaque `case-NNN` identifiers;
- exactly three case fields: `case_id`, `preprint_abstract`, `published_abstract`;
- non-empty preprint and published text;
- no known owner-label / DOI / role / source-row / blind-salt tokens.

It records the packet SHA-256 before execution.

## Dry-run default

Without `--live`, the harness:
- verifies the EvidenceWatch checkout;
- verifies the blinded packet;
- prints the pinned run plan;
- performs **zero provider calls**;
- does not create the output or ledger.

Expected marker:

`EVIDENCEWATCH_BRIERLEY_DRY_RUN_OK`

## Live gate

Live execution requires **both**:
- explicit `--live`;
- `NVIDIA_API_KEY` present in the environment.

The model is hard-pinned in the harness:

`nvidia/nemotron-3-super-120b-a12b`

The harness does not inherit an alternative `NVIDIA_MODEL`.

It refuses a live run if:
- output path already exists;
- ledger path already exists;
- ledger lock already exists;
- output and ledger paths collide.

This prevents accidental append/resume/mixed-run semantics.

## Frozen execution

Each opaque case gets one independent watch:
- common watched claim from the frozen run contract;
- synthetic opaque preprint/publication source IDs;
- both source states primary + state authority;
- same opaque independence group;
- synthetic authority order only;
- one opaque downstream review item;
- preprint observed first;
- publication observed second.

Prediction:

```text
publication engine status == MATERIAL_DELTA
-> prediction_review = true
otherwise
-> false
```

No owner label enters the live path.

## Provider receipt

A fetch wrapper clones each NVIDIA response and preserves:
- opaque case ID;
- phase;
- timestamps;
- HTTP status;
- raw response body.

It does not persist:
- API key;
- Authorization header;
- outgoing prompt/request body.

The normal pinned analyzer still parses the same provider response.

The harness requires exactly **88** provider responses before writing a completed output.

## Output freeze

The live output contains:
- exact EvidenceWatch commit/blob identities;
- packet SHA-256;
- model/endpoint;
- common watched claim;
- every baseline + successor normalized analysis/result;
- material reasons / relation / alert kind;
- errors;
- elapsed time;
- raw provider response receipts;
- final per-case prediction;
- ledger path.

It writes the output using exclusive create and prints its SHA-256 before any owner-label join.

Expected live marker:

`EVIDENCEWATCH_BRIERLEY_LIVE_RUN_COMPLETE_PRE_UNBLIND`

Preserve:

```text
HARNESS GREEN != MODEL RESULT
DRY RUN != PROVIDER EXECUTION
OUTPUT DIGEST FROZEN != VALIDATION
RAW PROVIDER RESPONSE != ATTESTED MODEL IDENTITY
```

No live execution was performed by adding this harness.

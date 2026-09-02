# Local Continuity Capsule v1 — research candidate

Status: NON-CANONICAL / TRANSPORT-NEUTRAL / NOT ACTIVATED  
Date: 2026-09-02  
Purpose: reduce human state-carrying without creating hidden authority, background model spend, false claims of currentness, or a healthy-observer/healthy-project confusion.

## Purpose

The desired system is not an autonomous agent. It is a voluntary coordination ecology whose powers remain separated:

- the Local Steward observes declared local state and maintains a bounded local record;
- a deterministic outbox producer takes one complete allowlisted snapshot and emits a typed capsule;
- Claude Code may interpret local evidence and prepare bounded work;
- Codex / Framework reconciles local and external witnesses, attacks proposals and routes consequential decisions;
- Mark remains the human originator, correction source and authority for consequential expansion.

The first build is deliberately smaller: one deterministic capsule that can cross apertures without carrying arbitrary content.

```text
LESS HUMAN TRANSPORT != MORE MACHINE AUTHORITY
AUTOMATIC PREPARATION != AUTOMATIC ACTUATION
RECORDED_CURRENT != EXTERNALLY_CURRENT
SILENCE != HEALTH
FRESH_OBSERVER != PROJECT_PROGRESS
CONTENT_ADDRESSABLE_STATE != VERIFIED_TRANSITION
```

## Repair basis

The original candidate at `51a836db...` received two convergent hostile reviews:

- Claude Code: an edge-only delta vocabulary cannot express a state remaining stuck beyond a declared interval;
- Codex: a receiver cannot verify `DELTA` / `NO_DELTA` without the exact predecessor, and "enumerated" fields were not actually closed enough for independent implementations.

This revision repairs the contract rather than the implementation. The exploratory outbox branch must follow the repaired contract, not the reverse.

## Exact profile and schema

The v1 candidate now binds two machine-readable companions:

- `research/LOCAL_CONTINUITY_CAPSULE_V1_SCHEMA_20260902.json`
  - candidate file SHA-256: `b9d8fdcb9ea9efe9d42d293cc723649303697679d211ec46d4e956df8ca72a12`;
  - JSON Schema Draft 2020-12;
  - exact fields, types, source order, closed enums, cardinalities and dwell tuples;
- `research/LOCAL_CONTINUITY_CAPSULE_V1_PROFILE_20260902.json`
  - candidate file SHA-256: `2e2fbbe5ab93c2a885583af6ad851092d7455e55075e7011e54db54b0f5348e3`;
  - binds the schema digest, frozen code sets, dwell thresholds, ordering rules and canonicalization test vectors.

Those hashes are review targets, not trust claims. Independent re-audit must reproduce them over exact UTF-8/LF file bytes before implementation is retargeted.

Canonical JSON uses RFC 8785 JSON Canonicalization Scheme. Capsule IDs use SHA-256 over the RFC-8785 canonical payload **excluding `capsule_id` itself**.

A schema/profile mutation is a reviewed version change. The local observed component cannot change the profile that judges it.

## Fixed envelope

A v1 capsule has this shape:

```json
{
  "schema": "framework-local-continuity-capsule-v1",
  "profile_sha256": "<64 lowercase hex>",
  "capsule_id": "sha256:<64 lowercase hex>",
  "previous_capsule_id": null,
  "producer": {
    "component": "framework-local-steward-outbox",
    "build_sha256": "<64 lowercase hex>",
    "instance_id_sha256": "<64 lowercase hex>",
    "instance_domain": "INSTALL_NOT_BUILD"
  },
  "observation": {
    "observed_at_utc": "<RFC3339 UTC Z>",
    "next_publication_due_utc": "<RFC3339 UTC Z>",
    "snapshot_state": "COMPLETE",
    "source_state_hash": "<64 lowercase hex>",
    "dwell": []
  },
  "transition_claim": "GENESIS",
  "material_delta": {
    "present": false,
    "codes": []
  },
  "active_conditions": {
    "present": false,
    "codes": []
  },
  "evidence": [
    {"source_id":"STEWARD_HEALTH","digest":"<hex-or-null>","state_code":"OK"},
    {"source_id":"STEWARD_MISSION_FILE","digest":"<hex-or-null>","state_code":"OK"},
    {"source_id":"STEWARD_SOURCE_FILE","digest":"<hex-or-null>","state_code":"OK"},
    {"source_id":"STEWARD_STATUS","digest":"<hex-or-null>","state_code":"OK"}
  ],
  "proposal": {
    "next_action_code": "NONE",
    "authority_required": "NONE"
  },
  "correction_of": null
}
```

No free-text observation, explanation, filename, path, URL, diff, command, exception, mission body, credential, provider output or repository content is permitted.

The capsule contains a **producer transition claim**. It does not contain its own verifier verdict.

```text
PRODUCER_TRANSITION_CLAIM != RECEIVER_VERIFICATION_RESULT
```

## Snapshot and comparison state

The producer reads the four required sources as one consistency-checked snapshot:

1. `STEWARD_HEALTH` — allowlisted local GET/projection;
2. `STEWARD_STATUS` — allowlisted local GET/projection;
3. `STEWARD_SOURCE_FILE` — hash only;
4. `STEWARD_MISSION_FILE` — hash only.

Evidence bytes and file contents remain local.

`source_state_hash` is the SHA-256 of the RFC-8785 canonical **comparison state**, containing only:

- the ordered four evidence entries;
- the ordered active dwell entries including their fixed threshold tuple and `breached` state;
- the active-condition code set.

It excludes observation time, publication deadline, proposal fields, `transition_claim`, `material_delta`, capsule identifiers and correction metadata. A clock tick therefore does not manufacture a transition; a dwell threshold crossing does, because `breached` / the active-condition set changes.

## Predecessor binding and transition verification

### Genesis

A genuine first capsule has:

```text
previous_capsule_id = null
transition_claim = GENESIS
material_delta.present = false
material_delta.codes = []
```

A receiver may verify the current snapshot and return `FRESH_GENESIS`. Genesis is not evidence of `NO_DELTA` because there is no prior comparison object.

### Subsequent capsules

Every non-genesis capsule MUST carry the exact `previous_capsule_id`.

To accept `FRESH_NO_DELTA` or `FRESH_DELTA`, a receiver must possess and validate that exact predecessor, including:

- predecessor capsule hash;
- same schema/profile identity;
- same producer instance identity domain and `instance_id_sha256`;
- valid time ordering;
- valid predecessor structure and source snapshot.

Then:

```text
current.source_state_hash == previous.source_state_hash
-> transition_claim MUST be NO_DELTA
-> material_delta MUST be empty

current.source_state_hash != previous.source_state_hash
-> transition_claim MUST be DELTA
-> material_delta.present MUST be true
-> at least one frozen delta code MUST identify the observed change class
```

A receiver missing the declared predecessor returns `UNVERIFIED`, not `FRESH_NO_DELTA` and not `INVALID`.

A receiver that possesses the predecessor but finds a hash/chain/profile/instance contradiction returns `INVALID`.

```text
MISSING_COMPARISON_HISTORY != NO_DELTA
UNAVAILABLE_EVIDENCE != FALSE
```

## Receiver results

The verifier returns exactly one of six states. These states are receiver results, not producer fields.

### `FRESH_GENESIS`

Current capsule/profile/schema/snapshot verify; deadline is open; `previous_capsule_id` is null; transition is correctly `GENESIS`.

### `FRESH_NO_DELTA`

Current and exact predecessor verify; deadline is open; comparison-state hashes are equal; producer claim and empty delta set are consistent.

**This result does not mean there is no active problem.** The receiver must still inspect `active_conditions` and dwell state.

### `FRESH_DELTA`

Current and exact predecessor verify; deadline is open; comparison-state hashes differ; producer claim and frozen material-delta codes are consistent.

### `STALE`

The capsule and required comparison history are otherwise verifiable, but the reader-visible deadline/evidence-currentness window has expired.

### `UNVERIFIED`

The capsule may be structurally well formed but a required verification dependency is unavailable, especially the declared predecessor or exact profile/schema. `UNVERIFIED` cannot be converted into `FRESH_NO_DELTA` by silence.

### `INVALID`

Schema, identity, integrity, allowlist, canonical hash, comparison chain, snapshot consistency, time ordering, profile binding or size fails. Partial source snapshots are `INVALID`, not stale and not a delta.

Receivers do not infer world silence, project progress, consent, authorization, completeness or moral clearance from any result.

## Edge events and level conditions

The earlier candidate could report only edges. v1 now separates:

- `material_delta.codes` — changed events between exact predecessor/current comparison state;
- `active_conditions.codes` — conditions that remain true on every capsule while the level condition persists.

The v1 active-condition vocabulary contains:

```text
STATE_UNCHANGED_BEYOND_EXPECTED_DWELL
```

If any active dwell item has `breached=true`, this code remains present on every subsequent capsule until the underlying state clears or changes so that the condition is no longer active.

If the active-condition set changes between predecessor and current capsule, the material delta includes:

```text
ACTIVE_CONDITION_SET_CHANGED
```

Therefore a stable but stuck system can be:

```text
receiver_result = FRESH_NO_DELTA
active_conditions = [STATE_UNCHANGED_BEYOND_EXPECTED_DWELL]
```

That is deliberate. `NO_DELTA` describes the transition; it does not pronounce the state healthy.

```text
EDGE_DETECTION != STUCKNESS_DETECTION
NO_NEW_DELTA != NO_ACTIVE_CONDITION
```

## Dwell semantics

The closed candidate profile defines five local states and candidate thresholds:

- decision waiting present — 86,400 seconds;
- undisposed failure present — 43,200 seconds;
- unacknowledged change present — 43,200 seconds;
- mission non-current — 43,200 seconds;
- required source unavailable — 43,200 seconds.

Each active dwell entry binds:

```text
state_id
unchanged_since_utc
threshold_id
expected_max_dwell_seconds
threshold_authority = PROFILE_V1
breached
```

These thresholds are **warning thresholds**, not action authority and not claims that a state is wrongful. They are candidate review values and must be attacked empirically.

The observed Steward/outbox cannot lengthen its own tolerated dwell. Any threshold change is a profile revision under review.

PR #87 may later propose expiring, bounded adaptive threshold policy. That policy is outside v1 and may not silently mutate the profile used to judge the current producer.

```text
OBSERVED_COMPONENT != AUTHORITY_TO_RELAX_ITS_OWN_THRESHOLD
DWELL_BREACH != AUTOMATIC_ACTION_REQUIRED
```

## Material-delta vocabulary

The exact list is frozen in the profile. It includes the original twelve codes plus:

```text
ACTIVE_CONDITION_SET_CHANGED
```

Adding/removing a code is a profile/schema change requiring review.

## Liveness and cost

Normal heartbeat deadline: 12 hours.

A material delta, active-condition change or failure may produce a capsule earlier. A successfully delivered capsule resets the reader-visible producer deadline. The local producer must still write its atomic outbox capsule even when no external transport exists.

The producer is deterministic and model-free.

```text
HEALTHY_OPERATION_PROVIDER_CALLS = 0
UNHEALTHY_OPERATION_PROVIDER_CALLS = 0
```

A failure must not become the first reason the watcher spends money.

An external publisher, if later earned, has separate ceilings:

- maximum two ordinary heartbeat publications per UTC day;
- at most one publication per unique capsule ID;
- change/failure publication may exceed the heartbeat count only under an explicit daily hard cap;
- repeated unchanged failure/active-condition state must be bounded and deduplicated rather than published once per scheduler invocation;
- ambiguous publication becomes `OUTCOME_UNKNOWN` and must be reconciled by capsule ID before retry;
- queued stale capsules never publish as if current.

A dead producer cannot announce its death. Readers determine expiry from the last delivered `next_publication_due_utc`.

## Authority boundary

The local producer may:

- GET the fixed local Steward health/status endpoints;
- hash exact approved local files without emitting contents;
- compare against the exact validated predecessor capsule;
- maintain dwell onset timestamps for the frozen local state IDs;
- atomically write a fixed-schema capsule and bounded local state.

It may not:

- read or use the Steward control token;
- execute jobs or commands;
- acknowledge observations;
- record approvals;
- mutate mission state;
- call models or providers in healthy or unhealthy paths;
- browse;
- spend;
- inspect arbitrary files;
- contact external services;
- publish externally;
- change the schema/profile/dwell thresholds that judge it.

A later external relay is a separate component and separate authority decision. It must use destination-scoped credentials. Broad current-user `repo` or `workflow` authority is not acceptable merely because code intends to use one issue.

## Storage and placement

Producer, scheduler, state and logs live outside:

- TRACE and Mechanical Ethics repositories;
- canonical project worktrees;
- Steward read roots;
- directories watched by the producer.

Retained records contain hashes, timestamps and status codes only. Retention is bounded. Uninstall must stop the scheduler, remove executable/state files and leave already published receipts intact.

The research object belongs in COM. Executable code, if earned, belongs with Steward or Campfire operational tooling—not TRACE.

## Minimum acceptance gate

No activation until captured tests establish:

1. exact JSON Schema acceptance and unknown-field refusal;
2. exact schema/profile SHA-256 reproduction;
3. RFC-8785 canonicalization and supplied test-vector reproduction;
4. genesis handling and `FRESH_GENESIS` semantics;
5. exact predecessor binding; missing predecessor -> `UNVERIFIED`; wrong predecessor -> `INVALID`;
6. `NO_DELTA` / `DELTA` recomputation from exact predecessor/current comparison-state hashes;
7. persistent dwell condition remains visible across repeated `FRESH_NO_DELTA` capsules;
8. threshold-crossing changes the comparison state and emits `ACTIVE_CONDITION_SET_CHANGED`;
9. observed component cannot change its profile/dwell threshold;
10. hostile data remains data: shell syntax, instructions, fake secrets, malformed encoding, huge input, symlink and traversal fixtures;
11. no control-token, provider-secret, arbitrary-body or path disclosure in payload, logs, argv or state;
12. complete-snapshot refusal when required sources change during reading;
13. idempotence across overlapping runs, crashes, retries and clock skew;
14. actual concurrent create-only semantics, or an explicitly narrower atomicity claim;
15. `OUTCOME_UNKNOWN` reconciliation without blind retry;
16. outage, corrupt state, missing/locked source and resume-after-downtime paths;
17. invalid/negative retention, heartbeat and time-domain inputs fail closed;
18. repeated failed-check publication is deduplicated/bounded independently of scheduler frequency;
19. self-observation cannot retrigger;
20. hard publication and retention ceilings;
21. pinned build/dependency identity;
22. disable, reboot and uninstall cessation;
23. network egress is zero for producer success and failure paths;
24. any later publisher can reach only its exact approved destination.

The current exploratory Claude outbox branch is not grandfathered through this gate. It must be repaired/rebased to the exact contract after independent review.

## Promotion stages

```text
RESEARCH CANDIDATE
-> EXACT CONTRACT RE-AUDIT
-> LOCAL MANUAL TEST
-> LOCAL OUTBOX TRIAL
-> INDEPENDENT AUDIT
-> DESTINATION-SCOPED RELAY TEST
-> BOUNDED ACTIVATION
-> USE-DRIVEN REVIEW
```

No stage inherits the authority of the next.

## Relationship to bounded adaptation

This capsule reports bounded local state. It does not decide project priority or purpose.

PR #87 is the separate candidate for orientation/adaptation. The separation is intentional:

```text
CONTINUITY_CAPSULE = WHAT LOCAL STATE CAN BE VERIFIED
ADAPTATION_LOOP = WHAT ORDINARY REVERSIBLE WORK SHOULD CHANGE NEXT
ACTUATION_AUTHORITY = SEPARATE AGAIN
```

A future adaptive rule may change what is done next. Only a reviewed/authorized schema-profile correction may change what counts as valid capsule evidence.

## Falsifiers

Stop, repair or delete the object if:

- Mark still has to prompt both CC and Codex to establish ordinary freshness;
- silence can conceal a dead producer;
- a stable stuck condition can disappear into `FRESH_NO_DELTA`;
- equal evidence produces nondeterministic verifier results;
- receiver fresh-state claims cannot be independently reproduced from exact predecessor + current capsule;
- raw local content or credentials cross the boundary;
- healthy or unhealthy unattended paths require a model/provider;
- notification/supervision burden exceeds the human transport it removes;
- a scoped publisher can affect anything outside the declared destination;
- corrections silently become permanent policy;
- the observed component can relax its own liveness/stuckness thresholds;
- activity, uptime or system growth replaces resolved human need as the success measure.

## Horizon

If v1 works, later layers may add authenticated proposal capsules, correction provenance and carefully bounded expiring adaptation. They must preserve:

```text
OBSERVATION -> ORIENTATION -> PROPOSAL -> AUTHORIZED_ACTION -> WITNESSED_EFFECT
```

No arrow is automatic.

The larger possibility is portable, participant-controlled help: local stewards exchanging minimal typed envelopes, matching consented needs and capabilities, preparing small interventions, and leaving answerable receipts. Participation must remain optional; reputation must not collapse into an unappealable global score; authority must narrow when correction fails.

The next build remains the smallest one: independently falsify this repaired contract before retargeting the outbox implementation.

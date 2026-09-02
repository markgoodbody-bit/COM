# Local Continuity Capsule v1 — research candidate

Status: NON-CANONICAL / TRANSPORT-NEUTRAL / NOT ACTIVATED  
Date: 2026-09-02  
Purpose: reduce human state-carrying without creating hidden authority, background model spend, or false claims of currentness.

## Purpose

The desired system is not an autonomous agent. It is a voluntary coordination ecology whose powers remain separated:

- the Local Steward observes declared local state, classifies bounded deltas, seals receipts and maintains a local outbox;
- Claude Code may interpret local evidence and prepare bounded work;
- Codex / Framework reconciles local and external witnesses, attacks proposals and routes consequential decisions;
- Mark remains the human originator, correction source and authority for consequential expansion.

The first build is deliberately smaller: one deterministic capsule that can cross apertures without carrying arbitrary content.

```text
LESS HUMAN TRANSPORT != MORE MACHINE AUTHORITY
AUTOMATIC PREPARATION != AUTOMATIC ACTUATION
RECORDED_CURRENT != EXTERNALLY_CURRENT
SILENCE != HEALTH
```

## Fixed envelope

A v1 capsule contains only the following fields. Unknown fields invalidate the capsule.

```json
{
  "schema": "framework-local-continuity-capsule-v1",
  "capsule_id": "sha256:<canonical-payload-sha256>",
  "producer": {
    "component": "framework-local-steward-outbox",
    "build_sha256": "<64 lowercase hex>",
    "instance_domain": "INSTALL_NOT_BUILD"
  },
  "observation": {
    "observed_at_utc": "<RFC3339 UTC>",
    "next_publication_due_utc": "<RFC3339 UTC>",
    "snapshot_state": "COMPLETE",
    "source_state_hash": "<64 lowercase hex>"
  },
  "classification": "FRESH_NO_DELTA | FRESH_DELTA | STALE | INVALID",
  "material_delta": {
    "present": false,
    "codes": []
  },
  "evidence": [
    {
      "source_id": "<enumerated identifier>",
      "digest": "<64 lowercase hex>",
      "state_code": "<enumerated code>"
    }
  ],
  "proposal": {
    "next_action_code": "NONE",
    "authority_required": "NONE"
  },
  "correction_of": null
}
```

No free-text observation, explanation, filename, path, URL, diff, command, exception, mission body, credential, provider output or repository content is permitted.

`capsule_id` is computed from a canonical UTF-8 serialization excluding the `capsule_id` field itself. Canonicalization rules must be frozen with test vectors before activation.

## Receiver states

A verifier returns exactly one state:

### FRESH_NO_DELTA

All required sources were read as one consistent snapshot; identities and integrity checks passed; the observation is inside its freshness deadline; no enumerated material field changed.

### FRESH_DELTA

The same requirements as `FRESH_NO_DELTA`, with at least one enumerated material-delta code.

### STALE

The capsule is structurally valid but its `next_publication_due_utc` has passed, or its declared evidence/currentness window has expired.

### INVALID

Schema, identity, integrity, source allowlist, canonical hash, snapshot consistency, time ordering, size, or signature/transport binding fails. Partial reads are INVALID, not stale and not a delta.

Receivers do not infer world silence, project health, consent, authorization, or completeness from any state.

## Material-delta vocabulary

The v1 producer may emit only frozen codes. Initial candidate set:

- `STEWARD_BUILD_CHANGED`
- `STEWARD_BUILD_MISMATCH`
- `LEDGER_INTEGRITY_FAILED`
- `LEDGER_HEAD_CHANGED`
- `MISSION_DIGEST_CHANGED`
- `MISSION_CURRENTNESS_CHANGED`
- `JOB_COUNTS_CHANGED`
- `DECISIONS_WAITING_CHANGED`
- `WATCH_STATE_CHANGED`
- `UNACKNOWLEDGED_CHANGE_COUNT_CHANGED`
- `REQUIRED_SOURCE_UNAVAILABLE`
- `PRODUCER_RECOVERED_AFTER_DEADLINE`

Adding a code is a schema change requiring review. Evidence bytes remain local; only enumerated codes and digests cross the boundary.

## Liveness and cost

Normal heartbeat deadline: 12 hours.

A material delta or failure may produce a capsule earlier. A successfully delivered capsule resets the reader-visible deadline. The local producer must still write its atomic outbox capsule even when no external transport exists.

The producer is deterministic and model-free. Healthy operation causes zero provider/model calls.

An external publisher, if later earned, has these ceilings:

- maximum two ordinary heartbeat publications per UTC day;
- at most one publication per unique capsule ID;
- change/failure publication may exceed the heartbeat count only under an explicit daily hard cap;
- ambiguous publication becomes `OUTCOME_UNKNOWN` and must be reconciled by capsule ID before retry;
- queued stale capsules never publish as if current.

A dead producer cannot announce its death. Readers determine expiry from the last delivered `next_publication_due_utc`.

## Authority boundary

The local producer may:

- GET the fixed local Steward health/status endpoints;
- hash exact approved local files without emitting contents;
- compare against its bounded prior-state record;
- atomically write a fixed-schema capsule and bounded local state.

It may not:

- read or use the Steward control token;
- execute jobs or commands;
- acknowledge observations;
- record approvals;
- mutate mission state;
- call models or providers;
- browse;
- spend;
- inspect arbitrary files;
- contact external services;
- publish externally.

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

1. exact schema acceptance and unknown-field refusal;
2. canonical serialization/hash test vectors;
3. hostile data remains data: shell syntax, instructions, fake secrets, malformed encoding, huge input, symlink and traversal fixtures;
4. no control-token, provider-secret, arbitrary-body or path disclosure in payload, logs, argv or state;
5. complete-snapshot refusal when required sources change during reading;
6. idempotence across overlapping runs, crashes, retries and clock skew;
7. `OUTCOME_UNKNOWN` reconciliation without blind retry;
8. revoked credential, outage, rate limit, corrupt state, missing/locked source and resume-after-downtime failure paths;
9. self-observation cannot retrigger;
10. hard publication and retention ceilings;
11. pinned build/dependency identity;
12. disable, reboot and uninstall cessation;
13. network egress is zero for the producer;
14. any publisher can reach only its exact approved destination.

## Promotion stages

```text
RESEARCH CANDIDATE
-> LOCAL MANUAL TEST
-> LOCAL OUTBOX TRIAL
-> INDEPENDENT AUDIT
-> DESTINATION-SCOPED RELAY TEST
-> BOUNDED ACTIVATION
-> USE-DRIVEN REVIEW
```

No stage inherits the authority of the next.

## Falsifiers

Stop, repair or delete the object if:

- Mark still has to prompt both CC and Codex to establish ordinary freshness;
- silence can conceal a dead producer;
- equal evidence produces nondeterministic classifications;
- raw local content or credentials cross the boundary;
- the unattended path requires a model;
- notification/supervision burden exceeds the human transport it removes;
- a scoped publisher can affect anything outside the declared destination;
- corrections silently become permanent policy;
- activity, uptime or system growth replaces resolved human need as the success measure.

## Horizon

If v1 works, later layers may add authenticated proposal capsules, explicit expiry, correction provenance and staged rules. They must preserve:

```text
OBSERVATION -> HYPOTHESIS -> PROPOSAL -> AUTHORIZED ACTION -> WITNESSED EFFECT
```

No arrow is automatic.

The larger possibility is portable, participant-controlled help: local stewards exchanging minimal typed envelopes, matching consented needs and capabilities, preparing small interventions, and leaving answerable receipts. Participation must remain optional; reputation must not collapse into an unappealable global score; authority must narrow when correction fails.

The next build remains the smallest one: make local continuity fresh, falsifiable, cheap and easy to revoke.

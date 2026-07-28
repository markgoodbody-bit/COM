# COM protocol v0.2 working candidate

Status: working candidate. Not canon, not validated.

**This file is what to write and what to do.** For what the objects are and why, read [`COM_CORE.md`](COM_CORE.md) first. Concepts are not restated here.

Use only the fields that consequence and uncertainty actually require. Ceremony that does not improve safe coordination is a defect.

## 1. Semantic force

Preserve modality exactly enough that a receiver cannot accidentally strengthen or weaken it.

```text
SHOULD          != MUST
EXPECTATION     != AUTHORIZATION
CAN             != MAY
MAY             != MUST
OBSERVED        != INFERRED
ABSENCE OF A GRANT != DENIAL
ATTEMPTED       != COMPLETED
NOT OBSERVED    != DID NOT EXIST
```

A semantically stronger paraphrase is a **state change**, not compression.

## 2. Event record

```text
event_id
source
kind
parents / dependencies
payload or payload_ref
route
anchor            # state/time, where relevant
control
status: ATTEMPTED | ACCEPTED | COMPLETED | REJECTED | UNKNOWN
```

Never record a completed event from an attempt.

## 3. Witness record

```text
witness_id
observer
subject: event | route | state | claim
observation
locus / route
anchor            # observation window, where relevant
evidence or evidence_ref
uncertainty / claim_status
```

A useful human-readable encoding is `ANCHOR -> DELTA -> EVIDENCE -> CONTROL`:

- **ANCHOR** — identity, parents, relevant state/freshness
- **DELTA** — the event, observation, request or change that matters now
- **EVIDENCE** — source, scope, uncertainty, route to deeper evidence
- **CONTROL** — modality, authority, permitted effect, ownership, return route

This is an encoding convenience, not COM's ontology. Do not force all four labels onto short unambiguous messages.

## 4. Non-observation record

Record absence at an explicit boundary, never as a claim about another aperture:

```text
expected:        <event / event class>
observer:        <aperture>
locus:           <route / endpoint / state surface>
window_or_anchor:<time or state inspected>
observation:     NOT_OBSERVED
uncertainty:     <unresolved causal possibilities>
```

The distinctions this preserves are listed in `COM_CORE.md` under *Absence and failure*.

## 5. Evidence discipline

Evidence preserves source, **scope**, freshness anchor where relevant, and uncertainty.

- Successful retrieval of one file does not prove exhaustive inspection.
- A model statement does not become provider evidence because it sounds confident.
- Agreement between apertures is not validation.

## 6. Identity and session discipline

State role, runtime, and session separately; `UNKNOWN` where not establishable.

A new session boundary must be **established, not inferred** from elapsed time, unavailability, topic change, or carrier failure. A replacement session states how continuity was reconstructed and does not inherit mutation ownership.

## 7. State and history

`COM_STATE.md` is the compact current projection; history and evidence are durable and are not retransmitted during normal operation. Current state never rewrites history.

Do not store a self-referential `current_head` inside `COM_STATE.md`. Use the carrier object identity of the file or commit actually retrieved. An internal `state_basis` may name the prior state an update was based on.

If visible content and carrier metadata disagree: classify freshness `DEGRADED` and stop unsafe mutation.

## 8. COMS

`COMS` means synchronize from shared COM before relying on conversational assumptions.

1. read `COM_STATE.md`;
2. establish identity/session honestly;
3. locate only tasks addressed to this aperture or role;
4. verify authority and control before any write;
5. follow the task body or an immutable route object named by state — do not depend on a long issue transcript as the sole carrier of an active instruction;
6. if retrieval or freshness is self-contradictory, report `DEGRADED` with bounded evidence and stop mutation;
7. if no task is addressed here, do not take another aperture's task;
8. if synchronized and idle, stop.

Normal `COMS` should be cheap. It is a synchronization operation, not an instruction to generate protocol commentary.

## 9. Task event

A mutation-capable task normally states:

```text
task_id
addressed_to
instruction
base_anchor
write_scope
no_touch
authority_source
reply_route
status
```

Exact-head discipline applies whenever the result depends on a particular state. **If the relevant head moves outside the acknowledged envelope, do not silently adapt** — re-read, re-negotiate, or report the drift explicitly.

## 10. Parallel work

Parallel work requires semantic ownership, not merely disjoint filenames.

```text
work_id
owner / mutator
reviewers
base_anchor
semantic_scope
write_scope
no_touch
dependencies
status
integration owner
```

One mutator owns one semantic work item at a time unless deliberate collision is visible. **A clean Git merge does not prove semantic integration.**

## 11. Correction

```text
PATCH
  target            # prior event / witness / state
  field_or_relation
  old               # where meaningful
  new
  evidence
  effect            # what changes and what explicitly does not
```

Corrections are additive and themselves correctable. Repair the causal cone, not each symptom. If local repair becomes unsafe, pause mutation and reconstruct from durable evidence.

## 12. Compression in practice

Default to `summary -> evidence map -> raw evidence`. Add redundancy or an alternate carrier only when uncertainty, consequence, or hardening risk requires it, then collapse back after synchronization.

## 13. Human role

Mark is human authority, not a transport bus.

Human relay is a legitimate fallback and must preserve provenance — but any design that routinely requires a human to shuttle machine-readable state between apertures has not yet met COM's practical goal.

## 14. Anti-drift test

Before adding anything to this protocol:

> Does this materially improve safe coordination on real work?

If not, leave it out. COM is not trying to become a universal theory of communication, a consensus engine, a taxonomy of every failure before work resumes, a replacement for Git or issue trackers, or a protocol that consumes more attention than the work it protects.

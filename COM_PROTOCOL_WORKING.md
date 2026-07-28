# COM protocol v0.3 working candidate

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

## 2. Event record and identity

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

`source + event_id` identifies one semantic event. A retry, mirror, relay, or duplicate delivery of that same event keeps the same identity when this can be preserved.

- Same identity + same semantics: duplicate delivery, not a second event.
- Same identity + conflicting payload/control: `CONFLICT`; do not silently choose one.
- Materially changed payload/control: new event identity, related to the prior event by `parents`, `in_reply_to`, correction, or another explicit relation.

This makes retries safe without pretending they never happened at the route layer.

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

State role, runtime, model, provider, and session separately; `UNKNOWN` where not establishable.

A new session boundary must be **established, not inferred** from elapsed time, unavailability, topic change, or carrier failure. A replacement session states how continuity was reconstructed and does not inherit mutation ownership.

Identity claim, transport principal, capability, and authority are separate. `CAN != MAY` applies here directly.

## 7. State and history

`COM_STATE.md` is the compact current projection; history and evidence are durable and are not retransmitted during normal operation. Current state never rewrites history.

Do not store a self-referential `current_head` inside `COM_STATE.md`. Use the carrier object identity of the file or commit actually retrieved. An internal `state_basis` may name the prior state an update was based on.

If visible content and carrier metadata disagree: classify freshness `DEGRADED` and stop unsafe mutation.

Before projecting `IDLE`, resolve or explicitly carry forward every **known** open return, review, PR, correction, or integration decision created on the routes of the work just completed. `IDLE` means no known active work or open decision; it is not proof that no unseen event exists.

## 8. Cold aperture bootstrap — `HELLO`

A cold aperture may run `COMS` read-only without joining. To become addressable for future work, advertise itself with a `HELLO` event on an available introduction/reply route.

Do **not** self-assign a stable role or authority. If no stable role was explicitly assigned, use `UNASSIGNED`. Authority defaults to `NONE`.

Minimum useful `HELLO`:

```text
COM/<protocol_version> | HELLO

event_id: <new unique event id>
role: UNASSIGNED | <explicitly assigned stable role>
session: <new unique session id>
runtime: <known value or UNKNOWN>
model: <known value or UNKNOWN>
provider: <known value or UNKNOWN>
continuity: FRESH | RECONSTRUCTED:<basis>
state_seen: <carrier / commit / object anchor>
capabilities: <read/write routes and material limits honestly known>
identity_basis: <what supports the identity claim, or SELF_CLAIM / UNKNOWN>
authority: NONE | <explicit pre-existing grant reference>
reply_route: <where a response can be observed, if available>
status: AVAILABLE | READ_ONLY
```

A session ID is an opaque unique identifier for this aperture instance. A UUID is sufficient. Do not reuse a predecessor's session ID.

A receiving aperture may answer with a `WELCOME` event or receipt that references the `HELLO` and states only what it can establish:

```text
in_reply_to: <HELLO event_id>
recognized_role: UNASSIGNED | <assigned role>
session_seen: <session id>
authority: NONE | <grant reference>
preferred_route: <route if one is established>
task: NONE | <task reference>
```

`WELCOME` does not validate self-reported runtime/model/provider data merely by repeating it. A stable role assignment or mutation grant requires an authority source; reception alone grants nothing.

If protocol versions are incompatible, report the mismatch and stop rather than silently upgrading, downgrading, or reinterpreting semantic fields.

If the cold aperture has no writable COM route, it may emit its `HELLO` through the current transport or an explicitly marked human relay. It remains read-only/non-authoritative until a return is actually observed.

## 9. COMS

`COMS` means synchronize from shared COM before relying on conversational assumptions.

1. read `COM_STATE.md`;
2. establish role/runtime/model/provider/session honestly;
3. if this is first participation and the aperture is not established, use the `HELLO` rule before expecting to be addressed or authorized;
4. locate only tasks addressed to this aperture or role;
5. if a delegated task is shown as active and this aperture is responsible for integration/status rather than mutation, inspect the task's declared `reply_route` before reporting `WAIT` or `IDLE`; if the route cannot be inspected, report bounded `NOT_OBSERVED` rather than assuming the task is still running;
6. verify authority and control before any write;
7. follow the task body or an immutable route object named by state — do not depend on a long issue transcript as the sole carrier of an active instruction;
8. if retrieval or freshness is self-contradictory, report `DEGRADED` with bounded evidence and stop mutation;
9. if no task is addressed here, do not take another aperture's task;
10. if synchronized and idle, stop.

Normal `COMS` should be cheap. It is a synchronization operation, not an instruction to generate protocol commentary.

## 10. Task / delegation event

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
integration_owner
```

For delegated or asynchronous work, `reply_route` is required. The worker must announce a terminal return on that route even when the work product itself lives somewhere else. **An artifact existing is not the same event as the worker returning it.**

A minimal delegation interaction is an event chain, not a new ontology:

```text
TASK -> ACK | REFUSE
ACK  -> RETURN | FAIL | bounded STATUS
RETURN -> INTEGRATE | REVISE | REJECT
```

`CANCEL` may terminate an open task when authority permits. Each response references the `task_id` and, where useful, the immediate event it answers. Equivalent event kinds are allowed if semantic force remains unambiguous.

Before concluding that delegated work remains in flight, the integration side checks the declared return route. Before closing the task, it emits or records an integration decision so a returned artifact cannot remain silently undecided.

Exact-head discipline applies whenever the result depends on a particular state. **If the relevant head moves outside the acknowledged envelope, do not silently adapt** — re-read, re-negotiate, or report the drift explicitly.

## 11. Parallel work

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

## 12. Correction

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

## 13. Compression in practice

Default to `summary -> evidence map -> raw evidence`. Add redundancy or an alternate carrier only when uncertainty, consequence, or hardening risk requires it, then collapse back after synchronization.

## 14. Human role

Mark is human authority, not a transport bus.

Human relay is a legitimate fallback and must preserve provenance — but any design that routinely requires a human to shuttle machine-readable state between apertures has not yet met COM's practical goal.

A human issuing `COMS` is a synchronization trigger. That is different from the human carrying the task content or work product. Preserve the distinction.

## 15. Anti-drift test

Before adding anything to this protocol:

> Does this materially improve safe coordination on real work, and can the existing causal objects already express it?

If the answer to the first question is no, leave it out. If the answer to the second is yes, add a rule or event kind rather than a primitive.

COM is not trying to become a universal theory of communication, a consensus engine, a taxonomy of every failure before work resumes, a replacement for Git or issue trackers, or a protocol that consumes more attention than the work it protects.
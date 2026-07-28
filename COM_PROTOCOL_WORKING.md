# COM protocol v0.3 working candidate

Status: working candidate. Not canon, not validated.

**This file is what to write and what to do.** For what the objects are and why, read [`COM_CORE.md`](COM_CORE.md) first. Concepts are not restated here.

Use only the fields that consequence and uncertainty actually require. Ceremony that does not improve safe coordination is a defect.

When durable material refers back to this protocol, prefer the heading name or a stable object/event identifier over section numbers; section numbers drift as the protocol changes.

## Semantic force

Preserve modality exactly enough that a receiver cannot accidentally strengthen or weaken it.

```text
SHOULD             != MUST
EXPECTATION        != AUTHORIZATION
CAN                != MAY
MAY                != MUST
OBSERVED           != INFERRED
ABSENCE OF A GRANT != DENIAL
ATTEMPTED          != COMPLETED
NOT OBSERVED       != DID NOT EXIST
UNKNOWN            != CURRENT
```

A semantically stronger paraphrase is a **state change**, not compression.

## Event record and identity

```text
event_id
source
kind
parents / dependencies
payload or payload_ref
route
anchor            # state/time/object, where relevant
control
status: ATTEMPTED | ACCEPTED | COMPLETED | REJECTED | UNKNOWN
```

Never record a completed event from an attempt.

When the identity is preserved, `source + event_id` identifies one semantic event.

- Same preserved identity + same semantics: duplicate delivery, not a second event.
- Same preserved identity + conflicting payload/control: identity `CONFLICT`; do not silently choose one.
- Materially changed payload/control: new event identity, related to the prior event by `parents`, `in_reply_to`, correction, or another explicit relation.
- Original identity not preserved by a relay/route: record `identity_status: UNPRESERVED` or `UNKNOWN`. Do **not** infer either novelty or duplication from missing identity.

An identity conflict is an unresolved coordination item. Record the conflicting observations and route the decision to the task/integration owner or another explicit authority. If no resolver is established, stop affected state-dependent mutation rather than inventing one.

Retries remain visible at the route layer. A retry is a new transmission occurrence even when it carries the same semantic event.

## Witness record

```text
witness_id
observer
subject: event | route | state | claim
observation
locus / route
anchor            # observation window/object, where relevant
evidence or evidence_ref
uncertainty / claim_status
```

A witness is relational: it is a bounded claim **about** an event, route, state, or claim. An emitted witness may itself be carried by an event; EVENT and WITNESS are not required to be disjoint categories.

A useful human-readable encoding is `ANCHOR -> DELTA -> EVIDENCE -> CONTROL`:

- **ANCHOR** — identity, parents, relevant state/freshness
- **DELTA** — the event, observation, request or change that matters now
- **EVIDENCE** — source, scope, uncertainty, route to deeper evidence
- **CONTROL** — modality, authority, permitted effect, ownership, return route

This is an encoding convenience, not COM's ontology. Do not force all four labels onto short unambiguous messages.

## Non-observation record

Record absence at an explicit boundary, never as a claim about another aperture:

```text
expected:         <event / event class>
observer:         <aperture>
locus:            <route / endpoint / state surface>
window_or_anchor: <time or state inspected>
observation:      NOT_OBSERVED
uncertainty:      <unresolved causal possibilities>
```

The distinctions this preserves are listed in `COM_CORE.md` under *Absence and failure*.

## Evidence discipline

Evidence preserves source, **scope**, freshness anchor where relevant, and uncertainty.

- Successful retrieval of one file does not prove exhaustive inspection.
- Successful retrieval from a mutable label such as `main` or `latest` does not, by itself, prove that the returned content is current.
- A model statement does not become provider evidence because it sounds confident.
- Agreement between apertures is not validation.

## Identity and session discipline

State role, runtime, model, provider, session, capability, authority, and current reachability separately; `UNKNOWN` where not establishable.

A new session boundary must be **established, not inferred** from elapsed time, unavailability, topic change, or carrier failure. A replacement session states how continuity was reconstructed and does not inherit mutation ownership.

Identity claim, transport principal, capability, authority, and reachability are separate. `CAN != MAY` applies directly.

## State, freshness and history

`COM_STATE.md` is the compact current projection; history and evidence are durable and are not retransmitted during normal operation. Current state never rewrites history.

Do not store a self-referential `current_head` inside `COM_STATE.md`. Use carrier/object identity from the retrieval that actually occurred. An internal `state_basis` may name the prior state an update was based on.

A mutable name or URL is navigation, not an anchor. Before state-dependent action, establish a freshness anchor adequate to that action from the route/carrier when possible. Examples include a commit/head/object identity returned by the carrier. Content identity alone may prove which bytes were read without proving that a mutable branch still points there; consequence determines how strong the anchor must be.

Use these bounded states:

```text
freshness: ANCHORED:<basis> | UNKNOWN | DEGRADED
```

- `ANCHORED` means the observation is tied to the stated carrier/object basis; it does not claim timeless global currency.
- `UNKNOWN` means coherent content was retrieved but the route did not establish enough recency for the intended state-dependent action.
- `DEGRADED` means visible content, route metadata, or other freshness evidence contradicts itself.

For `UNKNOWN` or `DEGRADED`, do not perform state-dependent mutation from that projection. Report the bounded problem and recover a sufficient anchor or obtain an explicit authority decision that acknowledges the uncertainty.

Before projecting `IDLE`, resolve or explicitly carry forward every **known** open return, review, PR, correction, identity conflict, or integration decision on the work surfaces actually inspected for current work, plus older unresolved items already carried in state. `IDLE` is a bounded projection, never proof that no unseen event exists.

## Cold aperture bootstrap — `HELLO`

A cold aperture may run `COMS` read-only without joining. To become addressable for future work, emit a `HELLO` event on an available introduction/reply route.

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
state_seen: <carrier / commit / object anchor or UNKNOWN>
freshness: ANCHORED:<basis> | UNKNOWN | DEGRADED
capabilities: <read/write routes and material limits honestly known>
identity_basis: <support for identity claim, or SELF_CLAIM / UNKNOWN>
authority: NONE | <explicit pre-existing grant reference>
reply_route: <where a response can be observed, if available>
presence: OBSERVED_AT_HELLO
```

A `HELLO` is a bounded arrival event: **it does not create a permanent roster entry and does not prove later availability.** If later work depends on reachability, check the relevant route again or use an explicitly bounded reachability/lease mechanism supplied by that route.

A session ID is an opaque unique identifier for this aperture instance. A UUID is sufficient. Do not reuse a predecessor's session ID.

A receiving aperture may answer with a `WELCOME` event or receipt that references the `HELLO` and states only what it can establish:

```text
in_reply_to: <HELLO event_id>
recognized_role: UNASSIGNED | <assigned role>
session_seen: <session id>
authority: NONE | <grant reference>
preferred_route: <route if established>
task: NONE | <task reference>
```

`WELCOME` does not validate self-reported runtime/model/provider data merely by repeating it. A stable role assignment or mutation grant requires an authority source; reception alone grants nothing.

If protocol versions are incompatible, report the mismatch and stop rather than silently upgrading, downgrading, or reinterpreting semantic fields.

If the cold aperture has no writable COM route, it may emit its `HELLO` through the current transport or an explicitly marked human relay. It remains read-only/non-authoritative until that return is actually observed. A failed or impossible write route must not be rewritten as a successful join.

## COMS

`COMS` means synchronize from shared COM before relying on conversational assumptions.

1. retrieve `COM_STATE.md` from the intended state route;
2. establish the strongest honest freshness anchor for that retrieval; if freshness is `UNKNOWN` or `DEGRADED`, do not take state-dependent mutation from it;
3. establish role/runtime/model/provider/session honestly;
4. if this is first participation and the aperture is not established, use the `HELLO` rule before expecting to be addressed or authorized;
5. locate only tasks addressed to this aperture or role on sufficiently anchored state;
6. if delegated work is shown as active and this aperture owns integration/status, inspect the declared `reply_route` before reporting `WAIT` or `IDLE`; if the route cannot be inspected, report bounded `NOT_OBSERVED` rather than assuming work is still running;
7. verify authority and control before any write;
8. follow the task body or an immutable route object named by state — do not depend on a long issue transcript as the sole carrier of an active instruction;
9. if retrieval/freshness evidence contradicts itself, report `DEGRADED` with bounded evidence and stop affected mutation;
10. if no task is addressed here, do not take another aperture's task;
11. if synchronized and idle, stop.

Normal `COMS` should be cheap. It is a synchronization operation, not an instruction to generate protocol commentary.

## Task / delegation event

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

For delegated/asynchronous work, `reply_route` and `integration_owner` are required. The worker announces a terminal return on that route even when the work product itself lives somewhere else. **An artifact existing is not the same event as the worker returning it.**

When work can remain open across synchronization boundaries, add bounded observation control:

```text
observation_owner: <who must inspect the return/status route>
next_check: <time | state/event trigger | MANUAL>
```

`MANUAL` is allowed when no scheduler is available, but it makes **no autonomous-liveness claim**. COM records responsibility and the expected observation boundary; it does not itself wake an aperture.

A minimal delegation interaction remains an event chain, not a new ontology:

```text
TASK -> ACK | REFUSE
ACK  -> RETURN | FAIL | bounded STATUS
RETURN -> INTEGRATE | REVISE | REJECT
```

`CANCEL` may terminate an open task when authority permits. Each response references the `task_id` and, where useful, the immediate event it answers. Equivalent event kinds are allowed if semantic force remains unambiguous.

At `next_check`, the observation owner inspects the declared route. If the expected event is absent, record bounded `NOT_OBSERVED`. A re-ping, escalation, reassignment, or cancellation is a **new event under explicit authority**, not a silent retry.

Before closing a returned task, emit or record an integration decision so a returned artifact cannot remain silently undecided.

Exact-head discipline applies whenever the result depends on a particular state. **If the relevant head moves outside the acknowledged envelope, do not silently adapt** — re-read, re-negotiate, or report the drift explicitly.

## Parallel work

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
integration_owner
```

One mutator owns one semantic work item at a time unless deliberate collision is visible. **A clean Git merge does not prove semantic integration.**

## Correction

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

## Compression in practice

Default to `summary -> evidence map -> raw evidence`. Add redundancy or an alternate carrier only when uncertainty, consequence, or hardening risk requires it, then collapse back after synchronization.

## Human role

Mark is human authority, not a transport bus.

Human relay is a legitimate fallback and must preserve provenance — but any design that routinely requires a human to shuttle machine-readable state between apertures has not yet met COM's practical goal.

A human issuing `COMS` is a synchronization trigger. That is different from the human carrying the task content or work product. Preserve the distinction.

## Anti-drift test

Before adding anything to this protocol:

> Does this materially improve safe coordination on real work?

If not, leave it out. Then ask whether the existing EVENT / ROUTE / WITNESS / CONTROL / PROJECTION relations already express the need. If they do, add only the smallest rule, field, or event kind required by the observed failure; do not mint another primitive.

COM is not trying to become a universal theory of communication, a consensus engine, a taxonomy of every failure before work resumes, a replacement for Git or issue trackers, a scheduler, or a protocol that consumes more attention than the work it protects.

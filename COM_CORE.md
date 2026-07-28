# COM core v0.3 working candidate

Status: working candidate. Not canon, not validated, not a claim of universal communication theory.

**This file explains what COM's objects are and why they exist.** For what to write and do, see [`COM_PROTOCOL_WORKING.md`](COM_PROTOCOL_WORKING.md). Normative detail for a rule should have one authoritative home across the two files; the other may summarize it and point back.

## What COM is for

COM is a small shared coordination field for independent human and AI apertures working under uncertainty.

Its practical test:

> Can a participant arrive with little or no conversational context, recover enough current state to act safely, preserve disagreement and provenance, and continue without making the human carry the whole collaboration?

COM should reduce coordination burden. If the protocol becomes the work, or makes the human a permanent relay, it is failing.

## The smallest causal model

COM distinguishes what happened from what was observed about what happened.

```text
Aperture -- EVENT[CONTROL] --> Route --> observation by Aperture
                                      |
                                      +--> route state/failure may be witnessed independently
```

The durable record is not one transcript:

```text
COM = Event graph + Witness graph + Current-state projection
```

## The generative recurrence

The same small relations should recur at every scale rather than creating a new ontology for every workflow:

```text
EVENT[CONTROL] --via ROUTE--> observation
                              |
                              v
                           WITNESS
                           /     \
                          v       v
                    next EVENT  PROJECTION update
                                  |
                                  +---- may inform later EVENT
```

`PROJECTION` is **not** a mandatory causal hop. An aperture may act directly on a bounded witness and update shared projection afterward; the COM-OPT-001 deadlock episode demonstrated exactly that. Projection is a derived coordination surface supported by witnesses, not a gate through which every event must pass.

The objects are relational, not a disjoint partition. An emitted witness can itself be carried by an event; what makes it a **WITNESS** is that it is a bounded claim about an event, route, state, or claim. **CONTROL** constrains what an event is permitted to mean or do. **ROUTE** is the carrier with causal state of its own.

`HELLO`, `WELCOME`, `TASK`, `ACK`, `RETURN`, `REFUSE`, `FAIL`, `GRANT`, `REVOKE`, `CANCEL`, and `CORRECT` remain event kinds or relations, not new primitives.

The anti-drift test is conceptual: **can the proposed structure be represented honestly by the existing causal objects?** Add a primitive only when the answer is no and a real failure demonstrates the need. The operational anti-drift rule lives in `COM_PROTOCOL_WORKING.md` under *Anti-drift test*.

### EVENT — what happened or was attempted

An addressable occurrence relevant to shared work: a claim emitted, a task assigned, a mutation attempted, a refusal, a proposed correction, a route accepting or rejecting a write.

**Attempted and completed are different states.** An attempt never implies a success.

When preserved, `source + event_id` identifies one semantic event across retransmission. Redelivery of that same event does not become a second event merely because another route or retry carried it.

If a route or relay cannot preserve the original event identity, identity becomes **UNPRESERVED / UNKNOWN**. That does not prove the received content is a new event and does not prove it is a duplicate. Reuse of a preserved identity with conflicting semantic payload or control is an identity conflict and must be routed to the task/integration owner or other explicit authority before state-dependent mutation proceeds.

### ROUTE — the carrier, which has causal state of its own

GitHub, a pasted relay, an API, a file, email, a model connector.

A route can accept, delay, cache, truncate, reorder, duplicate, transform, hide, or fail — independently of what either aperture intended. Route is causal, not decorative metadata.

Do not collapse Route into authority or into message content.

### WITNESS — a bounded observation by an aperture

A witness is a claim about an event, route, state, or claim, made from one vantage point.

A witness is not truth because it exists, and not truth because several apertures repeat it.

Several things are witness *types* rather than separate primitives:

- **receipt** — "I observed event E at locus L";
- **parse failure** — "I observed carrier content for E but could not reconstruct its meaning";
- **route failure** — a witness about the carrier;
- **staleness** — a witness about an anchor mismatch;
- **freshness unknown** — the route returned content but did not establish whether it was current.

### CONTROL — an envelope, not a causal node

Cross-cutting metadata on events and actions: modality, authority source, permitted effect, ownership and mutation scope, no-touch boundaries, correction/return route, exact base/head where state matters, and bounded observation responsibility where asynchronous work can otherwise remain open indefinitely.

**Semantic force is structural data, not tone.** `SHOULD != MUST`. `EXPECTATION != AUTHORIZATION`. `CAN != MAY`. Absence of a grant is not denial.

## Absence and failure

COM must never turn missing visibility into a claim about another aperture.

> "I did not receive M" does not establish "M was not sent."

A non-observation is a witness about the observer's own vantage, bounded by an explicit expectation. It keeps these outcomes distinct rather than collapsing them into one silence:

- nothing was sent;
- send attempted but rejected;
- sent, then lost or delayed by the route;
- held by the route but not retrievable by the receiver;
- retrieved as bytes but not parseable as meaning;
- received, and no action taken;
- explicitly refused.

Silence is therefore never automatically assent, refusal, unavailability, or absence.

## Correction

Correction is not a primitive node. It is a new event or witness related to prior addressable state.

Corrections are **additive**: they qualify or supersede, and never erase the earlier witness. Prefer the smallest repair that contains the defect. If a defect invalidates dependent state, repair the affected causal cone rather than each visible symptom. If local repair is unsafe, pause mutation and reconstruct from durable evidence.

## Identity

Three layers, kept separate:

- **role** — stable collaboration identity;
- **runtime** — model/provider information, where honestly establishable;
- **session** — this specific aperture instance.

Unknown stays `UNKNOWN`.

A cold aperture that has not been assigned a stable role uses `role: UNASSIGNED`; it does not create authority by naming itself. **Identity claim, transport identity, capability, authority, and current reachability are separate facts.** A GitHub account, API credential, model self-description, or human relay may support part of an identity claim without proving the rest.

A `HELLO` records that an aperture presented itself **at a particular observed anchor**. It is not a permanent roster entry and does not establish ongoing availability. Later work that depends on reachability must use fresh route evidence rather than treating an old `HELLO` as a live presence signal.

A transport gap, elapsed time, topic change, temporary unavailability, or stale read **does not create a new session**. A genuine replacement aperture takes a new session identity and reconstructs continuity from durable state; it never silently inherits predecessor confidence or mutation ownership.

## State, freshness and history

Two public surfaces have different jobs:

1. **durable history and evidence** — append-only enough to preserve what was claimed, done, failed, corrected, or disputed;
2. **`COM_STATE.md`** — a small, replaceable projection of what a participant needs *now*.

Current state is not truth. It is a reconstructable working projection supported by witnesses.

A mutable navigation label such as `main`, `latest`, a branch URL, or a successful file fetch is **not itself freshness proof**. Freshness identity should come from carrier/object metadata that anchors the retrieved object — for example a commit/object identifier where the route exposes one. A state file cannot authenticate its own recency from the inside.

If a route returns coherent state but cannot establish a usable freshness anchor, freshness is `UNKNOWN`, not `CURRENT`. If content and carrier metadata contradict each other, freshness is `DEGRADED`. State-dependent mutation must stop in either case until the required anchor is recovered or the uncertainty is explicitly re-authorized by the relevant authority.

This limit cannot be repaired by writing better prose inside the same potentially stale route. If the route itself cannot expose or verify a sufficient anchor, the aperture remains read-only for state-dependent action through that route. It may still contribute bounded review or witness evidence, but that evidence carries the route's freshness uncertainty. QW's stale `web_extractor` return is evidence of this unresolved route-level limit, not evidence that the prose repair closes it.

`IDLE` means no **known** active task and no **known** unresolved integration decision on the work surfaces the state writer has actually inspected or explicitly carried forward. It must never be read as proof that no unseen work exists.

## Active work and bounded observation

A task is an EVENT carrying a control envelope.

Delegated work needs an explicit return route. Completion is not discoverable merely because an artifact exists somewhere: the worker emits a bounded return event or witness on the declared route, and the integration side inspects that route before concluding the task remains in flight.

COM does not itself provide a scheduler. Delegated/asynchronous work that can remain open across synchronization boundaries **must** name who is responsible for the next observation and the bound/trigger for that observation. A `MANUAL` trigger is honest but makes **no autonomous-liveness claim**. When a bound passes without the expected event, the observer records bounded `NOT_OBSERVED`; any re-ping, escalation or cancellation is a new authorized event, never a silent retry.

Parallel work needs **semantic** ownership, not merely disjoint filenames: one mutator owns one semantic work item at a time, unless a collision is deliberate and visible.

## Compression

Transmit the minimum sufficient state to orient, act, verify, correct, or ask for more.

```text
summary -> evidence map -> raw evidence
```

Compress content. Do not compress provenance, modality, uncertainty, dissent, authority, route state, freshness, or correction paths.

> A summary with no route back to evidence is deletion, not reversible compression.

Adaptive depth is allowed: when uncertainty or consequence rises, add bounded redundancy or an alternate carrier, then collapse back once synchronized.

## Non-goals

COM v0.3 is not a truth oracle, a consensus machine, a universal theory of minds, a requirement to expose private reasoning, a reason to turn every exchange into metadata ceremony, a replacement for domain workflow tools, a scheduler, or a mandate to keep the human in the transport path.

The core succeeds when independent apertures coordinate real work with less ambiguity and less human relay burden than ordinary chat.

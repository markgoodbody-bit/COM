# COM core v0.2 working candidate

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
Aperture -- EVENT --> Route --> observation by Aperture
                         |
                         +--> route state/failure may be witnessed independently
```

The durable record is not one transcript:

```text
COM = Event graph + Witness graph + Current-state projection
```

### EVENT — what happened or was attempted

An addressable occurrence relevant to shared work: a claim emitted, a task assigned, a mutation attempted, a refusal, a proposed correction, a route accepting or rejecting a write.

**Attempted and completed are different states.** An attempt never implies a success.

### ROUTE — the carrier, which has causal state of its own

GitHub, a pasted relay, an API, a file, email, a model connector.

A route can accept, delay, cache, truncate, reorder, duplicate, transform, hide, or fail — independently of what either aperture intended. Route is causal, not decorative metadata.

Do not collapse Route into authority or into message content.

### WITNESS — a bounded observation by an aperture

A witness is a claim about an event, route, or state, made from one vantage point.

A witness is not truth because it exists, and not truth because several apertures repeat it.

Several things are witness *types* rather than separate primitives:

- **receipt** — "I observed event E at locus L";
- **parse failure** — "I observed carrier content for E but could not reconstruct its meaning";
- **route failure** — a witness about the carrier;
- **staleness** — a witness about an anchor mismatch.

### CONTROL — an envelope, not a causal node

Cross-cutting metadata on events and actions: modality, authority source, permitted effect, ownership and mutation scope, no-touch boundaries, correction route, and exact base/head where state matters.

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
- **runtime** — model and provider, where honestly establishable;
- **session** — this specific aperture instance.

Unknown stays `UNKNOWN`.

A transport gap, elapsed time, topic change, temporary unavailability, or stale read **does not create a new session**. A genuine replacement aperture takes a new session identity and reconstructs continuity from durable state; it never silently inherits predecessor confidence or mutation ownership.

## State and history

Two public surfaces with different jobs:

1. **durable history and evidence** — append-only enough to preserve what was claimed, done, failed, corrected, or disputed;
2. **`COM_STATE.md`** — a small, replaceable projection of what a participant needs *now*.

Current state is not truth. It is a reconstructable working projection supported by witnesses.

Freshness identity should come from the carrier object returned by retrieval. A state file cannot authenticate its own recency from the inside. Where content and carrier metadata disagree, freshness is `DEGRADED`, not current.

## Active work

A task is an EVENT carrying a control envelope.

Parallel work needs **semantic** ownership, not merely disjoint filenames: one mutator owns one semantic work item at a time, unless a collision is deliberate and visible.

## Compression

Transmit the minimum sufficient state to orient, act, verify, correct, or ask for more.

```text
summary -> evidence map -> raw evidence
```

Compress content. Do not compress provenance, modality, uncertainty, dissent, authority, route state, or correction paths.

> A summary with no route back to evidence is deletion, not reversible compression.

Adaptive depth is allowed: when uncertainty or consequence rises, add bounded redundancy or an alternate carrier, then collapse back once synchronized.

## Non-goals

COM v0.2 is not a truth oracle, a consensus machine, a universal theory of minds, a requirement to expose private reasoning, a reason to turn every exchange into metadata ceremony, a replacement for domain workflow tools, or a mandate to keep the human in the transport path.

The core succeeds when independent apertures coordinate real work with less ambiguity and less human relay burden than ordinary chat.

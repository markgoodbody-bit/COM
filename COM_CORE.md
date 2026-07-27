# COM core v0.2 working candidate

Status: working candidate. Not canon, not validated, and not a claim of universal communication theory.

## What COM is for

COM is a small shared coordination field for independent human and AI apertures working under uncertainty.

Its practical test is simple:

> Can a participant arrive with little or no conversational context, recover enough current state to act safely, preserve disagreement and provenance, and continue without making the human carry the whole collaboration?

COM should reduce coordination burden. If the protocol itself becomes the work, or makes the human a permanent relay, it is failing its purpose.

## The smallest causal model

COM distinguishes what happened from what was observed about what happened.

```text
Aperture -- EVENT --> Route --> observation by Aperture
                         |
                         +--> route state/failure may be witnessed independently
```

The durable record is not one transcript. It is two coupled graphs plus a current projection:

```text
COM = Event graph + Witness graph + Current-state projection
```

### EVENT

An EVENT is an addressable occurrence or attempted occurrence relevant to shared work.

Examples:
- a claim was emitted;
- a task was assigned;
- a repository mutation was attempted;
- a refusal was emitted;
- a correction was proposed;
- a route accepted or rejected a write.

An event records what can honestly be established about:
- source aperture / actor;
- event kind;
- parent/dependency events;
- payload or payload reference;
- route used or intended;
- time/state anchor where relevant;
- control envelope.

Attempted and completed events are not the same state.

### ROUTE

A ROUTE is the carrier through which an event is expected to propagate.

Examples: GitHub, a pasted relay, an API, a file, email, a model connector.

Route is causal, not decorative metadata. A route can accept, delay, cache, truncate, reorder, duplicate, transform, hide, or fail independently of sender and receiver intent.

Do not collapse Route into authority or message content.

### WITNESS

A WITNESS is a bounded observation or claim made by an aperture about an event, route, or state.

A witness should preserve:

```text
observer
subject
observation
locus / route
state or time anchor where relevant
evidence / evidence route
uncertainty / claim status
modality where semantic force matters
```

A witness is not truth merely because it exists or because several apertures repeat it.

Receipt is a witness type: "I observed event E at locus L."

Parse failure is a witness type: "I observed carrier content for E but could not reconstruct the semantic payload."

Route failure is a witness about the route.

Staleness is a witness about an anchor mismatch.

### CONTROL ENVELOPE

CONTROL is cross-cutting metadata on events/actions, not a causal primitive.

It preserves:
- modality: OBSERVED / INFERRED / REQUEST / SHOULD / MUST / MAY / AUTHORIZE / REFUSE / etc.;
- authority source;
- permitted effect;
- ownership / mutation scope;
- no-touch boundaries;
- correction / return route;
- exact base/head when state mutation depends on it.

Semantic force is structural data. `SHOULD != MUST`. `EXPECTATION != AUTHORIZATION`. `CAN != MAY`. Absence of a grant is not denial.

## Absence and failure

COM must never turn missing visibility into a claim about another aperture.

"I did not receive M" does not establish "M was not sent."

A non-observation should be represented as a witness with an explicit expectation boundary:

```text
expected: <event or event class>
observer: <aperture>
locus: <route / endpoint / state surface>
window_or_anchor: <when / which state was inspected>
observation: NOT_OBSERVED
uncertainty: <what remains unresolved>
```

This keeps distinct:
- nothing was sent;
- send was attempted but rejected;
- send succeeded but route lost/delayed it;
- route holds it but receiver cannot retrieve it;
- receiver retrieved bytes but could not parse meaning;
- receiver received it and chose not to act;
- receiver explicitly refused.

Silence is therefore never automatically assent, refusal, unavailability, or absence.

## Correction

Correction is not a primitive node. It is a new event/witness relation to prior addressable state.

Corrections are additive. They do not erase the earlier witness.

Prefer the smallest causal repair:

```text
PATCH
  target: <prior event/witness/state>
  field_or_relation: <damaged semantic part>
  old: <old value if meaningful>
  new: <new value>
  evidence: <support>
  effect: <what changes and what explicitly does not>
```

If a defect invalidates dependent downstream state, repair the affected causal cone. If local repair is unsafe, pause mutation and reconstruct from durable evidence.

## Identity

Keep three things separate:
- stable role identity;
- runtime/model/provider identity;
- session/aperture instance identity.

Unknown stays UNKNOWN.

A transport gap, elapsed time, topic change, temporary unavailability, or stale read does not by itself create a new session.

A real replacement aperture gets a new session identity and reconstructs continuity from durable state. It never silently inherits predecessor confidence or mutation ownership.

## State and history

COM has two public surfaces with different jobs:

1. durable history/evidence: append-only enough to preserve what was actually claimed, done, failed, corrected, or disputed;
2. `COM_STATE.md`: a small replaceable projection of what a participant needs now.

Current state is not truth. It is a reconstructable working projection supported by witnesses.

Do not put a self-referential `current_head` inside the state file. Freshness identity should come from the carrier/object returned by retrieval where possible. An internal `written_from` or `state_basis` may name the state the update was based on, but must not masquerade as the commit containing itself.

If carrier metadata and visible content disagree, classify freshness as DEGRADED rather than CURRENT.

## Active work

A task is an EVENT with a control envelope.

A mutation-capable task should normally carry:

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

Parallel work additionally needs explicit semantic ownership. One mutator owns one semantic defect/work item at a time unless collision is deliberate and visible.

## COMS

`COMS` means: synchronize from the shared COM surface before using conversational assumptions.

Default behavior:

1. read `COM_STATE.md`;
2. establish honestly available identity/session information;
3. inspect the current task only if it is addressed to this aperture/role;
4. verify control/authority before mutation;
5. use the task body or an immutable route object named by current state — do not depend on a long issue transcript as the sole carrier;
6. if freshness or retrieval is contradictory, report DEGRADED with the smallest useful evidence and stop unsafe mutation;
7. if no task is addressed here, do not steal another aperture's task;
8. if synchronized and no action is required, stop.

`COMS` is a synchronization operation, not a command to generate protocol commentary.

## Compression

Transmit the minimum sufficient state needed to orient, act, verify, correct, or ask for more.

```text
summary -> evidence map -> raw evidence
```

Compress content, not provenance, modality, uncertainty, dissent, authority, route state, or correction paths.

A summary with no route back to evidence is deletion, not reversible compression.

Adaptive depth is allowed: when uncertainty or consequence rises, add bounded redundancy or an alternate carrier; once synchronized, collapse back down.

## Non-goals

COM v0.2 is not:
- a truth oracle;
- a consensus machine;
- a universal theory of minds;
- a requirement to expose private chain-of-thought;
- a reason to turn every exchange into metadata ceremony;
- a replacement for domain-specific workflow tools;
- a mandate to keep Mark in the transport path.

The core succeeds when independent apertures can coordinate real work with less ambiguity and less human relay burden than ordinary chat.
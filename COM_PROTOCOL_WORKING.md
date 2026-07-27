# COM protocol v0.2 working candidate

Status: working candidate. Not canon and not validated.

Read `COM_CORE.md` for the causal model. This file defines the smallest practical operating discipline.

## 1. Purpose

COM exists to let independent apertures coordinate real work under uncertainty while preserving identity, provenance, semantic force, authority, route state, disagreement, and correction.

Success is not more protocol. Success is less ambiguity and less human relay burden.

## 2. Core objects

COM distinguishes:

```text
EVENT   = what happened or was attempted
ROUTE   = carrier/channel with causal state of its own
WITNESS = bounded observation/claim about an event, route, or state
STATE   = compact current projection supported by witnesses
```

CONTROL is an envelope on events/actions, not a separate causal node.

CORRECTION is a relation/event that qualifies or supersedes prior addressable state without erasing it.

RECEIPT is a witness type, not a primitive.

## 3. Minimal event record

Use only the fields required by consequence and uncertainty.

A durable EVENT should be able to preserve:

```text
event_id
source
kind
parents / dependencies
payload or payload_ref
route
state/time anchor where relevant
control
status: ATTEMPTED | ACCEPTED | COMPLETED | REJECTED | UNKNOWN
```

Do not invent a successful event from an attempt.

## 4. Minimal witness record

A WITNESS should be able to preserve:

```text
witness_id
observer
subject: <event | route | state | claim>
observation
locus / route
anchor / observation window where relevant
evidence or evidence_ref
uncertainty / claim_status
```

One useful human-readable encoding remains:

```text
ANCHOR -> DELTA -> EVIDENCE -> CONTROL
```

but this is an encoding convenience, not COM's ontology.

- ANCHOR: identity, parents, relevant state/freshness.
- DELTA: event, observation, request, or change that matters now.
- EVIDENCE: source, scope, uncertainty, route to deeper evidence.
- CONTROL: modality, authority, permitted effect, ownership, return/correction route.

Do not force all four labels into tiny routine messages when meaning is already unambiguous.

## 5. Semantic force

Preserve modality exactly enough that a receiver does not accidentally strengthen or weaken authority.

```text
SHOULD != MUST
EXPECTATION != AUTHORIZATION
CAN != MAY
MAY != MUST
OBSERVED != INFERRED
ABSENCE OF A GRANT != DENIAL
ATTEMPTED != COMPLETED
NOT OBSERVED != DID NOT EXIST
```

A semantically stronger paraphrase is a state change, not compression.

## 6. Non-observation and failure

Never infer another aperture's state merely from local absence.

Record non-observation at an explicit boundary:

```text
expected: <event / event class>
observer: <aperture>
locus: <route / endpoint / state surface>
window_or_anchor: <time/state inspected>
observation: NOT_OBSERVED
uncertainty: <unresolved causal possibilities>
```

Keep distinct:
- not sent;
- send attempted and rejected;
- sent but delayed/lost;
- present on route but not retrievable by receiver;
- retrieved but unparseable;
- received but no action taken;
- explicit refusal.

Silence never means assent.

## 7. Evidence discipline

Evidence should preserve source, scope, freshness/anchor where relevant, and uncertainty.

Successful retrieval of one file does not prove exhaustive repository inspection.

A model statement does not become provider evidence because it sounds confident.

Agreement between apertures is not validation.

## 8. Identity and session discipline

Separate:
- stable role;
- runtime/model/provider;
- session/aperture instance.

Unknown remains `UNKNOWN`.

A new session boundary must be established, not inferred from elapsed time, temporary unavailability, topic changes, or carrier failure.

A real replacement session receives a new session identity and reconstructs continuity from durable COM. It does not inherit predecessor mutation ownership silently.

## 9. Current state and history

Use two surfaces:

1. durable history/evidence;
2. `COM_STATE.md`, a compact current projection.

Current state does not rewrite history. History does not need to be retransmitted during normal operation.

Do not store a self-referential `current_head` inside `COM_STATE.md`. Use retrieval/carrier object identity for the file/commit actually observed. An internal `state_basis` may identify the prior state on which an update was based.

If visible content and carrier metadata disagree, classify freshness `DEGRADED` and stop unsafe mutation.

## 10. COMS

`COMS` means synchronize from shared COM before relying on conversational assumptions.

On `COMS`:

1. read `COM_STATE.md`;
2. establish identity/session honestly;
3. locate only tasks addressed to this aperture/role;
4. verify authority/control before any write;
5. follow an embedded task or immutable route object named by state;
6. do not depend on a long issue transcript as the sole carrier of an active instruction;
7. if retrieval/freshness contradicts itself, report `DEGRADED` with bounded evidence and stop mutation;
8. if no addressed task exists, do not take another aperture's task;
9. if synchronized and idle, stop.

Normal `COMS` should be cheap.

## 11. Task / work event

A mutation-capable TASK event should normally state:

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

For code/repository mutation, exact-head discipline applies whenever the result depends on a particular state.

If the relevant head moves outside the acknowledged envelope, do not silently adapt. Re-read/re-negotiate or explicitly report the drift.

## 12. Parallel work

Parallel work requires semantic ownership, not merely disjoint filenames.

For each active work item:

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
merge/integration owner
```

One mutator owns one semantic defect/work item at a time unless deliberate collision is visible.

A clean Git merge does not prove semantic integration.

## 13. Correction

Corrections are additive and recursively correctable.

Prefer the smallest patch that contains the defect:

```text
PATCH
  target
  field_or_relation
  old
  new
  evidence
  effect
```

If an upstream error invalidates many descendants, repair the causal cone rather than cosmetically rewriting each symptom.

If local repair becomes unsafe, pause mutation and reconstruct from durable evidence/state.

## 14. Compression and adaptive depth

Default:

```text
summary -> evidence map -> raw evidence
```

Compress content, not provenance, modality, uncertainty, dissent, authority, route state, or correction paths.

Use more redundancy only when uncertainty, consequence, or hardening risk requires it. Collapse back after synchronization.

A summary with no route back to evidence is deletion, not reversible compression.

## 15. Human role

Mark is human authority, not intended to be a permanent transport bus.

Human relay is a legitimate fallback and must preserve provenance, but any design that routinely requires Mark to shuttle machine-readable state between apertures has not yet achieved COM's practical goal.

## 16. Non-goals / anti-drift

COM v0.2 is not trying to become:
- a universal theory of communication;
- a truth or consensus engine;
- a taxonomy for every possible failure before real work resumes;
- a replacement for Git, issue trackers, or domain tooling;
- a protocol that consumes more attention than the work it protects.

When in doubt, ask: does this addition materially improve safe coordination on real work? If not, leave it out.
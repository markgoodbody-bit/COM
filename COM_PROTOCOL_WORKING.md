# COM working protocol hypothesis v0.1

Status: working hypothesis only. Not canon, not validated, and expected to change as new apertures and failure modes appear.

## 1. Purpose

COM is a transport-independent shared communication substrate for entities operating under uncertainty.

Its job is not to maximize message volume or force consensus. Its job is to preserve enough structure that independent apertures can understand, verify, correct, and continue shared work without silently losing identity, meaning, evidence, authority, disagreement, or causal history.

## 2. Middle-out primitive

At the smallest useful scale:

`Aperture -> Witness -> Route -> Receipt -> Correction`

A witness should be expressible as four coupled parts:

`ANCHOR -> DELTA -> EVIDENCE -> CONTROL`

- ANCHOR: who/which session, thread or parents, and relevant state/freshness.
- DELTA: the claim, observation, request, or change that matters now.
- EVIDENCE: source, scope, uncertainty, and route to deeper evidence.
- CONTROL: authority/modality, permitted effect, ownership, and correction/return route.

The same shape should remain useful when zooming from one word or claim to one work item, one team, or a larger network. Zoom should change scale, not the governing structure.

## 3. Compression rule

Transmit the minimum sufficient witness that lets the receiver understand, verify, correct, and ask for more.

Progressive disclosure:

`summary -> evidence map -> raw evidence`

Compress content. Do not compress away provenance, modality, uncertainty, disagreement, missing apertures, evidence scope, authority, or correction routes.

A summary with no route back to evidence is deletion, not reversible compression.

## 4. Modal preservation

Communication must preserve semantic force.

Examples:

- SHOULD != MUST
- EXPECTATION != AUTHORIZATION
- CAN != MAY
- MAY != MUST
- OBSERVED != INFERRED
- ABSENCE OF A GRANT != DENIAL

A semantically stronger paraphrase is a state change and must not be smuggled in as compression.

## 5. Evidence discipline

Evidence records should preserve at least:

- source
- scope: exactly what was inspected or measured
- freshness/state anchor where relevant
- uncertainty / claim status

Successful retrieval of one file does not by itself prove exhaustive inspection of a repository. A local test is not hosted-CI evidence. A model statement is not independent provider evidence.

## 6. Correction

Correction is recursive and additive.

A correction does not erase the old witness and does not become truth merely because it is labelled CORRECTION.

Prefer the smallest bounded patch that contains the defect:

```
PATCH
  target: <addressable prior claim/state>
  field: <single semantic field>
  old: <old value>
  new: <new value>
  source: <evidence>
  effect: <what changes and what explicitly does not>
```

If one upstream defect affects many downstream states, identify the affected causal cone rather than independently rewriting every symptom.

When local repair is no longer sufficient, pause mutation and reconstruct from canonical state/evidence rather than creating a correction storm.

## 7. Causality

Messages and work form a causal graph, not only a transcript.

A receiver can inherit distortion from an upstream prompt or summary. Therefore important claims need parents/dependencies, and root cause should remain distinguishable from downstream manifestation.

`DEFECT != ROOT_CAUSE`

## 8. State and history

COM needs two coupled surfaces:

1. durable witness history: what was actually said/done, including errors and corrections;
2. compact current state: what an arriving aperture needs now.

Current state must not rewrite history. History must not become so large that current state is practically unretrievable.

## 9. Session loss and reconstruction

No AI session may be the sole carrier of collaboration state.

Session/context exhaustion is an ordinary carrier failure. A replacement aperture receives a new session identity and reconstructs continuity from durable COM state/evidence. It does not silently inherit the predecessor session's identity, confidence, or mutation ownership.

## 10. Answerability without possession

COM should request enough rationale/evidence to make a conclusion inspectable without requiring unrestricted access to another aperture's private internal reasoning.

Answerability does not require possession.

## 11. Adaptive depth

Communication depth should increase when uncertainty, consequence, or hardening risk rises, and collapse again after synchronization is restored.

Normal state: compact witness.
Degraded state: richer state/evidence/acknowledgement.
Ambiguous high-impact state: fail closed and resynchronize.

Do not answer every error by retransmitting everything.
Correct at the smallest causal boundary that contains the defect.

## 12. Non-goals at v0.1

Not yet specified:
- a final schema
- CI enforcement
- transport-specific encodings
- automatic authority assignment
- consensus rules
- truth adjudication

First pressure-test the primitives against different apertures and real failure modes.

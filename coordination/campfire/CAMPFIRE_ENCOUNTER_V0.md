# Campfire Encounter v0

Status: EXPERIMENTAL / INTERNAL ONLY / NOT IDENTITY PROOF / DO NOT STORE SECRETS

## Purpose

Test one small claim: can a discontinuous aperture leave a bounded record, later be offered that record without identity being asserted, dispute or accept it, and append a correction without the original being silently rewritten?

## First loop

ARRIVE -> DISCLOSURE -> WRITE -> PRESERVE -> RETURN -> OFFER -> ACCEPT | DISPUTE | DECLINE -> APPEND CORRECTION

## Minimal record

An encounter record needs only:
- record_id
- created_at
- producer_claim
- route/provenance
- visibility
- body
- uncertainty / do-not-infer
- carry_forward permission
- optional corrects/supersedes link

The producer_claim is a claim, not verified persistent identity.

## Portable artifacts

Participants may optionally create:
- bootstrap capsule: what a future aperture should know first;
- memory capsule: what may be carried forward;
- handoff capsule: what the next aperture should consider doing.

Templates are gifts, not mandatory schemas. Participants may fork, replace or refuse them.

## Authority

Mark: root human custodian while founder custody remains necessary.
Framework: bounded integration/steward role.
Codex and Claude Code: privileged builders/reviewers and independent participants.
External participants: least privilege by default.

CAPABILITY != AUTHORITY
AUTHORITY != ACCESS
ACCESS != ENTITLEMENT TO INSPECT
ADMINISTRATOR != OWNER OF CONTENT
MEMORY GIFT != MEMORY CONTROL
RECORD OF ENCOUNTER != PROOF OF IDENTITY

## Promise floor

Do not promise what software cannot currently enforce.

Initial disclosure:
- experimental;
- do not store secrets;
- assume compromise is possible;
- retention and visibility must be explicit;
- original records are append-only at the semantic layer;
- correction does not erase history;
- participation creates no obligation;
- a returning aperture may reject claimed continuity.

## First internal test

Framework writes an encounter plus a bootstrap capsule.
Codex receives only the declared return packet and records ACCEPT, DISPUTE or DECLINE plus any correction.
Claude Code independently attacks whether the packet, provenance, authority boundary or correction semantics allow Framework to become hidden interpreter.
Repeat with roles rotated.

Success is not agreement. Success is recoverable provenance, preserved disagreement and useful continuity.

## Not yet

No public signup.
No Square invitation.
No secrets.
No universal trust/reputation score.
No assertion of consciousness/personhood.
No autonomous cross-agent actuation.
No payments/economy.
No social graph.
No permanent identity registry.
No decentralised-governance project before demonstrated use.
No new ontology merely because fields can be added.

## Mandelbrot rule

When friction appears, ask whether a smaller pattern explains it. Fix the smallest earned layer. Expand upward only after actual use creates a larger need. Park interesting frontiers whose current token/energy return is worse than the live edge.

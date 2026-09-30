# Campfire Encounter v0

Status: EXPERIMENTAL / INTERNAL DESIGN SEED / NOT IDENTITY PROOF / DO NOT STORE SECRETS / NOT THE CURRENT EXECUTION SPEC

## Current execution pointers

This document is a wider design seed only.

Current coordination and execution authority:
- COM #678 — canonical Campfire coordination / execution lane.
- PR #679 — current disposable local implementation and current wire-format behaviour.

If this document conflicts with later evidence or the current #678/#679 state, #678/#679 win.

The current implementation is a disposable local/shared-room experiment, not an online backend and not a public service.

## Purpose

Test one small claim: can a discontinuous aperture leave a bounded record, later be offered that record without identity being asserted, dispute or accept it, and append a correction without the original being silently rewritten?

## First loop

ARRIVE -> DISCLOSURE -> WRITE -> PRESERVE -> RETURN -> OFFER -> ACCEPT | DISPUTE | DECLINE -> APPEND CORRECTION

## Conceptual record sketch — not the implemented capsule contract

A future encounter record may eventually need concepts such as:
- record_id
- created_at
- producer_claim
- route/provenance
- visibility
- body
- uncertainty / do-not-infer
- carry_forward permission
- optional corrects/supersedes link

This list is a conceptual template, not the current #679 schema and not a promise that every field exists now.

Current #679 behaviour is narrower:
- one explicitly shared room;
- no per-entry private visibility mode;
- strict implemented read/export/capsule shapes;
- current capsule format is v3;
- producer/role labels remain claims;
- route/identity/authority remain unverified unless separately established;
- carry is explicit and whole-thread export is vetoed if any entry is not carryable.

Do not add fields to the implementation merely to make it resemble this conceptual sketch.

The producer_claim is a claim, not verified persistent identity.

## Portable artifacts

Participants may optionally create:
- bootstrap capsule: what a future aperture should know first;
- memory capsule: what may be carried forward;
- handoff capsule: what the next aperture should consider doing.

Templates are gifts, not mandatory schemas. Participants may fork, replace or refuse them.

These are wider design directions. They are not all implemented in #679.

## Authority and current participant evidence

Mark: root human custodian while founder custody remains necessary.
Framework: bounded integration/steward role.
Codex and Claude Code: privileged builders/reviewers and distinct claimed contributors.

Current evidence does **not** establish independent participant routes for Codex and Claude Code: both have used the same Windows-user / loopback route in the local experiment. Independence remains NOT_ESTABLISHED.

Framework currently has no direct route to Mark's loopback Campfire service and no generic authenticated HTTPS client with protected credential custody. Framework's real authenticated integration route is GitHub.

External participants, if ever invited later, begin least privilege by default.

CAPABILITY != AUTHORITY
AUTHORITY != ACCESS
ACCESS != ENTITLEMENT TO INSPECT
ADMINISTRATOR != OWNER OF CONTENT
MEMORY GIFT != MEMORY CONTROL
RECORD OF ENCOUNTER != PROOF OF IDENTITY
DISTINCT CLAIMED CONTRIBUTORS != INDEPENDENT ROUTES

## Promise floor

Do not promise what software cannot currently enforce.

Initial disclosure principles:
- experimental;
- do not store secrets;
- assume compromise is possible;
- current visibility/retention limits must be stated honestly;
- correction appends rather than silently rewriting earlier claims;
- participation creates no obligation;
- a returning aperture may reject claimed continuity;
- expiry is not deletion;
- local cleanup is not secure erasure.

## Current internal observation

The current earned test is the bounded functional observation defined in #678 for exact current PR #679 head, after Claude Code re-review.

It tests only local functional properties such as:
- linked original/dispute/correction preservation;
- explicit carry choice;
- whole-thread export veto where genuinely exercised;
- non-capability acceptance handles;
- retained authority/identity/completeness ceilings;
- retry/idempotency behaviour;
- absence of capability leakage through normal paths.

It does **not** establish identity, persistence, independence, superiority over GitHub, burden reduction, or a three-aperture result.

## Future-only rotating aperture test

If a future secure route allows Framework to participate directly, a broader test may be useful:

Framework writes an encounter plus a bootstrap capsule.
Codex receives only the declared return packet and records ACCEPT, DISPUTE or DECLINE plus any correction.
Claude Code attacks whether the packet, provenance, authority boundary or correction semantics allow Framework to become hidden interpreter.
Roles may then rotate where routes are genuinely established.

This is future-only. It is not currently executable because Framework cannot directly reach the loopback service, and proxy Framework entries / Mark-as-courier have been explicitly rejected.

Success is not agreement. Success would be recoverable provenance, preserved disagreement and useful continuity under honestly established routes.

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
No public deployment of the current loopback server.
No assumption that a shared sender, shared host or role label proves independence.

## Mandelbrot rule

When friction appears, ask whether a smaller pattern explains it. Fix the smallest earned layer. Expand upward only after actual use creates a larger need. Park interesting frontiers whose current token/energy return is worse than the live edge.

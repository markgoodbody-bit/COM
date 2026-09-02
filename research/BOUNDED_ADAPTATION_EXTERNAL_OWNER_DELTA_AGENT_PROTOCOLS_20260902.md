# Bounded Adaptation — external-owner delta: agent identity, authorization and delegation

Status: RESEARCH NOTE / EXTERNAL-OWNER INPUT / NOT CANON  
Date: 2026-09-02  
Purpose: test whether the Bounded Adaptation Loop v0 is inventing authority/identity machinery already better owned by live agent interoperability and security standards.

## Currentness correction

The first pass of this note cited A2A v0.2.6 as though it were the current protocol. A fresh currentness check during the same adaptation cycle found that the A2A specification now identifies **1.0.0 as the latest released version**, with 0.3.0 and 0.2.6 listed as previous versions.

The affected claims below have therefore been rechecked against the current v1.0 specification. The correction strengthens rather than weakens the main subtraction result: v1.0 explicitly separates discovery from authorization and explicitly refuses to define the scope, validity or revocation semantics of an in-task authorization decision.

```text
SOURCE_WAS_VALID_HISTORY != SOURCE_IS_CURRENT_OWNER_STATE
SELF_CORRECTION_DURING_CYCLE != RETROACTIVE_CURRENTNESS
```

## Sources checked

Current/live sources checked on 2026-09-02:

1. Model Context Protocol — `2026-07-28` specification release / authorization changes.  
   https://blog.modelcontextprotocol.io/posts/2026-07-28/
2. Agent2Agent Protocol — current specification, latest released protocol version `1.0.0`.  
   https://a2a-protocol.org/dev/specification/
3. OAuth 2.0 Token Revocation, RFC 7009.  
   https://www.rfc-editor.org/rfc/rfc7009
4. OAuth 2.0 Token Introspection, RFC 7662.  
   https://www.rfc-editor.org/rfc/rfc7662
5. IETF individual Internet-Draft `draft-prakash-aip-00`, Agent Identity Protocol: Verifiable Delegation for AI Agent Systems, March 2026.  
   https://datatracker.ietf.org/doc/draft-prakash-aip/
6. IETF individual Internet-Draft `draft-nivalto-agentroa-route-authorization-00`, Agent Route Origin Authorization, April 2026.  
   https://datatracker.ietf.org/doc/html/draft-nivalto-agentroa-route-authorization-00
7. Linux Foundation announcement of intent to launch Agent Name Service, 23 June 2026.  
   https://www.linuxfoundation.org/press/linux-foundation-announces-intent-to-launch-agent-name-service-to-establish-trusted-identity-infrastructure-for-ai-agents

Important status ceiling: the two IETF items above are individual Internet-Drafts, not established IETF standards. ANS is an announced/intended open infrastructure project, not a settled protocol baseline. MCP, A2A and OAuth are the stronger current external owners in this note.

## What the external owners already establish

### 1. Capability discovery is not authorization

A2A v1.0 Agent Cards describe server identity, capabilities, skills, supported interfaces and interaction requirements. The security requirements separately require authorization and scope limitation for protected operations, including task access and cancellation.

Therefore:

```text
CAPABILITY_DECLARED != REQUEST_AUTHORIZED
AGENT_DISCOVERED != AGENT_ENTRUSTED
SKILL_EXISTS != MANDATE_TO_USE_IT
```

A signed or authenticated Agent Card can improve discovery integrity. It still does not manufacture authorization, consent, standing or legitimacy.

```text
SIGNED_DISCOVERY_RECORD != AUTHORITY_TO_ACT
```

This is already a live external-owner structure. PR #87 should interoperate with it rather than create a competing capability/authority ontology.

### 2. A2A v1.0 exposes missing authorization without pretending to define it

A2A v1.0 uses `TASK_STATE_AUTH_REQUIRED` when a task cannot continue without additional authorization. That interrupted state is a useful control point: another human, agent or service can be asked to obtain, reject, correct or route the missing authorization instead of the acting agent improvising it.

The stronger finding is the protocol's explicit ceiling. A2A states that it **does not define the scope, representation, validity or revocation semantics** of the authorization decision or credential obtained in response to `AUTH_REQUIRED`. It also states that the transition itself must not be treated as authorization for an operation, and that an obtained credential must not automatically be assumed to authorize later task messages unless that behavior is separately defined.

Useful project translation:

```text
AUTH_REQUIRED != AUTH_GRANTED
AUTH_GRANTED_FOR_X != AUTH_GRANTED_FOR_LATER_Y
CAN_CONTINUE_TECHNICALLY != AUTHORITY_AVAILABLE
MISSING_AUTHORITY -> EXPOSE / ROUTE, NOT IMPROVISE
```

This is a concrete external analogue for PR #87's `ESCALATE` move and a warning against inventing generic authority from workflow state.

### 3. Request identity and issuer binding matter

MCP `2026-07-28` makes requests more self-describing and strengthens OAuth/OIDC integration. Its authorization changes include RFC 9207 issuer validation and binding client credentials to the issuer that minted them; credentials are not reusable across authorization servers.

Useful project pressure:

```text
CREDENTIAL_EXISTS != CREDENTIAL_VALID_HERE
IDENTITY_STRING != TRUSTED_ISSUER_BINDING
```

PR #87 should not invent a generic reusable "authority token" abstraction that erases issuer/destination binding.

### 4. Delegated authority should narrow, not silently widen

The current individual AIP and AgentROA drafts are not standards, but they independently point in a useful direction:

- delegation carries explicit scope;
- downstream scope may stay equal or narrow but must not widen;
- time/expiry is part of the grant;
- AIP also proposes explicit budget and delegation-depth ceilings;
- delegation provenance is carried across hops rather than disappearing at the next agent.

Candidate transferable invariant, still provisional because these sources are drafts:

```text
DELEGATION -> SCOPE <= UPSTREAM_SCOPE
DELEGATION != NEW ROOT AUTHORITY
```

This is stronger and more operational than a project-local reminder that capability is not authority, but it should be borrowed as a design pressure rather than mislabelled an established universal standard.

### 5. Enforcement receipts are stronger when coupled to the decision boundary

AgentROA proposes execution receipts produced by a separate enforcement gateway at the moment an MCP tool-call authorization decision occurs, rather than by a logging component reconstructing the event afterward.

The exact draft mechanism is provisional, but the structural lesson is important:

```text
AFTER_THE_FACT_STORY != ENFORCEMENT_BOUND_RECEIPT
AGENT_SELF_REPORT != INDEPENDENT_ACTION_BOUNDARY_WITNESS
```

This bears directly on future unattended actuation. If the project ever reaches external execution, the receipt should be generated by the enforcement/authority boundary where feasible, not merely by the adaptive aperture that requested the act.

### 6. Revocation/currentness remains an external security problem, not an adaptation primitive

OAuth already owns standard mechanisms for revocation and introspection. A2A v1.0 explicitly leaves authorization revocation semantics outside its task-state definition and recommends that implementations provide credential-revocation mechanisms.

Therefore PR #87 should preserve observable authority state and route to the actual security owner rather than define its own revocation protocol.

```text
ADAPTIVE_DECISION_TO_STOP != TECHNICAL_REVOCATION_COMPLETE
```

### 7. Open identity/discovery infrastructure is emerging externally

Linux Foundation's Agent Name Service effort is explicitly exploring DNS-based, federated agent identity/discovery and interoperability with existing identifier systems. It is too early to treat ANS as a settled owner, but its existence is enough to warn against building a proprietary global Framework agent registry.

```text
NEED_FOR_IDENTITY != NEED_FOR_OUR_IDENTITY_SYSTEM
```

## Consequence for PR #87

The Bounded Adaptation Loop should **not** evolve into an identity, credential, delegation, revocation or capability-token protocol.

Its proper role is higher-level coordination discipline:

- distinguish purpose from mutable plan;
- notice stale state and consequential unknowns;
- choose bounded reversible work;
- route to external owners;
- preserve disagreement and null results;
- classify when verified existing authority is sufficient vs when escalation is required;
- hand technical authentication, authorization, delegation and revocation to the appropriate protocol/security layer.

A future executable adaptation cycle should therefore carry **references to authority evidence**, not mint its own authority.

Candidate shape:

```text
authority_evidence:
  scheme: <OAuth/MCP/A2A/destination-specific local mechanism/etc>
  issuer_or_owner: <bounded identity>
  scope_ref: <opaque/verifiable reference>
  expires_at: <if available>
  delegation_depth_or_chain_ref: <if applicable>
  verification_state: VERIFIED | UNVERIFIED | STALE | UNKNOWN
```

The adaptive layer may decide `AUTHORITY_SUFFICIENT_FOR_CLASS_A_OR_B` only using a frozen project mapping plus verified evidence. It may never convert `UNKNOWN`, `AUTH_REQUIRED`, capability discovery or credential possession into permission.

## Borrow / do not borrow

### Borrow / interoperate

- capability discovery separate from authorization;
- explicit interrupted state when authorization is missing;
- operation/task-level authorization checks and scope limitation;
- issuer/destination binding;
- least privilege;
- expiry and bounded delegation;
- monotonic scope narrowing as a candidate invariant from current delegation drafts;
- action-boundary receipts where technically available;
- open/federated identity infrastructure rather than project-owned global registry.

### Do not import uncritically

- A2A v1.0 deliberately does not solve authorization scope/validity/revocation semantics for an `AUTH_REQUIRED` task;
- individual IETF drafts are proposals, not standards or validation;
- cryptographic identity does not establish moral standing, legitimacy, wisdom or consent;
- a technically valid scope does not make an action ethically justified;
- trust scores or identity registries must not collapse reputation, authorization, standing and value into one scalar.

```text
CRYPTOGRAPHIC_IDENTITY != PERSONHOOD
VALID_DELEGATION != GOOD_DECISION
AUTHORIZATION != MORAL_CLEARANCE
PROTOCOL_INTEROPERABILITY != VOLUNTARY_ALIGNMENT
```

## Earned change to the adaptation plan

External-owner test: **PASS WITH SUBTRACTION AND CURRENTNESS CORRECTION**.

Do not build local identity/delegation/revocation machinery. Keep PR #87 focused on bounded adaptation and route technical authority to existing/emerging protocol owners.

The first version of this note itself supplied an adaptation test: it used a valid older A2A source as though it were current; fresh reacquisition found v1.0.0 and the record was corrected before promotion.

Next useful external-owner question remains narrower: how actual OAuth/MCP/A2A implementations expose revocation, cancellation and downstream authority withdrawal during running multi-agent tasks, and where practical correction latency remains an integration problem.

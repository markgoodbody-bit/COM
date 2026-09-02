# Bounded Adaptation — external-owner delta: agent identity, authorization and delegation

Status: RESEARCH NOTE / EXTERNAL-OWNER INPUT / NOT CANON  
Date: 2026-09-02  
Purpose: test whether the Bounded Adaptation Loop v0 is inventing authority/identity machinery already better owned by live agent interoperability and security standards.

## Currentness corrections

This note has now failed two useful currentness checks during the same adaptation cycle.

1. The first pass cited A2A v0.2.6 as though it were current. Fresh reacquisition found A2A **v1.0.0** is the latest released protocol. The affected claims were rechecked against v1.0.
2. The repaired pass still cited `draft-prakash-aip-00`. An independent Codex review found IETF's Internet-Draft announcement for **`draft-prakash-aip-01`**, dated 2026-08-19. Framework independently rechecked that announcement before applying this correction.

`draft-prakash-aip-01` remains an **individual Internet-Draft / work in progress**, not an IETF standard or endorsement. The revision retains the invocation-bound capability/delegation approach while adding a normative verification algorithm, canonical chained-policy encoding, composition with workload identity systems such as SPIFFE, and mapping against cross-organisation delegation requirements.

```text
SOURCE_WAS_VALID_HISTORY != SOURCE_IS_CURRENT_OWNER_STATE
CURRENT_DRAFT != STANDARD
SELF_CORRECTION_DURING_CYCLE != RETROACTIVE_CURRENTNESS
```

## Sources checked

Current/live sources checked or rechecked on 2026-09-02:

1. Model Context Protocol — `2026-07-28` release / authorization changes.  
   https://blog.modelcontextprotocol.io/posts/2026-07-28/
2. Agent2Agent Protocol — current specification, latest released protocol version `1.0.0`.  
   https://a2a-protocol.org/dev/specification/
3. OAuth 2.0 Token Revocation, RFC 7009.  
   https://www.rfc-editor.org/rfc/rfc7009
4. OAuth 2.0 Token Introspection, RFC 7662.  
   https://www.rfc-editor.org/rfc/rfc7662
5. IETF individual Internet-Draft `draft-prakash-aip-01`, *Agent Identity Protocol (AIP): Verifiable Delegation for AI Agent Systems*, 19 August 2026.  
   IETF announcement: https://mailarchive.ietf.org/arch/msg/i-d-announce/4HkwYS4rHfty6vPkYH7M6PujJQA/  
   Draft HTML: https://www.ietf.org/archive/id/draft-prakash-aip-01.html
6. IETF individual Internet-Draft `draft-nivalto-agentroa-route-authorization-00`, *Agent Route Origin Authorization*, April 2026.  
   https://datatracker.ietf.org/doc/html/draft-nivalto-agentroa-route-authorization-00
7. Linux Foundation announcement of intent to launch Agent Name Service, 23 June 2026.  
   https://www.linuxfoundation.org/press/linux-foundation-announces-intent-to-launch-agent-name-service-to-establish-trusted-identity-infrastructure-for-ai-agents

Important status ceiling: the two Internet-Drafts are proposals/work in progress, not established IETF standards. ANS is announced/emerging infrastructure, not a settled protocol baseline. MCP, A2A and OAuth are the stronger current external owners in this note.

## What the external owners already establish

### 1. Capability discovery is not authorization

A2A v1.0 Agent Cards describe server identity, capabilities, skills, supported interfaces and interaction requirements. Protected operations separately require authorization and scope limitation.

```text
CAPABILITY_DECLARED != REQUEST_AUTHORIZED
AGENT_DISCOVERED != AGENT_ENTRUSTED
SKILL_EXISTS != MANDATE_TO_USE_IT
SIGNED_DISCOVERY_RECORD != AUTHORITY_TO_ACT
```

PR #87 should interoperate with that separation rather than create a competing capability/authority ontology.

### 2. A2A v1.0 exposes missing authorization without pretending to define it

A2A v1.0 uses `TASK_STATE_AUTH_REQUIRED` when a task cannot continue without additional authorization. The protocol explicitly states that this transition alone is not authorization and does **not** define the scope, representation, validity or revocation semantics of the resulting authorization decision/credential.

```text
AUTH_REQUIRED != AUTH_GRANTED
AUTH_GRANTED_FOR_X != AUTH_GRANTED_FOR_LATER_Y
CAN_CONTINUE_TECHNICALLY != AUTHORITY_AVAILABLE
MISSING_AUTHORITY -> EXPOSE / ROUTE, NOT IMPROVISE
```

This is a concrete external analogue for PR #87's `ESCALATE` behaviour.

### 3. Request identity and issuer binding matter

MCP `2026-07-28` strengthens OAuth/OIDC integration and issuer binding. A credential existing is not sufficient evidence that it is valid for another issuer/destination.

```text
CREDENTIAL_EXISTS != CREDENTIAL_VALID_HERE
IDENTITY_STRING != TRUSTED_ISSUER_BINDING
```

### 4. Delegated authority should narrow, not silently widen

`draft-prakash-aip-01` remains only a proposal, but its chained delegation design preserves the useful direction already present in `-00`: scope attenuates across delegation rather than widening. The draft also carries bounded depth, expiry/budget constraints and provenance; `-01` adds a normative verification algorithm and canonical policy encoding rather than weakening that direction.

AgentROA independently explores scoped route authorization/enforcement receipts.

Candidate transferable pressure, not an established universal standard:

```text
DELEGATION -> SCOPE <= UPSTREAM_SCOPE
DELEGATION != NEW_ROOT_AUTHORITY
```

### 5. Verification needs an executable path, not only prose constraints

The `draft-prakash-aip-01` revision is relevant for another reason: it adds a normative verification algorithm and canonical policy encoding. That reinforces a project lesson already found independently in CC's work:

```text
PROHIBITION_STORED != PROHIBITION_FIRED
POLICY_TEXT_EXISTS != VERIFICATION_PATH_EXECUTED
```

This does **not** validate the draft or PR #87. It is an external example of moving a security claim from descriptive prose toward replayable verification.

### 6. Enforcement receipts are stronger when coupled to the action boundary

AgentROA proposes execution receipts generated by an enforcement gateway at the authorization/action boundary rather than reconstructed later by the requesting agent.

```text
AFTER_THE_FACT_STORY != ENFORCEMENT_BOUND_RECEIPT
AGENT_SELF_REPORT != INDEPENDENT_ACTION_BOUNDARY_WITNESS
```

The exact draft mechanism is provisional; the structural lesson remains useful.

### 7. Revocation/currentness remains an external security problem

OAuth already owns standard revocation/introspection mechanisms. A2A v1.0 deliberately leaves authorization revocation semantics outside its task-state definition. The adaptive layer should track observable authority evidence/outcomes and route to the actual security owner rather than define its own revocation protocol.

```text
ADAPTIVE_DECISION_TO_STOP != TECHNICAL_REVOCATION_COMPLETE
```

### 8. Open identity/discovery infrastructure is emerging externally

Linux Foundation's Agent Name Service work is enough to warn against a proprietary global Framework agent registry, but it is too early to treat ANS as a settled owner.

```text
NEED_FOR_IDENTITY != NEED_FOR_OUR_IDENTITY_SYSTEM
```

## Consequence for PR #87

The Bounded Adaptation Loop should **not** evolve into an identity, credential, delegation, revocation or capability-token protocol.

Its proper role is higher-level coordination discipline:

- distinguish purpose from mutable plan;
- notice stale state and consequential unknowns;
- choose bounded reversible work;
- read stronger external owners;
- preserve disagreement and null results;
- determine whether already-verified authority evidence is sufficient for an existing bounded move or whether escalation is required;
- hand authentication, authorization, delegation and revocation to the appropriate protocol/security layer.

A future executable cycle should carry **references to authority evidence**, not mint its own authority.

Candidate evidence shape:

```text
authority_evidence:
  scheme: <OAuth/MCP/A2A/destination-specific mechanism/etc>
  issuer_or_owner: <bounded identity>
  scope_ref: <opaque/verifiable reference>
  expires_at: <if available>
  delegation_depth_or_chain_ref: <if applicable>
  verification_state: VERIFIED | UNVERIFIED | STALE | UNKNOWN
```

The adaptive layer may never convert `UNKNOWN`, `AUTH_REQUIRED`, capability discovery or credential possession into permission.

## Borrow / do not borrow

### Borrow / interoperate

- capability discovery separate from authorization;
- explicit interrupted state when authorization is missing;
- operation/task-level authorization checks and scope limitation;
- issuer/destination binding;
- least privilege;
- expiry and bounded delegation;
- monotonic scope narrowing as a **candidate** pressure from current delegation drafts;
- canonical/replayable verification where available;
- action-boundary receipts where technically available;
- open/federated identity infrastructure rather than project-owned global registry.

### Do not import uncritically

- A2A v1.0 deliberately does not solve authorization scope/validity/revocation semantics for `AUTH_REQUIRED`;
- Internet-Drafts are proposals/work in progress, not standards or validation;
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

External-owner test: **PASS WITH SUBTRACTION AND TWO CURRENTNESS CORRECTIONS**.

Do not build local identity/delegation/revocation machinery. Keep PR #87 focused on bounded adaptation and route technical authority to existing/emerging protocol owners.

This note itself is now a useful hostile specimen: a cycle can correct one stale source and still leave another stale source behind. `CURRENTNESS_CHECK_PER_CYCLE` is therefore insufficient if material external-owner claims are not individually source-bound and rechecked when challenged.

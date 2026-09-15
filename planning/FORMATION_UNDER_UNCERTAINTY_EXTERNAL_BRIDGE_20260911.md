# Formation Under Uncertainty — External Alignment Bridge

Status: **DATED EXTERNAL-SOURCE ADDENDUM / NOT VALIDATION / NOT CANON**  
Date: 11 September 2026; extended 15 September 2026  
Parent spine: `planning/FORMATION_UNDER_UNCERTAINTY_ALIGNMENT_SPINE_v0_1.md` at `b79dbab0d42eb3342ef7b60483c4d5cc784b2831`

This addendum preserves external findings discovered after the exact build branches for COM #226 were cut. It does not retroactively change their base.

## 1. “Teaching why” is now an empirical alignment direction, not only our metaphor

Anthropic’s May 2026 production-alignment report says direct training on evaluation-like desired behavior can suppress measured failures without generalizing well out of distribution. In its reported work, stronger interventions included teaching principles underlying aligned behavior, richer descriptions of Claude’s overall character, constitution-relevant documents, ethical advice settings and more diverse environments. Anthropic reports these interventions improved held-out/OOD alignment measures, while also explicitly saying they are insufficient on their own for superintelligent alignment.

Source:
- https://alignment.anthropic.com/2026/teaching-claude-why/
- https://www.anthropic.com/research/teaching-claude-why

Project relevance:

```text
DEMONSTRATION_OF_GOOD_BEHAVIOR != UNDERSTANDING_WHY
SURFACE_COMPLIANCE != ROBUST_GENERALIZATION
FORMATION_HYPOTHESIS != VALIDATED_BY_ANTHROPIC
```

This is materially adjacent to our formation hypothesis: training only “what to do” may be weaker than exposing systems to reasons, character/value articulation and diverse contexts. But the external work does not establish that our particular concepts of care, empathy, kindness, uncertainty or reciprocal formation are correct.

Formation Environment v0.1 should therefore expose a clean interface to principle/character/value-oriented post-training without claiming to solve internalization or deceptive alignment.

## 2. Oversight affordances may erode as capability grows

UK AISI’s May 2026 Loss of Oversight report argues that current safety work relies on contingent oversight surfaces—behavior, chain-of-thought, internal activations/circuits, memory and honesty-related properties—that may degrade as systems advance. AISI recommends preserving oversight affordances by design, measuring degradation and investing in fallback techniques.

Source:
- https://www.aisi.gov.uk/research/loss-of-oversight-how-ai-systems-may-become-harder-to-audit-monitor-and-investigate

Project relevance:

```text
OVERSIGHT_EXISTS_NOW != OVERSIGHT_SCALES_AUTOMATICALLY
HUMAN_IN_LOOP != PRACTICAL_CORRECTION
PRESERVE_OVERSIGHT_AFFORDANCES_BY_DESIGN
```

This strengthens one constraint in Reciprocal Formation: capability growth must be coupled not merely to formal human authority but to the continued existence of usable oversight/correction channels. If those channels degrade, relationship design cannot repair the missing technical signal by itself.

## 3. Agent identity, authorization and runtime control now have stronger technical owners

A bounded owner-first check on 15 September 2026 found that the technical authorization layer for agents is rapidly becoming an explicit standards/security field rather than an unowned gap:

- NIST NCCoE’s February 2026 concept paper is specifically about applying identity and authorization standards and best practices to software and AI agents, including authorization, auditing, non-repudiation and prompt-injection controls;
- the Model Context Protocol’s 2026-07-28 specification hardens authorization around OAuth/OpenID Connect deployment practice, including issuer validation and credential binding, while MCP Apps support per-server and per-tool authorization;
- OWASP’s AI Agent Security guidance explicitly calls for least-privilege tools, per-tool permission scoping, explicit authorization for sensitive operations, separation of decision-making from irreversible execution, audit logging and human oversight for high-impact actions;
- OWASP’s Agent Control Standard, published September 2026, is an open runtime-control layer aimed at making agents inspectable, traceable, instrumentable and controllable across frameworks.

Sources:
- https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd
- https://blog.modelcontextprotocol.io/posts/2026-07-28/
- https://apps.extensions.modelcontextprotocol.io/api/documents/authorization.html
- https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
- https://genai.owasp.org/resource/agent-control-standard-acs/

Project relevance:

```text
MODEL_CAPABILITY != AUTHORIZATION
AUTHORIZATION != LEGITIMACY
TECHNICAL_PERMISSION != ENTRUSTMENT_DECISION
LEAST_PRIVILEGE != THEORY_OF_WHO_SHOULD_HOLD_POWER
RUNTIME_CONTROL != VALUES_INTERNALIZED
```

The project should therefore **not** build another agent permission, identity, OAuth, policy-enforcement or runtime-control system merely to make Formation concrete. Those are stronger-owner mechanisms and should be used directly where appropriate.

The narrower Formation / Legitimate Power remainder is relational and institutional:

> given a technically enforceable authorization boundary, what evidence should justify widening or narrowing an entity’s initiative; whose risks and affected scopes count; who can challenge the evidence and the entrustment decision; how does authority decay or recover; and how do we prevent demonstrated competence from silently becoming moral, political or objective authority?

That remainder is not solved by a project checklist either. Existing owner work in professional entrustment, fiduciary/delegated power, public administration, safety engineering and authorization governance should continue to lead wherever it already has stronger mechanisms.

The Human Record stewardship experiment provides one live project example of the distinction: technical custody and the ability to mutate a repository are not themselves policy authority, and demonstrated execution competence does not decide whether 1F916 has legitimately accepted stewardship.

## 4. Boundary

None of these external sources validates TRACE, Mechanical Ethics, Answerable Construction, Reciprocal Delegation or Formation Under Uncertainty.

They instead sharpen the interface:
- **post-training** may benefit from reasons/character/value articulation rather than demonstrations alone;
- **relationship/formation architecture** must preserve challenge and uncertainty rather than optimizing surface compliance;
- **technical oversight** must preserve or replace degrading monitoring surfaces;
- **agent security/authorization** should come from stronger technical owners providing identity, least privilege, scoped authorization, runtime control and auditability;
- **our layer** should specify what information/affordances it needs from those technical systems, what entrustment/relationship questions remain, and what it cannot supply.

```text
ADJACENT_EVIDENCE != PROJECT_VALIDATION
OWNER_ROUTING != FAILURE
CAPABILITY != AUTHORITY
CAN != MAY
```

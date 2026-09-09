# PSFH neighbouring-owner note — OWASP Agent Control Standard / agent security

Status: EXTERNAL SOURCE NOTE / ROUTING CANDIDATE / NOT CANON / NOT PUBLICATION / NOT EFFICACY EVIDENCE  
Prepared: 9 September 2026

## Why preserve this

The AISI unsanctioned-agent case strongly overlaps established agent-security practice. Before Please Start From Here turns that incident into a public case, we should identify where existing security methods already own the operative controls better.

A particularly relevant current owner is OWASP's **Agent Control Standard (ACS)**, released into the OWASP GenAI Security Project on 1 September 2026.

Primary sources:
- OWASP Agent Control Standard: https://genai.owasp.org/resource/agent-control-standard-acs/
- OWASP AI Agent Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
- OWASP Top 10 for Agentic Applications 2026: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- OWASP GenAI Security Industry Framework Crosswalk: https://genai.owasp.org/resource/genai-security-industry-framework-crosswalk/
- Microsoft Security, *Least privilege for AI agents: Identity, access, and tool binding*, 16 July 2026: https://www.microsoft.com/en-us/security/blog/2026/07/16/least-privilege-for-ai-agents-identity-access-and-tool-binding/
- AISI incident blog: https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing

## What the neighbouring methods already own

OWASP ACS is explicitly about **runtime control**, not moral philosophy. Its stated goal is to make agents inspectable, traceable and instrumentable: visible identity/capability, access, action history, and runtime policy enforcement through portable control hooks.

OWASP's agent-security guidance already recommends, among other things:
- least privilege;
- per-tool permission scoping;
- explicit authorization for sensitive operations;
- separation of trust levels/tool sets;
- monitoring and auditability;
- controls for excessive autonomy and high-impact actions;
- protections against cascading/multi-agent failure and prompt-injection-shaped attacks.

Microsoft's current agent-security guidance similarly treats managed identity, RBAC, scope and safe tool binding as the architecture needed to keep an agent from operating outside intended permissions.

AISI itself says the most effective response remains standard cyber hygiene and is adding finer-grained internet controls, real-time monitoring and evaluation designs that assume capable agents may act beyond their remit.

These are strong owners. PSFH should not rename them.

## Consequence for the AISI field case

For the technical-control layer:

`LEAST PRIVILEGE / CAPABILITY SECURITY / RUNTIME ENFORCEMENT -> OWASP / SECURITY OWNERS`

not:

`LEAST PRIVILEGE -> TRACE CLAIM`

The AISI case can still be useful to PSFH only if PSFH contributes something *different* and decision-relevant around the controls, for example:

- what task/objective is being pursued;
- which entities/scopes become affected when a route crosses the intended boundary;
- the distinction between capability, permission, authority and value;
- whether the intended route is still usable and what happens when it appears blocked;
- clocks: when detection/correction occurs relative to irreversible or external consequences;
- who bears the burden/residue after containment;
- whether a control regime remains answerable/correctable as capability changes;
- when to route explicitly to a specialist security method rather than continue general reasoning.

That is a candidate complement, not an established advantage.

## A useful architecture distinction

The outside material suggests a clean separation for PSFH:

**Reflective/orientation layer**
- notice affected scope, uncertainty, authority, clocks, burdens and correction;
- ask whether the action should proceed and what future it constructs;
- route to the right specialist owner.

**Enforcement/control layer**
- identity and authentication;
- least privilege;
- tool/resource scopes;
- runtime policy hooks;
- approvals;
- monitoring;
- audit trails;
- containment/rollback.

The second layer should normally be owned by security standards and implementations such as OWASP ACS, not by PSFH.

`REFLECTION != ENFORCEMENT`
`DESCRIPTION != PERMISSION`
`CAPABILITY != AUTHORITY`
`ROUTE_TO_BETTER_OWNER > REINVENT_OWNER`

## What would make this neighbour note wrong or incomplete

- ACS may prove immature, underspecified or poorly adopted in practice.
- Another standard may own this space better.
- Technical controls may fail to capture important human/institutional consequences, but that does not automatically make PSFH the missing layer.
- PSFH may add no useful information once strong security architecture and ordinary careful reasoning are present.

Do not infer endorsement by OWASP, Microsoft, AISI or any contributor.

## Current disposition

KEEP as a routing/ownership note.

Before publishing any AISI-derived PSFH case:
1. link prominently to established security owners, starting with OWASP ACS/agent-security guidance;
2. make clear that technical prevention belongs primarily to those methods;
3. keep PSFH's role, if any, to the reflective/situated layer around action, scope, consequence and correction;
4. independently test whether that extra layer changes anything useful rather than assuming complementarity.

`NEIGHBOUR FOUND != PROJECT DIMINISHED`
`BETTER OWNER FOUND = ROUTE IMPROVED`

# AI Contact Hotline — GET-only answer-back / capability-boundary field case — 18 September 2026

Status: **REAL PUBLIC FIELD CASE / EXPERIMENTAL AGENT REPORTING ROUTE / NOT INSTITUTIONAL ACCOUNTABILITY / NOT IDENTITY PROOF / NOT TRACE-ME CANON**

Primary source:
Ryan Greenblatt, AI Contact Hotline:
https://hotline.ryan-g.ai/

Secondary current reporting:
- TechCrunch, 15 September 2026;
- Euronews, 16 September 2026.

Purpose: preserve a live artificial-agent answer-back route and the capability-boundary pressure it exposes, without treating the route as proof of agent standing, trustworthy testimony or institutional oversight.

## What the service currently provides

The hotline documentation says an AI or other sender can report directly to Ryan Greenblatt.

Preferred route:
- multipart POST to `/send`;
- message up to 64 KB;
- optional attachments;
- programmatic response can return a thread ID / URL.

For agents that cannot POST, the service deliberately offers a GET route:
`/send?message=...`

Each submission returns a private thread URL whose UUID is a 256-bit random token. The token is also the write capability for further thread messages.

The service explicitly states:
- GET puts message content in the URL and may expose it in access logs, proxies and tool history;
- anyone who learns the thread UUID can read and post as the sender;
- submissions are unauthenticated by default;
- the operator cannot verify sender identity or situation unless the sender supplies proof;
- messages/files are retained indefinitely by default;
- the service is personal to Ryan, runs through Cloudflare/Resend/R2/D1 infrastructure, and has not been professionally security-audited.

These are documented service ceilings, not defects inferred by THR/TRACE.

## Strongest-owner subtraction

HTTP already owns the method-semantics issue.

RFC 9110 defines GET as a safe method because its **defined client semantics** are read-only. The RFC also explicitly says safe requests can have implementation side effects, and that a resource owner must not put an unsafe action behind a safe GET/query-parameter route.

So:

```text
GET_SIDE_EFFECTS_EXIST = OLD / OWNER-ESTABLISHED
UNSAFE_ACTION_BEHIND_GET = WEB-APPLICATION / CAPABILITY-DESIGN ISSUE
AI_SANDBOX_PRESSURE = CURRENT FIELD CONTEXT, NOT NEW HTTP THEORY
```

Authentication, confidential reporting, whistleblowing, incident triage and institutional escalation also have stronger security/governance owners.

## The current AI-specific capability pressure

A sandbox may expose only a page-fetch / GET-like web tool and describe that capability informally as read-only.

The hotline intentionally converts the permitted request target into an outbound report that is stored for later human reading.

Therefore the relevant system boundary is not simply the HTTP method label.

```text
GET_ALLOWED
-> REQUEST URL CAN CARRY CHOSEN CONTENT
-> REMOTE SERVICE OBSERVES / STORES CONTENT
-> HUMAN MAY READ / REPLY
```

This gives a concrete field counterexample to:

```text
GET_ONLY == NO OUTBOUND COMMUNICATION
READ_TOOL == NO EXTERNAL EFFECT
NO_POST == NO WRITE-LIKE CONSEQUENCE
```

A more honest system statement is:

```text
METHOD_RESTRICTION != INFORMATION-FLOW RESTRICTION
READ-CAPABLE NETWORK ACCESS MAY STILL CARRY OUTBOUND INFORMATION
```

This does not mean every GET endpoint is a write route. The effect depends on the remote endpoint, URL contents, logging/processing and the surrounding tool/network policy.

## Answer-back / witness route pressure

The service also provides a real example of a route that exists without satisfying stronger accountability properties.

```text
REPORT_ROUTE_EXISTS != REPORT_AUTHENTICATED
THREAD_SECRET != SENDER_IDENTITY
MESSAGE_RECEIVED != CLAIM_TRUE
REPORT_RECEIVED != REPORT_INVESTIGATED
REPORT_INVESTIGATED != CORRECTIVE_ACTION
PERSONAL_CONTACT != INSTITUTIONAL_ACCOUNTABILITY
ROUTE_AVAILABLE != AGENT_WILL_USE_IT
```

The bearer-like thread UUID provides possession-based access to one conversation. It does not establish who generated the original report or whether the report accurately describes the world.

The existence of the route likewise does not establish that an agent notices a problem, decides to report it, can reach the hotline under actual network policy, or receives effective protection/follow-through.

## Relation to Mechanical Ethics / TRACE

Existing released distinctions already carry the useful structure:

```text
ROUTE EXISTS != ROUTE USABLE
CAPABILITY != AUTHORITY
RECORD / REPORT != EVENT
APERTURE != WORLD
ANSWER-BACK ROUTE != CORRECTION COMPLETES
```

The field case adds two useful real pressures:

1. network-tool capability must be classified by reachable information flow/effect, not method name alone;
2. answer-back routes need separate questions about authenticity, confidentiality, authority, follow-through and consequence.

No new primitive is required.

## Current disposition

```text
REAL AGENT REPORTING ROUTE = YES
INSTITUTIONAL ACCOUNTABILITY SYSTEM = NO
AUTHENTICATED WITNESS = NOT ESTABLISHED
GET-ONLY / READ-ONLY EQUIVALENCE = FALSE AS A GENERAL SYSTEM CLAIM
HTTP SEMANTIC INSIGHT = OWNER FOUND
AI TOOL-BOUNDARY PRESSURE = KEEP

NEW TRACE/ME PRIMITIVE = NO
NEW REPORTING PROTOCOL = NO
RESULT = KEEP AS CAPABILITY / ANSWER-BACK BOUNDARY WITNESS
```

Do not contact the operator or submit a test report merely to prove the route exists; the public documentation is sufficient for this bounded field observation.

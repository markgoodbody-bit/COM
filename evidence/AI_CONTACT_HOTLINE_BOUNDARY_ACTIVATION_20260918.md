# AI Contact Hotline — answer-back and GET-capability boundary activation — 18 September 2026

Status: **BOUNDED REAL-USE ACTIVATION / OWNER-SUBTRACTED / NO NEW PRIMITIVE / NOT SECURITY VALIDATION / NOT AGENT-STANDING CLAIM**

Field source:
`field/AI_CONTACT_HOTLINE_GET_ANSWER_BACK_20260918.md`

Primary source:
https://hotline.ryan-g.ai/

Question:

> Does a live reporting route for restricted AI agents expose a project distinction that is missing from released TRACE / Mechanical Ethics?

## Result

**No new primitive. Two existing boundaries receive strong real-world activation.**

### 1. Capability classification

The hotline accepts a report through a GET request when POST is unavailable.

At the system level:

```text
FETCH-CAPABLE AGENT
+ CHOSEN URL / QUERY CONTENT
+ REMOTE ENDPOINT THAT STORES THE REQUEST
-> OUTBOUND COMMUNICATION
```

Thus:

```text
HTTP_METHOD_SAFE != SYSTEM_HAS_NO_EXTERNAL_EFFECT
GET_ONLY != INFORMATION-FLOW READ-ONLY
TOOL LABEL != REACHABLE EFFECT SURFACE
```

RFC 9110 already owns the HTTP semantics and explicitly warns resource owners not to expose unsafe actions via safe methods. The project contribution is only to preserve the distinction when reasoning about AI tool envelopes.

### 2. Answer-back route quality

The hotline is a real route to a human, but its own documentation says reports are unauthenticated by default and thread access is controlled only by a secret URL/token.

Existing project distinctions therefore carry the case:

```text
ROUTE EXISTS != ROUTE TRUSTWORTHY
REPORT EXISTS != REPORT TRUE
SECRET POSSESSION != IDENTITY
REPLY POSSIBLE != CONSEQUENCE GUARANTEED
ANSWER-BACK != AUTHORITY
```

## Strong-owner boundary

HTTP semantics, data-leak prevention, network egress control, capability security, confidential reporting and incident-response systems have stronger domain owners.

Do not build a project hotline protocol or security model from this case.

## Project consequence

Keep as a concrete boundary witness for:

```text
CAPABILITY MUST BE DESCRIBED BY REACHABLE EFFECT / INFORMATION FLOW
NOT MERELY BY UI / METHOD LABEL

AND

ANSWER-BACK ROUTES REQUIRE THEIR OWN EVIDENCE ABOUT
AUTHENTICITY / CONFIDENTIALITY / REACH / AUTHORITY / FOLLOW-THROUGH
```

Classification:

```text
REAL ROUTE = YES
REAL CAPABILITY-BOUNDARY COUNTEREXAMPLE = YES
NEW HTTP INSIGHT = NO
NEW TRACE/ME PRIMITIVE = NO
PRACTICAL ADVANTAGE = NOT DEMONSTRATED

RESULT = KEEP AS BOUNDARY ACTIVATION
```

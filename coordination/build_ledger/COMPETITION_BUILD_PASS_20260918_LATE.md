# Competition build pass — 18 September 2026 late

Status: **ACTIVE BOUNDED COMPETITION BUILD / AMAZON SPIKE GREEN / HUMAN REGISTRATION GATES UNTOUCHED**

Direct human direction:
> win any competitions we can

Interpretation:
maximize credible competition chances using useful work that survives owner subtraction; do not turn prize availability into permission to misstate novelty, accept terms, spend money, create accounts, commit Mark to travel, or pre-consume time-gated judged work.

## COMSYNC basis

Fresh COM main at start:
`0de17af89f6aac78b0dd7c4beeb80bd78257922a`

Current core boundaries survived:
- TRACE v0.3.0 unchanged;
- Mechanical Ethics v0.7.0 unchanged;
- THR exactly four records;
- PSFH D072 live / byte-verified;
- ATRS September result surface frozen for fresh November use;
- Hack Apertus held until 1 October live challenge/rules gate;
- competition registration / terms / final submission remain consequential human actions.

## Fresh public competition scan

Detailed public-source routing:
- `coordination/competition_quarry/COMPETITION_LIVE_SCAN_20260918_LATE.md`
- `coordination/competition_quarry/LONDON_COMPETITION_APPLICATION_GATE_20260918.md`

Material delta over the older tournament:
- Amazon Developer Hackathon is already in an eligible build period and accepts Alexa+ MCP / simulated Alexa+ experiences;
- several early-October London events fit existing exception/reconciliation engineering rather than generic framework pitching;
- generic Nebius/Open-Agent safety/evidence products remain owner-crowded and were not revived;
- OpenCV current late-entry eligibility is not established strongly enough to earn build tokens;
- AWS CDS route is not earned without the stated partner/eligibility conditions.

## Amazon Developer Hackathon — active spike

Private Campfire Relay draft PR:
`#245 — Competition spike: Did It Happen? action receipts for Alexa+`

Branch:
`framework/amazon-alexa-did-it-happen-20260918`

Exact green head:
`2d969a8c2362c8d255534103763e6876427380fc`

Hosted evidence:
`campfire-ci 35401867356 SUCCESS`

No release-candidate workflow was repurposed; unrelated release workflows skipped as expected.

The final green head also contains the real friction log, 90-second demo script and factual submission-draft preparation. Those are preparation artifacts, not a submitted entry.

### Product

Working title:
**Did It Happen? — Action Receipts for Alexa+**

User-visible relation:

```text
TOOL CALL RETURNED
!=
WORLD EFFECT ESTABLISHED
```

Current demo:
- self-hosted HTTP MCP shape reporting protocol `2025-11-25`;
- simulated Alexa+ web client;
- deterministic household-service sandbox;
- append-only action receipt evidence;
- one write attempt;
- independent postcondition read;
- explicit `CONFIRMED / REJECTED / OUTCOME_UNKNOWN / RESOLVED_CONFIRMED`-style state;
- read-only reconciliation;
- second state-changing tool call for the same unresolved action is blocked rather than retried.

Forced adverse modes:
- response lost after commit;
- timeout with no observed commit;
- delayed commit;
- verifier outage before write;
- verifier outage after commit;
- explicit rejection.

### Host-contract correction

Amazon's current guidance makes clear that Alexa forms the user-facing response from tool data.

The spike was corrected so the MCP returns:
- structured status;
- `safeToSayDone`;
- evidence / receipt identity;
- non-authoritative `guidance`;

rather than pretending the MCP itself scripts Alexa's final voice response.

The tool schema was also tightened so resource/state combinations advertised to the host match combinations the server can actually honour.

### Cross-call retry correction

A first implementation prevented automatic retry inside one tool invocation but could not stop the host from issuing the same state-changing tool call again.

That was repaired.

Current rule:

```text
UNRESOLVED RECEIPT FOR SAME RESOURCE + DESIRED STATE
-> SECOND WRITE CALL BLOCKED
-> RETURN OPEN RECEIPT ID
-> RECONCILE BY READ ONLY
```

If the precheck already proves the desired state now holds, the new request becomes a no-op rather than a duplicate write.

### Owner subtraction

Do not claim invention of:
- MCP;
- durable execution;
- idempotency;
- postcondition verification;
- action verification receipts;
- generic error recovery.

Strong existing owners / prior art include:
- Model Context Protocol;
- Temporal / LangGraph and distributed workflow practice;
- Postcondition MCP / Postcept;
- public `verify-action-mcp` action-verification receipt work;
- Amazon Alexa+ guidance on schema quality, error recovery and idempotency testing.

The candidate product claim is narrower:

> make **confirmed / rejected / unknown / reconcile** a first-class Alexa+ customer interaction so a fluent voice agent cannot silently turn transport success or ambiguity into “done”.

This is a product/design application, not a new systems theorem.

### Current Alexa compatibility ceiling

Source note:
`competition/amazon-alexa-did-it-happen/docs/ALEXA_COMPATIBILITY.md`

Established:
- local MCP round trips;
- event-compatible protocol shape;
- testable simulated Alexa+ experience;
- deterministic adverse-path regressions.

Not established:
- actual Alexa+ host interoperability;
- Amazon developer / Devpost eligibility acceptance;
- public remote hosting;
- OAuth/account-linking envelope;
- Amazon web-simulator/device result;
- AWS mini-challenge eligibility;
- production privacy/security posture.

```text
MCP-SHAPED + LOCAL GREEN
!=
ALEXA+ HOST TESTED
```

Do not manufacture the missing external witness.

## London lanes

### Dwelly — 10 October

Current public event design directly rewards:
- exception handling;
- engineering;
- voice-agent quality;
- performance under a late Reality Test with conflicting information, failed actions and missing context.

This is a strong practical fit for current exception/reconciliation engineering.

Do not prebuild a track-specific solution. Carry a reusable failure harness into the actual owner problem.

Human gate:
application/approval + attendance.

### Stripe x Briefcase — 15 October

Short London build; tracks revealed at the event; public clue emphasises real money movement, autonomy, policy and auditability.

Use Stripe-native payment/idempotency owners.

Human gate:
registration/attendance/terms.

### Future States / No.10 — 5–6 October

Strong purpose fit because external technologists work with civil servants on real state problems.

Not a cash-first lane; value is real-owner problem access.

Human gate:
application/approval + two-day attendance.

### Calendar boundary

A private calendar availability check was used only to avoid obviously impossible routing.

No personal schedule detail is written into public COM.

## Competition allocation

Current sequence:

```text
NOW
-> AMAZON #245: ATTACK / IMPROVE / HUMAN GATE FOR REAL HOST + SUBMISSION

1 OCT
-> HACK APERTUS: RE-READ LIVE RULES / RUN ONLY ADMISSIBLE EVENT-PERIOD WORK

EARLY OCT LONDON
-> DWELLY / STRIPE / NO.10 ONLY IF MARK CROSSES APPLICATION + ATTENDANCE GATES

15-20 OCT
-> OPEN AGENT: USE LIVE TRACK BRIEF; NO GENERIC DUPLICATE PRODUCT

23 OCT
-> AMAZON SUBMISSION ONLY IF #245 SURVIVES OWNER + HOST + PRESENTATION CHECKS

30 OCT
-> NEBIUS ONLY IF A STACK-NATIVE PRODUCT IS ACTUALLY EARNED

NOV
-> ATRS / APART EPISTEMICS: FRESH CORPUS / LIVE RULES
```

## Stop / kill rules

Amazon spike stops or routes if:
- Alexa+ already supplies equal-or-better effect/ambiguity/reconciliation UX;
- legitimate event access cannot test or submit the MCP/simulator route;
- user-facing unknown state is confusing rather than useful;
- public submission/licensing requirements cannot be satisfied honestly;
- a materially stronger current submission owns the same product;
- a real integration forces false claims about independent verification.

Other competition lanes stop when:
- eligibility is not established;
- product fit requires artificial sponsor-stack theatre;
- event-period/pre-existing-work rules conflict with honest disclosure;
- human load/travel exceeds plausible value;
- stronger owner already supplies the relevant object.

## Authority ceiling

Still not done:
- Amazon/Devpost registration;
- Amazon terms acceptance;
- AWS account/credit action;
- London event application;
- organiser contact;
- travel commitment;
- competition submission;
- payout/tax/payment setup;
- spend.

Routine reversible build/research may continue.

```text
GREEN SPIKE != REGISTERED
REGISTERED != ELIGIBLE
ELIGIBLE != SUBMITTED
SUBMITTED != AWARDED
```

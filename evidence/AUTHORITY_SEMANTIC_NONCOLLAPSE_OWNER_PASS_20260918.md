# Authority-state semantic non-collapse — owner pass — 18 September 2026

Status: **REAL ENGINEERING PROPERTY / OWNER MECHANISMS FOUND / NO OBSERVED COMPILER FAILURE / NO FUNDING THESIS EARNED**

## Candidate seam tested

Earlier resource work retained one narrow question:

> Across human requirements -> machine policy -> negotiation/composition -> executable decision, can states such as UNKNOWN, REFUSED, WITHHELD, OUTSIDE_AUTHORITY and CONFLICT_UNRESOLVED avoid being silently coerced into one another or into a definite Permit/Deny without an authorised transition?

The strongest adversarial shape is not the immediate decision alone. Several states can legitimately yield the same current `Deny` while implying different next behaviour: seek missing information, respect an explicit refusal, preserve deliberate withholding, reject an unauthorised principal, or escalate unresolved conflict.

That relation is real. The owner pass materially reduces the claim that it is a missing project mechanism.

## Strong owners / mechanisms

### W3C Data Privacy Vocabulary / ISO 27560 guidance

Current DPV consent vocabulary already distinguishes operational states including:
- ConsentUnknown;
- ConsentRequested;
- ConsentRequestDeferred;
- ConsentRefused;
- ConsentWithdrawn;
- ConsentRevoked;
- ConsentExpired / Invalidated;
- valid given/renewed states.

DPV also carries who indicated a consent action and when. ISO/IEC TS 27560 guidance using DPV requires consent state in the record.

Owner:
https://www.w3.org/community/reports/dpvcg/CG-FINAL-dpv-20240801/
https://www.w3.org/community/reports/dpvcg/CG-FINAL-guide-27560-20240801/

Therefore:
`UNKNOWN != REFUSED != DEFERRED` as a status vocabulary is not our gap.

### XACML

XACML 3.0 already separates Permit / Deny / Indeterminate / NotApplicable. Its response model can carry StatusCode, StatusMessage and StatusDetail. Missing-attribute Indeterminate can identify information needed to refine a later request. The JSON profile also exposes optional Obligations and AssociatedAdvice.

Owners:
https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-csd06-en.html
https://docs.oasis-open.org/xacml/xacml-json-http/v1.0/xacml-json-http-v1.0.html

Thus a policy decision need not erase the reason or next-action metadata merely because the final authorization surface later becomes Permit/Deny.

### Cedar

Cedar's authorizer returns Allow/Deny plus diagnostics, including determining policies and evaluation errors. Missing optional data can be tested explicitly; attempts to use absent attributes can produce diagnostics. Cedar also makes the surrounding application responsible for gathering and supplying relevant context.

Owner:
https://docs.cedarpolicy.com/auth/authorization.html
https://docs.cedarpolicy.com/schema/schema.html

Again:
`BINARY FINAL DECISION != REASON MUST BE LOST`.

### ODRL / policy composition

ODRL already has explicit permissions, prohibitions, duties and conflict strategies including an `invalid` strategy where conflicting rules void the policy rather than silently selecting a winner.

Owner:
https://www.w3.org/TR/odrl-model/

## What is not established

This pass does **not** prove that current natural-language requirement compilers, LLM agents or multi-agent negotiation stacks preserve these distinctions correctly end to end.

A genuine research result would require a concrete pipeline where:
1. richer source state is present;
2. a transformation is supposed to preserve it or its operational consequence;
3. the implementation collapses it;
4. the collapse produces a materially wrong authorization/correction behaviour;
5. existing status/diagnostic/obligation mechanisms cannot repair the failure without a new contribution.

No such real pipeline failure has been observed in this project yet.

## Disposition

`RICH STATUS VOCABULARY = OWNER FOUND`
`AUTHORIZATION REASON / DIAGNOSTIC CHANNEL = OWNER FOUND`
`OBLIGATION / ADVICE / REFINEMENT MECHANISMS = OWNER FOUND`
`SEMANTIC PRESERVATION AS GENERAL REQUIREMENT = NOT PROJECT-SPECIFIC`
`OBSERVED END-TO-END COMPILER FAILURE = NO`
`ARIA PROPOSAL THESIS = NOT EARNED`
`CRF PROPOSAL THESIS = NOT EARNED`

Possible future wake condition:

> a real requirement-to-policy or multi-agent workflow collapses a refusal/unknown/authority/conflict distinction and that collapse changes what legitimate correction should do.

Until then: **OWNER FOUND / NO APPLICATION OBJECT / STOP BUILDING THE SEAM BY MOMENTUM.**

`THEMATIC_FIT != RESEARCH_GAP`
`DENY_EQUIVALENCE != WORKFLOW_EQUIVALENCE`
`NO_OBSERVED_FAILURE -> NO NEW MECHANISM`
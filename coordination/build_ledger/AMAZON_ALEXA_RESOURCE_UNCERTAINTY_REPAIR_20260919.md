# Amazon Alexa+ resource-uncertainty repair — 19 September 2026

Status: **BOUNDED HOSTILE-REVIEW REPAIR / GREEN SOURCE CANDIDATE / NOT REGISTERED / NOT SUBMITTED**

> HOW CAN WE MAKE A BETTER FUTURE?

This receipt records a fresh Framework aperture continuing the already-green Amazon Alexa+ competition candidate after the 19 September FULL COMSYNC.

It does **not** reopen competition fanout or create a new product lane.

## Starting point

Campfire Relay draft PR #245:

`Did It Happen? — Action Receipts for Alexa+`

Starting exact head:
`ce9f3d4029f4aed8de6f39e166eafc14ac69da2e`

Starting hosted evidence:
`campfire-ci 1520 / 35405626849 SUCCESS`

The candidate was frozen unless a concrete adverse-path defect survived.

## Fresh hostile findings

### 1. MCP output-schema mismatch

`change_household_service` legally permits action states including:
- `active`;
- `paused`;
- `cancelled`;
- `scheduled`.

But `list_open_action_receipts` advertised only:
`paused | cancelled`.

Therefore a legal unresolved `active` or `scheduled` intent could produce structured content outside the tool's own advertised output schema.

This is a contract defect, not presentation polish.

### 2. Resource-level unresolved-write gap

The unresolved guard matched:

`resource + desiredState + unresolved status`

That blocked an exact repeated change but allowed a different desired state against the same resource while the earlier write outcome remained unresolved.

Example:
```text
meal_kit -> pause
write outcome = UNKNOWN
before reconciliation:
meal_kit -> cancel
```

Without owner evidence about ordering/linearizability, the system cannot prove the first ambiguous side effect will not commit after or interfere with the second.

For this candidate, the safer boundary is:

```text
UNRESOLVED ACTION ON RESOURCE
-> NO FURTHER WRITE TO THAT RESOURCE
-> READ-ONLY RECONCILIATION FIRST
```

This does not claim a universal rule for all external systems. It is the conservative contract for this demo's evidence ceiling.

## Repair

Campfire Relay PR #245 now:
- blocks any new state-changing action on a resource while any prior action receipt for that resource is unresolved;
- leaves other resources available;
- routes the blocked caller to the existing unresolved receipt;
- performs no automatic retry;
- keeps recovery read-only;
- advertises all legal action states in the open-receipt MCP output schema;
- adds focused regressions for cross-state resource blocking and schema coverage;
- aligns the existing guidance-string regression with the repaired wording.

## Exact evidence

Final exact head:
`d727ccca61ccad9c54750285e59dc7674d0981af`

Hosted:
`campfire-ci 1524 / 35436153754 SUCCESS`

Standalone focused suite:
`23 tests`

PR #245 remains draft/open.

## Claim ceiling

```text
GREEN CI != REAL ALEXA+ HOST VALIDATION
RESOURCE SERIALIZATION != EXACTLY-ONCE EXTERNAL EXECUTION
POSTCONDITION READ != INDEPENDENT INFRASTRUCTURE WITNESS
SIMULATED WORLD != PRODUCTION SERVICE SEMANTICS
PREPARED != SUBMITTED
SUBMITTED != AWARDED
```

No claim is made that every external API should serialize all unresolved operations this way.

## Human gates unchanged

No:
- Amazon/Devpost registration;
- terms acceptance;
- developer-account or AWS-credit action;
- public deployment;
- OAuth/account linking;
- demo-video upload;
- final submission;
- new spend.

Amazon remains:

```text
GREEN SOURCE CANDIDATE
+ PREPARED JUDGE PACKAGE
+ HUMAN ONBOARDING / SUBMISSION GATE
```

Hack-Nation remains a separate same-day human application gate. ARC remains STOP after owner subtraction. Hack Apertus and ATRS remain time-gated.

`CONCRETE DEFECT -> SMALLEST REPAIR -> GREEN -> FREEZE AGAIN`

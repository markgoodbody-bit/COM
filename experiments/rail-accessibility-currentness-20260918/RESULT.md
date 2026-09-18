# Rail accessibility currentness v0 - result

Status: **LIVE PUBLIC EXISTENCE CONTRADICTIONS REPRODUCED / HOSTILE-REVIEW SHRUNK / OWNER-ROUTABLE / ROOT CAUSE UNKNOWN / NOT ACCESSIBILITY CERTIFICATION**

Date: 18 September 2026

## Owner context

ORR's 2025-26 annual assessment already reports that a significant number of completed Access for All stations still state that they have no lifts on National Rail station pages/maps.

National Rail describes Knowledgebase as the central repository for station facilities/accessibility information and says station operators keep that data up to date.

ORR requires station accessibility information to be kept up to date for passengers.

Therefore the project does not claim discovery of the general problem.

## Original bounded audit

The first live proof on PR #383 reproduced three lift-existence contradictions and three controls.

Original exact tested head:
`129f4563dde0d24617275815879fd236ece518b9`

Workflow:
`35380766892 SUCCESS`

Existence result:
- HIR — `CONTRADICTION`
- IRL — `CONTRADICTION`
- DSY — `CONTRADICTION`
- BIW — `CONSISTENT_EXISTS`
- AGV — `CONSISTENT_EXISTS`
- LLE — `CONSISTENT_EXISTS`

## Hostile-review shrink

A fresh adversarial read preserved the existence result but rejected the draft's station-level operational classifier.

Concrete failure mode:
- a current owner surface can contain an outage statement while another current surface, or even another part of the same surface, reports an in-service lift;
- stations can have multiple lifts with different states;
- collapsing those observations into one `IN_SERVICE` or `OUT_OF_SERVICE` station label overclaims the evidence.

The operational classifier was therefore removed rather than complicated.

The same pass added two further protections:
1. locally negated phrases such as `no lift access available` and `no lifts have been installed` cannot create positive lift-existence evidence;
2. a failed corroborating fetch cannot silently become a negative result.

This is a **SHRINK / KEEP OWNER-ROUTABLE** result, not a new framework feature.

## Current contradiction set

### HIR - Horton-in-Ribblesdale

National Rail passenger summary:
`There are no lifts`

National Rail Accessibility Map surface:
`Lifts have been installed with access to an overbridge, there is now step-free access to both platforms.`

Conclusion:
`CONTRADICTION`

### IRL - Irlam

National Rail passenger summary:
`There are no lifts`

The same passenger page carries a lift-out-of-order alert.

National Rail Accessibility Map surface says lifts were installed in Spring 2025 and exposes individual lift records.

Conclusion:
`CONTRADICTION`

No station-level operational conclusion is drawn from those changing status surfaces.

### DSY - Daisy Hill

National Rail passenger summary:
`There are no lifts`

Northern current station page:
`Island platform with lift access available` and `lifts have now been installed`.

Conclusion:
`CONTRADICTION`

## Controls

- BIW - `CONSISTENT_EXISTS`
- AGV - `CONSISTENT_EXISTS`
- LLE - `CONSISTENT_EXISTS`

The controls demonstrate only that the existence detector does not label every lift station contradictory.

## What can and cannot be inferred

Observed:
- three current public lift-existence contradictions;
- all three contradiction stations are managed by Northern;
- for HIR and IRL, a National Rail Accessibility Map surface already contains positive lift-existence information while the high-level station summary says there are no lifts;
- the bounded controls return the expected existence state.

Not established:
- which organisation or software component caused the stale summary;
- whether the formal Knowledgebase feed has the same defect;
- whether any particular lift is working at this moment;
- whether a passenger can currently make a fully step-free journey at any station;
- network-wide prevalence beyond the six-station bounded set;
- whether the defect will persist after owner correction.

## Current disposition

```text
REAL PUBLIC INFORMATION DEFECT = YES
GENERAL PROBLEM OWNER = ORR / NATIONAL RAIL / OPERATORS
BOUNDED EXISTENCE CHECKER = USEFUL ENOUGH TO KEEP
OPERATIONAL CLASSIFIER = DELETED / STRONGER OWNER
NEW THEORY = NO
ROOT CAUSE = UNKNOWN
NETWORK-WIDE CLAIM = NO
EXTERNAL CONTACT = NOT AUTHORISED
```

Best next external action, if separately human-authorised: route the three exact contradictions and reproduction method to National Rail / relevant station-information owner as a correction packet, not as a project claim.

```text
LIFT EXISTS != LIFT WORKING NOW
LIFT WORKING NOW != STEP-FREE ROUTE USABLE
PUBLIC METADATA CONTRADICTION != OPERATOR BLAME
OWNER FOUND -> SHRINK
```

A final exact-head CI/live-run receipt is required before merge.

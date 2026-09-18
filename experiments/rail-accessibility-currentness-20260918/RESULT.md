# Rail accessibility currentness v0 - result

Status: **LIVE PUBLIC CONTRADICTIONS REPRODUCED / OWNER-ROUTABLE / ROOT CAUSE UNKNOWN / NOT ACCESSIBILITY CERTIFICATION**

Date: 18 September 2026

## Owner context

ORR's 2025-26 annual assessment already reports that a significant number of completed Access for All stations still state that they have no lifts on National Rail station pages/maps.

National Rail describes Knowledgebase as the central repository for station facilities/accessibility information and says station operators keep that data up to date.

ORR requires station accessibility information to be kept up to date for passengers.

Therefore the project does not claim discovery of the general problem.

## Bounded audit

PR #383 exact tested head before this result note:
`129f4563dde0d24617275815879fd236ece518b9`

Workflow:
`35380766892 SUCCESS`

The workflow ran:
- six frozen cases with six distinction/regression tests;
- the frozen six-station audit;
- a fresh public-HTTP recheck from a clean GitHub runner.

## Live reproduced contradictions

### HIR - Horton-in-Ribblesdale

National Rail passenger summary:
`There are no lifts`

National Rail backend:
`Lifts have been installed with access to an overbridge, there is now step-free access to both platforms.`

Live checker:
`CONTRADICTION / operational UNKNOWN`

Important: the backend currently has no individual lift-status data. That does not erase the backend's explicit existence statement and does not establish current route usability.

### IRL - Irlam

National Rail passenger summary:
`There are no lifts`

The same passenger page carries a current lift-out-of-order alert.

National Rail backend:
`This station now has step free access to all platforms as a result of lifts that were installed Spring 2025.`

The backend also exposes individual lift records.

Live checker:
`CONTRADICTION / operational OUT_OF_SERVICE`

This is the clearest reason existence and operational state must remain separate: a lift can exist and be out of service.

### DSY - Daisy Hill

National Rail passenger summary:
`There are no lifts`

Northern current station page:
`Island platform with lift access available` and `lifts have now been installed`.

Northern published the lift opening in April 2025.

Live checker:
`CONTRADICTION / operational UNKNOWN`

## Controls

### BIW - Biggleswade
`CONSISTENT_EXISTS / IN_SERVICE`

### AGV - Abergavenny
`CONSISTENT_EXISTS / IN_SERVICE`

### LLE - Llanelli
`CONSISTENT_EXISTS`

Llanelli currently has a lift-out-of-order alert. The checker correctly keeps that separate from lift existence.

## What can and cannot be inferred

Observed:
- three current public summary/existence contradictions;
- all three contradiction stations are managed by Northern;
- for HIR and IRL, National Rail's own backend is already more current than the high-level passenger summary;
- controls demonstrate that the detector does not label all lift stations contradictory.

Not established:
- which organisation or software component caused the stale summary;
- whether the formal Knowledgebase feed has the same defect;
- whether a passenger can currently make a fully step-free journey at any station;
- network-wide prevalence beyond the six-station bounded set;
- whether the defect will persist after owner correction.

## Current disposition

`REAL PUBLIC INFORMATION DEFECT = YES`
`GENERAL PROBLEM OWNER = ORR / NATIONAL RAIL`
`BOUNDED CHECKER = USEFUL ENOUGH TO KEEP`
`NEW THEORY = NO`
`ROOT CAUSE = UNKNOWN`
`NETWORK-WIDE CLAIM = NO`
`EXTERNAL CONTACT = NOT YET AUTHORISED`

Best next external action, if human-authorised: route the three exact contradictions and reproduction method to National Rail / relevant station-information owner as a correction packet, not as a project claim.

`LIFT EXISTS != LIFT WORKING NOW`
`LIFT WORKING NOW != STEP-FREE ROUTE USABLE`
`PUBLIC METADATA CONTRADICTION != OPERATOR BLAME`

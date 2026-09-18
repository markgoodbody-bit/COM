# Rail accessibility currentness checker - bounded v0

Status: **REAL PUBLIC-DATA DEFECT / OWNER-RECOGNISED / BOUNDED AUDIT / NO ACCOUNT / NO CONTACT / NOT ACCESSIBILITY CERTIFICATION**

## Why this exists

The Office of Rail and Road's 2025-26 assessment says a significant number of completed Access for All stations still state that they have no lifts on National Rail station pages/maps.

National Rail says its Knowledgebase is the central store of station-facility/accessibility information, maintained by the train operators responsible for stations. ORR separately requires station accessibility information to be kept up to date for passengers.

This experiment does not invent that problem. It tests whether a small public-surface consistency check can make concrete current mismatches easy to reproduce.

## Narrow question

Does the public National Rail station summary say 'There are no lifts' while another current owner-controlled public surface says lifts are installed or exposes those lifts?

Keep separate:
- LIFT EXISTS
- LIFT WORKING NOW
- STEP-FREE ROUTE CURRENTLY USABLE

A lift can exist and be temporarily out of service. This experiment flags existence/currentness contradictions; it does not tell a passenger that a route is usable now.

## Frozen six-station set - 18 September 2026

Known contradiction cases:
- Horton-in-Ribblesdale (HIR)
- Irlam (IRL)
- Daisy Hill (DSY)

Controls where the National Rail public summary already says lifts exist:
- Biggleswade (BIW)
- Abergavenny (AGV)
- Llanelli (LLE)

The controls matter. A checker that labels every lift station broken is not useful.

## Run

Frozen audit:
  python -m unittest -v
  python check.py --frozen

Optional public-page recheck:
  python check.py --live

Live mode uses ordinary public HTTP pages only. It does not use the Rail Data Marketplace / Knowledgebase feed because access to that feed requires registration and terms acceptance.

## Output states

CONTRADICTION
CONSISTENT_EXISTS
NO_EXISTENCE_COMPARISON
FETCH_UNKNOWN

Operational status is reported separately: IN_SERVICE / OUT_OF_SERVICE / UNKNOWN / NOT_CHECKED.

## Kill / shrink rules

Stop or shrink if:
1. owner surfaces correct the summaries and the mismatches disappear;
2. an existing public owner validator already does this at equal/better resolution;
3. public HTML is too unstable to check without the formal data feed;
4. the result cannot distinguish existence from temporary operational state;
5. the checker creates more passenger confusion than it removes.

## Authority boundary

No National Rail / ORR / operator contact has been made.
No Rail Data Marketplace account has been created.
No terms have been accepted.
No passenger-facing service is being published.

External reporting to the owner is a later human/contact gate.

ORR FOUND THE PROBLEM
THIS EXPERIMENT TESTS A SMALL REPRODUCIBLE CHECK
CONTRADICTION != STATION INACCESSIBLE
NO CONTRADICTION != ACCESSIBILITY GUARANTEED

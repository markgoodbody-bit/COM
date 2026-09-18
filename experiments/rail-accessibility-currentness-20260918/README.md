# Rail accessibility currentness checker - bounded v0

Status: **REAL PUBLIC-DATA DEFECT / OWNER-RECOGNISED / BOUNDED EXISTENCE AUDIT / NO ACCOUNT / NO CONTACT / NOT ACCESSIBILITY CERTIFICATION**

## Why this exists

The Office of Rail and Road's 2025-26 assessment says a significant number of completed Access for All stations still state that they have no lifts on National Rail station pages/maps.

National Rail says its Knowledgebase is the central store of station-facility/accessibility information, maintained by the train operators responsible for stations. ORR separately requires station accessibility information to be kept current for passengers.

This experiment does not invent that problem. It tests whether a small public-surface consistency check can make concrete current lift-**existence** mismatches easy to reproduce.

## Narrow question

Does the public National Rail station summary say `There are no lifts` while another current owner-controlled public surface says lifts are installed, exposes individual lifts, or carries a lift-outage statement that necessarily implies a lift exists?

Keep separate:

- `LIFT EXISTS`
- `LIFT WORKING NOW`
- `STEP-FREE ROUTE CURRENTLY USABLE`

The checker deliberately answers only the first question.

### Hostile-review shrink

An earlier draft also emitted a station-level operational status. That layer was removed after adversarial re-reading.

Why:
- stations can have several lifts with different states;
- two current owner surfaces can temporarily disagree about operation;
- a single `IN_SERVICE` or `OUT_OF_SERVICE` label can therefore overstate what was actually observed;
- live lift-operation information already has stronger owners, including National Rail's Accessibility Map / lift data.

An outage statement may still count as evidence that a lift exists. It is **not** converted into advice that a passenger can or cannot make a journey.

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

`python -m unittest -v`

`python check.py --frozen`

Optional public-page recheck:

`python check.py --live`

Live mode uses ordinary public HTTP pages only. It does not use the Rail Data Marketplace / Knowledgebase feed because access to that feed requires registration and terms acceptance.

## Output states

- `CONTRADICTION`
- `CONSISTENT_EXISTS`
- `NO_EXISTENCE_COMPARISON`
- `FETCH_UNKNOWN`

`FETCH_UNKNOWN` is used rather than a negative result when a required corroborating public fetch fails and no remaining surface supplies the positive side of the comparison.

## Parser ceiling

The parser looks only for a small number of explicit lift-existence phrases. Positive phrases are rejected when locally negated, so text such as `no lift access available` or `no lifts have been installed` is not promoted into lift-existence evidence.

This is intentionally narrow. It is not natural-language understanding and does not attempt to infer existence from generic step-free wording.

## Kill / shrink rules

Stop or shrink if:
1. owner surfaces correct the summaries and the mismatches disappear;
2. an existing public owner validator already does this exact existence-consistency check at equal/better resolution;
3. public HTML is too unstable to check without the formal data feed;
4. the result starts drifting into operational-status or journey-usability advice;
5. the checker creates more passenger confusion than it removes.

## Authority boundary

No National Rail / ORR / operator contact has been made.
No Rail Data Marketplace account has been created.
No terms have been accepted.
No passenger-facing service is being published.

External reporting to the owner is a later human/contact gate.

```text
ORR FOUND THE GENERAL PROBLEM
THIS EXPERIMENT TESTS A SMALL REPRODUCIBLE EXISTENCE CHECK
CONTRADICTION != STATION INACCESSIBLE
NO CONTRADICTION != ACCESSIBILITY GUARANTEED
LIVE LIFT OPERATION = STRONGER OWNER / OUT OF SCOPE
```

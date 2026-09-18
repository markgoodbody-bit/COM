# Rail accessibility currentness — bounded result — 18 September 2026

Status: **MERGED / SHRUNK / OWNER-ROUTABLE / NO EXTERNAL CONTACT / NOT ACCESSIBILITY CERTIFICATION**

> HOW CAN WE MAKE A BETTER FUTURE?

## Result

PR #383 merged after a fresh-aperture hostile reread.

```text
PR #383 final branch head = f8a95125fee58cf7bfa6458ea30618e424186542
merge-ref workflow = 35382364633 SUCCESS
merged main commit = 4630b07d6c9f9844cba862ef297cddafd9c11698
hostile return = SHRINK -> KEEP_OWNER_ROUTABLE
external contact = NONE
```

Fresh exact merge-ref workflow:
- syntax PASS;
- 7/7 regression tests PASS;
- frozen six-station audit PASS;
- live public-page observation PASS.

Live existence result at the workflow:
- HIR = CONTRADICTION;
- IRL = CONTRADICTION;
- DSY = CONTRADICTION;
- BIW = CONSISTENT_EXISTS;
- AGV = CONSISTENT_EXISTS;
- LLE = CONSISTENT_EXISTS.

## Hostile-review correction

The previous draft's station-level operational classifier did **not** survive.

Reason:
- stations may have multiple lifts with different states;
- current owner surfaces can carry mixed or conflicting operational signals;
- National Rail already owns live operational information through the Accessibility Map / lift-data route;
- a single station label such as `IN_SERVICE` or `OUT_OF_SERVICE` could overstate the evidence.

The operational layer was deleted rather than expanded.

Two further seams were repaired:
1. locally negated positive-looking phrases cannot manufacture lift-existence evidence;
2. failed corroborating public fetches fail to `FETCH_UNKNOWN` rather than silently supporting a negative conclusion.

```text
OWNER FOUND -> SHRINK
LIFT_EXISTS != LIFT_WORKING_NOW
LIFT_WORKING_NOW != STEP_FREE_ROUTE_USABLE
PUBLIC_METADATA_CONTRADICTION != OPERATOR_BLAME
```

## Owner boundary

ORR already owns the general regulatory problem. National Rail / station operators own the passenger information surfaces. The experiment is only a small reproducible existence/currentness check plus an unsent correction packet.

No:
- Rail Data Marketplace registration;
- terms acceptance;
- private feed access;
- passenger-facing service;
- network-wide prevalence claim;
- root-cause attribution;
- National Rail / Northern / ORR contact.

The owner packet remains prepared but unsent. External routing remains a consequential human/contact gate.

## Project reading

This is a useful field witness for the core project, not a new primitive:

```text
PHYSICAL WORLD CORRECTED
-> SOME OWNER DATA CORRECTED
-> PASSENGER DECISION SURFACE STALE
-> CORRECTION DID NOT FULLY PROPAGATE
```

It activates existing distinctions around currentness, route usability, record/world separation and correction propagation. It earns no new TRACE primitive or Mechanical Ethics doctrine.

Next:
`RETURN TO WORLD / REAL USE`.

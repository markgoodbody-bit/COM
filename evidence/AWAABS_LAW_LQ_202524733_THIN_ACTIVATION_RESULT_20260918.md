# Awaab's Law / L&Q 202524733 — thin ME/TRACE activation result — 18 September 2026

Status: **BOUNDED SELF-TEST / SINGLE FRAMEWORK APERTURE / NO DOMAIN DELTA FOUND / NOT VALIDATION / NOT EFFICACY**

Field source:
`field/AWAABS_LAW_LQ_202524733_CORRECTION_WINDOW_20260918.md`

Primary domain owner:
Housing Ombudsman, case 202524733:
https://www.housing-ombudsman.org.uk/decisions/london-quadrant-housing-trust-202524733/

Regulatory owner:
Awaab's Law guidance:
https://www.gov.uk/government/publications/awaabs-law-guidance-for-social-landlords/awaabs-law-guidance-for-social-landlords-timeframes-for-repairs-in-the-social-rented-sector

Released project sources used:
- Mechanical Ethics v0.7.0 current released baseline;
- TRACE v0.3.0 current released baseline.

Question:

> Does a thin ME/TRACE reading expose a material relationship in this case that the Housing Ombudsman's domain account does not already keep visible?

Falsifier:

```text
IF DOMAIN OWNER ALREADY PRESERVES THE CONSEQUENTIAL RELATIONS
THEN RESULT = NO DOMAIN DELTA / COMPRESSION ONLY
```

## 1. Domain-owner account without project vocabulary

The Housing Ombudsman's determination already preserves all of the following.

### Affected people / vulnerability

- resident health vulnerabilities were known;
- reports that mould affected the resident's son's breathing;
- reported chest infections;
- resident-reported loss of use of a bedroom;
- distress/inconvenience and damaged belongings were considered.

### Material state / causal repair problem

- mould, electrics, windows/doors and building defects were separated;
- gutter/fascia/soffit and brickwork were identified as relevant to recurrence;
- an inspection, mould wash and underlying works were distinguished;
- outstanding windows/doors remained separately visible.

### Evidence and uncertainty

- the Ombudsman distinguishes what records showed from what the resident reported;
- it explicitly notes where evidence was absent;
- it does not accept the resident's report of bedroom/property uninhabitability as established fact;
- access refusals are recorded rather than erased;
- landlord failure to use its own non-access escalation process is separately recorded.

### Routes / authority

- tenancy repair duties;
- repairs policy;
- damp and mould policy;
- property-access policy;
- complaint stages;
- rehousing/transfer route;
- Awaab's Law;
- Ombudsman investigation/orders.

### Clocks

The determination quantifies multiple clocks directly, including:

- 146 working days before contacting a contractor after the complaint;
- 227 / 295 working days to mould wash / inspection from complaint;
- 25 November 2025 post-commencement damp/mould inspection;
- 82 working days from that inspection to completion of guttering/brickwork on 24 March 2026;
- 18 months from complaint to stated damp/mould resolution.

### Required decision point

The Ombudsman explicitly identifies the missing post-Awaab assessments:

- potential emergency/significant hazard;
- household health/vulnerability;
- whether temporary accommodation was needed.

### Burden / consequence

- distress and inconvenience;
- vulnerability increasing likely impact;
- reported health effects;
- reported damage to personal property;
- reported loss of bedroom use.

### Correction / residue

- repairs eventually completed for damp/mould;
- compensation/apology ordered;
- windows/doors remained outstanding;
- further inspection/update duties remained;
- earlier delay and distress were not treated as erased by later repair.

### Procedural/function split

The Ombudsman itself makes the key split:

```text
PROPERTY CONDITION -> MALADMINISTRATION
REHOUSING -> SERVICE FAILURE
COMPLAINT HANDLING -> REASONABLE REDRESS
```

So an ordinary reader does not need ME/TRACE to discover that a complaint route can function better than the underlying repair route.

## 2. Thin released ME/TRACE reading

Using only already-released project distinctions, the case can be compressed as:

```text
AFFECTED SCOPE
resident + household / son + vulnerabilities

STATE / CHANGE
damp + mould + defects + unresolved windows/doors

ROUTES
repair + damp/mould + access + complaint + rehousing + Awaab + Ombudsman

DECISION POINT
hazard severity?
vulnerability effect?
temporary accommodation?

CLOCK
inspection -> underlying corrective work = 82 working days recorded

BURDEN
health concern + distress + lost room use reported + repeated pursuit

CORRECTION
eventual work + compensation/orders

RESIDUE
experienced delay not reversible; windows/doors still open at determination
```

Relevant released distinctions include:

```text
ROUTE_EXISTS != ROUTE_USABLE
SERIOUS_CORRECTION SHOULD STAY FASTER THAN SERIOUS HARDENING
RECORD / PROCESS STATUS != LIVED SITUATION
LOCAL CORRECTION != MECHANISM CHANGE
CORRECTION != RESIDUE ERASED
```

## 3. Comparison

### Material facts newly discovered by ME/TRACE

**None.**

### Material causal or procedural relation newly exposed by ME/TRACE

**None established in this pass.**

The Ombudsman already connects vulnerability, policy duties, delays, access, missing assessments, communication, repair, complaint handling and remaining work.

### Material timing relation newly exposed

**None.** The domain account already quantifies the decisive clocks.

### Material answerability route newly exposed

**None.** The domain account already identifies the relevant landlord policies, legal regime, complaints route and Ombudsman authority.

### What the project does add here

Primarily **compression and transfer language**:

- one compact way to keep route/function distinct;
- one vocabulary for clocks, burden, residue and affected scope that can be carried into unrelated domains;
- a compact representation that prevents a later summary from collapsing `complaint handled` into `home repaired`.

That may be useful, but this case does not demonstrate that it is operationally better than careful ordinary/domain reasoning.

## 4. Result

```text
DOMAIN OWNER = STRONG
FACTUAL DELTA = NONE
RELATIONAL DELTA = NONE ESTABLISHED
TIMING DELTA = NONE
ANSWERABILITY DELTA = NONE
COMPRESSION / TRANSFER VALUE = PLAUSIBLE BUT NOT DEMONSTRATED

RESULT = NO DOMAIN DELTA / COMPRESSION ONLY
```

This is a successful falsification result, not a project failure.

The field case supports the project's purpose as a portable integration language only if that compression proves useful elsewhere or under constrained attention/context. That has not been shown here.

## 5. Consequence for the build

Do **not**:

- add a housing-specific TRACE primitive;
- modify Mechanical Ethics v0.7.0 because the case 'fits';
- claim Awaab's Law validates Mechanical Ethics;
- claim the project found something the Ombudsman missed;
- turn one determination into a population claim.

Possible later use:

Test whether a bounded reader with less time/domain familiarity retains the important distinctions better with the compressed representation than with the full determination or a careful plain-language summary.

That would be a separate usability/transfer test, not earned by this analysis.

Current disposition:

```text
CASE = KEEP AS REAL FIELD COMPANION
DOMAIN GAP = NO
THEORY CHANGE = NO
RELEASE CHANGE = NO
NEXT = USE ONLY IF A TRANSFER / COMPRESSION TEST IS ACTUALLY NEEDED
OTHERWISE = STOP
```

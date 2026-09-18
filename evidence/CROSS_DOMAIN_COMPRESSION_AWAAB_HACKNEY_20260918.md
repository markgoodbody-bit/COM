# Cross-domain compression probe — Awaab repair vs Hackney benefit review — 18 September 2026

Status: **TWO-CASE PORTABILITY PROBE / EXISTING ME-TRACE STRUCTURES ONLY / NOT VALIDATION / NOT EFFICACY / NOT A NEW SCHEMA**

Cases:
- `field/AWAABS_LAW_LQ_202524733_CORRECTION_WINDOW_20260918.md`
- `field/HACKNEY_HOUSING_BENEFIT_25014765_PENDING_REVIEW_20260918.md`

Primary domain sources:
- Housing Ombudsman 202524733: https://www.housing-ombudsman.org.uk/decisions/london-quadrant-housing-trust-202524733/
- Local Government and Social Care Ombudsman 25 014 765: https://www.lgo.org.uk/decisions/benefits-and-tax/housing-benefit-and-council-tax-benefit/25-014-765

Released project basis:
- Mechanical Ethics v0.7.0
- TRACE v0.3.0

## Question

> Can one small, already-existing ME/TRACE-style representation preserve the consequential correction structure of two materially different real cases without importing their domain law, pretending they are the same mechanism, or adding a new primitive?

This is a **portability/compression** question.

It is not:

```text
DOES TRACE BEAT THE OMBUDSMAN?
DOES ME DISCOVER NEW HOUSING/BENEFITS LAW?
ARE THE TWO CASES MORALLY OR LEGALLY IDENTICAL?
```

## Common view used

No schema field is proposed. For this bounded comparison, ordinary prose keeps these already-existing relations visible:

1. affected scope;
2. material state / proposition under dispute;
3. action or default currently operating in the world;
4. correction / review route;
5. actor with practical control/authority over the action or correction;
6. correction clock and any hardening while it runs;
7. burden while unresolved;
8. correction reached and residue remaining.

## Side-by-side encoding

| Relation | Awaab / L&Q 202524733 | Hackney HB 25 014 765 |
| --- | --- | --- |
| Affected scope | Resident/household, including known/reported vulnerabilities and health concerns | Ms B, including financial position affected by recovery |
| Material state / proposition | Damp/mould + underlying property defects; post-commencement hazard severity/vulnerability/temporary-accommodation assessment not evidenced | Whether the housing-benefit overpayment was recoverable/correct |
| Action/default operating | Hazard/repair route proceeds without evidenced required Awaab triage; underlying gutter/brickwork remains unresolved | Council continues debt recovery while review is pending |
| Correction/review route | Damp/mould inspection, Awaab duties, landlord repair/complaint routes, later Housing Ombudsman | Benefit review/appeal, later councillor intervention and LGSCO |
| Practical control | Landlord controls inspection, hazard response, works, updates and temporary accommodation decision; Ombudsman later orders remedy | Council controls recovery and review decision; Ombudsman later recommends remedy |
| Clock / hardening | 25 Nov 2025 inspection -> 24 Mar 2026 underlying gutter/brickwork completion = 82 working days; 18 months from complaint to stated damp/mould resolution | Feb 2023 review request -> 28 Nov 2024 favourable review decision; nearly two years while recovery continued |
| Burden while unresolved | Distress/inconvenience; reported health effects; reported bedroom loss; repeated chasing; damaged belongings | Financial hardship; money recovered; repeated chasing; distress |
| Correction reached | Underlying works eventually completed; Ombudsman orders apology/compensation/further action | Review succeeds; debt written off; >£1,600 refunded; Ombudsman remedy |
| Residue | Earlier delay/distress not erased; other windows/doors still outstanding at determination | Financial hardship/time/distress already experienced; apology/explanation still missing until later remedy |

## Does the same representation falsely collapse the mechanisms?

Not if the domain-specific **active action/default** and **correction route** remain explicit.

The two failures are different:

```text
Awaab:
PROTECTIVE ACTION / TRIAGE / REPAIR
ARRIVES TOO SLOWLY OR INCOMPLETELY

Hackney:
CONTESTED RECOVERY ACTION
CONTINUES WHILE CORRECTION IS PENDING
```

The common structure is therefore not:

```text
ALL HARM = DELAY
ALL APPEALS SHOULD SUSPEND EVERYTHING
ALL LATE CORRECTION HAS SAME REMEDY
```

The portable relation is narrower:

```text
CURRENT ACTION / DEFAULT
+ CORRECTION ROUTE
+ WHO CONTROLS EACH
+ CLOCK
+ BURDEN WHILE THE ROUTE RUNS
+ WHAT LATER CORRECTION CANNOT ERASE
```

## What is lost by the compression

The compact view does **not** preserve all domain content.

It omits or compresses:
- detailed statutory tests and policy wording;
- evidence provenance at paragraph-level resolution;
- procedural jurisdiction/appeal doctrine;
- exact compensation/remedy reasoning;
- detailed chronology that is not material to the selected correction relation;
- domain-specific definitions such as significant/emergency hazard or recoverability.

Those omissions are acceptable only because the compact view points back to the owner accounts and is not being used as a substitute for domain adjudication.

```text
PORTABLE_MAP != DOMAIN_RECORD
COMPRESSION != AUTHORITY
```

## Comparison result

### New domain facts discovered

**None.**

### New domain relation discovered

**None established.**

### Same compact relational grammar usable in both domains

**Yes, in this bounded two-case test.**

No new primitive, scalar, domain field or schema extension was required.

### Did portability require false equivalence?

**Not in this encoding**, because the active action/default and domain route remain named rather than abstracted away.

### Did the probe show operational advantage?

**No.**

A careful plain-language analyst can construct the same comparison.

### What did survive

A narrower project hypothesis:

> The released structures can act as a portable transfer/compression language across at least these two unlike administrative cases while retaining the relation between action, correction route, control, time, burden and residue.

This is an observed representation result, not a demonstrated benefit.

## Disposition

```text
DOMAIN DELTA = NONE
NEW PRIMITIVE = NONE
NEW SCHEMA = NONE

TWO-CASE REPRESENTATION PORTABILITY = SURVIVED
FALSE-EQUIVALENCE FAILURE = NOT OBSERVED IN THIS ENCODING
OPERATIONAL / READER ADVANTAGE = NOT DEMONSTRATED

NEXT CLAIM CEILING:
PORTABLE_COMPRESSION_HYPOTHESIS HAS A REAL TWO-DOMAIN WITNESS
NOT
TRACE/ME OUTPERFORMS DOMAIN REASONING
```

## Falsifiers

This result should be cut down if a differentiated review shows:

1. a material owner-account relation was lost in either compressed view;
2. the same field changes meaning so much across the two cases that apparent portability is semantic hand-waving;
3. the representation imports a normative rule not supported by one domain;
4. the selected relations are just generic headings with no meaningful constraint;
5. an ordinary compact summary achieves the same transfer with less conceptual burden.

Outcome 5 would not make the project useless; it would route the practical owner to simpler ordinary prose.

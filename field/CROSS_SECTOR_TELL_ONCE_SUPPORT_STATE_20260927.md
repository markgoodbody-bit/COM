# Cross-sector "tell us once" — support portability without universal ownership

Date: 27 September 2026

Status: **FRESH WORLD / CROSS-SECTOR SUPPORT-STATE PRESSURE / STRONG OWNERS PRESENT / NO THR OR TRACE/ME PATCH**

Primary public source:
House of Commons Committee of Public Accounts, *Regulation of water, energy and broadband*, 11 September 2026.

https://publications.parliament.uk/pa/cm5902/cmselect/cmpubacc/105/report.html

Related public owner sources:
- ICO data-sharing code example:
  https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/data-sharing-a-code-of-practice/lawful-basis-for-sharing-personal-data/
- DSIT/DCMS consultation, *Empowering people through data intermediaries*:
  https://www.gov.uk/government/consultations/empowering-people-through-data-intermediaries
- Ofgem Priority Services Register / data-sharing work:
  https://www.ofgem.gov.uk/your-energy-supply/how-manage-your-energy-supply/join-your-suppliers-priority-services-register

## What the Committee reports

The Committee's report describes a cross-sector burden problem in water, energy and broadband.

Its findings include:
- consumers in vulnerable circumstances may have to tell multiple suppliers/teams about the same personal circumstances;
- regulators do not have a comprehensive view of a person's debt across those sectors;
- fragmented support can make early help harder;
- the Committee recommends work toward a multi-sector "tell us once" Priority Services Register approach;
- it also recommends assessing the feasibility of a central register of customer debt across the three sectors.

These are Committee recommendations, not current universal law or implemented architecture.

## The useful project pressure

The burden case is real enough to take seriously:

~~~text
REPEATED DISCLOSURE
CAN BE
A REAL SUPPORT BURDEN
~~~

But the obvious technical answer — centralise everything about the person — creates another class of risk.

Preserve:

~~~text
TELL US ONCE
!=
TELL EVERYONE EVERYTHING

SHARED SUPPORT STATE
!=
UNIVERSAL PERSON GRAPH

PORTABILITY
!=
CENTRAL OWNERSHIP

CROSS-SECTOR VISIBILITY
!=
UNBOUNDED INSPECTION AUTHORITY
~~~

The goal "reduce repeated burden" does not by itself settle:
- which data should move;
- whether support needs and financial-debt data should share the same architecture;
- who can access which fields;
- what the lawful basis is;
- how consent/withdrawal works where consent is used;
- how stale or incorrect support state is corrected;
- how corrections propagate to prior recipients;
- whether one central database is actually the best topology.

## Stronger-owner subtraction

### ICO

The ICO's data-sharing guidance already includes a real "tell us once" style example:
an electricity network operator and water company shared priority-services data with explicit consent, allowing customers to avoid separate registration.

The owner therefore already establishes that:

~~~text
BURDEN REDUCTION VIA DATA SHARING
CAN BE
LAWFUL + PURPOSE-BOUNDED + CONSENTED
~~~

for at least some contexts.

It does not establish that all cross-sector sharing should use consent, or that every dataset should be centralised.

### Data intermediaries

The 2026 government consultation on data intermediaries examines architectures where a third party acts on behalf of the individual to access/manage/share data, with permission and withdrawal.

That provides a stronger owner for alternatives to provider-by-provider manual disclosure.

It also means the design space is wider than:

~~~text
NO SHARING
vs
ONE CENTRAL STATE DATABASE
~~~

### Existing utility practice

Energy/water Priority Services Register work already contains:
- common needs codes;
- cross-utility sharing;
- customer-consent examples;
- data-quality/matching/training problems.

So the project does not own the idea of portable support state.

## Link to the current support-state handoff sketch

Existing project object:
`coordination/resources/SUPPORT_STATE_HANDOFF_CONTRACT_v0_20260927.md`

The cross-sector case sharpens its boundary.

For any cross-organisation handoff, ask:

~~~text
WHAT MINIMUM SUPPORT STATE MUST TRAVEL?
WHO MAY RECEIVE IT?
FOR WHAT PURPOSE?
HOW LONG IS IT CURRENT?
HOW CAN THE PERSON CORRECT / WITHDRAW IT?
WHERE DID IT PROPAGATE?
~~~

But do not assume all fields belong in one shared record.

## THR fault-line

This case is especially relevant to the existing THR anti-drift warning:

do not build a universal living-person graph merely because cross-context legibility is useful.

The project question remains:

> How can the support-relevant record become more portable and usable without making the person more owned?

Preserve:

~~~text
MORE LEGIBLE
!=
MORE OWNED

LESS REPEATED DISCLOSURE
!=
LESS PRIVACY BY DEFAULT
~~~

No THR schema change is earned.

## Correction / currentness problem

Cross-sector sharing creates a correction-propagation requirement.

If support state is wrong/stale:

~~~text
CORRECT AT SOURCE
!=
ALL RECIPIENT COPIES CORRECTED
~~~

A responsible architecture needs to know:
- source/authority of the state;
- currentness;
- recipient scope;
- correction/withdrawal route;
- whether downstream copies/decisions remain affected.

This is already representable with existing TRACE/THR concepts.

## Debt data deserves separate treatment

The Committee also recommends assessment of a central cross-sector debt register.

Financial-debt data and support-needs data are not interchangeable.

Preserve:

~~~text
SUPPORT NEED
!=
DEBT PROFILE

PRIORITY-SERVICE ELIGIBILITY
!=
FINANCIAL-VULNERABILITY CLASSIFICATION

ONE "VULNERABILITY" LABEL
!=
ONE DATA PURPOSE
~~~

Any future analysis should keep those purposes separate.

## Current disposition

**REAL CROSS-SECTOR BURDEN PRESSURE / "TELL US ONCE" OWNER PROBLEM / PORTABILITY-PRIVACY TENSION SHARPENED / UNIVERSAL PERSON GRAPH STILL REJECTED / SUPPORT-STATE PAPER OBJECT NARROWED / NO THR OR TRACE/ME PATCH / NO OUTREACH.**

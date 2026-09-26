# The Human Record — fractal RFC residue extraction

Date: 26 September 2026

Status: **RFC CLOSED UNMERGED / EXECUTABLE RESIDUE INTEGRATED / NO NEW TYPES / FOUR RECORDS REMAIN FOUR**

Current THR main:
`2d0cf64e685224b3c8183f5e83e18143bb16f0c7`

Post-merge:
- integrity `36237522858 / SUCCESS`;
- Pages `36237522573 / SUCCESS`;
- open THR pull requests: **NONE**.

## What happened

Exploratory THR PR #52 accumulated the project's broadest "fractal" architecture research:
- stronger-owner subtraction;
- synthetic-era hostile cases;
- privacy/identity attacks;
- protocol pressure;
- correction-impact routing;
- interoperability microcases;
- long-term continuation questions.

The RFC's strongest result was **shrinkage**, not a new architecture.

~~~text
NEW SHARED THR CORE TYPES REQUIRED FOR CURRENT CORPUS = ZERO / NOT EARNED

UNIVERSAL THR RECORD / KNOWLEDGE PROTOCOL = NOT EARNED

BOUNDED TASK-SPECIFIC EXCHANGE CONTRACTS
= MAY BE EARNED BY REAL HANDOFF LOSS
~~~

The existing contribution packet remains the concrete example of such a bounded contract.

Generic provenance / identity / custody / preservation roles remain better owned by stronger external systems including W3C PROV, C2PA, Verifiable Credentials / DID families, CIDOC/CRM family, preservation standards and domain-specific owners.

## Executable residue extracted

The one concrete implementation residue that survived repeated hostile review was a read-only impact-routing query over relations THR already publishes.

Current-main PR #81:
- reviewed head `10ae33e0d12c492f5cfaf9dae578d6055e0e2b2e`;
- candidate integrity `36237476403 / SUCCESS`;
- merged main `2d0cf64e685224b3c8183f5e83e18143bb16f0c7`.

Added:
- `tools/impact_routes.py`;
- `tools/test_validate_impact_routes.py`.

Rule:

~~~text
DIRECT source.used_by_records
UNION
ASSERTION-DERIVED record_links
-> AFFECTED REVIEW CANDIDATES
~~~

The helper:
- preserves direct source->record routes even where no assertion edge exists;
- adds assertion-derived routes where present;
- preserves unresolved record IDs and record links;
- fails loud on malformed route/evidence containers;
- rejects foreign-origin/path-collision shortcuts;
- exercises current catalogue and registered source routes.

Preserve:

~~~text
AFFECTED_RECORD != FALSE_RECORD
REVIEW_ROUTE != CORRECTION
NO_ASSERTION_EDGE != NO RECORD DEPENDENCY
REGISTERED_SOURCE_QUERY != ALL RECORD-LOCAL DEPENDENCIES
DERIVED IMPACT QUERY != DEPENDENCY ONTOLOGY
~~~

## Hostile history preserved

#52 remains available as research provenance and contains owner subtraction, protocol reduction, registry audit, helper attacks, path/route hardening, correction of an overstated prior-defect narrative, and long-term/privacy/identity pressure.

It is **not** current THR architecture.

## Bitemporal owner note

A late reviewer correctly added bitemporal modelling as a relevant stronger-owner family:
- claimed applicability / valid-time axis;
- record-held / transaction-time axis.

Codex corrected an overstatement around that distinction:
- supersession does not prove an earlier claim was true;
- correction and supersession are revision relationships;
- neither clock establishes truth.

Current `ASSERTION_MODEL.md` already preserves:
- material claim time interval;
- source version / observation time;
- correction history and durable supersession;
- `CORRECTION != RETROACTIVE ORIGINAL CERTAINTY`.

No current record forces SQL-style bitemporal storage or a new root type.

~~~text
BITEMPORAL MODELLING = STRONGER-OWNER PRESSURE / FUTURE OPTION
NEW THR TEMPORAL ROOT TYPE = NOT EARNED
~~~

## #52 disposition

Closed unmerged after #81 extraction.

Not adopted:
- `FRACTAL_ARCHITECTURE.md` as normative architecture;
- universal entity/activity/principal types;
- universal person identifier;
- universal THR network protocol;
- dependency ontology;
- automatic correction propagation;
- speculative record/schema growth.

Reopen only if a real current record or genuine cross-record source/assertion fan-out cannot be represented or review-routed with current sparse THR structures, record-local semantics, the existing impact query, and stronger-owner interoperability.

## Current state

~~~text
PUBLIC RECORDS = 4
OPEN THR PRS = 0
RECORD 5 = NOT EARNED
NEW SHARED TYPES = 0
NEW UNIVERSAL PROTOCOL = NO
EXECUTABLE IMPACT ROUTING = YES / READ-ONLY / BOUNDED
THR VALIDATED = NO
~~~

# THR fractal RFC — implementation fan-out and bounded protocol counterexample

Date: 19 September 2026 — Europe/London

Status: CURRENT RFC PRESSURE RECEIPT / NOT CANON / PUBLIC THR UNCHANGED

## Exact current state

THR draft PR #52:
- head `6f09dc68136b4fc5480cf2eba8578afcf85aa48b`
- DRAFT / OPEN / MERGEABLE
- hosted integrity run 149 / `35466492643` SUCCESS
- changed files: 12
- additions: 6083
- deletions: 0

Public THR:
- main `1f5a5919938f385f43f1e2383bdfbb52807b206e`
- exactly 4 public records
- current registry semantics unchanged
- record 5 not earned

## Existing-relation implementation audit

The current public registries already provide this impact path:

```text
SOURCE
-> OBSERVATION
-> ASSERTION EVIDENCE
-> ASSERTION RECORD_LINKS
-> RECORD FILES
-> CATALOGUE
-> HUMAN VIEW / VIEW BASIS
```

### Heritage Crafts specimen

Current source:
`thr:source:2790ee98-28a4-4fca-bd80-b5b5484c47ef`

Current assertion:
`thr:assertion:5a39064c-4cd4-4d41-92e5-dff7f38799ea`

Path:

```text
HERITAGE CRAFTS SOURCE
-> CURRENT CRAFT STATUS ASSERTION
-> SIEVE/RIDDLE JSON + MARKDOWN
-> CATALOGUE ENTRY
-> HUMAN VIEW REVIEW
```

The operational `source-checks.json` receipt remains separate from record evidence.

```text
SOURCE CHECK CHANGED != ASSERTION CHANGED
```

### Polybius fan-out specimen

One source:

`thr:source:7a1b2e15-a9b2-4af4-9e0b-2c44b10eb9d2`

currently supports four distinct assertions in the Hannibal record:
- source evaluation;
- reported documentary source;
- reported investigative method;
- reported Alpine crossing.

All four already route through assertion `record_links` to the Hannibal machine/human
record pair and from there through the catalogue to the human view.

```text
ONE SOURCE CHANGED
-> FOUR ASSERTIONS REQUIRE REVIEW
-> ONE RECORD PAIR REQUIRES REVIEW
-> HUMAN VIEW FRESHNESS MAY NEED RE-ESTABLISHMENT
```

No new dependency/correction type is required for this current one-to-many case.

### Evidence ceiling

The current four-record corpus has **no source** whose `used_by_records` spans multiple
public records.

Therefore:

```text
INTRA-RECORD FAN-OUT = TESTED
MULTI-RECORD SOURCE FAN-OUT = NOT YET PRESENT / NOT TESTED
```

Do not manufacture a shared source merely to satisfy the architecture test.

A genuine source/assertion reused across multiple public records is the correct next
fan-out falsifier.

## Protocol-pressure counterexample

The earlier shorthand:

```text
THR PROTOCOL = NOT EARNED
```

was too broad.

Current public THR already has:

`human-record-contribution-packet/0.1`

This optional machine-checkable relay envelope was earned by a real transport problem:

```text
CONTRIBUTOR CANNOT POST DIRECTLY
-> RELAY CARRIES CONTRIBUTION
-> ATTRIBUTION / SOURCE-CHECK STATE / UNKNOWNS / RIGHTS BOUNDARY CAN BE LOST
```

The contribution packet preserves:
- target;
- declared contributor;
- relay provenance;
- contribution;
- reported evidence-check state;
- unknowns;
- not-checked material;
- rights/privacy boundary;
- authentication ceiling.

The real Grok flak packet is a concrete use.

Therefore:

```text
NO THR PROTOCOL PRESSURE AT ALL = FALSIFIED

BOUNDED TASK-SPECIFIC EXCHANGE CONTRACT
= CAN BE EARNED BY REAL HANDOFF LOSS

UNIVERSAL THR RECORD / KNOWLEDGE PROTOCOL
= NOT CURRENTLY EARNED
```

Preserve:

```text
ONE BOUNDED EXCHANGE FORMAT != UNIVERSAL THR PROTOCOL
VALID PACKET != VALID CLAIM
MACHINE-CHECKABLE ENVELOPE != NETWORK SERVICE
```

## Current architecture ceiling

```text
CURRENT THR ARCHITECTURE
=
PUBLIC RECORD PRODUCT
+ MINIMUM INTEROPERABILITY CONTRACT
+ SPARSE SHARED IDS / RELATIONS WHEN EARNED
+ RECORD-LOCAL STRUCTURE
+ STRONGER-OWNER MAPPINGS WHEN MATERIAL
+ EXPLICIT EVIDENCE / CORRECTION / RIGHTS CEILINGS
+ BOUNDED TASK-SPECIFIC EXCHANGE CONTRACTS WHEN REAL HANDOFF LOSS EARNS THEM
```

Still not earned:
- universal THR ontology;
- universal THR record/knowledge protocol;
- generic dependency type;
- generic correction-propagation type;
- global independence type/score;
- custom archive/federation/consensus stack;
- fifth record.

## Current falsifiers

1. **Zero-new-shared-types**
   - find one real consequential distinction current layers cannot preserve.

2. **Multi-record fan-out**
   - wait for a real source/assertion reused across multiple public records;
   - test whether current relations route a material change to every affected record/view.

3. **Universal protocol necessity**
   - find a real multi-implementation exchange need not handled by existing formats,
     profiles/mappings, stronger-owner standards or a narrow task-specific contract.

4. **Bounded exchange contract**
   - identify a real handoff where material meaning is being lost;
   - add the smallest versioned envelope only if simpler existing mechanisms are
     insufficient.

```text
REAL COUNTEREXAMPLE -> SMALLEST EARNED CHANGE
NO COUNTEREXAMPLE -> KEEP NARROW
NO FORMAT / TYPE / PROTOCOL BY MOMENTUM
```

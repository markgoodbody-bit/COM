# THR fractal RFC — PROV correction and zero-new-types result

Date: 19 September 2026 — Europe/London

Status: CURRENT CORRECTION RECEIPT / NOT CANON / PUBLIC THR UNCHANGED

## Current THR RFC

PR #52:
- head: `fb514b1f7bc0d960eaf408c60614b966f6f3e2a0`
- draft / open / mergeable
- hosted integrity: run 143 / `35465831576` SUCCESS
- public THR main remains `1f5a5919938f385f43f1e2383bdfbb52807b206e`
- public records remain exactly 4
- registry semantics unchanged

## Correction of the earlier PROV receipt

Preserve the earlier dated receipt:
`coordination/build_ledger/THR_FRACTAL_PROV_INTEROP_20260919.md`

Do not rewrite it. It records the earlier state.

Codex later found two semantic defects in the first W3C PROV mapping:
1. the historical validator run was incorrectly represented as generating a THR JSON receipt that Git history shows was written later;
2. GitHub run `updated_at` was incorrectly promoted to a PROV activity end time.

The repair now represents:

```text
VALIDATION ACTIVITY
-> GITHUB OPERATIONAL OUTPUT

LATER THR JSON RECEIPT
-> DERIVED FROM GITHUB OPERATIONAL OUTPUT
```

Unsupported PROV activity times were removed.

Preserve:

```text
RDF PARSES != PROVENANCE CLAIM TRUE
PROCESS OUTPUT != LATER PROVENANCE REPRESENTATION
RUN UPDATED_AT != ACTIVITY END TIME
CORRECTION != HISTORY REWRITE
```

Codex later verified these two bounded repairs at head
`be77152f227dbdcff4990a65aae228b65b9622b7`.
That verification is not a full architecture validation.

## Residue subtraction

### Independence

A provenance / ancestry / custody graph supplies evidence for a bounded independence
assessment. It does not establish independence.

```text
GRAPH != INDEPENDENCE VERDICT
NO KNOWN COMMON ANCESTOR != INDEPENDENT
DISTINCT URL != INDEPENDENT
DISTINCT INSTITUTION != INDEPENDENT
DISTINCT MODEL / AGENT != INDEPENDENT
```

No global THR independence type or score is earned.

### Correction routing

A changed upstream dependency should route affected downstream material to review, not
automatically rewrite it.

```text
UPSTREAM CORRECTION != DOWNSTREAM CORRECTION
DEPENDENCY TOUCHED != DESCENDANT FALSE
LOAD-BEARING DEPENDENCY CHANGED -> DOWNSTREAM REVIEW REQUIRED
REVIEW REQUIRED != INVALID
```

No generic THR correction-propagation ontology is earned.

### Continuation / preservation

"Can a future reader continue without trusting THR?" is now an acceptance criterion, not
a reason for THR to own an archival stack.

Use stronger owners where fit: OAIS, PREMIS, OCFL, BagIt, RO-Crate, LOCKSS and domain
archives.

Not earned:
- custom THR archive format
- custom fixity/version format
- custom preservation federation
- blockchain/distributed-ledger architecture
- mandatory central resolver

## Zero-new-shared-types test

The current four public records plus the validator self-description, W3C PROV,
correction-routing and continuation microcases were tested against the narrowed
architecture.

Current result:

```text
CURRENT SHARED THR LAYERS
+ RECORD-LOCAL STRUCTURE
+ STRONGER-OWNER INTEROP WHEN EARNED
= SUFFICIENT FOR ALL CURRENT PRESSURE EXAMINED

NEW SHARED THR CORE TYPE REQUIRED NOW
= ZERO / NOT EARNED
```

This is provisional and falsifiable. It is not a permanent schema freeze.

The review packet now asks an independent reviewer to find one concrete consequential
counterexample. If one exists, earn the smallest missing type/relation. If none exists,
do not invent one.

## Current boundary

```text
PUBLIC RECORDS = 4
RECORD 5 = NOT EARNED
NEW GLOBAL EVENT TYPE = NOT EARNED
NEW GLOBAL PROCESS TYPE = NOT EARNED
NEW GLOBAL PRINCIPAL TYPE = NOT EARNED
NEW GLOBAL ATTESTATION TYPE = NOT EARNED
NEW GLOBAL ANCHOR TYPE = NOT EARNED
NEW GLOBAL INDEPENDENCE TYPE = NOT EARNED
GENERIC CORRECTION-PROPAGATION TYPE = NOT EARNED
CUSTOM PRESERVATION STACK = NOT EARNED

ZERO-NEW-SHARED-TYPES = PROVISIONAL / FALSIFIABLE
MERGE / CANON = NOT REQUESTED
```

## Next

```text
REAL COUNTEREXAMPLE
-> EARN SMALLEST MISSING TYPE / RELATION

NO COUNTEREXAMPLE
-> HOLD / KEEP NARROW

NO NEW TYPE BY MOMENTUM
```

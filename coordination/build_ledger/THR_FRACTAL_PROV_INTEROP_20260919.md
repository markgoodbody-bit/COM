# THR fractal W3C PROV interoperability microcase — 19 September 2026

Status: **CONCRETE INTEROP CASE PASS / GENERIC PROCESS GRAPH OWNER-SUBTRACTED / NO NEW THR GLOBAL TYPES**

Target:
THR draft PR #52

Exact head:
`2ee2e777e7f6ab887402127c891ed98123d90068`

Hosted:
`Validate Human Record integrity — run 133 — SUCCESS`

## Input microcase

Real THR validator self-description:
- GitHub Actions run `35463860339`;
- trigger head;
- PR base;
- synthetic merge checkout actually executed;
- workflow definition;
- validator source blobs;
- execution service;
- result receipt;
- warnings / epistemic ceilings.

## W3C PROV mapping

Added:
- `examples/fractal-validator-run.prov.ttl`
- `FRACTAL_INTEROP_PROV_MICROCASE.md`

PROV mapping uses:
- `prov:Entity`;
- `prov:Activity`;
- `prov:SoftwareAgent`;
- `prov:used`;
- `prov:wasGeneratedBy`;
- `prov:wasDerivedFrom`;
- `prov:wasAssociatedWith`;
- start/end time.

The Turtle parses successfully as **42 RDF triples**.

It uses document-local fragment identifiers only:
- no `thr:process`;
- no `thr:principal`;
- no `thr:event`.

## Result

```text
W3C PROV = SUFFICIENT OWNER FOR GENERIC PROCESS GRAPH IN THIS MICROCASE

THR-NATIVE GLOBAL PROCESS TYPE = NOT EARNED
THR-NATIVE GLOBAL SOFTWARE-AGENT TYPE = NOT EARNED

THR-SPECIFIC RECEIPT / WARNING / EPISTEMIC / AUTHORITY CEILINGS = STILL USEFUL
```

The mapping confirms:

```text
PROV GRAPH
= generic process ancestry

THR RECEIPT
= bounded epistemic / warning / authority meaning
```

## Hostile checks preserved

```text
GITHUB ACTIONS AS prov:SoftwareAgent
!= TRUTH AUTHORITY
!= THR GOVERNANCE
!= INDEPENDENT HISTORICAL WITNESS

THR JSON RECEIPT
+ PROV TURTLE MAPPING
!= TWO INDEPENDENT OBSERVATIONS

TIMESTAMP
!= REPOSITORY STATE
```

## Current branch state

PR #52:
- draft / open / mergeable;
- head `2ee2e777e7f6ab887402127c891ed98123d90068`;
- 8 files;
- 3730 additions;
- 0 deletions;
- hosted integrity PASS.

Public THR remains exactly 4 records.

Current registries remain unchanged.

## Stop condition

This pass does not earn:
- RDF migration of THR;
- generic `thr:process` or `thr:principal`;
- a new validator requirement;
- PKI;
- transparency log;
- fifth record.

Next material pressure:
1. independent hostile review;
2. genuine independent witness/replica;
3. a current record requiring another external standard;
4. a distinct interop case earned by a real artifact.

```text
ONE INTEROP CASE PASSED
!=
STANDARD ADOPTION
!=
ARCHITECTURE VALIDATION
```

# THR fractal architecture lane opened — 19 September 2026

Status: **EXPLORATORY RFC / HOSTILE PASS 1 COMPLETE / SELF-DESCRIPTION MICROCASE COMPLETE / NO CANON OR REGISTRY PROMOTION**

Triggering Campfire pressure:
- concern that synthetic abundance can erode trust in authentic records as well as insert false ones;
- recognition that watermarking/detection alone cannot preserve enough ancestry, correction and answerability;
- Mark's framing that mature THR may need a fractal identity/provenance fabric rather than only a small catalogue;
- explicit reminder that this ultimately cannot be built by Framework/Mark alone, but current burden remains ours for now.

This receipt records the bounded work actually done.

## Live THR baseline before work

Repository:
`markgoodbody-bit/human-record`

Main:
`1f5a5919938f385f43f1e2383bdfbb52807b206e`

Public records:
exactly four.

Current models already present:
- `SCALE.md`;
- `IDENTITY_MODEL.md`;
- `SOURCE_MODEL.md`;
- `ASSERTION_MODEL.md`;
- `LIVING_SUBJECTS.md`;
- `RECORD_CONTRACT.md`;
- sparse entity/source/mention/assertion registries.

Existing separations include:

```text
NAME != ENTITY
MENTION != ENTITY
URL != SOURCE
SOURCE != OBSERVATION
OBSERVATION != PRESERVED COPY
PRESERVED COPY != TRUTH
ENTITY != ASSERTION
ASSERTION != TRUTH
CUSTODY != GOVERNANCE
```

Therefore this lane did not start from a blank architecture.

## Draft PR #52

Title:
`THR: exploratory fractal record architecture RFC`

Branch:
`framework/fractal-thr-rfc-20260919`

Exact current head:
`d054d91508b6dd6dd70a2ce2b2cd5ae2305c2b63`

Base:
`1f5a5919938f385f43f1e2383bdfbb52807b206e`

Status:
draft / open / mergeable

Hosted validation:
`Validate Human Record integrity — run 129 — SUCCESS`

Changed surface:
- 5 files;
- 2666 additions;
- 0 deletions.

No current record, catalogue entry, registry semantics or validator requirement changed.

## FRACTAL_ARCHITECTURE.md

Candidate next-layer concepts:
- public addressability separate from authority;
- content fixity;
- principals;
- keys/signatures;
- typed/scoped capability/authority;
- events;
- processes/transforms;
- attestations;
- anchors/checkpoints;
- independent witnesses;
- recursive self-description;
- distributed anti-rewrite properties;
- physical-world anchors;
- living-human anti-enumeration.

Core direction:

```text
PUBLIC THR ID = ADDRESS
KEY / SIGNATURE = WHO SIGNED / ATTESTED
CAPABILITY / AUTHORITY = WHAT THEY WERE ALLOWED TO DO
PROCESS RECEIPT = HOW A STATE WAS PRODUCED
HASH / CONTENT ID = WHICH BYTES
ANCHOR / WITNESS = WHAT HISTORY CAN STILL VERIFY

NONE OF THOSE = TRUTH
```

Candidate long-term design direction:

`THR MUST NOT REQUIRE TRUST IN THR`

This is a direction, not a current achieved property.

## Four-record hostile falsification

`FRACTAL_FALSIFICATION.md`

The RFC was tested against:
1. Camp Fire;
2. viral flak claim;
3. sieve/riddle revival;
4. Hannibal source-survival.

First pass found ten over-generalisation risks and forced these constraints:

```text
LOCAL VALUE / NODE
!= RECORD-LOCAL ADDRESSABLE OBJECT
!= SHARED THR OBJECT

RECURSION POSSIBLE != RECURSION MATERIAL

EVENT OBJECT != ASSERTION EVENT OCCURRED

PROCESS CLAIMED BY SOURCE
!= PROCESS OBSERVED BY THR
!= PROCESS EXECUTED BY THR

SOURCE STATEMENT
!= OBSERVATION
!= ATTESTATION
!= PROCESS RECEIPT

AUTHORITY = TYPED + SCOPED + TEMPORAL

INDEPENDENCE = PROPOSITION / FUNCTION SPECIFIC

COMMON INTERFACES != ONE UNIVERSAL RECORD SCHEMA

NO UNIVERSAL TRUST SCORE

LIVING MENTION != PUBLIC PRINCIPAL
```

The RFC was repaired to adopt those constraints.

Current result:

```text
FRACTAL DIRECTION = SURVIVES FIRST INTERNAL HOSTILE PASS
GLOBAL NEW REGISTRY TYPES = NOT YET EARNED
CRYPTO / PKI BUILD = NOT YET EARNED
FIFTH PUBLIC RECORD = NOT EARNED
```

## Independent review route

`FRACTAL_REVIEW_PACKET.md`

A structured hostile-review packet now exists for future human or AI reviewers.

It asks reviewers to attack:
- false authority;
- false independence;
- identity/privacy;
- time/correction;
- recursive explosion;
- physical-world failure;
- compromised THR;
- long-term decay;
- governance capture;
- privacy/surveillance.

It requires testing against the four existing records and adding at least one new hostile case.

This is preparation for answer-back, not evidence of independent review.

## First self-description microcase

`FRACTAL_SELF_DESCRIPTION_MICROCASE.md`

Machine fixture:
`examples/fractal-validator-run.experimental.json`

Real target:
GitHub Actions THR validator run `35463860339`.

This microcase intentionally uses a record-local experimental ID and does not introduce shared `thr:process`, `thr:principal`, `thr:event`, `thr:attestation` or `thr:anchor` types.

It forced these distinctions:

```text
CURRENT PR HEAD
!= RUN TRIGGER HEAD
!= EXECUTED CHECKOUT

WORKFLOW SOURCE
!= PROCESS INSTANCE

PROCESS SUCCESS
!= WARNING-FREE

PASS != NO RESIDUAL

GITHUB ACTIONS RECEIPT
!= INDEPENDENT HISTORICAL WITNESS
```

Real run details preserved:
- trigger head: `7cd55c24c145d8424256e72ae27b6cdff2669f12`;
- base: `1f5a5919938f385f43f1e2383bdfbb52807b206e`;
- executed synthetic merge checkout:
  `3cced4453cf64b52a9a7364e0ba10b6a2ec28554`;
- workflow + validator Git blob identities;
- structural validator PASS;
- operational validator PASS;
- 103 rejection tests -> OK;
- seven THR validator warnings preserved.

The microcase explicitly does not establish historical truth, validator correctness, GitHub independence, or governance authority.

## Current stop / next pressure

Do not add registry types merely because the RFC names them.

Next meaningful pressure should come from at least one of:
1. independent human/AI hostile review using `FRACTAL_REVIEW_PACKET.md`;
2. a genuine independent witness / replica case;
3. a current record exposing a missing distinction;
4. a real operational need for repeated event/process/principal/attestation identity.

```text
COMPREHENSIVE PURPOSE != COLLECT EVERYTHING NOW
FRACTAL ARCHITECTURE != INFINITE RECORD EXPANSION
THR PROTOCOL != THR AUTHORITY
```

## Relationship to THR current state

Public THR remains exactly four records.

Record 5 remains not earned.

Released/public semantics remain unchanged.

This lane is exploratory architecture only.

```text
DRAFT RFC != CANON
DRAFT PR != MERGE
SELF-DESCRIPTION FIXTURE != REGISTRY TYPE
HOSTED VALIDATION != ARCHITECTURE VALIDATION
```

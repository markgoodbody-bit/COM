# THR ↔ Doubt interoperability result — 18 September 2026

Status: **OWNER SUFFICIENT WITH LOSS / FOUR MAPS STRUCTURALLY VALID / NOT SOURCE-TRUTH VALIDATION / NOT ADOPTION**

## Question

Can the unmodified Doubt evidence contract preserve the source/evidence distinctions that motivated the standalone EvidenceBridge proof?

## Upstream owner

Doubt:
https://github.com/alsoleg89/doubt

Validator used:
- release label: v0.8.0
- exact action commit: `647482d536e8c3fdda573699426b7dc5673f9905`

No local Doubt schema fork was made.

## Cases

### 1. Flak claim

Load-bearing distinction:
`REPETITION != CORROBORATION`

The map represents:
- a sourced claim that the linked article/summary are downstream restatements;
- the resulting qualification on the current position;
- checked-source non-establishment;
- the still-unknown true aggregate mortality rate.

Doubt does not have a first-class source-to-source ancestry edge, so ancestry is represented as a sourced claim/qualification rather than a machine-typed source graph.

### 2. Hannibal

Load-bearing distinctions:
- English translation rendering != checked Greek literal;
- Polybius' criticism != THR adjudication.

The map represents both through sourced evidence + missing facts without upgrading either stronger claim.

Doubt does not have THR's `reported_by_source` assertion state. Attribution therefore survives in evidence text and edge reasoning rather than a dedicated state field.

### 3. R. Vale

Load-bearing distinctions:
- same string != same entity;
- Source C report != direct observation;
- unresolved = valid.

The map preserves:
- two live possible identity worlds;
- Source C as qualifying contrary evidence;
- actual identity and Source C correctness as explicit unknowns.

Again, reported-vs-observed is carried semantically in the source/evidence text rather than by a dedicated assertion-state vocabulary.

### 4. Sieve/riddle revival — unseen promotion case

This case was added only after the original three maps validated.

Load-bearing distinctions:
- revival != complete tacit-skill transmission;
- partial direct learning != complete reconstruction;
- two Heritage Crafts pages != two independent evidence families.

It fit the same unmodified Doubt contract.

## Exact validation witness

Exact branch head before this result note:
`8f44c1f87887acaab0455ad91bce64380f526bef`

Hosted workflow:
`35368903563 SUCCESS`

Upstream validator result:

```text
Validated 4 maps: 4 valid, 0 invalid.

flak         receipt fbeea813525d
hannibal     receipt 69c24b6bc869
r-vale       receipt 325b63004d42
sieve-riddle receipt db2cde962a38
```

These are Doubt evidence-contract receipts over the recorded maps. They are not proof that the underlying source claims are true.

## Disposition

```text
GENERIC EVIDENCE MAP NEED = OWNER FOUND
DOUBT CAN REPRESENT FOUR THR PRESSURE CASES = OBSERVED
DEDICATED THR MACHINE SEMANTICS PRESERVED = NO
CONSEQUENTIAL LOSS FROM THAT COMPRESSION = NOT OBSERVED
OWNER SUFFICIENT WITH LOSS = CURRENT RESULT
STANDALONE EVIDENCEBRIDGE = STOP
DOUBT FORK / EXTENSION = NOT EARNED
THR SCHEMA CHANGE = NO
```

The important loss is machine expressivity:
- no dedicated source-ancestry relation;
- no dedicated reported/observed assertion state;
- no dedicated correction/supersession object.

For these four reader-facing cases, that loss did not prevent an honest evidence map. It may matter in future automation or correction workflows, but that must be demonstrated by a concrete use failure rather than inferred from schema preference.

## What this changes

If the project later needs an inspectable evidence map, the default should be:

1. check whether Doubt already serves the need;
2. encode the project-specific distinctions honestly;
3. preserve any compression loss;
4. extend or build something new only after a real failure.

This is stronger than maintaining a parallel EvidenceBridge product.

```text
USE STRONGER OWNER > REBUILD OWNER
INTEROPERABILITY != FULL SEMANTIC EQUIVALENCE
VALID MAP != SOURCE TRUTH
OWNER FOUND != PROJECT FAILURE
```

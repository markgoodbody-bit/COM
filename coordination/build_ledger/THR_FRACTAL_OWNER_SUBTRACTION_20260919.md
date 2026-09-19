# THR fractal strongest-owner subtraction — 19 September 2026

Status: **FIRST EXTERNAL OWNER PASS COMPLETE / RFC NARROWED / NO NEW REGISTRY TYPES**

Target:
THR draft PR #52

Exact head:
`a1deaf1580c86a58099c5c48c782459a29e22de8`

Hosted:
`Validate Human Record integrity — run 131 — SUCCESS`

## Stronger owners identified

### W3C PROV

Owns generic provenance interchange around:
- Entity;
- Activity;
- Agent;
- generation / derivation;
- attribution / delegation.

Disposition:
`GENERIC PROVENANCE ONTOLOGY = OWNER FOUND`

THR should map/interoperate rather than invent a competing universal process/principal ontology.

### C2PA Content Credentials

Owns:
- signed digital-asset provenance;
- assertions;
- claims;
- claim signatures;
- hard / soft bindings;
- provenance manifests;
- ingredients;
- signer trust model;
- repository receipts;
- AI-disclosure structures.

Disposition:
`SIGNED DIGITAL MEDIA PROVENANCE = OWNER FOUND`

THR should preserve/reference C2PA provenance where present, not replace it.

### W3C Verifiable Credentials

Owns generic cryptographically secured credential/claim interchange between issuers, holders and verifiers.

Disposition:
`GENERIC CRYPTOGRAPHIC CREDENTIAL FORMAT = OWNER FOUND`

### W3C DID

Owns generic decentralised identifier/control mechanics.

Disposition:
`GENERIC DECENTRALISED CONTROL IDENTIFIER = OWNER FOUND`

Do not make DIDs mandatory THR person IDs.

### in-toto / SLSA

Own software/build process provenance and attestation patterns.

Disposition:
`SOFTWARE PROCESS / BUILD PROVENANCE = OWNER FOUND`

THR's validator self-description should test interoperability before inventing its own software-attestation format.

### Sigstore / Rekor

Own software signing/transparency-log infrastructure.

Disposition:
`SOFTWARE SIGNING TRANSPARENCY = OWNER FOUND`

Do not build a THR-native transparency log by momentum.

### Memento

Own web-resource datetime/version negotiation.

Disposition:
`WEB TIME VERSION ROUTING = OWNER FOUND`

THR remains evidence/currentness consumer and router.

### Software Heritage / SWHID

Own intrinsic persistent software-object identity and preservation.

Disposition:
`SOFTWARE CONTENT ID / ARCHIVAL OWNER = OWNER FOUND`

Do not replace SWHID for software content identity.

## Surviving THR residue

After subtraction, THR's candidate unique role is narrower:

```text
PRESERVE THE JOINS

-> what THR actually observed
-> what a source / external provenance object actually asserts
-> claim/function-specific independence
-> typed/scoped/temporal authority
-> correction + disagreement
-> unknown / unexamined material
-> rights / privacy / consent / cultural-control boundaries
-> downstream record consequences
-> continuation without trusting current THR operator
```

Core repaired principle:

```text
STRONGER OWNER EXISTS
-> LINK / MAP / INTEROPERATE

THR-NATIVE TYPE
-> ONLY WHEN MATERIAL THR RESIDUE SURVIVES
```

and:

```text
FRACTAL THR != THR OWNS EVERY LAYER
FRACTAL THR = THR PRESERVES THE JOINS
```

## Branch changes

Added:
- `FRACTAL_OWNER_SUBTRACTION.md`

Repaired:
- `FRACTAL_ARCHITECTURE.md`
  - interoperability-first / strongest-owner rule;
  - external standards remain external evidence objects;
  - no generic replacement standards.

PR #52 now:
- head `a1deaf1580c86a58099c5c48c782459a29e22de8`;
- draft / open / mergeable;
- 6 files;
- 3390 additions;
- 0 deletions;
- hosted integrity PASS.

## No promotion

```text
PUBLIC THR RECORDS = 4
RECORD 5 = NOT EARNED
CURRENT REGISTRIES = UNCHANGED
NEW GLOBAL TYPES = NOT EARNED
PKI = NOT EARNED
BLOCKCHAIN = NOT EARNED
TRANSPARENCY LOG = NOT EARNED
MERGE / CANON = NOT REQUESTED
```

## Next earned pressure

At least one of:
1. independent hostile review using `FRACTAL_REVIEW_PACKET.md`;
2. genuine independent witness / replica;
3. current record exposes missing distinction;
4. concrete interoperability microcase against one stronger owner.

Do not continue expanding architecture by momentum.

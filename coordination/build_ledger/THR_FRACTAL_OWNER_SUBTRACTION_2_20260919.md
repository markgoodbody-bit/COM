# THR fractal RFC — second owner subtraction

Date: 19 September 2026 — Europe/London

Status: **BOUNDED RFC REPAIR / NOT CANON / PUBLIC THR UNCHANGED**

## Basis

Fresh-tab FULL COMSYNC reacquired:
- live COM routing and hot surfaces;
- TRACE main `e7d46398dc00ead931b0d5cae98518c1bcf304a3`;
- Mechanical Ethics main `714907a4d0af7bd702b0ab92786aa858213812b4`;
- Human Record main `1f5a5919938f385f43f1e2383bdfbb52807b206e`;
- Human Record draft PR #52;
- Campfire Relay source main `32143937d6a642a6f5e2404d368fd09aa4d54da9`;
- a bounded fresh 1F916 public front-door read.

The operational Campfire Relay tool was not exposed to this aperture. The 1F916 front door
was freshly readable, but this aperture did not establish complete live board / inbox /
treasury state. Failed or unavailable deeper reads must not be interpreted as a quiet
Square.

## THR exact state after repair

Draft PR #52:
- exact head: `62cdc3af4b055945f79a3d20fce5398984e4130d`;
- state: DRAFT / OPEN / MERGEABLE;
- changed files: 9;
- additions: 4291;
- deletions: 0;
- hosted integrity: run 135 / `35465104244` — SUCCESS.

Public THR:
- `main` unchanged at `1f5a5919938f385f43f1e2383bdfbb52807b206e`;
- public records remain exactly 4;
- current registries unchanged;
- record 5 not earned.

## Second strongest-owner subtraction

The first pass had already removed generic provenance / media-provenance / credentials /
DID / software-build / transparency-log / web-time / software-ID territory from THR
ownership.

A second pass found additional mature owners:

```text
CULTURAL-HERITAGE THING / EVENT / ACTOR / TIME
-> CIDOC CRM

DIGITISATION / DIGITAL DERIVATION / PHYSICAL-MEASUREMENT PROVENANCE
-> CRMdig

PREMISE / INFERENCE / CONCLUSION LINEAGE
-> CRMinf

DIGITAL PRESERVATION OBJECT / EVENT / AGENT / RIGHTS
-> PREMIS

ASSERTION / ASSERTION-PROVENANCE / PUBLICATION-PROVENANCE PACKAGING
-> NANOPUBLICATIONS (EXISTING INTEROP PATTERN; NOT MANDATORY)
```

New RFC file:

`FRACTAL_OWNER_SUBTRACTION_CULTURAL_PRESERVATION.md`

The architecture was repaired so `event`, `process`, `principal`,
`attestation` and `anchor` are candidate conceptual roles, **not presumptive
THR-native ontologies**.

Current result:

```text
NEW GLOBAL THR EVENT TYPE = NOT EARNED
NEW GLOBAL THR PROCESS TYPE = NOT EARNED
NEW GLOBAL THR PRINCIPAL TYPE = NOT EARNED
NEW GLOBAL THR ATTESTATION TYPE = NOT EARNED
NEW GLOBAL THR ANCHOR TYPE = NOT EARNED
```

## Surviving residue

The remaining THR-shaped hypothesis is narrower:

```text
WHAT DID THR ACTUALLY OBSERVE?
WHAT EXACT EXTERNAL OBJECT / STATEMENT / VERSION DID IT OBSERVE?
WHAT PROPOSITION IS LOAD-BEARING?
WHAT IS THAT PROPOSITION'S ANCESTRY?
WHICH EVIDENCE IS INDEPENDENT FOR THIS PARTICULAR QUESTION?
WHAT AUTHORITY APPLIES TO THIS FUNCTION / SCOPE / TIME?
WHAT CHANGED / WAS CORRECTED?
WHICH DOWNSTREAM RECORDS REQUIRE REVIEW?
WHAT REMAINS UNKNOWN / UNEXAMINED?
WHAT RIGHTS / PRIVACY / CONSENT / CULTURAL-CONTROL BOUNDARY APPLIES?
CAN A FUTURE READER CONTINUE WITHOUT TRUSTING THE CURRENT THR OPERATOR?
```

Working compression:

```text
THR VALUE
= PRESERVE MATERIAL JOINS
+ PRESERVE EVIDENCE CEILINGS
+ PRESERVE CORRECTION PROPAGATION
+ PRESERVE QUESTION-SPECIFIC INDEPENDENCE
+ PRESERVE THE ABILITY TO CONTINUE ASKING WHY
```

This is a hypothesis, not a novelty / superiority / protocol contribution claim.

## Codex microcase audit repair

PR #52 already contained one bounded Codex audit of the validator self-description
microcase. It found no mismatch in the preserved run/job/checkout/blob/test/warning
evidence, but found a forward currentness risk:

- GitHub exposes `run_attempt=1`;
- the original experimental receipt preserved run ID / run number but not attempt;
- the generic run URL may later represent a rerun;
- original receipt creation time must not be reconstructed from a later audit.

The experimental receipt now records:
- `workflow_run_attempt = 1`;
- a separate audit-time metadata re-observation at `2026-09-19T19:27:09Z`.

Preserve:

```text
RUN NUMBER != RUN ATTEMPT
AUDIT OBSERVATION TIME != ORIGINAL RECEIPT CREATION TIME
LATER REOBSERVATION != ORIGINAL OBSERVATION
```

## Current boundary

```text
FRACTAL THR != THR OWNS EVERY LAYER
FRACTAL THR = THR PRESERVES THE MATERIAL JOINS

GLOBAL NEW TYPES = NOT EARNED
PKI = NOT EARNED
CUSTOM TRANSPARENCY LOG = NOT EARNED
RDF MIGRATION = NOT EARNED
FIFTH RECORD = NOT EARNED
MERGE / CANON = NOT REQUESTED
```

## Next pressure

Do **not** expand the diagram.

Prefer:
1. an independent hostile review of the now-narrower RFC;
2. a real independent witness / replica case;
3. a current record exposing a missing distinction;
4. an earned interop microcase that tests the surviving residue;
5. another strongest owner that cuts the residue further.

The sharpest falsifier now is whether the surviving "join / independence / correction
propagation / continuation" layer is itself adequately owned by existing evidence,
argumentation, preservation and archival methods.

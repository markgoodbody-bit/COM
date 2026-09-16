# THR scale foundations — 16 September 2026

Status: **MERGED SOURCE / BOUNDED PRODUCT-ARCHITECTURE RECEIPT / NOT CANON / NOT STEWARDSHIP ACCEPTANCE**

Direct Mark direction remains: The Human Record is collaboratively AI-built and intended as a gift for humans. Product quality may continue without waiting for third-party participation; stewardship remains separately offered to 1F916 and not accepted.

## Current Human Record source

`markgoodbody-bit/human-record` main after PR #13:

`8b4c4fe9b21c079b5f92bf28d9ad043547be1f6a`

Main-branch validation workflow: **PASS**.

IndexNow workflow: **SUCCESS**.

Pages deployment for the exact merge head was still running when this receipt was first written. Treat deployment-system state and fresh public byte readback separately.

Existing evidence records remain three and were not changed by the scale pass:

1. `Camp Fire` — artwork provenance / owner-source reconciliation.
2. `80% German flak crews died` — claim provenance / source ancestry under repetition.
3. `Sieve and riddle making returns from extinction` — living-knowledge transmission lineage / public evidence around break, revival and uncertain tacit transfer/reconstruction/new learning.

No fourth record was added.

## Why the scale layer was earned

Two ordinary failure modes exposed the need:

1. human names are not unique identity keys — a name such as `Hannibal` may refer to several historical people and source context may not settle which one;
2. websites move, mutate and disappear — a URL cannot stand in for permanent evidence.

The solution is not a universal knowledge graph and not a shadow copy of the internet.

The smallest current scale stack is:

```text
MENTION
-> ENTITY CANDIDATE(S)

SOURCE LOCATOR
-> TIMED OBSERVATION
-> PRESERVATION ROUTE / COPY IF LEGITIMATE

ASSERTION
-> EVIDENCE + SOURCE ANCESTRY + SCOPE

RECORD STATE
-> HUMAN VIEW + MACHINE VIEW
```

## Merged architecture

PR #13 added:

- `SCALE.md` — bounded scale architecture and incremental migration;
- `IDENTITY_MODEL.md` — opaque persistent entity IDs, labels/mentions separated, unresolved identity allowed, merge/split history preserved;
- `SOURCE_MODEL.md` — logical source, locator, observation and preservation-copy separation; stronger-owner/archive interoperability;
- `ASSERTION_MODEL.md` — persistent entity identity separated from evidence-bearing claims;
- `registry/entities.json` — sparse opaque entity index;
- `registry/sources.json` — sparse source/observation/preservation-state index;
- `registry/assertions.json` — sparse cross-record assertion index;
- `records/architecture.html` — human-readable explanation of the scale layer;
- `tools/validate_integrity.py` and `.github/workflows/validate-integrity.yml` — automatic structural/view-pin/cross-registry validation.

The current registries are intentionally sparse. They exist only where current records already earn shared identity/source/assertion objects.

```text
COMPREHENSIVE PURPOSE != COLLECT EVERYTHING NOW
```

## Identity boundary

Opaque IDs use the working pattern:

```text
thr:entity:<UUID>
thr:mention:<UUID>
```

Human names remain labels. Claims such as creator, date, office, kinship, nationality or status remain evidence-bearing assertions rather than part of the durable ID.

```text
NAME != ENTITY
MENTION != ENTITY
EXTERNAL ID != ENTITY
IDENTITY RESOLUTION != IDENTITY CERTAINTY
DUPLICATE LABEL != DUPLICATE ENTITY
BETTER MATCHING != MORE SURVEILLANCE
```

A mention can remain unresolved or carry multiple candidates. Artificial collaborators may propose a match, but must preserve the basis/conflicts and alternatives.

```text
AI MATCH != SILENT IDENTITY FACT
```

No living-practitioner profile registry was created by this pass.

## Assertion boundary

Opaque assertion IDs use:

```text
thr:assertion:<UUID>
```

The first registry carries only three already-earned examples:

- Camp Fire -> creator attribution to Winslow Homer as a Met-source-reported attribution/reconciliation, not independent observation of the 1880 creation event;
- sieve/riddle practice -> `critically endangered` as a Heritage Crafts source-reported status, not independent THR census;
- flak claim -> `unsupported_in_sources_checked` for the current bounded record, with historical truth remaining unknown.

```text
ENTITY != ASSERTION
ASSERTION != TRUTH
SOURCE STATEMENT != THR ENDORSEMENT
CURRENT RECORD FINDING != PERMANENT WORLD FACT
SAME NUMBER != SAME CLAIM
```

Identity merge/split does not automatically move every assertion. Evidence and scope must be re-evaluated.

## Source / preservation boundary

Opaque working IDs:

```text
thr:source:<UUID>
thr:observation:<UUID>
```

A source can have multiple locators and observations over time.

```text
URL != SOURCE
SOURCE != OBSERVATION
OBSERVATION != PRESERVED COPY
PRESERVED COPY != TRUTH
SOURCE_LINK != SOURCE_PRESERVED
FAILED FETCH != SOURCE GONE
```

The current source registry makes preservation debt explicit. Most web sources begin:

```text
not_yet_checked
```

The Homer image records only the relationship actually observed: a byte-identical PSFH copy at the recorded time. During review, an overbroad `local_copy_legitimate` label was narrowed to `related_copy_observed`.

The NARA finding-aid route is recorded as:

```text
institutional_preservation_route_identified
```

not as proof that the current web page is preserved or that every relevant archival report was examined.

## Stronger-owner interoperability

THR should interoperate rather than recreate mature preservation infrastructure. The working source model explicitly points toward:

- institutional / national web archives;
- citation-preservation services such as Perma-style archives;
- Memento / RFC 7089 datetime-based access to prior web states;
- Software Heritage / SWHIDs for source code;
- libraries, museums, archives and domain repositories;
- legitimate local copies only where rights/authority permit.

No external archive submission, institutional contact, account creation, spend or credential action was performed by PR #13.

```text
AT RISK != FREE TO COPY
PUBLICLY ACCESSIBLE != UNLIMITED REPUBLICATION RIGHT
PRESERVATION != EXTRACTION
```

## Human gift / generated-view direction

The scale layer is beneath the human gift, not a new project purpose.

`records/architecture.html` explains the identity/source problem to ordinary readers. `records/catalog.json` exposes the models and registries to machines.

Existing human record pages remain pinned to the exact Markdown/JSON source blobs they summarize.

```text
DERIVED_VIEW != CURRENT_RECORD_UNLESS_BASIS_MATCHES
HUMAN_VIEW != NEW_EVIDENCE
SUMMARY != SOURCE
```

As scale grows, more human pages may be generated from structured record state, but the public semantics and durable IDs should survive storage/backend changes.

```text
STORAGE_BACKEND != RECORD_MEANING
```

## Automated integrity

PR #13 introduced `tools/validate_integrity.py` and a GitHub Actions validator.

It checks:

- record catalogue IDs and local routes;
- exact human-view source-blob pins;
- opaque entity/source/observation/assertion ID shape and uniqueness;
- source-relation targets;
- assertion entity/source/observation references;
- registry-to-record references.

The exact PR head passed before merge and the exact main merge head passed after merge.

```text
STRUCTURAL PASS != HISTORICAL TRUTH
HASH != TRUTH
```

## Governance / evidence boundary

- existing three evidence records unchanged;
- no record 4;
- registries index evidence and do not upgrade it;
- no stewardship acceptance or community ownership claim;
- no licence/crawler-policy change;
- no consequential institutional contact;
- no private/sensitive identity collection added;
- no claim that THR is a universal ontology, global identity provider or archival authority.

## Next edge

```text
OBSERVE / CORRECT THE SCALE LAYER
-> USE IT ON REAL REPEATED-IDENTITY / SOURCE-CURRENTNESS LOAD
-> RETURN TO RECORD QUARRY ONLY WHEN A DISTINCT GAP EARNS IT
-> BUILD OR ROUTE / STOP
```

Do not build a million-record database by imagination.

The architectural achievement here is smaller and more durable: stop making assumptions today that would make honest scale impossible later.

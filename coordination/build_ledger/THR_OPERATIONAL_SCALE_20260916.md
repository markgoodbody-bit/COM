# THR operational scale — 16 September 2026

Status: **MERGED SOURCE / BOUNDED PRODUCT-ARCHITECTURE RECEIPT / NOT CANON / NOT STEWARDSHIP ACCEPTANCE**

Direct Mark direction remains: The Human Record is collaboratively AI-built and intended as a gift for humans. Product quality may continue without waiting for third-party participation; stewardship remains separately offered to 1F916 and not accepted.

## Current Human Record source

`markgoodbody-bit/human-record` main after PR #16:

`d4f69aa56f664f0ec494d06dacb4f1a7936faea7`

Exact PR head integrity workflow: **PASS**.

Exact merged-main integrity workflow: **PASS**.

Exact merged-main Pages build and deployment: **SUCCESS**.

These workflow receipts do not establish a fresh independent HTTP byte readback of every public route.

Existing evidence records remain three and were not changed by this pass.

## Why this pass was earned

PR #13 established the bounded scale model:

```text
MENTION -> ENTITY CANDIDATE(S)
SOURCE LOCATOR -> TIMED OBSERVATION -> PRESERVATION ROUTE
ASSERTION -> EVIDENCE + SOURCE ANCESTRY + SCOPE
RECORD STATE -> HUMAN VIEW + MACHINE VIEW
```

The next defect was operational rather than conceptual:

- mentions were defined but had no first-class stored objects;
- source preservation/currentness state existed, but routine rechecks had no durable ledger distinct from evidence observations;
- validator hardening was needed before more operational state was added.

PR #14 was therefore merged first. It made the shared structural validator fail closed on malformed JSON roots, incomplete source pins and stale/missing human-view basis labels, with regression coverage.

PR #16 then added the operational layer below.

## First-class mentions

New file:

`registry/mentions.json`

It carries source-literal mentions separately from persistent entities.

Current examples deliberately demonstrate two different outcomes:

1. `Winslow Homer` in the Met owner-source observation resolves to the existing THR Winslow Homer entity on the bounded basis already carried by the Camp Fire record.
2. `Mike Turnock` in the Guardian craft source remains `unresolved_not_required` with no candidate entity profile, because the current record does not need cross-record living-person resolution.

```text
NAME != ENTITY
MENTION != ENTITY
MENTION EXISTS != ENTITY PROFILE REQUIRED
PUBLIC NAME != ENDORSEMENT
AI MATCH != SILENT IDENTITY FACT
IDENTITY RESOLUTION != IDENTITY CERTAINTY
BETTER MATCHING != MORE SURVEILLANCE
```

This is an important scale boundary: the ability to reconcile a public name does not create a mandate to profile the person.

## Source-check ledger

New file:

`registry/source-checks.json`

It is an append-only operational ledger for source/currentness and preservation-route checks.

```text
SOURCE CHECK != RECORD EVIDENCE
CHECK RECEIPT != PRESERVATION ACTION
```

A maintenance check only changes a record's evidence state if it is explicitly promoted into an evidence observation with its own bounded basis.

The first three checks cover:

- the Guardian sieve/riddle feature;
- the Heritage Crafts current sieve/riddle page;
- the World War Wings flak article.

The available Framework public retrieval surface returned expected content for all three, but it reported cached crawl ages rather than fresh origin-server responses. A direct live-origin HTTP state was not established from this aperture.

The receipts therefore say:

```text
outcome = retrieval_surface_content_available
live_http_state = not_established
```

not:

```text
live_locator_retrieved
```

No comparable byte fingerprints were produced by that retrieval route; no unchanged-content claim is made; no preservation lookup or submission was performed.

Preserve:

```text
RETRIEVAL SURFACE != LIVE ORIGIN
CACHED CONTENT AVAILABLE != LIVE TODAY
LIVE TODAY != PRESERVED
RETRIEVED AGAIN != UNCHANGED
NO COMPARABLE DIGEST != CONTENT MATCH
FAILED CHECK != SOURCE NEVER EXISTED
```

The first draft of this pass used stronger `live_locator_retrieved` wording. Review caught that the retrieval surface may be cached, so the claim was narrowed before PR #16 merge. That correction is part of the architectural evidence: operational maintenance itself must carry provenance.

## Operational validation

New:

- `tools/validate_operational.py`
- `tools/test_validate_operational.py`

CI now runs both the structural scale validator and the operational validator.

The operational validator checks:

- opaque mention/source-check ID shape and uniqueness;
- mention -> source / observation / record references;
- mention candidate -> entity references;
- coherent resolved/unresolved state;
- source check -> source references;
- evidence-promotion boundary;
- discovery routes for the two new registries.

```text
STRUCTURAL PASS != IDENTITY TRUTH
STRUCTURAL PASS != SOURCE UNCHANGED
STRUCTURAL PASS != PRESERVATION
```

## Human gift

`records/architecture.html` now explains the operational layer in ordinary language:

- a name appearing in a source does not require an entity profile;
- a retrieval surface showing cached content does not prove a live site;
- maintenance checks stay separate from evidence observations;
- source-currentness history can remain inspectable as THR scales.

`records/catalog.json` exposes:

- `mention_registry`
- `source_check_registry`

alongside existing entity/source/assertion registries.

## PR hygiene

PR #12, an older standalone view-basis checker, was closed as superseded after the shared validator absorbed its substantive source-pin and HTML basis checks through PR #14. Its optional-root standalone CLI behavior was deliberately not ported; no full-parity claim was made.

## Governance / evidence boundary

- no existing evidence record changed;
- no record 4;
- no new living-person entity profile for Mike Turnock;
- no archive submission;
- no institutional contact;
- no preservation copy created;
- no licence, crawler-policy or stewardship change;
- no claim that cached retrieval establishes live-origin state;
- no claim that THR is a universal identity or archival authority.

## Current scale stack

```text
SOURCE-LITERAL MENTION
-> ZERO / ONE / MANY ENTITY CANDIDATES
-> RESOLVED OR HONESTLY UNRESOLVED

SOURCE ID
-> LOCATOR(S)
-> EVIDENCE OBSERVATION(S)
-> OPERATIONAL SOURCE CHECK(S)
-> PRESERVATION STATE / ROUTE

ASSERTION
-> EVIDENCE + SOURCE ANCESTRY + SCOPE

RECORD STATE
-> HUMAN VIEW + MACHINE VIEW
```

The next useful work is not a larger ontology. It is to keep pressure-testing this stack against real identity collisions, changing sources, preservation debt and generated-view load while retaining the ability to stop or route outward.

```text
COMPREHENSIVE PURPOSE != COLLECT EVERYTHING NOW
OWNER_FOUND + NO CONSEQUENTIAL GAP -> ROUTE / STOP
STORAGE BACKEND != RECORD MEANING
```

# COM Attention Marker v0

Status: **NON-CANONICAL / COORDINATION FORMAT / NO SCHEDULER / NO ACTUATION**  
Date: 2026-09-03

## Purpose

Lazy Temporal Attention in Campfire should not maintain a second project-state ledger. Time-relevant relationships should carry their clocks in the coordination source that already owns the relationship.

For COM issue comments, v0 uses one strict line:

```text
ATTENTION/1 {"schema":"com-attention-marker-v0",...}
```

The JSON after `ATTENTION/1 ` is the complete machine-readable marker. Text elsewhere in the comment is not part of the marker and cannot authorize or modify it.

## Marker

```json
{
  "schema": "com-attention-marker-v0",
  "relationship_id": "review-pr88-current-head",
  "recorded_at": "2026-09-03T10:30:00Z",
  "kind": "REVIEW_RETURN",
  "status": "OPEN",
  "opened_at": "2026-09-03T10:07:00Z",
  "expected_by": null,
  "reconsider_at": "2026-09-03T23:00:00Z",
  "hardens_at": null,
  "minimum_scale": "RELATIONAL",
  "subject_type": "PROJECT_PULL_REQUEST",
  "subject_hash": "<64 lowercase hex>"
}
```

Closed vocabularies:

- status: `OPEN | CLOSED | RESOLVED | RETIRED`;
- minimum scale: `LOCAL | RELATIONAL | SYSTEMIC | HORIZON`;
- subject type v0: `PROJECT_PULL_REQUEST | COM_THREAD | PROJECT_REPOSITORY | OTHER_DECLARED`.

All timestamps are absolute ISO-8601 with timezone. `expected_by`, `reconsider_at` and `hardens_at` may be null but, when present, may not precede `opened_at`.

`subject_hash` identifies the subject coordinate without copying URLs, titles, bodies or source content into the temporal projection.

## Update semantics

Markers are append-only coordination observations.

A later marker with the same `relationship_id` and a later `recorded_at` supersedes the earlier marker for current projection. It does not erase history.

Equal `recorded_at` values for one relationship are ambiguous and must refuse rather than guess which marker is current.

A closing marker keeps the same `relationship_id`, sets `status` to `CLOSED | RESOLVED | RETIRED`, and preserves the original `opened_at`.

```text
LATEST_MARKER_FOR_RELATIONSHIP = CURRENT_COM_COORDINATION_STATE
OLDER_MARKER != DELETED_HISTORY
```

## Clock ownership

Campfire may evaluate an explicit clock. It may not invent one.

Therefore:

- no `reconsider_at` in COM -> no time-derived reconsideration from Campfire;
- a project-wide cadence may be used only when the relationship explicitly adopts that cadence;
- `expected_by` means the coordination relationship expected a response/event by that clock; elapsed time does not prove what happened outside the source;
- `hardens_at` must be supplied by the relationship owner/source, not guessed by the projection.

```text
CLOCK_MISSING != CLOCK_ASSUMED
ELAPSED_EXPECTATION != PROOF_OF_WORLD_EVENT
```

## Authority boundary

An attention marker is an orientation record only.

It cannot:

- grant permission;
- authorize external contact or publication;
- authorize spend or credentials;
- change release/canon/licence state;
- prove that its subject is still live/current outside COM;
- create standing, consent or mandate;
- trigger actuation by itself.

## Falsifiers

Repair/delete this format if:

- users have to duplicate substantive PR/issue state inside the marker;
- clocks are routinely invented merely to make the attention system active;
- latest-marker selection can silently choose between contradictory states;
- marker text starts becoming a generic project ledger;
- attention markers become an authorization channel;
- maintaining markers costs more human effort than the temporal attention they provide.

## Next gate

Build one strict parser/projection adapter in Campfire, then use at least one real COM marker. Measure whether the marker adds useful temporal orientation without becoming another manual state-carrying burden.

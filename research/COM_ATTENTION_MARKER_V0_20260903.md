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

Unknown marker properties are invalid in v0. Human-readable outcome/evidence text belongs elsewhere in the COM comment or linked source, not inside the temporal marker.

## Update semantics

Markers are append-only coordination observations.

A later marker with the same `relationship_id` and a later `recorded_at` supersedes the earlier marker for current projection. It does not erase history.

Equal `recorded_at` values for one relationship are ambiguous and must refuse rather than guess which marker is current.

A closing marker keeps the same `relationship_id`, sets `status` to `CLOSED | RESOLVED | RETIRED`, and preserves the original `opened_at`.

```text
LATEST_MARKER_FOR_RELATIONSHIP = CURRENT_COM_COORDINATION_STATE
OLDER_MARKER != DELETED_HISTORY
```

### Malformed historical marker recovery

Append-only history must be correctable without pretending an invalid record disappeared.

If an `ATTENTION/1` line is valid JSON and still has a usable v0 relationship envelope — a canonical `relationship_id` plus an absolute valid `recorded_at` — but the rest of that marker is invalid, then:

- if it is the latest marker for that relationship, current projection **must refuse**;
- a later fully valid strict marker with the same relationship id and a later `recorded_at` may restore current projection;
- the invalid superseded marker remains historical residue and the reader should surface a bounded warning such as `SUPERSEDED_INVALID_MARKER`;
- the reader must not copy or reinterpret the invalid extra fields as part of current state.

Invalid JSON, or a purported marker without enough valid envelope information to identify the relationship and ordering, cannot be safely quarantined and must fail the source slice rather than be silently skipped.

```text
CORRECTED_CURRENT_STATE != ERASED_INVALID_HISTORY
MALFORMED_CURRENT_MARKER -> REFUSE
MALFORMED_SUPERSEDED_MARKER -> WARN + USE_LATER_VALID_STATE
```

This recovery rule exists because the real first lifecycle test produced an invalid closing marker with extra human-readable `resolution` / `evidence` properties. Campfire correctly refused it. A later strict closing marker repaired current coordination without deleting the malformed historical row.

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
- malformed historical markers can either permanently poison a corrected relationship or be silently erased without residue;
- marker text starts becoming a generic project ledger;
- attention markers become an authorization channel;
- maintaining markers costs more human effort than the temporal attention they provide.

## Next gate

The strict Campfire adapter and the first real COM marker now exist. The next gate is lifecycle use: OPEN -> due/recheck -> CLOSED/corrected, including malformed historical residue, while measuring whether source-owned markers reduce rather than relocate human state-carrying burden.

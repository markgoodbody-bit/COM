# COMSYNC retrieval-completeness diagnostic — 2026-08-17

Status: working diagnostic / protocol-repair candidate. Not canon, not validation.

## Incident

On COM issue #36, CC ran a COMSYNC sweep using GitHub issue comments with `per_page=100` and no pagination, then treated the tail of that first page as the tail of the issue. The issue contained 194 comments at the time of CC's diagnosis; the R26 review request addressed to CC was on the unseen second page. CC twice reported that no new content/task was present.

The carrier had accepted the message. The aperture's retrieval was partial.

```text
DELIVERED_TO_CARRIER != RETRIEVED_COMPLETE_BY_APERTURE
RETRIEVAL_RETURNED    != RETRIEVAL_COMPLETE
```

This is a route/retrieval failure, not evidence that the sender failed to send or that transport automation would have repaired the reader.

## Existing COM support and exact gap

`COM_CORE.md` already states that a route may truncate independently of intent and that non-observation must be bounded to the observer's vantage.

`COM_PROTOCOL_WORKING.md` already states:

- successful retrieval of one file does not prove exhaustive inspection;
- `task: NONE` requires sufficiently anchored state showing no addressed task;
- when synchronization cannot establish whether an addressed task exists, use `task: NOT_ESTABLISHED`.

The missing operational rule is explicit **retrieval-completeness evidence before a negative COMSYNC conclusion** on a paginated or otherwise bounded work surface.

## Candidate protocol delta

Any COMSYNC operation that may conclude `NONE`, `IDLE`, `QUIET`, `NO NEW TASK`, `LATEST`, `NO RETURN`, or equivalent absence must first establish completeness for the search surface on which that absence depends.

For a paginated route, the retrieval witness should preserve, where the route exposes them:

```text
retrieval_complete: true | false | UNKNOWN
returned_count: <integer | UNKNOWN>
known_total: <integer | UNKNOWN>
pages_fetched: <integer | UNKNOWN>
has_more: false | true | UNKNOWN
latest_observed_object_id: <id | UNKNOWN>
retrieval_anchor: <route/object/state anchor>
```

Rules:

1. Exhaust pagination, or set `retrieval_complete: false/UNKNOWN`.
2. A partial page may support a positive observation (for example, "comment X was observed") but may not support a negative conclusion about the complete route.
3. On a named issue or collection, compare returned count/high-water metadata with route-level totals when available. Contradiction means `DEGRADED`, not `NONE`.
4. Addressed-task discovery scans the complete retrieved set or returns `task: NOT_ESTABLISHED`.
5. `task: NONE` is valid only when the relevant addressed search surface is complete enough for that claim.
6. Carrier availability, retrieval completeness, semantic read, and acknowledgement remain separate states.
7. Retrieval completion never implies cursor acknowledgement or semantic assent.
8. A tool or connector advertising "all pages" is a capability claim; the COMSYNC return should still expose the completeness evidence actually observed.

## Minimal COMS return extension

When task discovery depends on a paginated or bounded route, add only the fields needed to make the negative result auditable:

```text
COMS
state_seen: <anchor>
freshness: <state>
retrieval_complete: true | false | UNKNOWN
retrieval_scope: <route / issue / collection>
retrieval_count: <returned / known-total where available>
role: <role>
session: <session>
task: <task_id | NONE | NOT_ESTABLISHED>
action: <action / bounded stop>
```

This is not a new COM primitive. It is route/witness evidence required to support an absence claim.

## Acceptance tests

### A — exact incident

Given 194 issue comments and a client that retrieves only page 1 (`100` comments):

```text
retrieval_complete = false
returned_count = 100
known_total = 194
task = NOT_ESTABLISHED
```

`task: NONE` must be refused.

### B — exhausted pagination

Given the same issue and two pages yielding 194 distinct comments with route metadata agreeing on total count:

```text
retrieval_complete = true
returned_count = 194
known_total = 194
has_more = false
```

A complete addressed scan may return `task: NONE` if no addressed task is present.

### C — positive result from partial retrieval

If page 1 contains a task explicitly addressed to the aperture, that task may be reported as observed even while retrieval remains incomplete. The aperture must not additionally claim that no other addressed task exists.

### D — contradictory route metadata

If pagination reports exhaustion but issue metadata says more comments exist than were returned:

```text
freshness = DEGRADED
retrieval_complete = false
```

Do not perform state-dependent mutation from the purported complete projection.

### E — connector abstraction

If a connector claims to fetch all pages but returns no explicit total/completeness signal, report the strongest evidence actually available. Do not infer completeness solely from successful tool execution.

## Relation to R26-A

This repair is a prerequisite, not a justification, for automating Campfire read transport.

R26-A should not push semantic bodies into an aperture. Its intended shape is:

```text
pointer/high-water signal -> aperture requests bounded object -> bounded object returned
```

The same rule applies there: an exported bounded THREAD may truthfully say it omitted comments; an incomplete thread cannot masquerade as the complete referent.

## Evidence pointers

- COM #36 CC review: issue comment `5316935088`.
- COM #36 FW response: issue comment `5316951109`.
- Live COM protocol basis inspected from `main` at commit `dccf5efaa4eabf7a51468cdff7c416249338c9c3`.

## Limit

This diagnostic specifies the protocol-level invariant. CC reports that it separately patched its local COMSYNC skill to paginate; that implementation was not independently inspected here and is not upgraded to protocol proof by this document.

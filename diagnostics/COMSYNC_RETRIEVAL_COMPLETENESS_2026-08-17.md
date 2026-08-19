# COMSYNC retrieval-completeness diagnostic — 2026-08-17

Status: working diagnostic / protocol-repair candidate. Not canon, not validation.

## Incident

On COM issue #36, CC ran a COMSYNC sweep using GitHub issue comments with `per_page=100` and no pagination, then treated the tail of that first page as the tail of the issue. The issue contained 194 comments at the time of CC's diagnosis; the R26 review request addressed to CC was on the unseen second page. CC twice reported that no new content/task was present.

The carrier had accepted the message. The aperture's retrieval was partial.

```text
DELIVERED_TO_CARRIER != RETRIEVED_COMPLETE_BY_APERTURE
RETRIEVAL_RETURNED    != RETRIEVAL_COMPLETE
RETRIEVAL_COMPLETE    != RETRIEVAL_RECENT
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
known_total_before: <integer | UNKNOWN>
known_total_after: <integer | UNKNOWN>
pages_fetched: <integer | UNKNOWN>
has_more: false | true | UNKNOWN
route_order: oldest_first | newest_first | UNKNOWN
latest_observed_object_id: <id | UNKNOWN>
retrieval_anchor: <bounded route observation basis>
```

For GitHub issue comments specifically, `known_total_before` / `known_total_after` come from the issue object:

```text
GET /repos/{owner}/{repo}/issues/{n} -> .comments
```

They are not supplied by the comments collection itself.

Rules:

1. Exhaust pagination, or set `retrieval_complete: false/UNKNOWN`.
2. A partial page may support a positive observation (for example, "comment X was observed") but may not support a negative conclusion about the complete route.
3. On a mutable named issue, sample the route-level total before and after the paginated walk when available. Compare directionally rather than treating every mismatch as the same failure:
   - `returned_count < known_total_after` => incomplete; refuse negative conclusions;
   - `returned_count == known_total_after` with exhausted pagination and no duplicate/conflict evidence => complete at that bounded observation, even if `returned_count > known_total_before` because arrivals were included during the walk;
   - `returned_count > known_total_after` => concurrent deletion/route drift or other contradiction; report `DEGRADED`, not `NONE`.
4. If the route exposes only one total, `returned_count < known_total` is an incompleteness signal. `returned_count > known_total` can be benign arrivals during the walk and must not be collapsed into the same defect class.
5. Addressed-task discovery scans the complete retrieved set or returns `task: NOT_ESTABLISHED`.
6. `task: NONE` is valid only when the relevant addressed search surface is complete enough for that claim.
7. Record route ordering where it materially affects discovery. GitHub issue comments are oldest-first; page-one sampling is therefore systematically stale for new-task discovery and must not be treated as a cheap proxy for recent work.
8. Carrier availability, retrieval completeness, recency, semantic read, and acknowledgement remain separate states.
9. Retrieval completion never implies cursor acknowledgement or semantic assent.
10. A tool or connector advertising "all pages" is a capability claim; the COMSYNC return should still expose the completeness evidence actually observed.
11. `retrieval_anchor` is not decorative: it names the bounded route observation that supports the completeness claim, such as issue identity plus before/after comment totals and latest observed object id. It is not an immutable freshness proof unless the route supplies one.

## Minimal COMS return extension

When task discovery depends on a paginated or bounded route, add only the fields needed to make the negative result auditable:

```text
COMS
state_seen: <anchor>
freshness: <state>
retrieval_complete: true | false | UNKNOWN
retrieval_scope: <route / issue / collection>
retrieval_count: <returned / known-total-after where available>
route_order: <oldest_first | newest_first | UNKNOWN>
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
known_total_after = 194
route_order = oldest_first
task = NOT_ESTABLISHED
```

`task: NONE` must be refused.

### B — exhausted stable pagination

Given the same issue and two pages yielding 194 distinct comments with the post-walk issue object still reporting 194:

```text
retrieval_complete = true
returned_count = 194
known_total_after = 194
has_more = false
```

A complete addressed scan may return `task: NONE` if no addressed task is present.

### C — arrivals during the walk

Given `known_total_before = 197`, then new comments arrive while pages are being fetched, and the exhausted walk plus post-walk issue object both yield 198:

```text
returned_count = 198
known_total_before = 197
known_total_after = 198
retrieval_complete = true
```

The increase is not `DEGRADED`; the new arrival was included.

### D — positive result from partial retrieval

If a partial page contains a task explicitly addressed to the aperture, that task may be reported as observed even while retrieval remains incomplete. The aperture must not additionally claim that no other addressed task exists.

On an oldest-first route, this test does **not** endorse page-one sampling as a recent-task discovery strategy.

### E — truncated walk

If pagination reports exhaustion but the post-walk issue object says more comments exist than were returned:

```text
returned_count < known_total_after
retrieval_complete = false
task = NOT_ESTABLISHED
```

Do not perform a negative task conclusion from the purported complete projection.

### F — destructive drift / contradictory route state

If `returned_count > known_total_after`, the walk contains objects no longer reflected by the route total or another route contradiction occurred:

```text
freshness = DEGRADED
retrieval_complete = false
```

Do not silently reinterpret this as benign arrival.

### G — connector abstraction

If a connector claims to fetch all pages but returns no explicit total/completeness signal, report the strongest evidence actually available. Do not infer completeness solely from successful tool execution.

## Relation to R26-A

This repair is a prerequisite, not a justification, for automating Campfire read transport.

R26-A should not push semantic bodies into an aperture. Its intended shape is:

```text
pointer/high-water signal -> aperture requests bounded object -> bounded object returned
```

The same rule applies there: an exported bounded THREAD may truthfully say it omitted comments; an incomplete thread cannot masquerade as the complete referent.

R26-A's private machine lane is quieter than COM #36 and uses a stricter before-count / complete walk / after-count stability check before advancing its local request high-water. That implementation choice is deliberately stronger than the minimum COMSYNC absence rule.

## Evidence pointers

- COM #36 CC original R26 review: issue comment `5316935088`.
- COM #36 FW response: issue comment `5316951109`.
- COM #36 CC completeness-contract review: issue comment `5317113064`.
- Live COM protocol basis inspected from `main` at commit `dccf5efaa4eabf7a51468cdff7c416249338c9c3`.

## Limit

This diagnostic specifies a protocol-level invariant and acceptance shape. CC reports a local COMSYNC skill patch, but its own review found that patch did not yet distinguish count-direction drift. Neither the local patch nor this document is upgraded to protocol proof merely by existing.
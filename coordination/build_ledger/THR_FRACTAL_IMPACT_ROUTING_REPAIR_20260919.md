# THR fractal RFC — executable impact routing / independent code repair

Date: 19 September 2026 — Europe/London

Status: CURRENT RFC IMPLEMENTATION RECEIPT / NOT CANON / PUBLIC THR UNCHANGED

## Exact branch state

THR draft PR #52:
- head: `cea984dca9ff4b79e5cad8409272cdf46b7798ec`
- state: DRAFT / OPEN / MERGEABLE
- hosted integrity: run 155 / `35467028963` SUCCESS

Public THR:
- main: `1f5a5919938f385f43f1e2383bdfbb52807b206e`
- public records: exactly 4
- registry semantics: unchanged
- record 5: not earned

## Independent registry audit

Codex comment `5744972035` checked:
- all 20 registered sources;
- all 8 registered assertions;
- assertion record_links;
- all four catalogue records.

Result:
- no current multi-record source found;
- Polybius source correctly reaches four assertions / one Hannibal record;
- **11 of 20 registered sources have no assertion evidence edge but do have direct used_by_records routes**.

Therefore:

```text
SOURCE IMPACT ROUTING
=
DIRECT source.used_by_records
UNION
ASSERTION-DERIVED record routes

NO ASSERTION EDGE
!=
NO RECORD DEPENDENCY
```

Do not repair this by manufacturing assertions for every source.

## Small executable safeguard

RFC branch adds:
- `tools/impact_routes.py`
- `tools/test_validate_impact_routes.py`

The helper is read-only. For one registered source it derives:
- direct used_by_records;
- assertion-derived record routes;
- their union as affected review candidates;
- unresolved direct record IDs;
- unresolved assertion record links.

Ceilings include:

```text
AFFECTED_RECORD != FALSE_RECORD
REVIEW_ROUTE != CORRECTION
NO_ASSERTION_EDGE != NO_RECORD_DEPENDENCY
ROUTE_DERIVED != COMPLETE_DEPENDENCY_PROOF
REGISTERED_SOURCE_QUERY != ALL_RECORD_LOCAL_DEPENDENCIES
```

This is a derived query, not a new stored dependency type.

## Independent code audit

Codex comment `5745004069` audited the first helper implementation and returned:

`REPAIR`

Four concrete counterexamples:

1. **Foreign-origin false positive**
   - unrelated.example/cases/b.json could falsely resolve to thehumanrecord.net/cases/b.json.

2. **Ambiguous catalogue path**
   - duplicate record ownership of one path silently selected the later record.

3. **Malformed route container**
   - malformed used_by_records could become apparent emptiness.

4. **Query/fragment inconsistency**
   - relative and absolute fragment-bearing paths behaved differently.

Codex explicitly said:
- the direct-plus-assertion union is the correct bounded operation;
- output ceilings do not repair false routing;
- no new dependency registry is needed.

## Repair

Current helper now:
- accepts absolute record routes only from exact canonical origin `https://thehumanrecord.net`;
- rejects credentials, explicit ports, foreign origins and wrong schemes;
- rejects query/fragment-bearing record routes instead of stripping identity-bearing components;
- rejects ambiguous catalogue path ownership across records;
- permits repeated same-record path ownership;
- fails loudly on malformed present used_by_records / record_links containers or items;
- keeps unknown-but-well-formed targets visible as unresolved.

Focused suite now has 15 tests covering:
- direct-only route;
- unresolved direct target;
- malformed direct route;
- assertion-added route;
- union deduplication;
- assertion-only route;
- unresolved assertion route;
- malformed assertion route;
- unknown source;
- canonical public URL / repo path equivalence;
- foreign origin rejection;
- credentials / explicit port / wrong scheme rejection;
- query/fragment consistency;
- ambiguous catalogue path rejection;
- same-record duplicate path acceptance.

Hosted:
`Validate Human Record integrity — run 155 / 35467028963 — SUCCESS`

Green CI != semantic validation.

Repair verification requested in PR #52 comment:
`5745019308`

Current response state:
PENDING.

## Record-local dependency ceiling

Direct comparison of the four current machine records with the source registry found that
the source registry is intentionally not the complete evidence universe.

Concrete example:

`cases/sieve-riddle-revival.json`

contains local evidence node:
`homo-faber-overthrow-interview`

URL:
`https://2022.homofaber.com/en/discover/discover-steve-overthrow`

The published interview supports the bounded record finding that Steve Overthrow reports
learning partly from Mike Turnock.

It is not currently a shared `thr:source:<uuid>` object.

Therefore:

```text
REGISTERED SOURCE
-> impact_routes query available

RECORD-LOCAL SOURCE WITHOUT SHARED ID
-> not addressable by source_id query
-> local review route still exists

NOT IN SOURCE REGISTRY
!= NOT EVIDENCE

NOT QUERYABLE BY source_id
!= NO DEPENDENCY
```

Generic URL scraping is not the answer because current records also contain URLs for:
- correction/challenge receipts;
- build/review receipts;
- contribution routes;
- other non-evidence surfaces.

```text
URL OCCURS IN RECORD
!= SOURCE DEPENDENCY
```

If future operational currentness/review need becomes material, either:
- promote the local source to the already-existing source registry; or
- use a record-type-specific adapter.

Neither currently earns a new global type.

## Source ancestry check

Current source registry:
- 20 sources;
- 13 registered relation edges.

No current relation produces a genuine cross-public-record fan-out.

One ANZAC source has a `quotes` relation to an unregistered target label
(Martin Middlebrook, The Berlin Raids) with `target_source_id: null`.
That is an explicit unresolved/local target, not a demonstrated malformed registry ID.

Current ceiling remains:

```text
INTRA-RECORD REGISTERED FAN-OUT = TESTED
MULTI-RECORD SOURCE FAN-OUT = NOT YET PRESENT / NOT TESTED
ALL RECORD-LOCAL DEPENDENCIES = NOT GENERICALLY ROUTABLE
```

## Architecture result

```text
NEW SHARED DEPENDENCY TYPE = NOT EARNED
GENERIC CORRECTION-PROPAGATION TYPE = NOT EARNED

DERIVED REGISTERED-SOURCE IMPACT QUERY = EARNED

RECORD-LOCAL ADAPTER / SOURCE PROMOTION
= ONLY WHEN REAL OPERATIONAL PRESSURE EARNS IT
```

Universal THR record/knowledge protocol remains not earned.
Bounded task-specific exchange contracts remain allowed where real handoff loss earns them.

## Next

Wait for bounded repair verification on comment `5745019308`.

If PASS_WITH_CEILINGS:
- checkpoint helper as RFC evidence;
- stop helper churn;
- return to real multi-record fan-out / real field pressure.

If REPAIR:
- fix only the smallest demonstrated counterexample;
- rerun focused tests + hosted integrity.

Do not:
- globalise every local source;
- create a dependency registry;
- create record 5;
- merge/canon PR #52 without explicit release decision.

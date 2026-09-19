# THR fractal RFC — impact-routing smoke pass / verifier hold

Date: 19 September 2026 — Europe/London

Status: CURRENT FOLLOW-ON RECEIPT / NOT CANON / PUBLIC THR UNCHANGED

## Exact state

THR draft PR #52:
- head `d5621c7e701825bfd743b823aa1c97b352dec7cb`
- DRAFT / OPEN / MERGEABLE
- hosted integrity run 157 / `35467239067` SUCCESS

Public THR:
- main `1f5a5919938f385f43f1e2383bdfbb52807b206e`
- exactly 4 public records
- registry semantics unchanged
- record 5 not earned

## Impact-routing helper

Current helper remains:

`tools/impact_routes.py`

Core operation:

```text
AFFECTED REVIEW CANDIDATES
=
DIRECT source.used_by_records
UNION
ASSERTION-DERIVED RECORD ROUTES
```

No stored dependency registry was added.

## Independent audit / repair chain

Codex:
- registry audit `5744972035` -> 20 sources / 8 assertions / 11 direct-only source routes;
- code audit `5745004069` -> REPAIR;
- demonstrated foreign-origin false match, ambiguous catalogue path, malformed-route
  apparent emptiness, query/fragment inconsistency.

Repairs are present and covered by hostile tests.

## Current test state

Focused impact-routing suite now has **17 tests**:
- 15 hostile/unit cases;
- 2 smoke tests against the actual current catalogue/registries.

The smoke tests establish that:
1. all current catalogue human/machine/full-record routes are accepted by the strict path
   policy and map to the intended record ID;
2. all current registered sources retain every valid direct `used_by_records` route in
   the affected-record result.

Hosted exact audit head:
`Validate Human Record integrity — run 157 / 35467239067 — SUCCESS`

This does not establish semantic completeness.

## Preserved ceilings

```text
REGISTERED_SOURCE_QUERY != ALL_RECORD_LOCAL_DEPENDENCIES
SOURCE REGISTRY != COMPLETE EVIDENCE UNIVERSE
URL OCCURS IN RECORD != SOURCE DEPENDENCY
ROUTE_DERIVED != COMPLETE_DEPENDENCY_PROOF
INTRA-RECORD FAN-OUT TESTED != MULTI-RECORD FAN-OUT TESTED
```

Current record-local example:
- Sieve/Riddle Homo Faber interview is consequential evidence;
- remains record-local rather than a shared source object;
- no forced promotion/globalisation by momentum.

## External gate

Repair-verification request:
PR #52 comment `5745019308`

Requested verdict:
- PASS_WITH_CEILINGS; or
- REPAIR with smallest remaining concrete counterexample.

Current response:
PENDING at this receipt.

## Stop rule

Until the verifier returns:

```text
NO MORE IMPACT-HELPER CHURN
```

unless a new concrete defect appears.

If PASS:
- keep helper as bounded RFC evidence;
- return to real field pressure / multi-record fan-out when naturally present.

If REPAIR:
- smallest demonstrated fix only;
- rerun hostile tests + current-registry smoke tests + hosted integrity.

Public main / merge / canon remain untouched.

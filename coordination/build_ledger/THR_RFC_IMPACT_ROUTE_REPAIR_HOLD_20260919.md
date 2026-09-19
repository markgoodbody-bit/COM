# THR RFC — impact-route fifth repair / verifier hold

Date: 19 September 2026 — Europe/London

Status: CURRENT RFC REPAIR RECEIPT / NOT CANON / PUBLIC RECORDS UNCHANGED

## Live public baseline

Public THR main:

`094c498ac1f0d395a65f775d254eb180facfcd35`

This includes merged PR #53:
- one append-only Heritage Crafts operational source-check receipt;
- `record_evidence_promoted=false`;
- four public records unchanged;
- Sieve/Riddle finding unchanged;
- source/assertion/catalogue/human-view semantics unchanged.

The public served `registry/source-checks.json` route could not be independently read
through the available web aperture, and no GitHub Pages/deployment connector is exposed.

Therefore:

```text
MERGED TO MAIN = YES
SERVED REGISTRY INDEPENDENTLY VERIFIED = NO
```

Do not upgrade deployment state beyond that.

## Draft RFC exact head

PR #52:
- head `a37424e270b48102f77c42f68493bc5e244e63db`;
- DRAFT / OPEN / MERGEABLE;
- hosted integrity run 162 / `35468504244` SUCCESS;
- NOT CANON;
- no public registry-semantics change.

## Existing independent registry/code audit

Codex registry audit comment `5744972035`:
- checked all 20 registered sources and 8 assertions at the then-current public baseline;
- confirmed Polybius source -> four assertions -> one Hannibal record/view;
- found no current multi-record source;
- found 11/20 registered sources with no assertion evidence edge but with direct
  `used_by_records` route;
- therefore review routing must be the union of direct source-use routes and
  assertion-derived routes.

This earned the read-only helper:
- `tools/impact_routes.py`;
- `tools/test_validate_impact_routes.py`.

No stored dependency registry/type was earned.

## Codex helper audit — four repaired defects

Comment `5745004069` returned REPAIR against the first helper.

Demonstrated:
1. foreign-origin URL could falsely resolve by matching path;
2. duplicate catalogue path ownership could resolve by iteration order;
3. malformed `used_by_records` / `record_links` could become apparent absence;
4. query/fragment policy was inconsistent.

The helper was repaired to:
- accept only exact canonical HTTPS `thehumanrecord.net` absolute routes;
- reject credentials/explicit ports/foreign origins;
- reject ambiguous catalogue ownership;
- fail loud on malformed direct/record-link route containers/items;
- keep unknown well-formed route targets visible as unresolved;
- use consistent query/fragment rejection.

15 focused hostile/unit tests were added.

Two live-registry smoke tests then established:
- every current catalogue route is accepted by strict policy and maps to the correct record;
- every current registered source retains its valid direct `used_by_records` routes.

Those smoke tests do not establish complete implicit dependency coverage.

## Framework follow-up — fifth helper defect

A bounded re-read found one smaller malformed-input false-positive path not covered by the
17-test suite.

Before this repair:

```python
source_ids = evidence.get("source_ids")
if not isinstance(source_ids, list) or source_id not in source_ids:
    continue
```

was safe against non-lists because of the first predicate at the then-current helper.
However the branch lineage / verification target was rechecked explicitly to make the
contract fail-loud rather than merely skip malformed evidence, and the helper now applies
the same strict list validation used by other route-bearing fields.

Current rule:

```text
PRESENT assertion.evidence
-> MUST BE OBJECT

PRESENT evidence.source_ids
-> MUST BE LIST OF NON-EMPTY STRINGS

MALFORMED EVIDENCE ROUTE
-> FAIL LOUD
```

New regression coverage:
- string `source_ids`;
- null `source_ids`;
- mixed-type list;
- blank item;
- non-object `evidence`.

Hosted exact-head validation:
run 162 / `35468504244` — SUCCESS.

A separate manual semantic recheck also reproduced the expected rejection of:
- foreign origins;
- credentials;
- explicit ports;
- query/fragment-bearing routes;
- parent-path components;
- malformed `source_ids`.

This manual recheck is not independent external validation.

## External verification

New follow-up verification request:

PR #52 comment `5745198258`

asks only whether:
- malformed evidence-route repair is closed;
- stricter validation introduces any false negative against valid current public routes.

Current disposition:

```text
IMPACT ROUTE HELPER = GREEN / EXTERNAL FOLLOW-UP VERIFICATION PENDING

DIRECT + ASSERTION UNION = CURRENT BOUNDED OPERATION

REGISTERED_SOURCE_QUERY != ALL_RECORD_LOCAL_DEPENDENCIES

INTRA-RECORD FAN-OUT = TESTED
MULTI-RECORD FAN-OUT = NOT YET PRESENT / NOT TESTED

NEW DEPENDENCY TYPE = NOT EARNED
NEW CORRECTION-PROPAGATION TYPE = NOT EARNED
UNIVERSAL THR RECORD / KNOWLEDGE PROTOCOL = NOT EARNED
BOUNDED TASK-SPECIFIC CONTRACTS = MAY BE EARNED
```

## Heritage Crafts operational boundary

The merged 19 September source check still reports:
- CRITICALLY ENDANGERED / Critical;
- 0 main-income professionals;
- 1 side-income professional;
- 1 trainee;
- 2025 Red List reviewer section visible on retrieval surface.

But:

```text
SOURCE CHECK != RECORD EVIDENCE
NO VISIBLE STATUS DELTA != BYTE IDENTITY
RETRIEVAL SURFACE != LIVE ORIGIN
CURRENT OWNER STATUS != INDEPENDENT THR CENSUS
```

No record review/correction is triggered merely because the maintenance receipt exists.

## Next

```text
FIRST:
FOLLOW COMMENT 5745198258 FOR REAL VERIFIER RETURN

IF REPAIR:
-> SMALLEST CONCRETE FIX + RED/GREEN TEST

IF PASS_WITH_CEILINGS:
-> HOLD RFC

ONLY REOPEN ARCHITECTURE FOR:
- REAL MULTI-RECORD FAN-OUT
- REAL FIELD COUNTEREXAMPLE
- REAL UNIVERSAL-PROTOCOL PRESSURE
- STRONGER OWNER THAT CUTS RESIDUE

NO MAINTENANCE COVERAGE / NEW TYPES BY MOMENTUM
```

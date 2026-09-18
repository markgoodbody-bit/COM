# THR production semantic repairs — 18 September 2026

Status: **PRODUCTION INTEGRATION RECEIPT / NOT TRUTH VALIDATION / NO RECORD-4 PROMOTION**

## Earned path

Hannibal/JFK research probes exposed four reusable production defects:
1. assertion evidence could name an observation owned by a different source;
2. public/default mention validation could be loosened into a misleading publication boundary;
3. a report-page observation could be upgraded from `reported_by_source` to `observed` by changing one state word;
4. `unsupported_in_sources_checked` could claim a checked aperture without proving that cited sources were actually inspected.

Sibling hostile-review PRs #32/#33 refined the last two repairs.

Framework first integrated the reviewed work on research PR #30, then extracted only reusable production files into PR #34 so Hannibal/JFK research fixtures and owner maps would not enter main by momentum.

## Production merge

PR #34:
`Harden assertion evidence states and research/public boundaries`

Exact pre-merge head:

`b8fca327d06b87c17a2e827b44bdcc5bf15fb459`

Hosted witness:
- workflow `35329512132 SUCCESS`
- job `105550339640 SUCCESS`
- structural + operational validation PASS
- production regression suite: **64 tests / OK**
- open-vocabulary warnings: **7**

Merged main:

`194012dcb8247d3cb964cfc65b5082ce67355529`

No separate merge-head workflow run had appeared at the last exact check. The verified witness is therefore the exact PR head plus conflict-free merge, not an invented post-merge CI receipt.

## Integrated behavior

- assertion evidence observations must belong to a cited source;
- public/default mention validation requires `record_id`; uncatalogued research validation is explicit isolated/in-memory mode only;
- public repository branches/fixtures are public, not private staging;
- source observations remain bounded retrieval/inspection events of source representations;
- cross-record `observed` / `reconciled` states fail closed until typed observation/reconciliation target support exists;
- the direct-evidence guard fails integrity if its model section disappears;
- `unsupported_in_sources_checked` requires a non-empty inspected source aperture;
- failed / not-retrieved / access-restricted / citation-only observations do not count as checked;
- negative/unsupported findings should expose their bounded evidence aperture without implying exhaustive search;
- four flak-source observations already substantively inspected in the existing record were corrected from legacy `referenced_by_record` metadata to scoped `partial` observations.

```text
STRUCTURAL_PASS != TRUTH
SOURCE_OBSERVATION != DIRECT_WORLD_OBSERVATION
SOURCES_CHECKED != ALL_POSSIBLE_SOURCES
DEFECT_REPAIRED != MODEL_VALIDATED
```

## Cleanup

Closed as integrated/superseded:
- PR #32 — direct assertion-state sibling repair;
- PR #33 — checked-source sibling repair;
- PR #30 — Hannibal/JFK research integration surface;
- PR #27 — early Hannibal candidate;
- PR #29 — early Hannibal candidate.

Remaining Hannibal candidate surface:
- PR #28 only.

THR still has exactly **three public records**. No catalogue/public record 4 was created.

Public hostile-review issue #31 remains open. Comment `5728047635` records that the two named false passes are repaired on main and explicitly keeps the wider break aperture open.

## Independent follow-up

Codex separately checked PR30 integrated head `ac5a329...` before production extraction: 71 tests + both validation stages passed, seven warnings remained, and no new code blocker was found. It did not independently reconstruct the original flak inspections; therefore this is corroborating implementation review, not evidence validation.

## Next THR gate

Do not add another stress specimen.

Advance only PR #28 against the new main:
- strongest-owner/source-criticism check;
- preserve surviving-source bias and source dependence;
- test against current production validators;
- hostile review;
- no catalogue promotion unless the public record is genuinely earned.

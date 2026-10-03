# 2026-10-03 — YAC admission v2 scratch transport prerequisite pass

Status: **SCRATCH TRANSPORT PREREQUISITE PASS / NOT FULL V2 / NO PRODUCTION MUTATION**

## Exact execution receipt

Mark ran `C:/Users/markg/Downloads/YAC-Scratch-Atomicity.ps1`, SHA-256 `ef5f63f69c3b614b146a9110597132aaa36a9316d8bcf75eb25941ec1e4b0139`, against scratch D1 `50e314e9-14b1-41b9-b33f-a97002dc09a6`.

Returned at COM #723 `5968698316`:

- status: `PREREQUISITE_PASS_NOT_FULL_REHEARSAL_PASS`
- stopped_at: `COMPLETE_PREREQUISITE`
- HTTP status: 200
- scratch query requests: 13
- write attempted: true, scratch only
- production requests: 0
- real content: false
- automatic retry: false
- schema SHA-256: `3d34512f9453b2ef6c3081dddaa6b9d8e9e5aa623b1c4ae1fbc1ed5d0a1174c6`
- fixture prefix: `yac_probe_6377f73cf1bb`
- fixtures retained for inspection: true
- token revoked: false; held by Mark

## Earned result

For this bounded three-table transport fixture:

1. positive item + envelope + provenance insertion passed;
2. intended CHECK failure at companion 2 rolled back without partial rows;
3. intended CHECK failure at companion 3 rolled back without partial rows;
4. injected cleanup failure preserved the pre-cleanup state;
5. successful synthetic cleanup passed its null/hash invariants.

## Explicit ceilings

- ceiling 3: `TRANSPORT_FIXTURE_PASS_FULL_V2_NOT_TESTED`;
- ceiling 4: `TRANSPORT_FIXTURE_PASS_ACTUAL_CLEANUP_WITHDRAWAL_NOT_TESTED`;
- ceiling 5: NOT_RUN;
- ceiling 6: NOT_RUN;
- ceiling 7: NOT_RUN;
- ceiling 8: NOT_RUN.

The execution receipt is Mark-supplied local evidence, not an independent Codex remote run. The earlier confirmation failure did not reproduce; invisible whitespace remains a hypothesis, not an established cause.

## Next bounded scratch target

The retained fixture now supports inspection before preparing the full-v2 migration/FK, old-writer migration-window, replay/idempotency and capacity rehearsal under the frozen design. Do not rerun the empty-database helper or erase the fixtures.

No production request/mutation, real participant/provider content, xAI carry, provider/model call, public intake, publication or THR canonical mutation occurred. Active source build remains NONE.

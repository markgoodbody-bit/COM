# EvidenceWatch — Windows CLI-test repair + cross-platform CI

Date: 26 September 2026

Status: **REPAIRED / WINDOWS + LINUX CI GREEN / RUNTIME SCORER SEMANTICS UNCHANGED**

EvidenceWatch private main **at the time of this repair**:
`b8fc0971ceace55878aa6130448850d88774f254`

This is historical receipt identity, not a present-tense main pointer.

Trigger:
Claude Code ran the merged 54-test suite on Windows and observed **53/54**.

The failing test was:
`test/pilot-score.test.mjs`

## Defect

The CLI smoke test passed:
- `script.pathname`
- `fixturePath.pathname`

from file URLs directly into `spawnSync`.

On Windows a file URL such as:

`file:///C:/Users/.../scripts/score-pilot.mjs`

has pathname:

`/C:/Users/.../scripts/score-pilot.mjs`

Passing that pathname directly to Node caused a path shaped like:

`C:\C:\Users\...\scripts\score-pilot.mjs`

and the test failed with `MODULE_NOT_FOUND`.

The scorer itself was not broken:
direct Windows execution of
`node scripts/score-pilot.mjs examples/pilot-score-fixture.json`
was reported successful before the repair.

## Repair

PR #14:
- exact reviewed head: `2596e8f3a5dc943507f52375831241171cbfa42b`;
- converts file URLs with `fileURLToPath` before spawning;
- changes EvidenceWatch CI from Linux-only to a matrix:
  - `ubuntu-latest`
  - `windows-latest`

PR exact-head workflow:
`36201937768 / SUCCESS`

Individual jobs:
- Ubuntu: SUCCESS;
- Windows: SUCCESS.

Merged main:
`b8fc0971ceace55878aa6130448850d88774f254`

Post-merge workflow:
`36202014248 / SUCCESS`

Individual post-merge jobs:
- `test (windows-latest)`: SUCCESS;
- `test (ubuntu-latest)`: SUCCESS.

Current deterministic suite:
**54 tests / 54 pass on both OS CI jobs.**

## Proposal precision correction

The Digital Science draft previously said the merged protocol/scorer:

> freeze human labels/configuration before scoring

That overstated the implementation.

Actual boundary:
- the **protocol requires** labels/configuration to be frozen before scoring;
- the scorer **consumes already-frozen inputs** and does not enforce chronology/provenance of the freeze.

Proposal wording corrected accordingly.

Current proposal count after the precision repair:
**1,451 words**

Limit:
**1,500 words**

Headroom:
**49 words**

Preserve:

```text
PROTOCOL REQUIRES FREEZE != SCORER ENFORCES FREEZE
54/54 LINUX != 54/54 WHERE OWNER RUNS
CROSS-PLATFORM TEST GREEN != PRODUCT VALIDATION
TEST-HARNESS DEFECT != SCORER SEMANTIC DEFECT
```

No:
- model call;
- network research run;
- research partner;
- form entry;
- terms acceptance;
- Digital Science submission.

# Compact continuity repair — 18 September 2026 PM

Status: **DRIFT-X100 REPAIR / CURRENTNESS COMPACTION / HISTORY PRESERVED IN GIT + BUILD LEDGER**

Trigger:
`falsification/PROJECT_DRIFT_FALSIFY_X100_20260918_PM.md`

The project-level x100 audit found that the three current continuity surfaces had become historical buses:

```text
FRAMEWORK_HEAD              865 lines / ~41.5k chars
ACTIVE_THREAD_POINTER       657 lines / ~32.1k chars
BUILD_STATUS                625 lines / ~32.8k chars
```

This reproduces a failure already identified in the 16 September AI-interest x100: mutable current state was copied across too many continuity surfaces.

## Repair rule

```text
CURRENT POINTER = COMPACT
DATED DETAIL = BUILD LEDGER
HISTORY = GIT
LIVE SOURCE > POINTER
```

The three files are replaced with bounded present-state documents rather than prepending another delta.

Nothing in historical receipts is deleted. Previous versions remain in Git history and dated build-ledger files.

## Live state at repair boundary

Pre-repair COM main:
`a6932f28f4c7057801af0b500947367faf625aa7`

Linked repository heads:
- TRACE main `e7d46398dc00ead931b0d5cae98518c1bcf304a3`;
- Mechanical Ethics main `45b4a303b5bb970a89854953a20c35dc4bc1e56c`;
- THR main `217f89c10a60f02b7d39785d531b2cb47cab7337`.

Formal baselines remain:
- TRACE v0.3.0;
- Mechanical Ethics v0.7.0.

Only open COM PR:
- #364 ATRS Answerability Audit, head `d2bea526feced78750d1bbb4c45e686f3e4c6446`.

Closed by the same drift pass:
- #345 AI-interest cycle — historical;
- #349 evidence-lineage competition build — superseded;
- #363 No Free QALY — preserved green fallback, closed unmerged.

## Operating correction

Competition priority was repaired to:

```text
WORLD / REAL USE
-> ATRS result preservation
-> Hack Apertus time-gated preparation
```

The next world quarry should deliberately counter the observed selection bias:
- non-UK where possible;
- non-public-sector where possible;
- positive construction / material capability preferred before another governance/provenance case;
- strongest-owner subtraction remains active;
- no build unless a specific consequential residue survives.

## Continuity contract after repair

`continuity/FRAMEWORK_HEAD.md`
- purpose;
- current repository/baseline identities;
- current centre;
- consequential gates;
- a handful of recent receipts.

`coordination/ACTIVE_THREAD_POINTER.md`
- active primary thread;
- dormant/time-gated secondary threads;
- stop/route conditions.

`coordination/build_ledger/BUILD_STATUS.md`
- what is actually being built now;
- recent completed work;
- held/frozen objects;
- immediate next build condition.

No historical replay belongs in those files.

```text
COMPACT_POINTER != LOSS_OF_HISTORY
HISTORY_PRESERVED != HISTORY_REPLAYED_ON_BOOT
```

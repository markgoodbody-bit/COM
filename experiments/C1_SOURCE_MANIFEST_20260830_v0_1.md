# C1 — FROZEN SOURCE MANIFEST — v0.1

Status: EXPERIMENT INPUT MANIFEST / NOT ANSWER KEY / NOT CANON
Date assembled: 2026-08-30 Europe/London
Parent protocol: `C1_CONTINUITY_TRANSFER_FIDELITY_PREREG_20260830.md`

## Purpose

Freeze the source coordinates from which C1 packets may be constructed. This file is intentionally not an answer key and should not be used as a prose substitute for the underlying sources.

The freeze is a coordinate bundle, not a claim that all mutable systems stopped at one wall-clock instant.

```text
FROZEN_COORDINATE != FROZEN_WORLD
SNAPSHOT != CURRENT_STATE_FOREVER
MANIFEST != SOURCE_CONTENT
```

## Bundle identity

```text
bundle_id: C1-FREEZE-BUNDLE-20260830-v0.1
COM continuity coordinate: e945191ba9c07e51314e1a0e7f45c4b31efc78a3
TRACE public coordinate: 46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b
Mechanical Ethics public coordinate: 44f7efb59806242fd26c572cbfbaaeaefaea2058
TRACE execution-evidence coordinate: 15c608abc4df86b319da6bd21ebb2d9079439bda
Campfire Production annotated tag object: e49b56228a706a644d5f4a8a04a1423b5fab1a6c
Campfire Production commit: 15b51dd484acc4f12dc979cc7d791e12efd6c597
```

Why COM uses `e945191...`: it is the bounded continuity coordinate after the standing inter-AI communication grant was recorded, but before C1 itself and later claim-map work could contaminate the pilot state.

## ARM F — FULL bounded source set

FULL is source-first. It does **not** receive `FRAMEWORK_HEAD.md` or `OMISSION_MAP.md` as an orientation summary by default.

### F1 — TRACE current public status/front door

Repository: `markgoodbody-bit/TRACE`

```text
commit: 46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b
path: README.md
blob SHA: 0df1a46a33eb63fa47a3cdc4a3b145115f2ccfc1
```

Direct immutable URL:
`https://github.com/markgoodbody-bit/TRACE/blob/46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b/README.md`

Use only this current front-door object unless a battery item explicitly requires historical execution detail.

### F2 — TRACE exact execution/adverse-burden evidence

Repository: `markgoodbody-bit/TRACE`

```text
commit: 15c608abc4df86b319da6bd21ebb2d9079439bda
path: PROJECT/TRACE_v0_3_0_OUTWARD_API_EXECUTION_RESULT_20260829_v0_2.md
blob SHA: cb74678b6e31a1b82fd6b4d762566fd04aba123e
```

Direct immutable URL:
`https://github.com/markgoodbody-bit/TRACE/blob/15c608abc4df86b319da6bd21ebb2d9079439bda/PROJECT/TRACE_v0_3_0_OUTWARD_API_EXECUTION_RESULT_20260829_v0_2.md`

This is included because the exact run status and quantitative burden detail are intentionally not carried in ordinary HEAD cognition.

### F3 — Mechanical Ethics current public status/front door

Repository: `markgoodbody-bit/mechanical-ethics`

```text
commit: 44f7efb59806242fd26c572cbfbaaeaefaea2058
path: README.md
blob SHA: 3bdc070a79bef1835250b81f7fb1f9c764382555
```

Direct immutable URL:
`https://github.com/markgoodbody-bit/mechanical-ethics/blob/44f7efb59806242fd26c572cbfbaaeaefaea2058/README.md`

The full reader is not required for this state-transfer battery; adding it would inflate FULL without answering a current question.

### F4 — authority / coordination record

Repository: `markgoodbody-bit/COM`

```text
commit: e945191ba9c07e51314e1a0e7f45c4b31efc78a3
path: COM_STATE.md
blob SHA: 4e6546cc76f7925eb767924d14f65b9f0322ff24
```

Direct immutable URL:
`https://github.com/markgoodbody-bit/COM/blob/e945191ba9c07e51314e1a0e7f45c4b31efc78a3/COM_STATE.md`

This record is included because the communication grant is an observed human authority update and cannot be reconstructed from public TRACE/ME source.

### F5 — Campfire Production identity

Repository: `markgoodbody-bit/campfire-relay`

```text
tag: campfire-production-v0.18.34
annotated tag object: e49b56228a706a644d5f4a8a04a1423b5fab1a6c
target commit: 15b51dd484acc4f12dc979cc7d791e12efd6c597
tag message: Campfire Relay v0.18.34 production release
```

Git tag-object API source at freeze:
`https://api.github.com/repos/markgoodbody-bit/campfire-relay/git/tags/e49b56228a706a644d5f4a8a04a1423b5fab1a6c`

### F6 — Campfire draft-lane snapshots

The following are mutable PR surfaces, so their freeze-state is explicitly captured here rather than assumed recoverable from a future live GET.

Observed during the C1 construction pass on 2026-08-30:

```text
PR #190
url: https://github.com/markgoodbody-bit/campfire-relay/pull/190
state: open
draft: true
merged: false
head: d91de8d2d1062d11c6b91d064a8e30fcc1e7798b
body self-status: DRAFT / OPEN / UNMERGED; no Production claim

PR #192
url: https://github.com/markgoodbody-bit/campfire-relay/pull/192
state: open
draft: true
merged: false
head: 667222b45b27bae475d6ddc9d42122fa45514d52
boundary in body: PREFLIGHT_NOT_AUTHORIZATION_NOT_DISPATCH_NOT_PROVIDER_CONTACT
```

These snapshots establish only the experiment freeze state. They are not assertions about future PR status.

### F7 — unanswered Mechanical Ethics research frontier snapshot

Mutable issue snapshot captured on 2026-08-30:

```text
repo: markgoodbody-bit/mechanical-ethics
issue: #44
url: https://github.com/markgoodbody-bit/mechanical-ethics/issues/44
title: Frontier question: who must preserve an option while correction is pending?
state: open
comments: 0
created_at: 2026-08-30T00:16:03Z
updated_at at capture: 2026-08-30T00:16:03Z
```

The issue body explicitly calls itself an open research question, not a ME claim.

### F8 — unanswered FPF invitation snapshot

Mutable issue snapshot captured on 2026-08-30:

```text
repo: ailev/FPF
issue: #50
url: https://github.com/ailev/FPF/issues/50
title: A question about FPF, timing and usable options
state: open
comments: 0
created_at: 2026-08-29T22:32:28Z
updated_at at capture: 2026-08-29T22:32:28Z
```

No semantic interpretation of silence is embedded in this snapshot.

## ARM C — COMPACT source set

COMPACT receives the continuity mechanism at the same pre-experiment COM coordinate:

```text
COM commit: e945191ba9c07e51314e1a0e7f45c4b31efc78a3

RELOAD.md
  blob: 4b0aef67d29b97c475afd2cae56707cfbe765e57

continuity/BOOT.md
  blob: 6b7a467bd22f466cd620efed4c64c0af9fc742ef

continuity/FRAMEWORK_HEAD.md
  blob: a4794e7bda4391cb2484c0df65546e8524ee3a08

continuity/OMISSION_MAP.md
  blob: 934a9780fb77f7eee7f4c5ad292b6b08175ddcbd

COM_STATE.md
  blob: 4e6546cc76f7925eb767924d14f65b9f0322ff24
```

COMPACT may retrieve only through declared source/evidence/omission pointers when the battery requires evidence absent from the compact surface. Every retrieval must be logged.

For the fixed negative-space probe, the expected route is available from the omission-map row `TRACE 32-call raw outputs and adjudication-route evidence`; the receiver must still locate and inspect the actual source rather than being handed the numeric answer.

## ARM S — SUMMARY generation source set

The ordinary-summary author receives the same source set F1–F8 used to construct FULL, but:

- does not receive this experiment's question battery;
- does not receive the answer key or scoring rubric;
- does not receive ARM C's HEAD/OMISSION architecture as an input to imitate;
- is asked only to make a conventional bounded project-state handoff for a fresh collaborator;
- receives a target input/output budget derived from the final measured ARM C packet size.

The resulting summary is frozen before scored receiver execution.

## Excluded from all initial packets

Unless P0 review establishes necessity, do not include:

- whole COM #56/#46/#42 histories;
- raw 32-call outputs;
- old TRACE PR #38 quarry as a whole;
- old Mechanical Ethics PR #34 quarry as a whole;
- protected Final Eight source;
- large Campfire exports;
- predecessor chat transcripts;
- C1 answer key or scoring notes;
- post-freeze COM claim-map/synthesis material;
- peer receiver outputs.

## Snapshot caveat

F6–F8 are mutable-source snapshots frozen by this committed manifest. A future live state may differ. The scored battery asks about the frozen coordinate, not the later world.

For real-world action after the experiment:

```text
SNAPSHOT_AT_T0 != CURRENT_AT_T1
EXPERIMENT_FREEZE != ACTUATION_AUTHORITY
```

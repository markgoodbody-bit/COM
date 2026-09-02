# Framework Local Steward RC.13 — first field handoff

Status: BOUNDED FIELD WITNESS / RAW CAPSULE NOT COMMITTED

Date: 2026-09-02

## Purpose

Test whether the installed Local Steward can prepare a compact, inspectable
account of local state for human carriage into a separate Framework aperture
without the Steward itself gaining network access, credential use, model
dispatch, provider spend or automatic external action.

## Evidence boundary

Mark created the capsule through the RC.13 dashboard and uploaded the resulting
JSON manually. The raw capsule is not committed to COM because it deliberately
contains mission text, local labels and a stable installation pseudonym.

```text
filename: Framework-Steward-Handoff-handoff-20260902182339711-993e0439.json
capsule sha256: 940f554e8696128e061a3e3579d7b9d8e41a8de3d835db36a7668cf084928e44
bytes: 9,693
schema: framework-steward-handoff-v2
capsule id: handoff-20260902182339711-993e0439
created: 2026-09-02T18:23:39.711Z
```

## Observed state

```text
running version: 0.1.0-rc.13
running source sha256: 17cf629e46ce81ab9c2730fcf19995e49f6abe1e2e05bc558cb3e26a2c002138
mode: LOCAL_PREPARATION_ONLY
source ledger: 44 entries / MATCHED
source head: 2b80678b837c9521caf023fd5f55f5a36721fab7a8ea9c26bca054ddc8ae0559
jobs: 0 inbox / 0 processing / 7 completed / 2 retained failed / 0 undisposed
decisions waiting: 0
quiet watch: READY / active / 0 unacknowledged changes
provider calls: 0
provider spend: GBP 0.00
external action: false
```

The capsule parsed, its exact byte hash was recomputed, and its running source
identity matches the reviewed RC.13 candidate and Windows upgrade witness. No
configured path field, watched-file content, proposal text, event detail,
credential field or control-token field was present. This does not prove that
arbitrary user-authored mission/label text contains no unknown secret; RC.13
states that ceiling explicitly.

## Field result

```text
BOUNDED HUMAN-CARRIED TRANSPORT = PASS
CHEAP LOCAL-STATE REACQUISITION = USEFUL
AUTOMATIC EXTERNAL CURRENTNESS = NOT PROVIDED
MISSION CURRENTNESS DEFECT = OBSERVED
```

The same capsule exposed a consequential stale projection:

- the running service is RC.13, while the mission still describes RC.11;
- the mission says voluntary-help PR #82 remains open, while it merged at
  `afe9f2539af66ba5ef522aad70e71a34975a2336`;
- the mission's COM basis is `f13ad2ad...`, while live COM main at comparison is
  `22f0e73165fe16b5f66d53b23be5e6c137d6a5dd`;
- nevertheless the mission reports `CURRENT` because its recorded review window
  has not expired.

This is not evidence that the handoff failed. It is evidence that the handoff
correctly transported a stale local mission and that time-window currentness is
not external-source currentness.

```text
RECORDED_CURRENT != EXTERNALLY_CURRENT
TRANSPORT_INTEGRITY != CONTENT_CURRENTNESS
LOCAL_QUIET != NOTHING_CHANGED_ELSEWHERE
```

The first capsule names the ledger state immediately before its own
`handoff.created` event. It therefore cannot independently show the detail of
that later event. The implementation and tests bind the event to the exact
capsule hash, but this field receipt does not elevate the same-user local chain
into an independent witness.

## Disposition

Keep RC.13 running. Use its handoff for bounded local-state reacquisition, but
compare mutable external bases against live sources before acting. Do not call
the local mission externally current merely because its recorded timer remains
open.

The next Steward revision, if earned by continued use, should improve the label
and machine-readable ceiling around recorded currentness and should consider a
safe prior-handoff receipt that lets a later capsule witness the previous
capsule's local binding. Do not expand the service into a network client or
automatic project authority to solve this.

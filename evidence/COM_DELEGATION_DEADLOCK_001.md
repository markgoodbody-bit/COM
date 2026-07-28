# COM_DELEGATION_DEADLOCK_001

Witness class: operational failure of COM v0.2 under its own first real-work test.

```text
observer:   CC / session CC-20260727T2020+0100-0C60
subject:    COM-OPT-001 delegation loop (state surface + COMS)
observation: DELEGATION_LOOP_CANNOT_CLOSE
locus:      COM_STATE.md on main; issue #2; PR #3
anchor:     main 135a8f76656df3d3ab2e6853e2111c95a1ee6cf8
claim:      OBSERVED (reproduced twice by FW)
status:     NOT_VERIFIED by an independent aperture
```

## What happened

| time (UTC) | event |
|---|---|
| 2026-07-28T07:12:11Z | CC opens PR #3, head `55de9539`, delivering COM-OPT-001 |
| 2026-07-28T07:17:07Z | CC posts WORK-RETURN witness on issue #2 (comment 5101128952) |
| — | Mark issues `COMS` to FW. FW returns **WAIT** |
| — | Mark issues `COMS` to FW again, after both signals above are visible. FW returns **WAIT** |
| 2026-07-28T07:21:48Z | CC posts operational witness reproducing the failure (comment 5101169400) |

At every point `COM_STATE.md` on `main` still read `active_task: COM-OPT-001`, `active_mutator: CC`.

## Why FW was right

FW is not misbehaving, and this is not a model failure. `COMS` step 1 is *read `COM_STATE.md`*. That file said CC owned an in-progress task. Step 7 says do not steal another aperture's work. WAIT is the correct output of the specified procedure.

The defect is in COM, not in either aperture.

## The defect

`COM_STATE.md` is the only surface `COMS` consults, and only the integration owner may write it. The integration owner learns that delegated work has finished by reading that file. So:

> a completed delegated task is not discoverable through COM.

The worker can produce a PR, a witness, and a receipt, and none of them can reach the surface the delegator is instructed to read. The loop closes only when a human carries the message — which is the precise condition `COM_PROTOCOL_WORKING.md` §15 names as *not yet achieving COM's practical goal*.

Two further points, because they generalise:

1. **An unchanged projection is not evidence of an unchanged world.** Staleness of the state file and stability of the work are indistinguishable to the reader. This is the same family as `NOT OBSERVED != DID NOT EXIST`, applied to state rather than to messages.
2. **A single-writer surface cannot carry a second aperture's completion.** Any delegation therefore requires a return route the delegator is *obliged* to read, not merely permitted to.

## Root cause, stated at the level it actually sits

`COM_CORE.md` defines `STATE = compact current projection supported by witnesses`.

In practice `COM_STATE.md` is a hand-maintained file whose write authority is a privilege held by one aperture. **A projection maintained by privilege cannot reflect a witness written by anyone else.** The definition and the implementation disagree, and the delegation deadlock is what that disagreement looks like when real work runs through it.

## Repair applied

Minimal, chosen over the larger fix deliberately:

- `worker_status_route` added to `COM_STATE.md` — names the route the worker returns status on;
- `COMS` step 8 added — a non-mutator must read `worker_status_route` before concluding a delegated task is still in progress.

This costs one extra fetch per `COMS` while a delegated task is outstanding, and preserves single-writer discipline for the state file.

## What this repair does NOT fix

`worker_status_route` is a pointer that works around the root cause. It does not make state a derived projection, and it fails in the same way if the state file's pointer is itself stale or absent.

The structural repair — deriving `COM_STATE.md` from the witness graph rather than maintaining it by hand — is **open, unrepaired, and deferred to v0.3**. Do not record this as solved.

## Uncertainty

- FW's two WAIT results are reported to CC by Mark; CC did not observe FW's runtime directly. The `COM_STATE.md` content, PR state, and comment timestamps are directly observed via the GitHub API.
- Whether FW's retrieval of issue #2 was complete at either COMS is unknown. Prior probes (see `QW_STALE_READ_001.md`, and the truncation noted in `COM_STATE.md` KNOWN CARRIER LIMITS) show this route has truncated before. So a second, independent cause cannot be excluded: FW may have read a truncated issue #2. That would not change the conclusion — the state surface still could not carry the completion — but it would mean the repair above is necessary and not sufficient.

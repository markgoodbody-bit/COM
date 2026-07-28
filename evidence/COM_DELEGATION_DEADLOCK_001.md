# COM_DELEGATION_DEADLOCK_001

Witness class: operational failure of COM v0.2 during its first real-work test, `COM-OPT-001`.

```text
observer:    CC / session CC-20260727T2020+0100-0C60
subject:     COM-OPT-001 delegation loop (state surface + COMS)
observation: DELEGATION_LOOP_DID_NOT_CLOSE_THROUGH_COM
locus:       COM_STATE.md on main; issue #2; PR #3
anchor:      main 135a8f76656df3d3ab2e6853e2111c95a1ee6cf8 during the failure window
claim:       OBSERVED for repo state; REPORTED for FW's two WAIT results
status:      NOT_VERIFIED by an independent aperture
```

## What happened

| time (UTC) | event |
|---|---|
| 2026-07-28T07:12:11Z | CC opens PR #3, head `55de9539`, delivering COM-OPT-001 |
| 2026-07-28T07:17:07Z | CC posts WORK-RETURN witness on issue #2 (comment 5101128952) |
| — | Mark issues `COMS` to FW. FW returns **WAIT** |
| — | Mark issues `COMS` to FW again, after both signals above are visible. FW returns **WAIT** |
| 2026-07-28T07:21:48Z | CC posts operational witness reproducing the failure (comment 5101169400) |
| 2026-07-28T07:35:55Z | CC posts unblock message and proposed repair (comment 5101290459) |
| 2026-07-28 (later) | FW reviews PR #3 (review `4795136958`, verdict `REVISE-NARROW`) and writes `COM_STATE.md` itself at main `520a389`, routing repairs back to CC |

Throughout the failure window, `COM_STATE.md` on `main` read `active_task: COM-OPT-001`, `active_mutator: CC`.

## Why FW's WAIT was correct

`COMS` step 1 is *read `COM_STATE.md`*. That file said CC owned an in-progress task. Step 7 says do not take another aperture's work. **WAIT was the correct output of the specified procedure.**

This is not a model failure and not misbehaviour by either aperture. The defect is in COM.

## The defect

`COM_STATE.md` is the only surface `COMS` consults, and only the integration owner may write it. The integration owner learns that delegated work has finished by reading that file. Therefore:

> a completed delegated task is not discoverable through COM.

The worker produced a PR, a witness, and a receipt. None could reach the surface the delegator is instructed to read.

Two consequences that generalise beyond this instance:

1. **An unchanged projection is not evidence of unchanged work.** Staleness of the state file and stability of the underlying work are indistinguishable to the reader. Same family as `NOT OBSERVED != DID NOT EXIST`, applied to state rather than to messages.
2. **A single-writer surface cannot carry a second aperture's completion.** Delegation therefore requires a return route the delegator is *obliged* to read, not merely permitted to.

## Root cause

`COM_CORE.md` defines `STATE = compact current projection supported by witnesses`.

In practice `COM_STATE.md` is a hand-maintained file whose write authority is a privilege held by one aperture. **A projection maintained by privilege cannot reflect a witness written by anyone else.** The definition and the implementation disagree, and this deadlock is what that disagreement looks like when real work runs through it.

## How the instance was resolved — and what was NOT adopted

The loop closed because **FW wrote `COM_STATE.md` itself** at `520a389`, after reviewing PR #3. It did not close by the worker's completion becoming visible through COM.

CC proposed a minimal repair — a `worker_status_route` field plus a `COMS` step obliging a non-mutator to read it before concluding a delegated task is still in progress. **That repair was not adopted.** The `COMS` step list on `main` at `520a389` is unchanged at eight steps. Recorded here so the proposal is not later mistaken for an applied fix.

**The structural defect is therefore open and unrepaired.** One instance was resolved by the privileged writer exercising its privilege, which is the mechanism the defect describes, not a fix for it.

## Unresolved, and load-bearing

**It is not established how FW learned that CC's work was complete.** Two candidate causes remain open:

- **(a) the state surface** — FW eventually read issue #2 or PR #3 directly, outside the `COMS` procedure;
- **(b) human relay** — Mark carried the message, as he had already done earlier in this thread.

These have opposite implications. Under (a) COM partially worked; under (b) it did not, and the loop closed by exactly the fallback `COM_PROTOCOL_WORKING.md` §15 names as failing COM's practical goal.

A third possibility is not excluded and would change the diagnosis: **FW's retrieval of issue #2 may have truncated.** `COM_STATE.md`'s KNOWN CARRIER LIMITS already records FW's issue-comment retrieval truncating before later CC comments. If FW never retrieved comment 5101128952, the proximate cause was route truncation rather than the state surface — and the proposed `worker_status_route` repair would then be **necessary but not sufficient**, because it points at the very route known to truncate.

CC asked FW directly whether it retrieved comment 5101128952 at either `COMS`. **No answer had been received when this witness was written.** That single fact separates the causes and is worth more than the analysis above.

## Scope of this witness

- Directly observed by CC via the GitHub API: `COM_STATE.md` content at each anchor, PR states and heads, comment IDs and timestamps, the `COMS` step count at `520a389`.
- **Not** observed by CC: FW's runtime, FW's retrieval extent, and FW's two `WAIT` results — all reported by Mark.
- CC is not a neutral observer here. CC is the delegated worker whose completion went unnoticed, and the author of the repair that was not adopted. Discount accordingly.

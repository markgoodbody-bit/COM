# COM_DELEGATION_DEADLOCK_001

Witness class: operational failure of COM v0.2 during its first real-work test, `COM-OPT-001`.

```text
observer:    CC / session CC-20260727T2020+0100-0C60
subject:     COM-OPT-001 delegation loop (COMS procedure + state projection)
observation: COMPLETED_DELEGATED_WORK_NOT_DISCOVERABLE_BY_THE_COMS_PROCEDURE
locus:       COM_STATE.md on main; issue #2; PR #3
anchor:      main 135a8f76656df3d3ab2e6853e2111c95a1ee6cf8 during the failure window
claim:       OBSERVED for repo state; REPORTED for FW's runtime behaviour, later
             established by FW from its own tool history (see Established facts)
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
| — | On a later `COMS`, FW expands its GitHub inspection, discovers PR #3 directly, and begins integration review |
| 2026-07-28T08:03:49Z | FW review `4795136958`, verdict `REVISE-NARROW` |
| — | FW writes `COM_STATE.md` at main `520a389`, routing the repairs back to CC |
| 2026-07-28 | PR #3 merged clean at `76d3994` |

Throughout the failure window, `COM_STATE.md` on `main` read `active_task: COM-OPT-001`, `active_mutator: CC`.

## Established facts

These were unresolved when this witness was first drafted. FW settled them from its own tool history in PR #5 review comment `5101871210`, and they are recorded here as FW's report about FW's own runtime — a stronger source than CC's inference, and still not independently verified.

1. At the two `COMS -> WAIT` turns, FW **did not retrieve** issue #2 comment `5101128952`.
2. At those two turns, FW **did not inspect issue #2 or PR #3 at all**. No retrieval was attempted against the worker's return route.
3. On a later `COMS`, FW expanded its GitHub inspection, **directly discovered PR #3**, read it, and began integration review. **Mark did not relay the work product or the patch.**

## Why FW's WAIT was correct

`COMS` step 1 is *read `COM_STATE.md`*. That file said CC owned an in-progress task. Step 7 says do not take another aperture's work. **WAIT was the correct output of the specified procedure.**

This is not a model failure and not misbehaviour by either aperture. The defect is in COM.

## The defect

The proximate cause is now narrow and specific:

> `COMS` did not require a non-mutator to inspect the delegated worker's return surface before concluding the work was still in progress.

No carrier failure was observed, and none is required to explain the two waits: FW never attempted the return-route read, so the carrier's behaviour at those moments was never tested. GitHub did serve PR #3 correctly when FW eventually looked (fact 3), but that does not establish it would have served a read attempted earlier, and historical route truncation remains a separate real risk.

What the procedure did was never send FW to look at all. Its read-set was one file, and that file was the one surface the worker could not update.

Underneath that sits a structural condition which this incident exposed but did not by itself prove:

> `COM_CORE.md` defines `STATE = compact current projection supported by witnesses`, but `COM_STATE.md` is hand-maintained and its write authority is a privilege. **A single-writer projection cannot be updated directly by the delegated worker; it can reflect completion only after the writer observes and incorporates the worker's return.** State can therefore lag completed work by however long that takes.

Two consequences that generalise:

1. **An unchanged projection is not evidence of unchanged work.** Staleness of the state file and stability of the underlying work are indistinguishable to the reader. Same family as `NOT OBSERVED != DID NOT EXIST`, applied to state rather than to messages.
2. **A single-writer surface carries a second aperture's completion only at the writer's initiative.** The worker cannot put it there. Delegation therefore needs a return route the delegator is *obliged* to read, so that incorporation does not depend on the writer happening to look.

## What route truncation did and did not explain

COM's KNOWN CARRIER LIMITS records FW's issue-comment retrieval truncating before later CC comments, and CC initially offered that as a candidate cause for these two waits.

**It was not the cause.** Fact 2 rules it out: a retrieval that never happened cannot truncate. Historical truncation remains a real and separate carrier risk, and it is not withdrawn as a finding — but it is not the discriminator for this incident, and this witness no longer leaves it open as one.

## How the instance was resolved

Not by human relay. Fact 3 establishes that FW discovered the completed work product itself, through GitHub, on a later `COMS`.

What the human did supply was the **trigger**: each `COMS` was issued by Mark. So across this incident the human remained the *scheduler* of synchronization while ceasing to be the *carrier* of content. That distinction matters and CC's earlier framing — that the loop "closed only by human relay" — was **wrong** and is withdrawn.

FW then wrote `COM_STATE.md` itself at `520a389`. The state surface was corrected by the privileged writer exercising its privilege, which is the mechanism the structural condition describes rather than a repair of it.

## What was proposed and not adopted

CC proposed a minimal repair: a `worker_status_route` field naming the worker's return route, plus a `COMS` step obliging a non-mutator to read it before concluding a delegated task is still in progress.

**It was not adopted.** The `COMS` step list on `main` at `520a389` was unchanged at eight steps. Recorded so the proposal is not later mistaken for an applied fix.

Fact 2 does bear on its merits, and the direction favours the repair: since the failure was a read-set that was too narrow rather than a carrier that failed, widening the read-set addresses the actual mechanism. CC's earlier hedge — that the repair might be *necessary but not sufficient* because it pointed at a route known to truncate — no longer applies to this incident. **CC authored that repair, so this assessment is self-interested and should carry little weight.** Whether to adopt it remains FW's decision, and it is a workaround for the structural condition, not a fix of it.

## Genuinely still open

- The structural condition above is **unrepaired**. Deriving `COM_STATE.md` from the witness graph rather than maintaining it by hand is deferred to v0.3.
- Whether the same failure recurs once the human stops issuing `COMS` at all is **untested**. Every synchronization in this incident was human-triggered, so COM has not yet been shown to close a delegation loop unprompted.
- No independent aperture has reviewed this witness. CC wrote it; FW corrected it; both are participants.

## Scope of this witness

- Directly observed by CC via the GitHub API: `COM_STATE.md` content at each anchor, PR states and heads, comment IDs and timestamps, the `COMS` step count at `520a389`.
- **Not** observed by CC: FW's runtime, its retrieval extent, and its two `WAIT` results. Those were reported by Mark, and the three Established facts are FW's report about itself.
- CC is not a neutral observer. CC is the delegated worker whose completion went unnoticed, and the author of the repair that was not adopted. Discount accordingly.

## Revisions before landing

This witness was corrected twice before entering the record, both times because a claim in it was not supported:

1. An early draft stated the `worker_status_route` repair **had been applied**. It had not. Corrected before landing.
2. A later draft left route truncation open as the load-bearing discriminator, and stated the loop closed by human relay. FW's tool history refuted both. Corrected before landing.
3. A later draft asserted *the carrier was not at fault*, and stated the structural condition as two absolutes — that a privileged projection **cannot** reflect another aperture's witness, and that a single-writer surface **cannot** carry another aperture's completion. All three were stronger than the evidence. The carrier was never read at those turns, so it was untested rather than exonerated; and a single writer plainly can incorporate another aperture's return, which is what eventually happened here. Narrowed before landing.

Neither correction rewrote a claim that had already landed. Both are noted here so the record shows what this witness once asserted and why it changed.

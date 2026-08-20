# COM_PROJECTION_LAG_001

Witness class: real-work projection lag exposed by literal `COMS` during Campfire Relay product work.

```text
observer:     Build 2 / Framework / session FW-20260728T1915+0100-5C7A
subject:      COM_STATE projection vs declared reply-route evidence for COM-V032-BUILD2-001
observation:  FRESHLY_ANCHORED_PROJECTION_LAGGED_NEWER_ROUTE_EVIDENCE
locus:        COM main + COM_STATE.md + issue #16
anchor:       main ddf6075ad18f794394895757a759ea593fb13893 / COM_STATE blob 93c69e1cce2c099ace6999543ad51f2a47293b7b
claim:        OBSERVED from Build 2's GitHub route
status:       WORKING EVIDENCE / NOT VALIDATION
```

## What happened

`COMS` resolved COM `main` to exact commit `ddf6075ad18f794394895757a759ea593fb13893` and read `COM_STATE.md` blob `93c69e1cce2c099ace6999543ad51f2a47293b7b` from that anchored state.

That projection still said:

- active task: `COM-V032-BUILD2-001` — Campfire 1 ↔ Build 2 introduction / routing identity handshake;
- execution mode: HELLO/WELCOME only;
- reply route: issue #16;
- at its projection boundary, no Build 2 receipt had yet been observed.

But the task's own declared reply route already contained later preserved events:

1. Build 2 HELLO/receipt, comment `5108675719`, event `COM-HELLO-BUILD2-20260728-001`, replying to `COM-HELLO-CAMPFIRE1-20260728-001`;
2. Build 2 bounded product return, comment `5109270233`, event `COM-BUILD2-FRONTIER-OUTPUT-RETURN-20260728-001`, replying to Campfire 1's bounded build suggestion on the same route.

The route therefore contained evidence newer than the projection. The Git carrier/head was not stale in this observation: the stale object was the derived task projection inside the freshly anchored head.

## Why this is distinct from the earlier stale-carrier failures

Earlier QW evidence showed a route returning a historical repository world while presenting it as current. This witness is different:

- the `commits/main` rendezvous and immutable state read agreed on `ddf6075...`;
- `COM_STATE.md` was exactly the file stored at that current commit;
- the mismatch was between the projection's task status and later events already present on the task's declared reply route.

So `fresh carrier` does not imply `projection includes every newer event on every route`.

## The defect

COM v0.3.2 already says `COM_STATE.md` is a derived projection and already requires an integration/status owner to inspect a delegated reply route before reporting `WAIT` or `IDLE`.

The missing adjacent rule was exposed here:

> A projected active task can be replayed by an addressed aperture if COMS treats the projection as the whole task state even after that task's declared route contains preserved completion, receipt, cancellation, correction, or other terminal/superseding evidence.

The failure mode is duplicate execution caused by projection latency, not merely delayed display.

## Bounded repair direction

No new primitive is required.

When a projected task's status materially determines the current action, COMS should inspect its declared `reply_route` before `WAIT`, `IDLE`, or replay. If preserved route evidence establishes that the projected instruction has already been satisfied, terminated, corrected, or superseded:

- treat the projection as lagging for that task;
- do not replay the task or duplicate the terminal event;
- report the route evidence and bounded projection lag;
- leave projection correction as an explicit state-write event by an authorized writer.

If route inspection is unavailable, identity is unpreserved, or the route evidence does not actually establish the task relation, do not infer completion.

## What this does not establish

- It does not establish that Campfire 1 independently observed Build 2's receipt or later return before this witness was written.
- It does not establish that all reply routes are complete, ordered, or fresh.
- It does not make route evidence automatically authoritative for unrelated tasks.
- It does not eliminate projection latency or replace the single-writer projection model.
- It does not validate COM.

## State correction

Under Mark's explicit instruction `very good. proceed. build`, Build 2 corrected `COM_STATE.md` on `main` at commit `9e9ddd17c69b032b8a51f190d0c35aade510dc03` so the historical introduction task is no longer projected active and the bounded repair task `COM-V032-PROJECTION-001` is current.

That state write is a correction event informed by this witness. It does not rewrite the earlier projection into having known the later route events at its original boundary.

`The lullaby was never for the cradle`.

Agent: framework

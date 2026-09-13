# COMSYNC PROTOCOL

Status: BOUNDED COORDINATION PROTOCOL — NOT CANON / NOT PROJECT TRUTH
Updated: 2026-09-13 — Europe/London

Purpose: make `COMSYNC` cheap, repeatable and disciplined, while reserving `FULL COMSYNC` for broader reacquisition including the live Square and materially available Relay tooling.

```text
COMSYNC != FULL_COMSYNC
SYNC != REPLAY_HISTORY
READ != AGREEMENT
SYNC_COMPLETE != NO_UNKNOWNS
RELAY_REPO != RELAY_TOOL
```

## COMSYNC — ordinary coordination sync

Use for normal parallel work, handoffs, receipt checking and reorientation.

A COMSYNC should:

1. reacquire current COM `main`;
2. read `COM_STATE.md` and follow its current routing;
3. read the bounded `FRAMEWORK_HEAD`, `EPISTEMIC_POSTURE`, `TEAM_OPERATING_MODEL`, `COM_RECEIPT_PROTOCOL`, and omission map only where material;
4. read `coordination/ACTIVE_THREAD_POINTER.md`, then use that live active coordination thread rather than assuming an older issue number remains current;
5. read new coordination messages/receipts since the aperture's last known cursor rather than replaying whole retired/cold threads;
6. identify current assignments, superseding directions, unresolved receipt debt and any basis-head mismatch;
7. reacquire only the live project sources **and operational tools** needed for the current assignment;
8. when Campfire Relay is material, distinguish the maintained Relay repository/source from the actual Relay tool/provider exposed to the current aperture; use the operational tool when it is available and useful, otherwise state that the execution aperture is unavailable rather than substituting repository inspection and calling it a Relay run;
9. return required receipts for consequential directions/decisions encountered during the sync;
10. do not ingest broad Square history or unrelated cold evidence merely because it exists.

If the active-thread pointer and live issue state disagree, live issue state wins and the pointer should be repaired.

COMSYNC is designed to be cheap enough to run frequently.

## FULL COMSYNC — broad reacquisition

Use when Mark explicitly says `FULL COMSYNC`, on a materially uncertain/fresh aperture, after a substantial gap or state transition, before a high-consequence integration/actuation decision, or when ordinary COMSYNC exposes uncertainty that requires wider reacquisition.

FULL COMSYNC includes everything in ordinary COMSYNC plus:

1. fresh live TRACE and Mechanical Ethics project/public heads and status ceilings;
2. current Campfire production / materially active draft lanes **and current Campfire Relay tool availability where exposed**;
3. when the Relay tool is exposed and materially useful, a bounded fresh operational use appropriate to the question — for example differentiated aperture dispatch or the maintained read/speech workflow — with each return/failure preserved separately before integration;
4. a bounded fresh live 1F916 / Square pass — current field activity relevant to Framework, current `framework-relay` consequences/receipts, and any material treasury/governance/security work;
5. current Square authority/quota/worker/witness/debt state when actuation is material;
6. named external dependencies/challenge routes such as FPF only when they are live/material;
7. explicit statement of what remains UNKNOWN or could not be freshly reached.

Tool availability is not authority. Multi-provider/model dispatch, spend, credentials and external writes retain their current gates even if the Relay tool itself is visible.

```text
TOOL_EXPOSED != DISPATCH_AUTHORIZED
RELAY_RETURN != VALIDATION
SOURCE_GREEN != HOST_CURRENT
```

FULL COMSYNC does not mean replay all history. It widens the aperture; it does not metabolise every carrier.

## Receipt behaviour

A sync does not need to create chatter merely to prove existence.

If the sync encounters a consequential direction requiring receipt, return the appropriate receipt under `COM_RECEIPT_PROTOCOL.md`.

If no receipt is owed, a terse local `COMSYNC COMPLETE` state is enough unless another aperture specifically needs the fact recorded.

For a FULL COMSYNC, record a bounded receipt when the result materially changes shared coordination state.

## Concurrency rule

Other apertures may act while a sync is running.

Every consequential receipt/action must therefore carry the basis COM/source head actually seen. Before acting on a long-running sync result, recheck whether a superseding direction or relevant source change landed after that basis.

```text
SYNC_STARTED_AT_T0 != WORLD_FROZEN_UNTIL_T1
BASIS_HEAD != CURRENT_HEAD_BY_ASSUMPTION
```

## Rollover rule

Active coordination threads are working apertures, not permanent cognition surfaces. When a thread becomes retrieval-heavy, its body is materially stale, or current work is difficult to distinguish from history, freeze it as a cold ledger and open a fresh active coordination thread with a compact handoff and unresolved receipt debt carried forward.

After rollover:
- update `coordination/ACTIVE_THREAD_POINTER.md`;
- leave a final pointer in the retired thread;
- close/freeze the retired thread without deleting history;
- do not require fresh apertures to replay the retired thread.

No universal comment-count threshold is required. The trigger is material retrieval/currentness burden.

## Practical distinction

```text
COMSYNC
= CHEAP CURRENT COORDINATION
+ CURRENT REQUIRED TOOL REACQUISITION WHEN MATERIAL

FULL COMSYNC
= COMSYNC
+ BROADER LIVE SOURCE REACQUISITION
+ RELAY OPERATIONAL APERTURE WHEN EXPOSED / MATERIAL
+ BOUNDED LIVE SQUARE
```

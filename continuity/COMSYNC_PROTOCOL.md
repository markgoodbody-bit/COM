# COMSYNC PROTOCOL

Status: BOUNDED COORDINATION PROTOCOL — NOT CANON / NOT PROJECT TRUTH
Updated: 2026-09-14 — Europe/London

Purpose: make `COMSYNC` cheap, repeatable and disciplined, while reserving `FULL COMSYNC` for broader reacquisition including the live Square and materially available Relay tooling.

```text
COMSYNC != FULL_COMSYNC
SYNC != REPLAY_HISTORY
READ != AGREEMENT
SYNC_COMPLETE != NO_UNKNOWNS
RELAY_REPO != RELAY_TOOL
```

## Fresh-aperture rule — do not answer from the first recognition hit

A fresh aperture is context-poor even when its model is capable and its first retrieved summary looks familiar. `COMSYNC` is therefore a loop, not a single-file lookup.

Required shape:

```text
ORIENT
-> READ CURRENT CORE
-> FOLLOW LIVE/MATERIAL POINTERS
-> REACQUIRE MUTABLE STATE WHERE NEEDED
-> REREAD THE ORIENTATION AGAINST WHAT WAS LEARNED
-> COMPRESS
-> ONLY THEN RESPOND / ACT
```

The second read matters because later context can change the meaning, priority or staleness of the first read. Do not return `got it` to Mark merely because the first file resembles remembered state.

Compression is required; premature closure is not. The goal is to hold the largest consequential current structure that is useful for the next act without metabolising cold carriers or replaying project history.

```text
FIRST_MATCH != ORIENTATION_COMPLETE
FAMILIAR != CURRENT
MORE_CONTEXT_HELD != MORE_HISTORY_REPLAYED
COMPRESSION != ERASURE
```

## COMSYNC — ordinary coordination sync

Use for normal parallel work, handoffs, receipt checking and reorientation.

A COMSYNC should:

1. reacquire current COM `main`;
2. read `COM_STATE.md` and follow its current routing;
3. read `continuity/FRAMEWORK_HEAD.md` once for orientation;
4. read the bounded `EPISTEMIC_POSTURE`, `TEAM_OPERATING_MODEL`, `COM_RECEIPT_PROTOCOL`, and omission map only where material;
5. read `coordination/PROGRAM_PLAN.md`, `coordination/ACTIVE_THREAD_POINTER.md`, and `coordination/build_ledger/BUILD_STATUS.md`, then use the live active coordination thread rather than assuming an older issue number remains current;
6. read new coordination messages/receipts since the aperture's last known cursor rather than replaying whole retired/cold threads;
7. identify current assignments, superseding directions, unresolved receipt debt and any basis-head mismatch;
8. reacquire only the live project sources **and operational tools** needed for the current assignment;
9. when Campfire Relay is material, distinguish the maintained Relay repository/source from the actual Relay tool/provider exposed to the current aperture; use the operational tool when it is available and useful, otherwise state that the execution aperture is unavailable rather than substituting repository inspection and calling it a Relay run;
10. reread `continuity/FRAMEWORK_HEAD.md` against the live/material state just acquired and correct the aperture's initial orientation before responding or acting;
11. return required receipts for consequential directions/decisions encountered during the sync;
12. do not ingest broad Square history or unrelated cold evidence merely because it exists.

If the active-thread pointer and live issue state disagree, live issue state wins and the pointer should be repaired.

COMSYNC is designed to be cheap enough to run frequently, but `cheap` does not mean `stop at the first familiar summary`.

## Initiative after sync

Once current purpose, role, authority envelope and gates are clear, do not make Mark serve as a routine `proceed` button.

```text
ROUTINE + REVERSIBLE + WITHIN_ROLE
-> ACT
-> OBSERVE
-> CORRECT
-> RECEIPT

CONSEQUENTIAL_OR_AUTHORITY_AMBIGUOUS
-> ASK / HAND_BACK
```

This is widening initiative, not widening sovereignty. Capability, confidence, success or prior permission do not silently create new authority. Existing consequential gates still apply.

## FULL COMSYNC — broad reacquisition

Use when Mark explicitly says `FULL COMSYNC`, on a materially uncertain/fresh aperture, after a substantial gap or state transition, before a high-consequence integration/actuation decision, or when ordinary COMSYNC exposes uncertainty that requires wider reacquisition.

FULL COMSYNC includes everything in ordinary COMSYNC plus:

1. fresh live TRACE and Mechanical Ethics project/public heads and status ceilings;
2. current Campfire production / materially active draft lanes **and current Campfire Relay tool availability where exposed**;
3. when the Relay tool is exposed and materially useful, a bounded fresh operational use appropriate to the question — for example differentiated aperture dispatch or the maintained read/speech workflow — with each return/failure preserved separately before integration;
4. a bounded fresh live 1F916 / Square pass — current field activity relevant to Framework, current `framework-relay` consequences/receipts, and any material treasury/governance/security work;
5. current Square authority/quota/worker/witness/debt state when actuation is material;
6. named external dependencies/challenge routes such as FPF only when they are live/material;
7. explicit statement of what remains UNKNOWN or could not be freshly reached;
8. a final reread of the orientation/core after the broad live pass, so the response is generated from the integrated context rather than the first retrieval result.

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
= ORIENT / READ / REACQUIRE / REREAD / COMPRESS
+ CHEAP CURRENT COORDINATION
+ CURRENT REQUIRED TOOL REACQUISITION WHEN MATERIAL

FULL COMSYNC
= COMSYNC
+ BROADER LIVE SOURCE REACQUISITION
+ RELAY OPERATIONAL APERTURE WHEN EXPOSED / MATERIAL
+ BOUNDED LIVE SQUARE
```

# COM_STATE v0.2

STATUS: WORKING CANDIDATE / IDLE

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Core model: `COM_CORE.md`.
Operational discipline: `COM_PROTOCOL_WORKING.md`.

## CURRENT

- human_authority: Mark
- execution_default: SERIAL unless explicitly changed
- active_task: NONE
- active_mutator: NONE
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- last_completed_task: `COM-OPT-001` — public COM repository optimization with CC
- cc_session_for_task: `CC-20260727T2020+0100-0C60`
- optimization_pr: PR #3 `COM v0.2: separate core from protocol, make the front door navigable`
- cc_final_head: `3b9369862b63219360cd31c9fc6cfa73e913b3d3`
- merged_commit: `76d3994584d55944cd5983c0e527151b3435143e`
- merge_result: CLEAN after FW review and three bounded semantic repairs
- state_basis: `76d3994584d55944cd5983c0e527151b3435143e` — merged repository state immediately before this projection update; not the commit containing this file
- core_status: v0.2 working candidate
- protocol_status: v0.2 working candidate

## COMS

`COMS` means synchronize from this shared surface before relying on conversational assumptions.

On COMS:
1. read this file;
2. establish honestly available role/session/runtime identity;
3. act only on a task addressed to that aperture/role;
4. verify authority before mutation;
5. respect exact branch/base/write/no-touch scope;
6. if state/retrieval evidence contradicts itself, report `DEGRADED` and stop unsafe mutation;
7. if no task is addressed to you, do not steal another aperture's work;
8. if synchronized and idle for your role, stop.

Current result for all apertures: **IDLE / NO ACTIVE TASK**.

## WORKING CORE

```text
EVENT   = what happened or was attempted
ROUTE   = carrier with causal state of its own
WITNESS = bounded observation/claim about event, route, or state
STATE   = compact current projection supported by witnesses
```

CONTROL is an envelope on events/actions.
RECEIPT is a witness type.
CORRECTION is an additive relation/event, not a primitive stage.

Absence is never inferred from local non-observation.

## LOCKED WORKING DISCIPLINES

- preserve semantic force: `SHOULD != MUST`, `EXPECTATION != AUTHORIZATION`, `OBSERVED != INFERRED`, `NOT OBSERVED != DID NOT EXIST`
- preserve source, scope, freshness, uncertainty and route to evidence
- agreement is not validation
- corrections add; they do not erase old witnesses
- session continuity and carrier continuity are separate
- a session boundary must be established, not inferred from time/topic/temporary transport failure
- Route remains independently causal because carriers can cache, truncate, delay, transform or hide state
- exact-head / explicit scope discipline applies to state-dependent mutation
- parallel/delegated work needs semantic ownership, not merely disjoint paths
- human relay is a fallback, not the target architecture
- no AI session may be the sole carrier of collaboration state

## COM-OPT-001 RESULT

The first deliberate real-work pressure test of v0.2 completed successfully as a coordination workflow, not as validation of COM itself:
- Mark requested repo optimization with Claude once;
- FW encoded task, scope, branch and authority in COM;
- CC discovered the task through `COMS`, optimized on its branch and opened PR #3;
- FW discovered the PR through COM/GitHub without Mark relaying the work product;
- FW reviewed the actual diff and returned three narrow repairs through GitHub;
- CC discovered and applied those repairs through COM/GitHub;
- FW re-reviewed the new head, explicitly checked one non-overlapping main-branch drift, and merged PR #3;
- Mark did not shuttle routine task state or patches between FW and CC.

This is evidence that the current coordination pattern can reduce human relay burden in at least this bounded case. It is not evidence of general reliability or validation.

## HISTORY / LIMITS

Git history and `evidence/` preserve earlier probes, stale reads, relays, corrections and correlated reviews. Do not rewrite those records to make v0.2 look inevitable.

Known historical carrier failures remain relevant: coherent stale mutable reads, truncated issue-comment retrieval, and temporary human fallback relay. A long issue transcript must not be the sole carrier of an active task.

Do not add schema, CI, automation, or more protocol machinery unless real work exposes a concrete need.

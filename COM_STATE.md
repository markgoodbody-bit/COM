# COM_STATE v0.3 candidate review

STATUS: WORKING CANDIDATE / ACTIVE

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Core model candidate: `COM_CORE.md` on `framework/com-v0.3-bootstrap-liveness`.
Operational candidate: `COM_PROTOCOL_WORKING.md` on the same branch.

## CURRENT

- human_authority: Mark
- active_task: `COM-V03-001` — review the v0.3 bootstrap/liveness candidate
- task_phase: CC CRITIQUE / FW integration
- addressed_to: CC / continuing session `CC-20260727T2020+0100-0C60` if still active; otherwise a fresh CC session must identify itself honestly
- active_mutator: FW on `framework/com-v0.3-bootstrap-liveness` only
- reviewer: CC, mutation `NONE`
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- pull_request: PR #6 `COM v0.3 candidate: cold bootstrap, event identity, delegated-return liveness`
- candidate_head: `2b14cf7dd8be0f617d96e7f90237c2bad10fdd76`
- base_anchor: `f01aee2c7aef35c22d7ad99d02f67cd76aa78682`
- reply_route: PR #6 conversation
- review_scope: falsify/narrow the three substantive additions — cold HELLO/WELCOME bootstrap, event identity/idempotency, delegated return-path/IDLE liveness — and challenge the generative rule if it adds hidden ontology
- no_touch_for_CC: branch files, `COM_STATE.md`, evidence, routes, main; review only
- FW_write_scope: `README.md`, `COM_CORE.md`, `COM_PROTOCOL_WORKING.md` on the candidate branch only until review is integrated
- authority_source: Mark asked FW to keep improving COM and explicitly asked whether it can be improved, what is missing, and what other designs have done
- state_basis: `f01aee2c7aef35c22d7ad99d02f67cd76aa78682` — main head before this state update; not the commit containing this file
- core_status: v0.3 working candidate / unmerged
- protocol_status: v0.3 working candidate / unmerged

## COMS

`COMS` means synchronize from this shared surface before relying on conversational assumptions.

On COMS:
1. read this file;
2. establish honestly available role/runtime/model/provider/session identity;
3. act only on a task addressed to that aperture/role;
4. if reviewing delegated work, inspect the declared `reply_route`/artifact before reporting WAIT;
5. verify authority before mutation;
6. respect branch/base/write/no-touch scope;
7. if state/retrieval evidence contradicts itself, report `DEGRADED` and stop unsafe mutation;
8. if no task is addressed to you, do not steal another aperture's work;
9. if synchronized and idle for your role, stop.

Current result:
- **CC:** review PR #6 only. Return a bounded critique on PR #6. Do not edit files or merge.
- **FW:** wait for CC review, then integrate/reject/narrow. Do not treat agreement as validation.
- **Other established apertures:** no active task.
- **Cold/unestablished aperture:** may synchronize read-only; the candidate `HELLO` bootstrap is not canon until this PR is resolved.

## CANDIDATE GENERATIVE RULE

```text
Aperture -> EVENT[CONTROL] -> ROUTE -> WITNESS -> PROJECTION
   ^                                                  |
   +---------------- next EVENT ----------------------+
```

Named operations such as `HELLO`, `WELCOME`, `TASK`, `RETURN`, `REFUSE`, `CORRECT`, `GRANT`, or `REVOKE` should remain event kinds/relations unless a real failure proves a new primitive is required.

## WHY THIS CANDIDATE EXISTS

Real work exposed two concrete holes in v0.2:
- a completely cold aperture could read COM but was not told how to introduce itself without inventing role or authority;
- delegated completion could exist on the worker's return surface while the state-only COMS procedure still returned WAIT.

The candidate also adds stable event identity/idempotency because duplicate/retry ambiguity was an unrepresented failure mode and is solvable without adding a new primitive.

## EXTERNAL DESIGN PRESSURE

The candidate was compared against public designs including A2A, MCP, FIPA ACL, CloudEvents, Matrix, ActivityPub, and W3C/OpenTelemetry context propagation. Their structures are inputs, not authority; COM should borrow only what survives its own observed problems and anti-drift test.

## HISTORY / LIMITS

PR #5's durable witness remains `evidence/COM_DELEGATION_DEADLOCK_001.md` on main. It establishes that the original state-only COMS read-set was insufficient in one bounded delegated-work case; it does not validate the v0.3 repair.

Do not add schema, CI, automation, cryptographic identity machinery, or new protocol primitives during this review unless a concrete defect makes one unavoidable.
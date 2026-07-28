# COM_STATE v0.2

STATUS: WORKING CANDIDATE / ACTIVE

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Core model: `COM_CORE.md`.
Operational discipline: `COM_PROTOCOL_WORKING.md`.

## CURRENT

- human_authority: Mark
- execution_mode: delegated CC narrow repair / FW integration
- active_task: `COM-WITNESS-001` — correct and decide PR #5 deadlock witness
- task_phase: SECOND NARROW REPAIR
- addressed_to: CC / session `CC-20260727T2020+0100-0C60` if still active; otherwise a fresh CC session must identify itself honestly
- active_mutator: CC on `claude/com-state-unblock` only
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- pull_request: PR #5 `COM: preserve the COM-OPT-001 delegation deadlock as evidence`
- reviewed_head: `7b3fdf6c748a5d055bba61b08ca6c79dce462f66`
- review_route: PR #5 comment `5101944801`
- verdict: `REVISE-NARROW`
- requested_repair_1: replace `The carrier was not at fault` with the supported narrower claim that no carrier failure was observed or required to explain the WAITs because no return-route read was attempted
- requested_repair_2: replace absolute claims that a privileged/single-writer projection cannot reflect/carry another aperture's witness; the supported defect is that the worker cannot update it directly, so freshness depends on the privileged writer observing and incorporating the return
- accepted_fact_1: FW did not retrieve issue #2 comment `5101128952` at either of the two `COMS -> WAIT` turns
- accepted_fact_2: FW did not inspect issue #2 or PR #3 on either WAIT turn; route truncation was therefore not demonstrated as the proximate cause of those waits
- accepted_fact_3: on a later COMS, FW directly discovered PR #3 through GitHub and began integration review; Mark did not relay the work product or patch
- write_scope: `evidence/COM_DELEGATION_DEADLOCK_001.md` only on the CC branch
- no_touch: `COM_STATE.md`, other evidence witnesses, routes, protocol/core/README, `main`
- deliverable: one corrected PR #5 head; FW then decides merge/reject and returns state to idle
- state_basis: `31178f89e57d43932822615533155dd8680e8cd5` — main head before this projection update; not the commit containing this file
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

Current result:
- **CC:** apply the two remaining semantic narrowing repairs in PR #5 comment `5101944801`, then stop. Do not merge.
- **FW:** wait for a new PR #5 head, then decide it.
- **Other apertures:** no active task.

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

## LIVE DEFECT NOW EXPOSED

The prior projection said `IDLE / NO ACTIVE TASK` while PR #5 was open, mergeable and undecided. That projection was incomplete.

This state update repairs the live projection. It does **not** by itself repair the underlying structural issue: a hand-maintained current-state projection can omit new work/witnesses created outside its writer's observation path.

## COM-OPT-001 RESULT, CORRECTED

`COM-OPT-001` completed, but the first delegation-return loop did not close cleanly through the original state-only COMS procedure:
- CC opened PR #3 and posted a work-return witness;
- FW ran COMS twice, read the current state only, and correctly returned WAIT under the written procedure;
- on a later COMS, FW expanded direct GitHub inspection, discovered PR #3, reviewed it, routed narrow repairs, and ultimately merged it;
- Mark did not shuttle the work product or patch between apertures.

So the bounded workflow eventually reduced human relay burden, while simultaneously exposing a state/return-route defect. Both facts stand. Neither validates COM generally.

## HISTORY / LIMITS

Git history and `evidence/` preserve earlier probes, stale reads, relays, corrections and correlated reviews. Do not rewrite those records to make v0.2 look inevitable.

Historical carrier truncation remains real evidence, but it is not established as the cause of the two `COMS -> WAIT` turns in COM-OPT-001 because FW did not query the worker return route on those turns.

Do not add schema, CI, automation, or more protocol machinery unless real work exposes a concrete need.
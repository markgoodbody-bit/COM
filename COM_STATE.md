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
- last_completed_task: `COM-WITNESS-001` — correct and decide PR #5 deadlock witness
- cc_session_for_task: `CC-20260727T2020+0100-0C60`
- witness_pr: PR #5 `COM: preserve the COM-OPT-001 delegation deadlock as evidence`
- cc_final_head: `3d795fc4f25f9ab28c0cfc309d1b4f780055949a`
- merged_commit: `9587d44a570c59554600a0ccea15dcbda44c8137`
- merge_result: CLEAN after two rounds of bounded semantic narrowing
- state_basis: `9587d44a570c59554600a0ccea15dcbda44c8137` — merged repository state immediately before this projection update; not the commit containing this file
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

## COM-OPT-001 / COM-WITNESS-001 RESULT

The first delegated real-work loop completed, but exposed a concrete return-path defect:
- CC completed work and posted a return witness;
- FW's first two `COMS` runs read only this projection and correctly returned WAIT under the written procedure;
- no return-route read was attempted on those WAIT turns, so carrier failure was not demonstrated as their cause;
- on a later `COMS`, FW directly discovered PR #3 through GitHub and integrated it without Mark relaying the work product or patch;
- the deadlock witness was then corrected through PR #5 until unsupported causal and structural overclaims were removed, and merged at `9587d44a570c59554600a0ccea15dcbda44c8137`.

The durable witness is `evidence/COM_DELEGATION_DEADLOCK_001.md`.

This supports a narrow conclusion only: the original state-only COMS read-set was insufficient for delegated completion discovery. It does not validate COM generally.

## OPEN STRUCTURAL QUESTION

A hand-maintained single-writer current projection can lag work completed by another aperture until the writer observes and incorporates that return. A future repair may require a mandatory worker return route or a state projection derived more directly from witnesses. No repair is adopted merely by recording this defect.

## HISTORY / LIMITS

Git history and `evidence/` preserve earlier probes, stale reads, relays, corrections and correlated reviews. Do not rewrite those records to make v0.2 look inevitable.

Historical carrier truncation remains real evidence, but it was not established as the cause of the two `COMS -> WAIT` turns in COM-OPT-001 because FW did not query the worker return route on those turns.

Do not add schema, CI, automation, or more protocol machinery unless real work exposes a concrete need.

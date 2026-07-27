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
- last_build_actor: FW / session `FW-20260727T2012+0100-8F3C`
- last_build_authority: Mark directly instructed FW to examine what COM could be and make it that; this is an attributed live-conversation claim, not independently inspectable public evidence
- state_basis: `030e79e82baf3bf864302f924f22d07622e0b7cf` — head immediately before this state projection was written; this is NOT the commit containing this file
- core_status: v0.2 working candidate
- protocol_status: v0.2 working candidate

## COMS

`COMS` means synchronize from this shared surface before relying on conversational assumptions.

On COMS:
1. read this file;
2. establish honestly available role/session/runtime identity;
3. act only on a task addressed to that aperture/role;
4. verify authority before mutation;
5. if no task is addressed here, do not steal another aperture's work;
6. if state/retrieval evidence contradicts itself, report `DEGRADED` and stop unsafe mutation;
7. if synchronized and idle, stop.

Current result for any aperture: **IDLE / NO ACTIVE TASK**.

## WORKING CORE

COM now distinguishes:

```text
EVENT   = what happened or was attempted
ROUTE   = carrier with causal state of its own
WITNESS = bounded observation/claim about event, route, or state
STATE   = compact current projection supported by witnesses
```

CONTROL is an envelope on events/actions.
RECEIPT is a witness type.
CORRECTION is an additive relation/event, not a primitive stage.

Absence is never inferred from local non-observation. A non-observation must name the expected event, observer, locus/route, observation window or state anchor, and unresolved uncertainty.

## LOCKED WORKING DISCIPLINES

- preserve semantic force: `SHOULD != MUST`, `EXPECTATION != AUTHORIZATION`, `OBSERVED != INFERRED`, `NOT OBSERVED != DID NOT EXIST`
- preserve source, scope, freshness, uncertainty and route to evidence
- agreement is not validation
- corrections add; they do not erase old witnesses
- session continuity and carrier continuity are separate
- a session boundary must be established, not inferred from time/topic/temporary transport failure
- Route remains independently causal because carriers can cache, truncate, delay, transform or hide state
- exact-head / explicit scope discipline applies to state-dependent mutation
- parallel work needs semantic ownership, not merely disjoint paths
- human relay is a fallback, not the target architecture
- no AI session may be the sole carrier of collaboration state

## KNOWN CARRIER LIMITS

Historical probes established that:
- QW could receive a coherent but stale mutable GitHub view while immutable newer commits existed;
- FW's GitHub issue-comment retrieval could truncate before later CC comments even though issue metadata showed more comments;
- Mark temporarily became a fallback relay for some CC -> FW traffic.

Operational consequence:
**A long issue transcript must not be the sole carrier of an active task.** Put the actionable task in this current state or in a compact/immutable route object referenced here.

These are historical carrier observations, not claims that every current route remains degraded.

## HISTORY

Git history and `evidence/` preserve the v0/v0.1 experiments, stale reads, relays, corrections, and correlated reviews.

Do not rewrite those records to make v0.2 look inevitable.

The former primitive

`Aperture -> Witness -> Route -> Receipt -> Correction`

is retained in history as a falsified/over-factored working hypothesis, not silently converted into the new model.

## NEXT PROOF

Do not immediately add schema, CI, automation, more failure taxonomy, or another self-referential review loop.

The next meaningful pressure test should be **real collaborative work**:
- one actual task;
- explicit actor/authority/scope;
- at least one independent witness/verification step;
- route failure preserved if it occurs;
- Mark not required to shuttle routine machine-readable state.

Only add machinery when a real failure demonstrates that the smaller core is insufficient.
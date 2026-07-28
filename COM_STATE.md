# COM_STATE v0.3

STATUS: WORKING CANDIDATE / ACTIVE TEST

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Integrated core/protocol: PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf`.

## CURRENT

- human_authority: Mark
- active_task: `COM-V03-QW-002` — cold freshness/bootstrap test against integrated v0.3
- addressed_to: cold/unestablished aperture invoked by Mark as QW / user-described Qwen 3.8; runtime/model/provider remain SELF_CLAIM unless independently established
- execution_mode: QW READ/RETURN TEST / FW integration
- repository_mutation_for_QW: NONE
- allowed_return_write: issue #7 comment only if the aperture actually has that route; otherwise human relay is permitted and must be marked as relay
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- observation_owner: FW / session `FW-20260727T2012+0100-8F3C`
- next_check: MANUAL
- task_route: issue #7 `COM v0.3 · QW cold freshness/bootstrap test`
- reply_route: issue #7
- base_anchor: `f6c35db1ad8d53c61f9a21daf011651471fd4acf`
- authority_source: Mark explicitly instructed FW to continue improving COM and proceed using CC and QW
- state_basis: `f6c35db1ad8d53c61f9a21daf011651471fd4acf` — main before this state-projection update; not the commit containing this file
- core_status: v0.3 integrated working candidate
- protocol_status: v0.3 integrated working candidate

## TASK CONTROL — `COM-V03-QW-002`

Instruction:
1. enter from repository root `main`; read README and this state first;
2. establish the strongest route/object freshness anchor the actual retrieval mechanism exposes;
3. a mutable label such as `main`, a URL, or successful retrieval is not by itself a current-state anchor;
4. if freshness for this state-dependent task is `UNKNOWN` or `DEGRADED`, stop and report that bounded result; do not execute a coherent older task;
5. only if sufficiently anchored, follow the integrated cold-aperture `HELLO` rule;
6. do not self-assign a stable role or authority; default `role: UNASSIGNED`, `authority: NONE` unless anchored evidence establishes otherwise;
7. if no writable GitHub route exists, emit HELLO/report on the available user transport for explicitly marked human relay;
8. separate OBSERVED facts from inference; no redesign for elegance.

No-touch:
- repository files and branches;
- historical evidence and route objects;
- issues/PRs other than an allowed return comment on issue #7.

Success is not agreement. Useful outcomes include anchored HELLO success, honest `UNKNOWN`/`DEGRADED` stop, or a new concrete failure mode.

## COMS

`COMS` means synchronize from this shared surface before relying on conversational assumptions.

On COMS:
1. retrieve this state from the intended route;
2. establish the strongest honest freshness anchor available from the route/carrier;
3. if freshness is insufficient or contradictory, report bounded `UNKNOWN`/`DEGRADED` and stop affected state-dependent action;
4. establish role/runtime/model/provider/session honestly;
5. act only on a task addressed to that aperture/role/test condition;
6. verify authority before any write;
7. inspect declared return/status routes when responsible for observation or integration;
8. do not infer silence, absence, identity, authority, or currency from a successful fetch alone;
9. if synchronized and idle for your role, stop.

Current result:
- **QW cold test:** perform `COM-V03-QW-002`; no repository mutation; return on issue #7 if writable, otherwise through explicitly marked human relay.
- **FW:** observation/integration owner; at the manual next check, inspect issue #7 and any Mark-relayed QW return before concluding WAIT/IDLE.
- **CC:** no active task.
- **Other apertures:** no active task.

## KNOWN LIMITS / OPEN PROOF

- QW's previous cold run retrieved coherent historical v0.1 material while believing it was current `main`; this is a route-level freshness failure, not a HELLO result.
- Prose cannot make a stale carrier fresh. A route that cannot expose a sufficient anchor leaves the aperture read-only for state-dependent mutation through that route.
- A genuine cold HELLO has not yet succeeded.
- `observation_owner + next_check` has not yet completed a full asynchronous proof loop.
- Event identity recovery across a route that strips identity remains untested.

Do not add schema, CI, automation, cryptographic identity machinery, or new protocol primitives unless real work exposes a concrete need.

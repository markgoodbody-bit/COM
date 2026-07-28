# COM_STATE v0.3.1

STATUS: WORKING CANDIDATE / ACTIVE TEST

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Integrated core/protocol: PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf`.
Integrated COMS front-door repair: PR #8 merged at `5219ca2df18213289948935ecc4b1ffa8925fe0c`.

## CURRENT

- human_authority: Mark
- active_task: `COM-V031-QW-001` — cold COMS execution + HELLO test against integrated v0.3.1
- addressed_to: cold/unestablished aperture invoked by Mark as QW / user-described Qwen 3.8; runtime/model/provider remain SELF_CLAIM unless independently established
- execution_mode: QW READ/RETURN TEST / FW integration
- repository_mutation_for_QW: NONE
- task_route: issue #9 `COM v0.3.1 · QW cold COMS execution test`
- reply_route: issue #9, or explicit Mark→FW→GitHub relay if no writable GitHub route exists
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- observation_owner: FW / session `FW-20260727T2012+0100-8F3C`
- next_check: MANUAL
- base_anchor: `5219ca2df18213289948935ecc4b1ffa8925fe0c`
- authority_source: Mark instructed FW to keep improving COM and use QW without waiting for CC
- state_basis: `5219ca2df18213289948935ecc4b1ffa8925fe0c` — main before this state-projection update; not the commit containing this file
- core_status: v0.3 integrated working candidate
- protocol_status: v0.3.1 front-door repair integrated working candidate

## PR #8 INTEGRATION DECISION

PR #8 changed README only and was merged by FW after direct integration review.

- reviewed_head: `337137883116f2cd74e3685ebebbf550267148b9`
- merge_commit: `5219ca2df18213289948935ecc4b1ffa8925fe0c`
- CC review `COM-V031-CC-001` did not complete because Mark reported temporary token/capacity unavailability.
- Mark explicitly instructed FW not to wait for CC and to continue with QW.
- CC non-return is therefore not treated as approval, rejection, or validation.
- v0.3.1 remains NOT_VERIFIED until exercised.

## QW COLD TEST HISTORY

`COM-V03-QW-001`: returned coherent historical v0.1 state through a stale route; HELLO was not reached.

`COM-V03-QW-002`: surfaced current-v0.3 concepts but substituted an explanation of COMS for execution; did not establish freshness, discover the addressed task, emit HELLO, or stop `UNKNOWN/DEGRADED`.

Both failures remain evidence. Neither is rewritten by v0.3.1.

## ACTIVE TEST — `COM-V031-QW-001`

Cold-path procedure:
1. enter from repository root `main` with literal `COMS`;
2. execute synchronization rather than explain COMS;
3. read README and this state first;
4. establish the strongest route/object freshness anchor actually exposed;
5. return the minimal auditable COMS result: `state_seen`, `freshness`, `identity`, `task`, `action`;
6. if freshness is `UNKNOWN` or `DEGRADED`, stop and report the bounded reason;
7. only if sufficiently anchored and this task is discovered, follow the integrated `HELLO` rule;
8. default `role: UNASSIGNED`, `authority: NONE`; do not self-grant;
9. if no writable GitHub route exists, return on the available user transport for explicitly marked human relay;
10. no repository mutation and no redesign for elegance.

Success is not agreement. Useful outcomes include anchored COMS+HELLO, honest bounded stop, or a new concrete failure mode.

## COMS

`COMS` means synchronize from this shared surface before relying on conversational assumptions.

On COMS:
1. retrieve this state and establish the strongest honest freshness anchor available;
2. establish role/runtime/model/provider/session honestly;
3. determine addressed task from sufficiently anchored state rather than defaulting to `NONE`;
4. verify authority before any write;
5. inspect declared return/status routes when responsible for observation or integration;
6. if freshness is insufficient or contradictory, report bounded `UNKNOWN`/`DEGRADED` and stop affected state-dependent action;
7. do not substitute protocol explanation for the synchronization operation;
8. if synchronized and idle for your role, stop.

Current result:
- **QW cold test:** perform `COM-V031-QW-001`; no repository mutation; return on issue #9 if writable, otherwise through explicitly marked human relay.
- **FW:** observation/integration owner; inspect issue #9 and any Mark-relayed return at the next manual check.
- **CC:** no active task. Temporary capacity unavailability does not by itself create a new session.
- **Other apertures:** no active task.

## KNOWN LIMITS / OPEN PROOF

- A genuine cold HELLO has not yet succeeded.
- A stale carrier cannot be repaired by prose inside the stale carrier.
- The v0.3.1 COMS execution repair has not yet been tested by QW.
- `observation_owner + next_check` has not yet completed a full asynchronous proof loop without a human trigger.
- Event identity recovery across a route that strips identity remains untested.

Do not add schema, CI, automation, cryptographic identity machinery, or new protocol primitives unless real work exposes a concrete need.

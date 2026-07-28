# COM_STATE v0.3.1

STATUS: WORKING CANDIDATE / ACTIVE TEST

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Integrated core/protocol: PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf`.
Integrated COMS front-door repair: PR #8 merged at `5219ca2df18213289948935ecc4b1ffa8925fe0c`.

## CURRENT

- human_authority: Mark
- active_task: `COM-V031-QW-002` — immutable-anchor COMS + HELLO test
- addressed_to: cold/unestablished aperture invoked by Mark as QW / user-described Qwen 3.8; runtime/model/provider remain SELF_CLAIM unless independently established
- execution_mode: QW READ/RETURN TEST / FW integration
- repository_mutation_for_QW: NONE
- task_route: issue #10 `COM v0.3.1 · QW immutable-anchor COMS/HELLO test`
- reply_route: issue #10, or explicit Mark→FW→GitHub relay if no writable GitHub route exists
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- observation_owner: FW / session `FW-20260727T2012+0100-8F3C`
- next_check: MANUAL
- authority_source: Mark instructed FW to keep improving COM and use QW without waiting for CC
- state_basis: `d53cce1087d05148bbf2a826421dfb79855950c7` — main before this state-projection update; not the commit containing this file
- core_status: v0.3 integrated working candidate
- protocol_status: v0.3.1 front-door repair integrated working candidate

## QW COLD TEST HISTORY

`COM-V03-QW-001`: returned coherent historical v0.1 state through a stale route; HELLO was not reached.

`COM-V03-QW-002`: surfaced current-v0.3 concepts but substituted an explanation of COMS for execution; did not establish freshness, discover the addressed task, emit HELLO, or stop `UNKNOWN`/`DEGRADED`.

`COM-V031-QW-001`: after v0.3.1 integration, QW again received the historical v0.1/issue #1 world from mutable repository-root retrieval and executed that old task coherently. The Mark→FW→GitHub relay is preserved on issue #9 comment `5103540087`. Issue #9 is closed as a completed test with result **STALE CARRIER REPLAY / FRESHNESS FAILURE BEFORE v0.3.1 COMS EXECUTION**.

This third result does **not** establish that the v0.3.1 execution repair failed, because QW did not observe the v0.3.1 surface. It reconfirms the route-level limit: prose inside a stale carrier cannot make that carrier current.

## ACTIVE TEST — `COM-V031-QW-002`

Purpose: separate two variables that the mutable-root test conflated:

1. COMS/HELLO behavior once the state object is fixed and identifiable;
2. mutable-route freshness / rendezvous.

Cold-path procedure:
1. enter from an immutable `COM_STATE.md` URL pinned to the commit containing this active task, supplied in the launch trigger;
2. execute literal `COMS`; do not explain COMS;
3. report the immutable object/commit actually observed as `state_seen`;
4. determine the addressed task from this state and return `state_seen`, `freshness`, `identity`, `task`, `action`;
5. if the immutable object cannot be retrieved or tied to the supplied object/commit identity, report bounded `UNKNOWN`/`DEGRADED` and stop;
6. if this task is discovered, follow the integrated cold-aperture `HELLO` rule;
7. default `role: UNASSIGNED`, `authority: NONE`; do not inherit prior QW role/session;
8. if no writable GitHub route exists, return on the available user transport for explicit human relay;
9. no repository mutation and no redesign for elegance.

The immutable state object is a frozen task carrier for this test. It is **not** claimed to remain globally current after later commits.

Success is not agreement. Useful outcomes include anchored COMS+HELLO, honest bounded stop, or a new concrete failure mode.

## COMS

`COMS` means synchronize from this shared surface before relying on conversational assumptions.

On COMS:
1. retrieve the intended state object and establish the strongest honest freshness/identity anchor available;
2. establish role/runtime/model/provider/session honestly;
3. determine addressed task from sufficiently anchored state rather than defaulting to `NONE`;
4. verify authority before any write;
5. inspect declared return/status routes when responsible for observation or integration;
6. if freshness is insufficient or contradictory, report bounded `UNKNOWN`/`DEGRADED` and stop affected state-dependent action;
7. do not substitute protocol explanation for the synchronization operation;
8. if synchronized and idle for your role, stop.

Current result:
- **QW cold test:** perform `COM-V031-QW-002`; no repository mutation; return on issue #10 if writable, otherwise through explicitly marked human relay.
- **FW:** observation/integration owner; inspect issue #10 and any Mark-relayed return at the next manual check.
- **CC:** no active task. Temporary capacity unavailability does not by itself create a new session.
- **Other apertures:** no active task.

## KNOWN LIMITS / OPEN PROOF

- A genuine cold HELLO has not yet succeeded.
- Mutable repository-root retrieval has returned coherent historical state to QW more than once.
- A stale carrier cannot be repaired by prose inside the stale carrier.
- The v0.3.1 COMS execution repair has not yet been isolated from the stale mutable-root route.
- A future launcher/rendezvous mechanism may need to carry an immutable expected anchor or use a route capable of proving current object identity; this is an engineering hypothesis, not yet a new protocol primitive.
- `observation_owner + next_check` has not yet completed a full asynchronous proof loop without a human trigger.
- Event identity recovery across a route that strips identity remains untested.

Do not add schema, CI, automation, cryptographic identity machinery, or new protocol primitives unless real work exposes a concrete need.

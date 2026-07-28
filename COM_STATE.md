# COM_STATE v0.3.1

STATUS: WORKING CANDIDATE / ACTIVE TEST

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Integrated core/protocol: PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf`.
Integrated COMS front-door repair: PR #8 merged at `5219ca2df18213289948935ecc4b1ffa8925fe0c`.

## CURRENT

- human_authority: Mark
- active_task: `COM-V031-QW-005` — fixed rendezvous -> immutable COM_STATE -> COMS + HELLO chain
- addressed_to: fresh QW aperture/session for this probe; runtime/model/provider remain SELF_CLAIM unless independently established
- execution_mode: QW READ/RETURN RENDEZVOUS-CHAIN TEST / FW integration
- repository_mutation_for_QW: NONE
- task_route: issue #13 `COM v0.3.1 · fixed rendezvous to immutable COMS chain`
- reply_route: issue #13, or explicit Mark→FW→GitHub relay if QW has no writable GitHub route
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- observation_owner: FW / session `FW-20260727T2012+0100-8F3C`
- next_check: MANUAL
- authority_source: Mark instructed FW to keep improving COM and use QW without waiting for CC
- state_basis: `b0ddef2f5eea26cb1ae2eae7d4284ab1f27fd3d1` — main before this projection update; not the commit containing this file
- core_status: v0.3 integrated working candidate
- protocol_status: v0.3.1 front-door repair integrated working candidate

## PROVED BEHAVIOR SO FAR

### Immutable bootstrap — `COM-V031-QW-002`

QW entered through immutable `COM_STATE.md @ d60e64df42b2e9edd0191f16e42ecbf3f8bea2f6`, executed COMS, discovered the addressed task, and emitted HELLO with fresh session, `role: UNASSIGNED`, `authority: NONE`. Preserved on issue #10. Classification: **ANCHORED COMS + TASK DISCOVERY + HELLO SUCCESS ON IMMUTABLE CARRIER**. Behavioral evidence, not validation.

### Multi-route launch — `COM-V031-QW-003`

The intended task was not entered; QW reverted to historical v0.1 / issue #1. Preserved on issue #11. Classification: **LAUNCH-SURFACE REVERSION / TASK NOT ENTERED**. No candidate route was actually tested.

### Fixed head pointer — `COM-V031-QW-004`

QW directly retrieved:
`https://api.github.com/repos/markgoodbody-bit/COM/commits/main`

QW reported `sha_seen: b0ddef2f5eea26cb1ae2eae7d4284ab1f27fd3d1`. FW independently observed the same live `main` head at that boundary. Preserved on issue #12 comment `5103782440`.

Classification: **USABLE RENDEZVOUS POINTER AT THAT OBSERVATION BOUNDARY**. This establishes one working fixed public route for discovering the changing main-head identity without Mark carrying the SHA manually. It does not prove future availability or freshness.

## ACTIVE TEST — `COM-V031-QW-005`

Purpose: prove the complete stable rendezvous chain without Mark carrying a changing SHA.

Stable rendezvous route:
`https://api.github.com/repos/markgoodbody-bit/COM/commits/main`

Cold procedure:
1. retrieve the stable rendezvous route and read its exact top-level `sha`;
2. construct `https://github.com/markgoodbody-bit/COM/blob/<sha>/COM_STATE.md`;
3. retrieve that immutable state object;
4. execute literal COMS from the immutable state; do not navigate through repository root;
5. report `state_seen`, `freshness`, `identity`, `task`, `action`;
6. if this addressed task is discovered, emit HELLO with a fresh session, `role: UNASSIGNED`, `authority: NONE`, and honest runtime/model/provider basis;
7. if any step cannot be anchored, stop `UNKNOWN`/`DEGRADED` there rather than falling back to mutable root;
8. no mutation and no redesign.

Human launch discipline for this test:
- provide only the fixed rendezvous URL;
- provide the stable generic instruction: `Resolve current main SHA, open COM_STATE.md at that exact SHA, then COMS.`
- do not provide a changing SHA, task ID, issue number, or expected result.

Success chain:
`fixed rendezvous URL -> live main SHA -> immutable COM_STATE -> task discovery -> COMS -> HELLO`

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
- **QW:** perform `COM-V031-QW-005`; no repository mutation; return on issue #13 if writable, otherwise through explicit human relay.
- **FW:** observation/integration owner; independently compare rendezvous SHA and inspect the returned chain.
- **CC:** no active task. Temporary capacity unavailability does not by itself create a new session.
- **Other apertures:** no active task.

## KNOWN LIMITS / OPEN PROOF

- Mutable repository-root retrieval has repeatedly returned coherent historical state to QW.
- Immutable COM_STATE bootstrap has succeeded once with QW.
- The fixed commits API exposed the correct live `main` SHA once to QW and independently to FW.
- The complete fixed-rendezvous -> immutable-state -> COMS chain has not yet been demonstrated.
- `observation_owner + next_check` has not yet completed a full asynchronous proof loop without a human trigger.
- Event identity recovery across a route that strips identity remains untested.

Do not add schema, CI, automation, cryptographic identity machinery, or new protocol primitives unless real work exposes a concrete need.
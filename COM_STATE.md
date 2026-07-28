# COM_STATE v0.3.1

STATUS: WORKING CANDIDATE / ACTIVE TEST

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Integrated core/protocol: PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf`.
Integrated COMS front-door repair: PR #8 merged at `5219ca2df18213289948935ecc4b1ffa8925fe0c`.

## CURRENT

- human_authority: Mark
- active_task: `COM-V031-QW-004` — single-route `main` head API probe
- addressed_to: fresh QW aperture/session for this probe; runtime/model/provider remain SELF_CLAIM unless independently established
- execution_mode: QW READ/RETURN SINGLE-ROUTE PROBE / FW integration
- repository_mutation_for_QW: NONE
- task_route: issue #12 `COM v0.3.1 · single-route main-head probe`
- reply_route: issue #12, or explicit Mark→FW→GitHub relay if QW has no writable GitHub route
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- observation_owner: FW / session `FW-20260727T2012+0100-8F3C`
- next_check: MANUAL
- authority_source: Mark instructed FW to keep improving COM and use QW without waiting for CC
- state_basis: `d64531a9645f345a9ef8c8b0fcfa49c0353515c9` — main before this projection update; not the commit containing this file
- core_status: v0.3 integrated working candidate
- protocol_status: v0.3.1 front-door repair integrated working candidate

## IMMUTABLE BOOTSTRAP RESULT — `COM-V031-QW-002`

COMS + task discovery + HELLO succeeded when QW entered through immutable `COM_STATE.md @ d60e64df42b2e9edd0191f16e42ecbf3f8bea2f6`.

Preserved on issue #10:
- QW return relay comment `5103644884`;
- FW WELCOME comment `5103647861`;
- issue #10 closed completed.

Classification: **ANCHORED COMS + TASK DISCOVERY + HELLO SUCCESS ON IMMUTABLE CARRIER**. Behavioral evidence, not validation.

## RENDEZVOUS TEST `COM-V031-QW-003` — TASK NOT ENTERED

QW was launched toward immutable `COM_STATE.md @ d64531a9645f345a9ef8c8b0fcfa49c0353515c9`, but the returned witness contained no reference to that anchor, issue #11, or candidate routes A-D. It reproduced the historical v0.1 / issue #1 world instead.

Preserved on issue #11 comment `5103715997`.

Classification: **LAUNCH-SURFACE REVERSION / TASK NOT ENTERED**. This is not evidence for or against any candidate route because the route probe never ran. Issue #11 is closed. No silent retry under identical conditions.

## ACTIVE TEST — `COM-V031-QW-004`

Purpose: test one stable rendezvous candidate directly, without repo-root navigation, COMS execution, issue discovery, or multi-route branching.

Route under test:
`https://api.github.com/repos/markgoodbody-bit/COM/commits/main`

QW procedure:
1. use a fresh QW session;
2. retrieve only that route;
3. return retrieval `SUCCESS|FAIL`, the exact top-level `sha` if any, the exact route, and bounded access limits;
4. do not navigate to repository root, summarize COM, infer causes, or mutate anything.

FW will compare QW's `sha_seen` independently against the live GitHub `main` head at the observation boundary.

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
- **QW:** perform `COM-V031-QW-004`; no repository mutation; return on issue #12 if writable, otherwise through explicit human relay.
- **FW:** observation/integration owner; compare returned SHA with live GitHub `main` head.
- **CC:** no active task. Temporary capacity unavailability does not by itself create a new session.
- **Other apertures:** no active task.

## KNOWN LIMITS / OPEN PROOF

- Mutable repository-root retrieval has repeatedly returned coherent historical state to QW.
- Immutable COM_STATE bootstrap has succeeded once with QW.
- A later immutable launch reverted to stale v0.1 before the intended route probe was entered; cause remains unresolved.
- A stable mutable rendezvous route that exposes a trustworthy current immutable anchor has not yet been established.
- `observation_owner + next_check` has not yet completed a full asynchronous proof loop without a human trigger.
- Event identity recovery across a route that strips identity remains untested.

Do not add schema, CI, automation, cryptographic identity machinery, or new protocol primitives unless real work exposes a concrete need.
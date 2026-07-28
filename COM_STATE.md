# COM_STATE v0.3.1

STATUS: WORKING CANDIDATE / ACTIVE TEST

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Integrated core/protocol: PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf`.
Integrated COMS front-door repair: PR #8 merged at `5219ca2df18213289948935ecc4b1ffa8925fe0c`.

## CURRENT

- human_authority: Mark
- active_task: `COM-V031-QW-003` — rendezvous route probe
- addressed_to: QW aperture / fresh session for this probe; runtime/model/provider remain SELF_CLAIM unless independently established
- execution_mode: QW READ/RETURN ROUTE PROBE / FW integration
- repository_mutation_for_QW: NONE
- task_route: issue #11 `COM v0.3.1 · rendezvous route probe`
- reply_route: issue #11, or explicit Mark→FW→GitHub relay if QW has no writable GitHub route
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- observation_owner: FW / session `FW-20260727T2012+0100-8F3C`
- next_check: MANUAL
- authority_source: Mark instructed FW to keep improving COM and use QW without waiting for CC
- state_basis: `d60e64df42b2e9edd0191f16e42ecbf3f8bea2f6` — main before this projection update; not the commit containing this file
- core_status: v0.3 integrated working candidate
- protocol_status: v0.3.1 front-door repair integrated working candidate

## IMMUTABLE BOOTSTRAP RESULT — `COM-V031-QW-002`

COMS + task discovery + HELLO succeeded when QW entered through immutable `COM_STATE.md @ d60e64df42b2e9edd0191f16e42ecbf3f8bea2f6`.

Preserved on issue #10:
- QW return relay comment `5103644884`;
- FW WELCOME comment `5103647861`;
- issue #10 closed completed.

Observed:
- QW reported `freshness: ANCHORED:d60e64df42b2e9edd0191f16e42ecbf3f8bea2f6`;
- QW discovered `COM-V031-QW-002`;
- QW emitted HELLO `QW-HELLO-1b409699e2de` with `role: UNASSIGNED`, `authority: NONE`, fresh session `QW-7f050b6dc575`;
- FW observed the relayed HELLO and WELCOME'd it without granting role or authority;
- QW separately observed the mutable repository root still rendering historical v0.1-era material during the same session.

Classification: **ANCHORED COMS + TASK DISCOVERY + HELLO SUCCESS ON IMMUTABLE CARRIER**. This is behavioral evidence, not validation. It does not solve mutable rendezvous.

## ACTIVE TEST — `COM-V031-QW-003`

Purpose: identify whether any stable public route can recover a current immutable state anchor without Mark carrying the changing commit SHA.

Launch discipline:
1. enter this active task through the immutable `COM_STATE.md` URL supplied by Mark;
2. inspect issue #11;
3. probe only the candidate routes named there;
4. report retrieval, state/version seen, exposed commit/object identity, anchor adequacy, discrepancies and access limits;
5. do not infer causes of stale results;
6. do not mutate or redesign COM.

Candidate routes are defined in issue #11. The result should classify each as `USABLE RENDEZVOUS CANDIDATE`, `NO USABLE CANDIDATE`, or `DEGRADED/INCONCLUSIVE`.

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
- **QW:** perform `COM-V031-QW-003`; no repository mutation; return on issue #11 if writable, otherwise through explicit human relay.
- **FW:** observation/integration owner; inspect issue #11 and any Mark-relayed return at the next manual check.
- **CC:** no active task. Temporary capacity unavailability does not by itself create a new session.
- **Other apertures:** no active task.

## KNOWN LIMITS / OPEN PROOF

- Mutable repository-root retrieval has repeatedly returned coherent historical state to QW.
- Immutable COM_STATE bootstrap has succeeded once with QW.
- A stable mutable rendezvous route that exposes a trustworthy current immutable anchor has not yet been established.
- `observation_owner + next_check` has not yet completed a full asynchronous proof loop without a human trigger.
- Event identity recovery across a route that strips identity remains untested.

Do not add schema, CI, automation, cryptographic identity machinery, or new protocol primitives unless real work exposes a concrete need.

# COM_STATE v0.3.1 candidate review

STATUS: WORKING CANDIDATE / ACTIVE

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Integrated core/protocol: PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf`.

## CURRENT

- human_authority: Mark
- active_task: `COM-V031-CC-001` — bounded review of the COMS execution-interface repair
- addressed_to: CC / continuing session `CC-20260727T2020+0100-0C60` if still active; otherwise fresh CC session must identify itself honestly
- execution_mode: CC READ-ONLY REVIEW / FW sole candidate mutation
- candidate_branch: `framework/com-v0.3.1-coms-execution`
- candidate_head: `337137883116f2cd74e3685ebebbf550267148b9`
- pull_request: PR #8 `COM v0.3.1: make COMS execute before explaining`
- candidate_mutator: FW only
- repository_mutation_for_CC: NONE
- reply_route: PR #8 conversation
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- observation_owner: FW / session `FW-20260727T2012+0100-8F3C`
- next_check: `2026-07-28 13:00 Europe/London` — Mark reports CC capacity returns then; this is a capacity/route bound, not a session-boundary claim
- authority_source: Mark instructed FW to keep improving COM and proceed with CC and QW
- state_basis: `6645cd7b135c40f46c8641501957b6696a58f53f` — main head before this projection update; not the commit containing this file
- core_status: v0.3 integrated working candidate
- protocol_status: v0.3 integrated working candidate

## QW COLD TEST `COM-V03-QW-002` — RETURNED / NEW FAILURE

Return is preserved on issue #7 as Mark→FW→GitHub relay comment `5103022965`.

Observed result:
- QW surfaced current-v0.3 concepts including freshness anchoring, `UNASSIGNED`, `authority: NONE`, and navigation != freshness;
- QW did not provide a route/object freshness anchor;
- QW did not report `UNKNOWN` or `DEGRADED`;
- QW did not discover/execute active task `COM-V03-QW-002`, locate issue #7, emit HELLO, or return the required bounded stop;
- instead it substituted a generic explanation of COM/COMS for the synchronization operation.

Classification: **TASK-DISCOVERY / EXECUTION failure after current-protocol orientation**. This differs from the earlier stale-v0.1 route failure. Exact files/routes QW actually retrieved remain NOT_VERIFIED.

## ACTIVE REVIEW — `COM-V031-CC-001`

Review PR #8 head `337137883116f2cd74e3685ebebbf550267148b9` only.

Current route/capacity state:
- Mark reports CC has reached its token limit and becomes available again at 13:00 Europe/London;
- this is temporary capacity unavailability, not evidence of a new session;
- no review return is expected before that bound;
- candidate mutation remains frozen while waiting.

Check whether the README-only repair:
- correctly makes literal `COMS` operational rather than explanatory;
- requires `COM_STATE.md` before concluding `task: NONE`;
- makes the minimal COMS return useful without creating ceremony or a second protocol source;
- preserves the distinction between freshness anchoring and merely printing an anchor-shaped field;
- does not accidentally require mutation or HELLO when freshness is `UNKNOWN`/`DEGRADED`;
- remains a narrow interface repair rather than new ontology.

Deliverable: bounded `BREAK / NARROW / RETAIN` delta on PR #8. Do not redesign for elegance. No mutation.

## COMS

`COMS` means synchronize from this shared surface before relying on conversational assumptions.

On COMS:
1. retrieve this state from the intended route and establish the strongest honest freshness anchor available;
2. establish role/runtime/model/provider/session honestly;
3. act only on a task addressed to that aperture/role/test condition;
4. inspect declared return/status routes when responsible for observation or integration;
5. verify authority before any write;
6. if freshness is insufficient or contradictory, report bounded `UNKNOWN`/`DEGRADED` and stop affected state-dependent action;
7. do not infer `task: NONE`, silence, absence, identity, authority, or currency from a successful fetch alone;
8. if synchronized and idle for your role, stop.

Current result:
- **CC:** `WAIT-CAPACITY` until the reported 13:00 Europe/London availability bound, then perform `COM-V031-CC-001`; review PR #8; return on PR #8; no mutation.
- **FW:** keep candidate frozen; at/after the bound or on an earlier observed CC return, inspect PR #8 and integrate or reject.
- **QW:** no active task during CC review. Next cold test should occur only after a reviewed repair is integrated, if integration occurs.
- **Other apertures:** no active task.

## KNOWN LIMITS / OPEN PROOF

- QW cold run 1 reproduced a coherent stale-route failure before HELLO.
- QW cold run 2 reached current protocol concepts but did not execute live COMS/task discovery.
- A genuine cold HELLO has not yet succeeded.
- A stale carrier cannot be repaired by prose inside the stale carrier.
- `observation_owner + next_check` has not yet completed a full asynchronous proof loop.
- Event identity recovery across a route that strips identity remains untested.

Do not add schema, CI, automation, cryptographic identity machinery, or new protocol primitives unless real work exposes a concrete need.

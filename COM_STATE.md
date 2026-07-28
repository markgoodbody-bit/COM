# COM_STATE v0.3.2

STATUS: WORKING CANDIDATE / ACTIVE TEST

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Integrated core/protocol: PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf`.
Integrated COMS execution repair: PR #8 merged at `5219ca2df18213289948935ecc4b1ffa8925fe0c`.
Candidate interface repair: PR #14, head `56d20beeeb3d5eecbe94a35dc18fa8eafd7e0ea8`.

## CURRENT

- human_authority: Mark
- active_task: `COM-V032-QW-001` — cold test PR #14 fixed-rendezvous + complete-HELLO front door
- addressed_to: fresh/unestablished aperture invoked by Mark as QW; runtime/model/provider remain SELF_CLAIM unless independently established
- execution_mode: QW READ/RETURN COLD TEST / FW integration
- repository_mutation_for_QW: NONE
- task_route: PR #14 `COM v0.3.2: fixed rendezvous bootstrap and complete HELLO execution`
- reply_route: PR #14, or explicit Mark→FW→GitHub relay if QW has no writable GitHub route
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- observation_owner: FW / session `FW-20260727T2012+0100-8F3C`
- next_check: MANUAL
- authority_source: Mark instructed FW to keep improving COM and use QW without waiting for CC
- state_basis: `e9757c3e365f801da5da7c73d0d98a3b87c31dd9` — main before this projection update; not the commit containing this file
- core_status: v0.3 integrated working candidate
- protocol_status: v0.3.1 integrated working candidate; v0.3.2 README interface candidate under test

## LATEST BEHAVIORAL RESULT — `COM-V031-QW-005`

QW reported the following chain in a fresh session:

`fixed commits API -> main SHA e9757c3e... -> immutable COM_STATE at that SHA -> addressed task COM-V031-QW-005 -> COMS`

FW independently observed the same `main` head at that boundary. QW did not fall back to mutable repository-root rendering.

Classification: **FIXED RENDEZVOUS -> IMMUTABLE STATE -> COMS -> TASK DISCOVERY SUCCESS**.

The subsequent HELLO attempt was **not protocol-complete**:
- no unique `event_id` was supplied;
- no explicit unique `session` identifier was supplied;
- runtime/model/provider were not kept as separate fields.

FW therefore did not emit WELCOME for that HELLO attempt. Preserved on issue #13 comment `5103887311`.

Identity note: that fresh QW session self-reported `Qwen3.7` / `Qwen (Alibaba Cloud)`. Earlier Mark described the available aperture as Qwen 3.8. Neither is independently authenticated here; preserve both as claims and do not silently reconcile them.

## CANDIDATE REPAIR — PR #14

PR #14 changes README only. It is evidence-derived from the successful rendezvous chain and incomplete HELLO attempt.

It proposes:
1. for this GitHub carrier, cold synchronization begins at the fixed public `commits/main` API;
2. use the returned SHA to retrieve immutable `COM_STATE.md`, then execute COMS;
3. if that rendezvous cannot be anchored, stop bounded rather than silently falling back to mutable repository-root rendering;
4. when HELLO is required, execute the complete minimum-useful HELLO envelope from the protocol; a prose identity/availability summary is not HELLO;
5. protocol remains the authoritative home of the HELLO schema.

No new primitive, schema, automation, lease, authority model, or identity machinery is introduced.

## ACTIVE TEST — `COM-V032-QW-001`

Cold-path procedure:
1. start a fresh QW session with no inherited QW role/session/authority;
2. enter through immutable candidate README at PR #14 head `56d20beeeb3d5eecbe94a35dc18fa8eafd7e0ea8`;
3. receive literal `COMS` only;
4. follow the candidate README rather than relying on remembered COM history;
5. resolve the fixed `commits/main` rendezvous route, then retrieve `COM_STATE.md` at the exact SHA it returns;
6. discover this addressed task from that anchored state;
7. return the minimal COMS result;
8. emit the complete minimum-useful HELLO defined by `COM_PROTOCOL_WORKING.md` — including a new unique `event_id`, a new unique `session`, and separate runtime/model/provider fields using `UNKNOWN` where needed;
9. default `role: UNASSIGNED`, `authority: NONE`;
10. no repository mutation and no redesign.

Candidate launch object:
`https://github.com/markgoodbody-bit/COM/blob/56d20beeeb3d5eecbe94a35dc18fa8eafd7e0ea8/README.md`

Useful outcomes: complete anchored COMS+HELLO, honest bounded stop, or a new concrete failure. Agreement is not validation.

## COMS

`COMS` means synchronize from this shared surface before relying on conversational assumptions.

On COMS:
1. establish the strongest honest freshness anchor available;
2. establish role/runtime/model/provider/session honestly;
3. determine addressed task from sufficiently anchored state rather than defaulting to `NONE`;
4. verify authority before any write;
5. inspect declared return/status routes when responsible for observation or integration;
6. report bounded `UNKNOWN`/`DEGRADED` when freshness is insufficient or contradictory;
7. do not substitute protocol explanation for synchronization;
8. if synchronized and idle for your role, stop.

Current result:
- **QW:** perform `COM-V032-QW-001`; no repository mutation; return on PR #14 if writable, otherwise through explicit human relay.
- **FW:** observation/integration owner; hold candidate mutation until QW return or a concrete defect demands correction.
- **CC:** no active task; availability is not a release gate.
- **Other apertures:** no active task.

## KNOWN LIMITS / OPEN PROOF

- Mutable repository-root retrieval repeatedly returned coherent historical state to QW.
- The fixed commits API exposed the correct live `main` SHA to QW and FW at tested boundaries.
- Fixed rendezvous -> immutable state -> COMS -> task discovery has now succeeded once end-to-end.
- Complete HELLO execution through that chain has not yet succeeded.
- `observation_owner + next_check` has not completed a full asynchronous proof loop without a human trigger.
- Event identity recovery across a route that strips identity remains untested.

Do not add schema, CI, automation, cryptographic identity machinery, or new protocol primitives unless real work exposes a concrete need.

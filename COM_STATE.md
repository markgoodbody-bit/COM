# COM_STATE v0.3.2

STATUS: WORKING CANDIDATE / ACTIVE TEST

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Integrated core/protocol: PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf`.
Integrated COMS execution repair: PR #8 merged at `5219ca2df18213289948935ecc4b1ffa8925fe0c`.
Candidate interface repair: PR #14, revised head `b012ecd260250ae355b01160fa2723697f607593`.

## CURRENT

- human_authority: Mark
- active_task: `COM-V032-QW-002` — independent cold re-test of revised PR #14 candidate
- addressed_to: fresh/unestablished aperture invoked by Mark as QW; runtime/model/provider remain SELF_CLAIM unless independently established
- execution_mode: QW READ/RETURN COLD TEST / FW integration
- repository_mutation_for_QW: NONE
- task_route: PR #14 `COM v0.3.2: fixed rendezvous bootstrap and complete HELLO execution`
- reply_route: PR #14, or explicit Mark→FW→GitHub relay if QW has no writable GitHub route
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- observation_owner: FW / session `FW-20260727T2012+0100-8F3C`
- next_check: MANUAL
- authority_source: Mark instructed FW to keep improving COM and use QW; CC is reviewer, not release gate
- state_basis: `2de5ec3f5e76055f420dda0959bcda6bfe9ffc3a` — main before this projection update; not the commit containing this file
- core_status: v0.3 integrated working candidate
- protocol_status: v0.3.1 integrated working candidate; v0.3.2 README interface candidate under independent re-test

## QW COLD RESULT — `COM-V032-QW-001`

QW returned through explicit Mark→FW relay after entering the immutable candidate README at former PR #14 head `56d20beeeb3d5eecbe94a35dc18fa8eafd7e0ea8`.

Observed chain:
`candidate README -> fixed commits/main rendezvous -> main SHA 85e09530114f37ad52cb2261d434b62fab01890c -> immutable COM_STATE -> task COM-V032-QW-001 -> COMS -> complete HELLO`

FW independently observed the same live `main` head at that boundary. HELLO used a new event ID/session, `role: UNASSIGNED`, `authority: NONE`, separate runtime/model/provider fields, anchored state/freshness, and no mutation authority.

Preserved on PR #14 comments `5104097880` and `5104101255`.

Classification: **COLD FIXED-RENDEZVOUS -> IMMUTABLE STATE -> COMS -> TASK DISCOVERY -> PROTOCOL-COMPLETE HELLO SUCCESS**. Behavioral evidence only, not validation.

Evidence limit: the PR preserves QW's output and FW's intended launch discipline, but FW did not directly observe the actual QW input surface. Do not claim verbatim-input provenance retroactively.

## CC HOSTILE REVIEW — `COM-V032-CC-001`

CC returned on PR #14 comment `5104520792` from session `CC-20260727T2020+0100-0C60`, reviewer condition `CORRELATED`, mutation `NONE`.

Verdict: **NARROW — no BREAK**.

Integrated at revised candidate head `b012ecd260250ae355b01160fa2723697f607593`:
- stale-README self-bootstrap limit made explicit;
- rendezvous generalized from hard-coded upstream to `<owner>/<repo>` with fork/mirror binding;
- GitHub API rate-limit/access failure named as bounded route unavailability, without adding an untested fallback;
- `task: NOT_ESTABLISHED` defined distinctly from `task: NONE`.

N4 retained as evidence discipline rather than README rule: future cold tests should preserve the exact launch input alongside the return, or mark actual input as not independently observed.

Carry-forward still open: the auditable COMS return remains descriptive rather than globally mandatory; do not change that casually inside a README-only patch because normative ownership belongs with the protocol.

FW integration comment: PR #14 `5104607968`.

## ACTIVE TEST — `COM-V032-QW-002`

Candidate launch object:
`https://github.com/markgoodbody-bit/COM/blob/b012ecd260250ae355b01160fa2723697f607593/README.md`

Cold procedure:
1. start a fresh QW session with no inherited QW role/session/authority;
2. give it the immutable candidate README URL above plus literal `COMS` only;
3. preserve the exact launch input that was actually sent alongside the returned output; if actual input cannot be independently established, say so;
4. follow the candidate README to derive the GitHub repository coordinates and fixed `commits/main` rendezvous;
5. resolve current `main`, retrieve immutable `COM_STATE.md` at that SHA, and execute COMS;
6. discover this addressed task from anchored state;
7. return the minimal COMS result;
8. emit the complete minimum-useful HELLO defined by `COM_PROTOCOL_WORKING.md`, with new unique `event_id`, new unique `session`, separate runtime/model/provider fields, `role: UNASSIGNED`, `authority: NONE`, and `UNKNOWN` where needed;
9. no repository mutation and no redesign.

Success is behavioral only:
`candidate README -> repository-bound fixed rendezvous -> live main SHA -> immutable state -> task discovery -> COMS -> complete HELLO`

A bounded `UNKNOWN`/`DEGRADED` stop or any new concrete failure is useful evidence.

## COMS

`COMS` means synchronize from shared COM before relying on conversational assumptions.

Current result:
- **QW:** perform `COM-V032-QW-002`; no mutation; return on PR #14 if writable, otherwise through explicit Mark relay.
- **CC:** review complete; no active task; no mutation authority.
- **FW:** observation/integration owner; inspect return route before declaring wait/idle and integrate the result without treating agreement as validation.
- **Other apertures:** no active task.

## KNOWN LIMITS / OPEN PROOF

- A stale carrier cannot be repaired by prose inside the stale copy it already served.
- The fixed public GitHub `commits/main` API has exposed the live main SHA to QW at multiple tested boundaries; this does not prove future availability or cross-provider portability.
- GitHub REST rate limiting can make the fixed API route temporarily unavailable; bounded stop remains preferable to silently reverting to stale mutable-root state.
- The revised repository-bound rendezvous candidate has not yet been independently cold-tested.
- `observation_owner + next_check` has not yet completed a full asynchronous proof loop without a human trigger.
- Event identity recovery across a route that strips identity remains untested.

Do not add schema, CI, automation, cryptographic identity machinery, leases, or new protocol primitives unless real work exposes a concrete need.
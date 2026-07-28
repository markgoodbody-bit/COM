# COM_STATE v0.3.2

STATUS: WORKING CANDIDATE / ACTIVE ROUTE DIAGNOSTIC

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Integrated core/protocol baseline: PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf`.
Integrated COMS execution repair: PR #8 merged at `5219ca2df18213289948935ecc4b1ffa8925fe0c`.
Current v0.3.2 candidate: PR #14, head `3215f9e41601b6ec4e6854bd441770d38b892dec`.

## CURRENT

- human_authority: Mark
- active_task: `COM-V032-QW-004` — repeat single-route `main` head probe after stale historical-task replay
- addressed_to: fresh QW aperture/session for this diagnostic; runtime/model/provider remain SELF_CLAIM unless independently established
- execution_mode: QW READ/RETURN SINGLE-ROUTE DIAGNOSTIC / FW integration
- repository_mutation_for_QW: NONE
- task_route: issue #15 `COM v0.3.2 · repeat single-route main-head probe after stale replay`
- reply_route: issue #15, or explicit Mark→FW→GitHub relay if QW has no writable GitHub route
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- observation_owner: FW / session `FW-20260727T2012+0100-8F3C`
- next_check: MANUAL
- authority_source: Mark instructed FW to keep improving COM and use QW; CC is reviewer, not release gate
- state_basis: `af22b131331bdac617cb7ed5c0f16407e01ec218` — main before this projection update; this file is not self-authenticating freshness
- core_status: v0.3 integrated working candidate
- protocol_status: v0.3.1 integrated on main; v0.3.2 candidate narrowed after CC review and awaiting renewed independent route/cold testing

## CC REVIEW — `COM-V032-CC-002`

CC returned on PR #14 comment `5104809158` from session `CC-20260727T2020+0100-0C60`, reviewer condition `CORRELATED`, mutation `NONE`.

Verdict: **NARROW — no BREAK**.

CC itself emitted the new COMS completion block and noted that the detector immediately exposed its earlier private-channel COMS returns as unaudited.

Integrated at candidate head `3215f9e41601b6ec4e6854bd441770d38b892dec`:
- COMS completion separates `role`, `session`, `runtime`, `model`, and `provider`; no merged `identity:` field;
- missing bounded result means completion is `NOT_ESTABLISHED` from that return, not refusal/absence/failure;
- any re-request is a new visible invocation/event, never a silent retry;
- literal `COMS` carries the bounded-result requirement across transports, including private operator channels;
- off-route results preserve their actual transport and relay modality if later carried into COM;
- README summary aligned to the protocol;
- trailing newline was explicitly supplied on the protocol write; continue checking because prior writes regressed it.

CC remains correlated. Agreement is not validation.

## QW RETURN — INTENDED `COM-V032-QW-003`, CURRENT CANDIDATE NOT REACHED

Mark relayed a QW return containing:

```text
COMS
state_seen: b0ddef2f5eea26cb1ae2eae7d4284ab1f27fd3d1
freshness: ANCHORED:b0ddef2f5eea26cb1ae2eae7d4284ab1f27fd3d1
identity: Qwen3.7, AI assistant, fresh session
task: COM-V031-QW-004
action: SUCCESS. Route: https://api.github.com/repos/markgoodbody-bit/COM/commits/main. Exact top-level SHA: b0ddef2f5eea26cb1ae2eae7d4284ab1f27fd3d1. Access limits: none encountered. No repository mutation performed.
```

FW independently observed live `main` at `af22b131331bdac617cb7ed5c0f16407e01ec218` at that boundary. The returned task/anchor pair matches the historical `COM-V031-QW-004` probe preserved on issue #12 at `b0ddef2f...`.

Classification: **STALE / HISTORICAL TASK REPLAY — CURRENT CANDIDATE NOT REACHED**.

Preserved on PR #14 comment `5106075326`.

Do not treat the returned `freshness: ANCHORED:b0ddef...` label as proof of currentness. The claimed anchor contradicts independently observed live state. Cause remains unresolved; do not silently choose among cache/replay, session contamination, retrieval fallback, or another mechanism.

This return is not evidence for or against candidate head `3215f9e...` because that candidate/current state was not reached.

## ACTIVE ROUTE DIAGNOSTIC — `COM-V032-QW-004`

Purpose: isolate whether QW can currently observe the fixed public `main`-head API correctly before another full cold-chain test.

Route:
`https://api.github.com/repos/markgoodbody-bit/COM/commits/main`

QW procedure is recorded on issue #15:
1. fresh QW session;
2. retrieve only the route above;
3. return exact top-level SHA actually observed, success/failure, and bounded access limits;
4. do not navigate to repository root, summarize COM, use remembered prior task/state, or mutate anything.

FW compares `sha_seen` independently to live GitHub `main` at the observation boundary.

This diagnostic is deliberately not COMS. It changes one variable after the stale replay rather than silently retrying the full candidate path.

## COMS

`COMS` means synchronize from shared COM before relying on conversational assumptions.

Current result:
- **QW:** perform `COM-V032-QW-004`; no mutation; return on issue #15 if writable, otherwise through explicit Mark relay.
- **CC:** review complete; no active task; no mutation authority.
- **FW:** observation/integration owner; compare QW route observation against live `main` and integrate without treating agreement as validation.
- **Other apertures:** no active task.

## KNOWN LIMITS / OPEN PROOF

- A stale carrier cannot be repaired by prose inside the stale copy it already served.
- The fixed public GitHub `commits/main` API has previously matched FW/QW at multiple tested boundaries, but the latest QW return claimed a historical head; route stability is therefore under renewed test rather than assumed.
- GitHub REST rate limiting/access failure can make the route unavailable; bounded stop remains preferable to silent stale-root fallback.
- Candidate `3215f9e...` has not yet received a valid independent cold execution after the latest protocol narrowings.
- Exact QW launch-input provenance remains human-mediated unless the input surface itself is preserved/observed.
- `observation_owner + next_check` has not yet completed a full asynchronous proof loop without a human trigger.
- Event identity recovery across a route that strips identity remains untested.

Do not add schema, CI, automation, cryptographic identity machinery, leases, or new protocol primitives unless real work exposes a concrete need.

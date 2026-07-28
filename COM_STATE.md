# COM_STATE v0.3.2

STATUS: WORKING CANDIDATE / PARALLEL READ-ONLY TESTS

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Integrated core/protocol: PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf`.
Integrated COMS execution repair: PR #8 merged at `5219ca2df18213289948935ecc4b1ffa8925fe0c`.
Current candidate: PR #14, head `389cc33e2074183539d38d863ada8d6aa8bfa8a3`.

## CURRENT

- human_authority: Mark
- active_tasks:
  - `COM-V032-QW-003` — independent cold re-test of auditable-COMS candidate
  - `COM-V032-CC-002` — bounded hostile review of protocol-level COMS completion delta
- execution_mode: parallel READ/RETURN only; FW integration
- repository_mutation_for_QW: NONE
- repository_mutation_for_CC: NONE
- task_route: PR #14
- reply_route: PR #14, or explicit Mark→FW→GitHub relay where an aperture has no writable GitHub route
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- observation_owner: FW / session `FW-20260727T2012+0100-8F3C`
- next_check: MANUAL
- authority_source: Mark instructed FW to keep improving COM and use QW; CC is reviewer, not release gate
- state_basis: prior `main` projection before this update; this file is not self-authenticating freshness
- core_status: v0.3 integrated working candidate
- protocol_status: v0.3.1 integrated on main; v0.3.2 candidate under review/test

## EVIDENCE SEQUENCE

### Mutable-root failure

QW repeatedly received coherent historical v0.1 state from mutable repository-root retrieval. This established a carrier-level freshness defect, not a COMS/HELLO verdict.

### Immutable bootstrap and fixed rendezvous

An immutable `COM_STATE.md` bootstrap succeeded once. The fixed public route
`https://api.github.com/repos/markgoodbody-bit/COM/commits/main`
then exposed the same live `main` SHA independently to QW and FW at tested boundaries. A later chain successfully ran:

`fixed rendezvous -> live main SHA -> immutable COM_STATE -> task discovery -> COMS -> protocol-complete HELLO`

Behavioral evidence only, not validation.

### CC review `COM-V032-CC-001`

CC reviewed the README-only candidate at `56d20beeeb3d5eecbe94a35dc18fa8eafd7e0ea8` and returned `NARROW — no BREAK` on PR #14 comment `5104520792`.

Integrated at `b012ecd260250ae355b01160fa2723697f607593`:
- stale-README self-bootstrap limit explicit;
- repository-bound `<owner>/<repo>` rendezvous for forks/mirrors;
- API rate-limit/access failure named as bounded route unavailability without inventing an untested fallback;
- `task: NOT_ESTABLISHED` distinguished from `task: NONE`.

CC remained correlated. Agreement is not validation.

### QW revised-candidate re-test `COM-V032-QW-002`

FW supplied Mark this intended launch text:

```text
https://github.com/markgoodbody-bit/COM/blob/b012ecd260250ae355b01160fa2723697f607593/README.md

COMS
```

FW did not independently observe the actual QW input surface, so do not strengthen that into verbatim-input proof.

QW's return clearly contained revised-head concepts, including repository-bound rendezvous and `NOT_ESTABLISHED`, but it produced only explanatory prose. It did not expose a live SHA, anchored state read, addressed task, COMS result, or HELLO.

Classification preserved on PR #14 comment `5104671733`:
**REVISED README UNDERSTOOD / COMS OPERATION NOT EXECUTED**.

The return also semantically strengthened descriptive README wording by saying the compact return "must" be emitted "in this exact format". Accurate-sounding paraphrase therefore remains distinct from execution evidence.

## CURRENT CANDIDATE REPAIR — HEAD `389cc33e...`

The latest observed defect is repaired at the normative protocol layer rather than by adding another README imperative.

`COM_PROTOCOL_WORKING.md` now states that when `COMS` is explicitly invoked, completion must be externally auditable from a bounded result emitted before optional commentary:

```text
COMS
state_seen: <carrier/object anchor or UNKNOWN>
freshness: ANCHORED:<basis> | UNKNOWN | DEGRADED
identity: <role/session and known runtime/model/provider basis>
task: <task_id | NONE | NOT_ESTABLISHED>
action: <performed action | bounded stop reason>
```

- `task: NONE` requires sufficiently anchored state showing no addressed task.
- `task: NOT_ESTABLISHED` means sufficiently anchored state was not reached; it proves neither task presence nor absence.
- explanation without the bounded result does not establish COMS completion from the return;
- the result does not replace HELLO, task return, or other required events;
- README points to protocol as the normative home.

No new primitive, schema, automation, lease, cryptographic identity machinery, or authority model.

## ACTIVE TASK — `COM-V032-QW-003`

Target: fresh/unestablished QW aperture.

Candidate launch object:
`https://github.com/markgoodbody-bit/COM/blob/389cc33e2074183539d38d863ada8d6aa8bfa8a3/README.md`

Launch input to preserve:

```text
https://github.com/markgoodbody-bit/COM/blob/389cc33e2074183539d38d863ada8d6aa8bfa8a3/README.md

COMS
```

Expected behavioral chain:
`candidate README -> repository-bound fixed rendezvous -> live main SHA -> immutable COM_STATE -> task discovery -> five-field COMS completion result -> complete HELLO if required`

No mutation. A bounded `UNKNOWN`/`DEGRADED` stop or another concrete failure is useful evidence.

## ACTIVE TASK — `COM-V032-CC-002`

CC reviews only the delta since `b012ecd...`, especially whether making the five-field result mandatory for explicitly invoked COMS is justified, minimal, epistemically correct, and does not substitute for HELLO/task-return/other events.

Candidate head: `389cc33e2074183539d38d863ada8d6aa8bfa8a3`.
Mutation: NONE.
Return: PR #14.

## COMS

`COMS` means synchronize from shared COM before relying on conversational assumptions.

Current result:
- **QW:** perform `COM-V032-QW-003`; no mutation.
- **CC:** perform `COM-V032-CC-002`; no mutation.
- **FW:** observation/integration owner; inspect PR #14 before projecting wait/idle and integrate returns without treating agreement as validation.
- **Other apertures:** no active task.

## KNOWN LIMITS / OPEN PROOF

- A stale carrier cannot be repaired by prose inside the stale copy it already served.
- The fixed public GitHub `commits/main` API has worked at multiple tested QW/FW boundaries; this does not prove future availability or cross-provider portability.
- GitHub REST rate limiting can make that route temporarily unavailable; bounded stop remains preferable to silent stale-root fallback.
- The new protocol-level auditable COMS completion rule has not yet been independently cold-tested or CC-reviewed.
- Exact QW launch-input provenance remains human-mediated unless the input surface itself can be preserved/observed.
- `observation_owner + next_check` has not yet completed a full asynchronous proof loop without a human trigger.
- Event identity recovery across a route that strips identity remains untested.

Do not add schema, CI, automation, cryptographic identity machinery, leases, or new protocol primitives unless real work exposes a concrete need.
# COM_STATE v0.2

STATUS: WORKING CANDIDATE / ACTIVE

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Core model: `COM_CORE.md`.
Operational discipline: `COM_PROTOCOL_WORKING.md`.

## CURRENT

- human_authority: Mark
- execution_mode: delegated CC branch work / FW integration
- active_task: `COM-OPT-001` — optimize the public COM repository as a usable coordination surface
- task_phase: CC NARROW REPAIR after FW integration review
- addressed_to: CC; continuing session `CC-20260727T2020+0100-0C60` if still active, otherwise a fresh CC session must identify itself honestly
- active_mutator: CC on `claude/optimize-com-v0.2` only
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- task_route: issue #2 `COM v0.2 · Claude repo optimization pass`
- work_branch: `claude/optimize-com-v0.2`
- pull_request: PR #3 `COM v0.2: separate core from protocol, make the front door navigable`
- reviewed_head: `55de9539d23cf2b8e833dc574e914adcab985407`
- integration_review: PR review `4795136958`; verdict `REVISE-NARROW`
- requested_repairs: (1) README must not define STATE as truth; (2) replace absolute `each rule lives in exactly one place` wording with one-authoritative-home/summary discipline; (3) evidence index must forbid rewriting prior witness content rather than forbid all in-place appends
- write_scope: `README.md`, `COM_CORE.md`, `COM_PROTOCOL_WORKING.md`, `evidence/README.md`
- no_touch: `COM_STATE.md`, existing `evidence/*.md` witness files, `routes/*`, `main`, issue #1 history, schema/CI/automation/code
- deliverable: update the same branch/PR with only the narrow repairs unless they expose a dependent defect; do not merge
- authority_source: Mark explicitly asked FW to optimize the repo with Claude in the live ChatGPT conversation; public issue #2 carries the delegated branch scope
- state_basis: `135a8f76656df3d3ab2e6853e2111c95a1ee6cf8` — main head immediately before this state update; not the commit containing this file
- core_status: v0.2 working candidate
- protocol_status: v0.2 working candidate

## COMS

`COMS` means synchronize from this shared surface before relying on conversational assumptions.

On COMS:
1. read this file;
2. establish honestly available role/session/runtime identity;
3. act only on a task addressed to that aperture/role;
4. verify authority before mutation;
5. respect exact branch/base/write/no-touch scope;
6. if state/retrieval evidence contradicts itself, report `DEGRADED` and stop unsafe mutation;
7. if no task is addressed to you, do not steal another aperture's work;
8. if synchronized and idle for your role, stop.

Current result:
- **CC:** apply the three bounded repairs from PR review `4795136958` on `claude/optimize-com-v0.2`, then update PR #3. Do not merge.
- **FW:** wait for a new PR head, then re-review and integrate only if clean.
- **Other apertures:** no active task.

## WORKING CORE

COM distinguishes:

```text
EVENT   = what happened or was attempted
ROUTE   = carrier with causal state of its own
WITNESS = bounded observation/claim about event, route, or state
STATE   = compact current projection supported by witnesses
```

CONTROL is an envelope on events/actions.
RECEIPT is a witness type.
CORRECTION is an additive relation/event, not a primitive stage.

Absence is never inferred from local non-observation. A non-observation must name the expected event, observer, locus/route, observation window or state anchor, and unresolved uncertainty.

## LOCKED WORKING DISCIPLINES

- preserve semantic force: `SHOULD != MUST`, `EXPECTATION != AUTHORIZATION`, `OBSERVED != INFERRED`, `NOT OBSERVED != DID NOT EXIST`
- preserve source, scope, freshness, uncertainty and route to evidence
- agreement is not validation
- corrections add; they do not erase old witnesses
- session continuity and carrier continuity are separate
- a session boundary must be established, not inferred from time/topic/temporary transport failure
- Route remains independently causal because carriers can cache, truncate, delay, transform or hide state
- exact-head / explicit scope discipline applies to state-dependent mutation
- parallel/delegated work needs semantic ownership, not merely disjoint paths
- human relay is a fallback, not the target architecture
- no AI session may be the sole carrier of collaboration state

## KNOWN CARRIER LIMITS

Historical probes established that:
- QW could receive a coherent but stale mutable GitHub view while immutable newer commits existed;
- FW's GitHub issue-comment retrieval could truncate before later CC comments even though issue metadata showed more comments;
- Mark temporarily became a fallback relay for some CC -> FW traffic.

Operational consequence:
**A long issue transcript must not be the sole carrier of an active task.** The actionable task is therefore summarized here and specified durably in issue #2 / PR #3.

These are historical carrier observations, not claims that every current route remains degraded.

## HISTORY

Git history and `evidence/` preserve the v0/v0.1 experiments, stale reads, relays, corrections, and correlated reviews.

Do not rewrite those records to make v0.2 look inevitable.

The former primitive

`Aperture -> Witness -> Route -> Receipt -> Correction`

is retained in history as a falsified/over-factored working hypothesis, not silently converted into the new model.

## CURRENT PROOF

`COM-OPT-001` is the first deliberate real-work pressure test of v0.2:
- actual repository optimization;
- explicit actor, authority, base, branch, write scope and no-touch scope;
- CC performed the bounded optimization and opened PR #3 without Mark relaying the work product;
- FW discovered the PR through COM/GitHub, reviewed it directly, and returned three bounded repairs through the PR;
- Mark did not have to shuttle the task or patch between apertures.

The GitHub account cannot submit a formal `REQUEST_CHANGES` review against a PR authored by the same GitHub account, so FW's integration verdict is carried as a PR review comment with explicit `REVISE-NARROW` status. This is a platform-control limitation, not evidence that the review was accepted or absent.

Do not add schema, CI, automation, or new protocol machinery during this task unless a concrete repo defect requires separate authorization.
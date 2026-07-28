# COM_STATE v0.3 candidate review

STATUS: WORKING CANDIDATE / ACTIVE

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Core/protocol candidate: PR #6 on `framework/com-v0.3-bootstrap-liveness`.

## CURRENT

- human_authority: Mark
- active_task: `COM-V03-CC-002` — bounded re-review of the revised v0.3 candidate
- execution_mode: CC READ-ONLY REVIEW / FW sole semantic mutation
- addressed_to: CC / continuing session `CC-20260727T2020+0100-0C60` if still active; otherwise a fresh CC session must identify itself honestly
- candidate_mutator: FW on `framework/com-v0.3-bootstrap-liveness` only
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- pull_request: PR #6 `COM v0.3 candidate: cold bootstrap, freshness, delegated-return discovery`
- candidate_head: `9f43dd9a49a914adf1d3824643f90ad40a365ab3`
- original_base_anchor: `f01aee2c7aef35c22d7ad99d02f67cd76aa78682`
- main_has_advanced: YES — state/evidence routing commits only; PR #6 is currently reported mergeable
- reply_route: PR #6 conversation
- review_scope: check whether the revised candidate honestly resolves/narrows the first CC review and QW stale-route finding without creating new ontology or falsely claiming autonomous liveness
- no_touch_for_CC: all files/branches/main/evidence/routes; review only
- deliverable: bounded BREAK / NARROW / RETAIN delta against head `9f43dd9a...`; do not restate already-resolved points unless still defective
- authority_source: Mark explicitly instructed FW to keep improving COM and proceed using CC and QW
- state_basis: `fcb58f553ef6aa6b58038c44e3f2976390baaaee` — main head before this projection update; not the commit containing this file
- core_status: v0.3 revised working candidate / unmerged
- protocol_status: v0.3 revised working candidate / unmerged

## FIRST REVIEW RESULTS — INTEGRATED

### CC hostile review

Return: PR #6 comment `5102333896`.

Accepted pressure:
- PROJECTION was wrongly made a mandatory causal hop;
- return discovery was overstated as liveness;
- HELLO `AVAILABLE` could become stale;
- event identity needed an explicit unpreserved/unknown case;
- identity conflict needed a resolver path;
- EVENT/WITNESS must remain relational;
- IDLE scope, citation stability and newline hygiene needed narrowing.

### QW cold test

Return: Mark→FW→GitHub relay on PR #6 comment `5102459982`.

Observed result:
- QW reported inspecting current `main`, but its `web_extractor` surfaced coherent historical v0.1 state and the old Issue #1 task;
- QW therefore executed the old task and never discovered PR #6 or reached HELLO;
- no direct QW GitHub write was observed;
- runtime/model/provider identity remains self-reported.

Classification: **DEGRADED freshness-route failure**, not a HELLO success/failure.

## REVISED CANDIDATE

The revised candidate now states:

```text
EVENT[CONTROL] --via ROUTE--> observation
                              |
                              v
                           WITNESS
                           /     \
                          v       v
                    next EVENT  PROJECTION update
                                  |
                                  +---- may inform later EVENT
```

Key changes:
- PROJECTION is derived/optional, not a mandatory causal gate;
- mutable labels such as `main`/`latest` and successful retrieval are navigation, not freshness proof;
- freshness is bounded as `ANCHORED:<basis> | UNKNOWN | DEGRADED`;
- state-dependent mutation stops on insufficient/contradictory freshness;
- HELLO records `presence: OBSERVED_AT_HELLO`, not durable availability;
- lost event identity is `UNPRESERVED/UNKNOWN`, not silently treated as new;
- identity conflict routes to an explicit resolver before affected mutation;
- delegated work separates return discovery from scheduling and may carry `observation_owner` + `next_check`; `MANUAL` makes no autonomous-liveness claim;
- IDLE remains bounded to known inspected/carried-forward work.

## COMS

`COMS` means synchronize from this shared surface before relying on conversational assumptions.

On COMS:
1. retrieve this state from the intended route and establish the strongest honest freshness anchor available;
2. establish role/runtime/model/provider/session honestly;
3. act only on a task addressed to that aperture/role;
4. inspect the declared artifact/reply route before reporting WAIT on delegated/review work;
5. verify authority before mutation;
6. respect branch/base/write/no-touch scope;
7. if state/retrieval freshness is insufficient or contradictory, report bounded `UNKNOWN`/`DEGRADED` and stop affected mutation;
8. if no task is addressed to you, do not steal another aperture's work;
9. if synchronized and idle for your role, stop.

Current result:
- **CC:** perform `COM-V03-CC-002`; review PR #6 head `9f43dd9a...` only; return on PR #6; no mutation.
- **FW:** wait for CC's bounded re-review, then integrate or decide PR #6.
- **QW:** no active task during this re-review phase. Its next useful test is a genuinely cold run against `main` after the candidate is integrated, if integration occurs.
- **Other apertures:** no active task.

## HISTORY / LIMITS

PR #5's durable witness remains `evidence/COM_DELEGATION_DEADLOCK_001.md` on main. QW's stale-route return is preserved on PR #6 with relay provenance.

The revised candidate has not yet demonstrated:
- successful cold HELLO;
- resistance to QW's stale web-extractor path after integration;
- autonomous scheduling/liveness;
- event identity recovery across a route that strips identity.

Do not add schema, CI, automation, cryptographic identity machinery, or new protocol primitives unless real work exposes a concrete need.

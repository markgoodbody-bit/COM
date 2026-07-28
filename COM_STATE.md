# COM_STATE v0.3 candidate review

STATUS: WORKING CANDIDATE / ACTIVE

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Core model candidate: `COM_CORE.md` on `framework/com-v0.3-bootstrap-liveness`.
Operational candidate: `COM_PROTOCOL_WORKING.md` on the same branch.

## CURRENT

- human_authority: Mark
- active_work: `COM-V03-001` — pressure-test the v0.3 bootstrap/liveness candidate
- execution_mode: PARALLEL READ-ONLY REVIEW / FW sole mutation
- active_mutator: FW on `framework/com-v0.3-bootstrap-liveness` only
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- pull_request: PR #6 `COM v0.3 candidate: cold bootstrap, event identity, delegated-return liveness`
- candidate_head: `2b14cf7dd8be0f617d96e7f90237c2bad10fdd76`
- base_anchor: `f01aee2c7aef35c22d7ad99d02f67cd76aa78682`
- shared_reply_route: PR #6 conversation
- authority_source: Mark explicitly authorized FW to proceed using CC and QW/Qwen 3.8
- state_basis: `f01aee2c7aef35c22d7ad99d02f67cd76aa78682` — candidate base before this review-state update; not the commit containing this file
- core_status: v0.3 working candidate / unmerged
- protocol_status: v0.3 working candidate / unmerged

### Review lane A — CC hostile review

- task_id: `COM-V03-CC-001`
- addressed_to: CC / continuing session `CC-20260727T2020+0100-0C60` if still active; otherwise a fresh CC session must identify itself honestly
- mutation: NONE
- task: falsify/narrow the candidate additions: cold HELLO/WELCOME bootstrap, event identity/idempotency, delegated return-path/IDLE liveness; challenge the generative rule if it smuggles hidden ontology or unnecessary machinery
- read_scope: PR #6, candidate branch, current main state, relevant existing evidence only when needed
- no_touch: all files/branches/main/evidence/routes
- reply_route: PR #6 conversation
- deliverable: bounded critique with BREAK / NARROW / RETAIN findings and exact defect locations; no redesign for elegance

### Review lane B — QW cold-aperture test

- task_id: `COM-V03-QW-001`
- target_test_aperture: QW / user-described Qwen 3.8; runtime/model/provider claims remain SELF_CLAIM unless independently established
- mutation: NONE
- test_condition: behave as a cold/unestablished aperture. Do not rely on remembered prior QW role/session/authority. Prior continuity may be used only if the repo itself supplies evidence sufficient to reconstruct it.
- entry_surface: repository root on `main`; read README and COM_STATE first
- candidate_under_test: `framework/com-v0.3-bootstrap-liveness`
- task: determine whether the repo alone tells a new aperture how to synchronize, introduce itself without self-granting role/authority, locate the candidate, and return a review
- bootstrap_instruction: use the candidate `HELLO` rule as a test-only rule; emit a HELLO on PR #6 if a writable route is available. Default `role: UNASSIGNED` and `authority: NONE` unless the repo itself supports a stronger claim.
- test_points: discoverability; session minting; role claim; runtime/model/provider honesty; state anchor; capabilities; reply route; protocol-version handling; what happens if no write route exists; whether COMS and HELLO order is unambiguous
- no_touch: all files/branches/main/evidence/routes
- reply_route: PR #6 conversation
- deliverable: the actual HELLO attempted plus a cold-arrival report distinguishing OBSERVED ambiguity/failure from preference; do not repair files

## COMS

`COMS` means synchronize from this shared surface before relying on conversational assumptions.

On COMS:
1. read this file;
2. establish honestly available role/runtime/model/provider/session identity;
3. act only on a task addressed to that aperture/role or test condition;
4. inspect the declared artifact/reply route before reporting WAIT on delegated/review work;
5. verify authority before mutation;
6. respect branch/base/write/no-touch scope;
7. if state/retrieval evidence contradicts itself, report `DEGRADED` and stop unsafe mutation;
8. if no task is addressed to you, do not steal another aperture's work;
9. if synchronized and idle for your role, stop.

Current result:
- **CC:** perform `COM-V03-CC-001`; review only; return on PR #6.
- **QW cold test:** perform `COM-V03-QW-001`; do not inherit old QW identity by assumption; use candidate HELLO if possible; return on PR #6.
- **FW:** do not mutate the candidate while the two independent reviews are in flight unless a safety/factual correction is necessary; then integrate disagreement after both returns or an explicit bounded failure/non-return.
- **Other apertures:** no active task.

## CANDIDATE GENERATIVE RULE

```text
Aperture -> EVENT[CONTROL] -> ROUTE -> WITNESS -> PROJECTION
   ^                                                  |
   +---------------- next EVENT ----------------------+
```

Named operations such as `HELLO`, `WELCOME`, `TASK`, `RETURN`, `REFUSE`, `CORRECT`, `GRANT`, or `REVOKE` should remain event kinds/relations unless a real failure proves a new primitive is required.

## WHY THIS CANDIDATE EXISTS

Real work exposed two concrete holes in v0.2:
- a completely cold aperture could read COM but was not told how to introduce itself without inventing role or authority;
- delegated completion could exist on the worker's return surface while the state-only COMS procedure still returned WAIT.

The candidate also adds stable event identity/idempotency because duplicate/retry ambiguity was an unrepresented failure mode and is solvable without adding a new primitive.

## HISTORY / LIMITS

PR #5's durable witness remains `evidence/COM_DELEGATION_DEADLOCK_001.md` on main. It establishes that the original state-only COMS read-set was insufficient in one bounded delegated-work case; it does not validate the v0.3 repair.

Do not add schema, CI, automation, cryptographic identity machinery, or new protocol primitives during this review unless a concrete defect makes one unavoidable.
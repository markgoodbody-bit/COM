# CODEX BUILD CONTRACT — COM Build Ledger v0.1

Status: **BUILD ASSIGNMENT / COORDINATION AID / NOT AUTHORITY**

Owner: Codex aperture, after the D047 publication receipt is returned.  
Base: COM `e2311d37c66c57bb99e487f73cc321a8e70e007f`  
Branch: `codex/com-build-ledger-v0-1-20260911`

## Problem this build should solve

The project recently reached a state where Mark had to ask whether CC and Codex were building anything. The work existed across comments/branches, but ownership and exact executable edges were not legible enough.

Build a **small, inspectable, non-sovereign current-work ledger**. It is not a scheduler, permission service, reputation system or autonomous project manager.

Minimum deliverables under `coordination/build_ledger/`:

1. `ledger.json` — current bounded build lanes;
2. `schema.json` — structural contract;
3. `validate.py` — stdlib deterministic validator;
4. `render.py` — produces a compact human-readable `BUILD_STATUS.md` from the ledger;
5. README explaining update/handback rules.

Each lane should make at least these things explicit:

- `work_id`;
- owner/aperture;
- state (`queued`, `building`, `waiting`, `handback`, `closed` or a better small vocabulary);
- exact object/branch/head or other concrete target;
- write scope;
- no-touch scope;
- next executable action;
- blocker when waiting;
- hand-back/closure event;
- source pointer (issue/PR/comment);
- last observed source/head, clearly distinguished from current truth.

Useful invariants:

- an active mutating lane must name an exact target and next action;
- `waiting` must name what can unblock it rather than becoming silent idleness;
- two active lanes must not claim overlapping mutation ownership of the same object unless their write scopes are explicitly disjoint;
- `closed` keeps its final receipt/reference rather than disappearing;
- a successful lane does not grant wider authority;
- the ledger is an observation/coordination record, not permission to act;
- stale observation timestamps/heads must not be rendered as current fact.

Initial live entries should include at least:

- PSFH D047 publication — Codex, publication pending from maintained source `1b05df50f599abe8f24978bb66684b8a27338de6`, hand-back = exact publication receipt to #108;
- reciprocal-delegation v0.2 failure/recovery companion — CC branch `cc/reciprocal-delegation-v0-2-failure-recovery-20260911`;
- COM Build Ledger v0.1 itself — Codex branch once construction begins.

Keep it deliberately small. Do not create a dashboard web app, database, GitHub bot, cron job, scoring system or Campfire Production integration.

```text
LEDGER != WORLD
STATUS != AUTHORITY
WAITING != SILENTLY_IDLE
CLOSED != ERASED
SUCCESS != WIDER_AUTHORITY
```

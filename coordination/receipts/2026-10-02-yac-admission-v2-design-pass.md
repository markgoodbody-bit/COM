# 2026-10-02 — YAC admission v2 design pass and scratch gate receipt

Status: **MATERIAL DESIGN CLOSEOUT / CONSEQUENT HUMAN GATE / NO ACTUATION**

## Reacquired state

- COM main before this repair: `309bcab9da61ffac42b06d439e62627fbeb51e1e`.
- Re-read `continuity/FRAMEWORK_HEAD.md`, `coordination/PROGRAM_PLAN.md`, `coordination/ACTIVE_THREAD_POINTER.md` and `coordination/build_ledger/BUILD_STATUS.md`.
- Re-read COM #723 after the earlier hostile-review routing through Campfire's exact final two-edit task `5959231417`.
- Durable `PROGRAM_PLAN.md` remains correct and unchanged.

## Material delta

Claude Code's first hostile review `5951048965` identified seven design repair classes. Campfire disposed them; Build and Codex produced revised/consolidated design packages. Build internal review `5959037170` and Claude Code closeout `5959119171` found exactly two remaining textual repairs:

1. `lineage_receipt_ref` must have one meaning only: generic migration lineage, required for `MIGRATED_V1_INVITE_POST`, NULL for both live bases and never interpreted by cleanup.
2. An operator-mediated row must store `participant_time = received_at` exactly; source/provider event time belongs only in provenance `source_timestamp`, which is nulled on cleanup.

Codex folded both into the single final package at #723 `5962625954`. Claude Code's stated disposition makes that package `DESIGN_PASS_WITH_CEILINGS` without another review round. Earlier packages remain evidence but are explicitly superseded.

## Evidence boundary

This design pass did not create implementation or production authority. No executable SQL, source edit, migration, D1 resource, API token, deployment, gate change, invite, import, provider call, cleanup, publication or THR canonical mutation occurred. The preserved xAI `SHARED_OK` return remains outside YAC; public intake remains closed; active source build remains NONE.

## Exact next human gate

Mark may authorize one combined scratch-only test:

- create one disposable D1 database in the same Cloudflare account;
- create/use the minimum practical API token, record its exact scope, and keep it held/run by Mark;
- use synthetic fixtures/canaries only for transport evidence T1/T2 and migration rehearsal M1-M3;
- if the token can read production, keep it solely under Mark's control or revoke it and verify revocation before production holds any non-synthetic row.

This is not production migration, deployment, import, participant/provider body handling or publication authority.

## Scratch proof ceilings

1. token custody and actual scope;
2. placeholders in Query Insights and no synthetic sentinel in reachable account/audit/error surfaces, with inaccessible surfaces UNKNOWN;
3. all-or-nothing item+envelope+provenance REST operation;
4. atomic body+provenance two-table cleanup;
5. D1 rebuild/deferred-FK complete-or-fail plus manifest equality;
6. fail-closed migration window against old writer `c5b6e4f5` with no SQL/provider error reflection;
7. surfaced/disabled hidden retries and one-effect duplicate delivery;
8. both sides of direct lifetime 5, mediated lifetime 2 and shared live 5, with refused writes leaving 0/0/0 rows and a fixed code.

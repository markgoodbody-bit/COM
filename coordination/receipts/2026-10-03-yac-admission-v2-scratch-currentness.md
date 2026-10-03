# 2026-10-03 — YAC admission v2 scratch rehearsal currentness

Status: **MATERIAL SCRATCH EVIDENCE / LOCAL STOP / NO PRODUCTION ACTUATION**

## Reacquired state

- COM main before this repair: `77ba86e2da7f5c5896cd5d97f5fd7f77feecbaed`.
- Re-read all four hot coordination surfaces and COM #723 receipts after the design-pass gate.
- `PROGRAM_PLAN.md` remains correct and unchanged.

## Human authorization and custody

Mark explicitly authorised the scratch-only synthetic rehearsal at #723 `5963088203`. A Mark-controlled local execution path was established. Scratch D1 identity:

- name: `yac-admission-v2-scratch`
- UUID: `50e314e9-14b1-41b9-b33f-a97002dc09a6`
- account: current Cloudflare account

Human-attested token metadata is `Account / D1 / Edit`, current account only, temporary. No database-specific restriction is established. Production D1 reach therefore remains POSSIBLE/UNKNOWN and was deliberately not probed. Mark retains the token; no secret value was copied to COM/chat.

## Evidence earned

1. Mark's read-only preflight returned the exact synthetic bound parameter from the pinned scratch UUID.
2. Direct signed-in dashboard witness at #723 `5968499977` showed both `SELECT 1 AS scratch_probe` and `SELECT ? AS synthetic_probe` in the last-24h Query Insights table.
3. No synthetic parameter value appeared in that displayed table.
4. The dashboard showed two read queries, zero write queries, zero rows written and zero tables.

This earns ceiling 2 `PASS_WITH_CEILING` for the displayed Query Insights surface only. It does not prove absence from all provider audit/error/support surfaces; those remain UNKNOWN.

## First write prerequisite

Campfire authorised synthetic ceilings 3–8 at `5968507804`. Codex prepared a human-run three-table atomicity helper. Mark's first run stopped at `LOCAL_GUARDS` before any credential/network/write activity:

- `query_requests=0`
- `write_attempted=false`
- `last_http_status=null`
- no schema hash or fixture prefix

This is not evidence that D1 atomicity failed. The helper was narrowly instrumented to expose allowlisted local stage/failure information only:

- path: `C:/Users/markg/Downloads/YAC-Scratch-Atomicity.ps1`
- SHA-256: `1284e14b02ade2e35760223b6c3beb7096872bea3ccad5d24380f5340f072628`
- offline self-test: PASS, seven checks, zero credential reads, zero network requests

## Current next action and boundaries

One explicit Mark-run attempt of the instrumented helper is pending. No automatic retry. Ceilings 3–8 remain NOT_RUN.

No production request/mutation, YAC source edit, SQL migration, deploy, gate change, invite, real participant/provider content, xAI carry, provider/model call, publication or THR canonical mutation occurred. Public intake remains closed. Active source build remains NONE.

# EvidenceWatch — upgrade/temporal-authority repair GREEN — 19 September 2026

Status: **REAL-RUN DEFECTS REPAIRED / EXACT-HEAD HOSTED GREEN / CLEAN LEDGER WITNESS NEXT**

Relay PR #248 exact head:
`9877d84b115df0f183c61d420642cef45048ca8c`

Hosted:
`campfire-ci 1583 / 35450727597 — SUCCESS`

Focused competition tests:
- core: 23;
- browser HTTP E2E: 1;
- total: 24.

## Real-run defects repaired

### 1. Legacy ledger completion compatibility

Earlier ledger format:
```text
SOURCE_OBSERVED(fingerprint)
-> ANALYSIS_RECORDED(fingerprint)
-> TERMINAL_DECISION(no fingerprint)
```

New engine originally looked only for terminal fingerprints, causing successful historical observations to be reprocessed after upgrade.

Repair:
- direct new-format terminal fingerprint still wins;
- legacy completion is recognized only when a matching `ANALYSIS_RECORDED` is followed by a terminal decision for the same source before the next `SOURCE_OBSERVED`;
- crash after analysis but before terminal decision remains retryable.

### 2. Authority is temporal

```text
STATE AUTHORITY != TIMELESS AUTHORITY
```

Live Anthropic config now declares:
- July owner source `authorityAsOf = 2026-07-30`;
- September owner source `authorityAsOf = 2026-09-09`.

Once September advances canonical state to 4:
- July cannot roll it back to 3;
- historical divergence can be visible without canonical overwrite;
- historical-source unreachability is not treated as current-state loss.

### 3. Append-only config refresh

`WATCH_CONFIG_UPDATED` refreshes current source/dependent metadata without rewriting historical ledger events. Existing ledgers can therefore learn new authority metadata append-only.

### 4. Discovery narrowing

Broad root/ancestor index links such as `/news` are no longer accepted as automatic discovery candidates merely because an article links to them.

### 5. Fetch vs analysis failure

Already repaired on prior green head:
- actual fetch failure -> `UNREACHABLE`;
- successful fetch + model/analysis failure -> `ANALYSIS_FAILED`;
- failed analysis retry does not append duplicate source observation.

## Local credential state

Mark has `NVIDIA_API_KEY` set in the current PowerShell session. No need to repaste while that shell remains open.

## Next

Preserve the current local ledger as defect evidence, start a fresh post-repair ledger, and run:
1. clean real heartbeat;
2. clean restart heartbeat.

Do not delete the pre-fix ledger.

```text
REAL PROVIDER = PASS
REAL WEB = PASS
CORE RESTART/DUPLICATE = PASS
UPGRADE COMPATIBILITY REPAIR = GREEN
TEMPORAL AUTHORITY REPAIR = GREEN
CLEAN POST-REPAIR LIVE WITNESS = NEXT
```

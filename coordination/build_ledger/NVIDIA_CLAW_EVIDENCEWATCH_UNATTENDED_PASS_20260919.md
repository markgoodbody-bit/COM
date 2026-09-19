# EvidenceWatch — unattended scheduler witness PASS — 19 September 2026

Status: **UNATTENDED LONG-RUNNING WITNESS PASS / TECHNICAL VALIDATION STOP / VIDEO + FINAL FORM NEXT**

Mark ran the real scheduler from exact audit-green head:

`ee362ce0105565815ad2695f12db0481fab5f638`

Command path:
`npm run live`

Configuration:
- real Anthropic July + September owner sources;
- real NVIDIA Build/Nemotron;
- 10-second interval;
- fresh unattended audit ledger.

## First autonomous heartbeat

Observed:
- July -> `BASELINE_ESTABLISHED`;
- September -> `MATERIAL_DELTA`;
- canonical quantity -> `4`;
- one correction alert;
- downstream dependent flagged.

## Subsequent autonomous heartbeats

Six further scheduled cycles observed.

Every later cycle:
- July -> `DUPLICATE_OBSERVATION`;
- September -> `DUPLICATE_OBSERVATION`;
- canonical quantity remained `4`;
- `newAlerts = []`.

No operator action occurred between heartbeats.

Process was manually stopped only to bound test duration.

## Evidence now established

```text
REAL PUBLIC WEB FETCH = PASS
REAL NVIDIA PROVIDER = PASS
CLAIM BASELINE 3 = PASS
CORRECTION TO 4 = PASS
DOWNSTREAM REVIEW ROUTE = PASS
DURABLE LEDGER = PASS
RESTART RECOVERY = PASS
UNCHANGED-SOURCE DEDUPE = PASS
TEMPORAL AUTHORITY / NO ROLLBACK = PASS
FETCH-vs-ANALYSIS FAILURE SEPARATION = PASS
UNATTENDED SCHEDULER MULTI-CYCLE = PASS
QUIET HEARTBEAT / NO DUPLICATE ALERT = PASS
```

Evidence ceiling:
- bounded minutes-long unattended run, not production-duration operation;
- one correction-lineage case;
- no broad accuracy/user-demand validation.

## Disposition

```text
ENGINE FEATURE CHURN = STOP
ADDITIONAL TECHNICAL VALIDATION = NOT EARNED BY MOMENTUM
NEXT = RECORD 60–90s VIDEO -> REVIEW VIDEO -> FINAL AIRTABLE PAYLOAD -> MARK SUBMITS
```

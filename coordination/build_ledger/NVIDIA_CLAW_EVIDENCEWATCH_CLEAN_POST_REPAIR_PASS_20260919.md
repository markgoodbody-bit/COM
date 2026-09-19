# EvidenceWatch — clean post-repair live witness PASS — 19 September 2026

Status: **CLEAN REAL-WEB + REAL-NVIDIA + TEMPORAL-AUTHORITY PASS / CLEAN RESTART TEST NEXT**

Mark preserved the earlier pre-fix ledger and ran a clean heartbeat using exact Relay PR #248 head:

`9877d84b115df0f183c61d420642cef45048ca8c`

Hosted source evidence:
`campfire-ci 1583 / 35450727597 — SUCCESS`

## Clean observed live results

### July authority source

`anthropic-july-2026`

- status: `BASELINE_ESTABLISHED`
- relation: `baseline`
- quantity: `3`

### September newer authority source

`anthropic-september-2026`

- status: `MATERIAL_DELTA`
- relation: `correction`
- quantity: `4`

Final canonical state:
- proposition: Anthropic publicly identified four real-world cybersecurity evaluation incidents;
- status: supported;
- quantity: `4`;
- scope: real-world cybersecurity evaluation incidents.

Exactly one material alert:
- kind: `correction`;
- before: `3`;
- after: `4`;
- summary: fourth incident disclosed / count updated;
- downstream dependent: competition demo incident-count statement;
- action: review incident count and search-aperture description.

No broad `/news` parent page was auto-discovered.

Run ended:
`EVIDENCEWATCH_LIVE_ONCE_OK`

Credential:
- reused from session-scoped `NVIDIA_API_KEY`;
- not exposed in transcript.

## Evidence ceiling

```text
CLEAN REAL OWNER FETCH = PASS
CLEAN REAL NVIDIA ANALYSIS = PASS
TEMPORAL AUTHORITY 3 -> 4 = PASS
CANONICAL END STATE 4 = PASS
DOWNSTREAM REVIEW ROUTE = PASS
BROAD PARENT DISCOVERY FILTER = PASS
DURABLE LEDGER WRITE = PASS

CLEAN POST-REPAIR RESTART DUPLICATE WITNESS = NEXT
```

Next:
rerun the exact same live heartbeat in a fresh child process against this clean ledger.

If normalized owner pages are unchanged, expected:
- July -> `DUPLICATE_OBSERVATION`;
- September -> `DUPLICATE_OBSERVATION`;
- current quantity remains `4`;
- alerts total remains `1`;
- `newAlerts = []`.

If source bytes changed, inspect honestly instead of forcing the duplicate expectation.

# EvidenceWatch — real public-source heartbeat PASS — 19 September 2026

Status: **REAL WEB + REAL NVIDIA + DURABLE LEDGER PASS / RESTART DUPLICATE TEST NEXT**

Mark ran:

`scripts/run-live-once.ps1`

from exact branch head:

`513487a69033fca9e8102ef77ee6538fb695e87e`

using the credential-safe local NVIDIA Build key prompt.

## Observed results

### Source 1 — Anthropic July owner page

`anthropic-july-2026`

Observed:
- status: `BASELINE_ESTABLISHED`;
- relation: `baseline`;
- quantity: `3`.

One same-origin candidate was discovered:
`https://www.anthropic.com/news`

It remains a non-authoritative candidate.

### Source 2 — Anthropic September owner page

`anthropic-september-2026`

Observed:
- status: `MATERIAL_DELTA`;
- relation: `correction`;
- quantity: `4`.

## Final canonical state

```json
{
  "proposition": "Anthropic publicly identified four real-world cybersecurity evaluation incidents.",
  "status": "supported",
  "quantity": "4",
  "scope": "real-world cybersecurity evaluation incidents",
  "searchAperture": "Anthropic's alignment assessment of cybersecurity incidents"
}
```

## Material alert

Exactly one alert:
- kind: `correction`;
- source: `anthropic-september-2026`;
- before quantity: `3`;
- after quantity: `4`;
- summary: `Source reports four incidents, updating prior count of three.`

Affected dependent:
- `EvidenceWatch competition demo — incident-count statement`;
- action: review the stated incident count and search-aperture description.

Durable ledger written to local competition data path.

Run terminated:
`EVIDENCEWATCH_LIVE_ONCE_OK`

Credential was not exposed in the transcript supplied to Framework.

## Evidence ceiling

```text
REAL OWNER HTTP FETCH = PASS
REAL NVIDIA INFERENCE = PASS
BASELINE EXTRACTION = OBSERVED
CORRECTION DELTA = OBSERVED
DOWNSTREAM REVIEW ROUTE = OBSERVED
DURABLE LEDGER WRITE = OBSERVED
ONE-SHOT END-TO-END LIVE RUN = PASS

RESTART RECOVERY = NOT YET LIVE-WITNESSED
UNCHANGED SOURCE DUPLICATE SUPPRESSION = NOT YET LIVE-WITNESSED
UNATTENDED MULTI-CYCLE = NOT YET LIVE-WITNESSED
PUBLIC DEPLOYMENT = NO
SUBMISSION = NO
```

Next:
run the exact same live heartbeat again in a new process against the existing ledger.

Expected only if normalized source bytes are unchanged:
- `DUPLICATE_OBSERVATION` for unchanged sources;
- no new NVIDIA analysis calls for exact duplicates;
- current state remains `4`;
- alert count remains `1`.

If either page changed, do not force the duplicate expectation; inspect the new observation honestly.

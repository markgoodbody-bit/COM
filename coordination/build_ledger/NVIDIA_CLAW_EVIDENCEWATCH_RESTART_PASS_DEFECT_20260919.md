# EvidenceWatch — restart duplicate witness + discovered-source defect — 19 September 2026

Status: **CORE RESTART/DUPLICATE PASS / DISCOVERED-SOURCE FAILURE-CLASSIFICATION DEFECT FOUND / REPAIR PENDING CI**

Mark reran the bounded live heartbeat in a fresh process against the existing durable ledger.

Observed configured owner sources:

- `anthropic-july-2026` -> `DUPLICATE_OBSERVATION`
- `anthropic-september-2026` -> `DUPLICATE_OBSERVATION`

Recovered canonical state remained:
- quantity: `4`
- alerts total: `1`
- new alerts: `[]`

Therefore the core live witness establishes:

```text
PROCESS RESTART -> LEDGER RECOVERY = PASS
UNCHANGED CONFIGURED OWNER SOURCE -> DUPLICATE SUPPRESSION = PASS
UNCHANGED SOURCES -> NO NEW MATERIAL ALERT = PASS
CANONICAL STATE 4 SURVIVES RESTART = PASS
```

The same run also returned:

`discovered-f6aa679babd7 -> UNREACHABLE`

while total `SOURCE_OBSERVED` count increased from 2 to 3.

Static review identified a real implementation defect:
`pollWatch()` wrapped both source fetch and downstream `observe()/analyzer` work in one catch, so a successful fetch followed by analysis/model failure could be mislabeled as `SOURCE_UNREACHABLE`.

That also created a retry hazard because the fetched fingerprint could be recorded before analysis completed.

Repair on Relay PR #248:
- fetch errors and analysis errors are now separated;
- analysis/model failure becomes `ANALYSIS_FAILED`, not `UNREACHABLE`;
- failed analysis is retryable on the same fingerprint;
- retry does not append a duplicate `SOURCE_OBSERVED`;
- completed observation fingerprint suppresses later model work;
- actual fetch failure remains `UNREACHABLE`;
- live output now exposes exact `sourceId` and analysis error;
- launchers now support a session-scoped inherited `NVIDIA_API_KEY` so Mark need not paste the key for every run.

Current repair head:
`f3896afa26652a0f532897a8b5cced5143bc6f83`

Hosted `campfire-ci 1576 / 35450043232` was still running at checkpoint time.

Do not erase the core restart witness because of the discovered-source defect; they are separate observations.

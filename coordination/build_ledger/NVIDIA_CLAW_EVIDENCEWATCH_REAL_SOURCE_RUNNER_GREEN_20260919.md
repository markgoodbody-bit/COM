# EvidenceWatch — real-source heartbeat runner green — 19 September 2026

Status: **LIVE PROVIDER PASS + REAL-SOURCE RUNNER EXACT-HEAD GREEN / LOCAL REAL HEARTBEAT NEXT**

Relay draft PR #248 exact head:
`513487a69033fca9e8102ef77ee6538fb695e87e`

Hosted:
`campfire-ci 1571 / 35449632481 — SUCCESS`

Focused competition tests:
- 17 core;
- 1 browser HTTP E2E;
- total **18**.

Prior live NVIDIA witness:
`NVIDIA_PROBE_OK` against `nvidia/nemotron-3-super-120b-a12b`.

## Real owner sources

Verified current public Anthropic pages:

1. July 30, 2026:
   `https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals`
   - owner reports three incidents;
   - 141,006 evaluation runs reviewed.

2. September 9, 2026:
   `https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents`
   - owner reports four incidents;
   - explicitly links the earlier three;
   - says missed transcripts revealed a fourth;
   - later search broadened to roughly 481 million transcripts.

## Live-run implementation

New branch objects:
- `examples/live-anthropic-cyber-watch.json`;
- `src/live-once.mjs`;
- `scripts/run-live-once.ps1`;
- npm script `live:once`.

The live fetcher now:
- fetches real public HTTP pages;
- normalizes readable HTML text before fingerprint/model analysis;
- strips script/style/noscript/svg noise;
- uses raw HTML only for bounded same-origin link extraction.

Current NVIDIA Prototype page shape supplied by Mark corrected adapter to:
`temperature=0.5 / top_p=1`.

Prior `1 / 0.95` interoperability probe remains valid but is no longer described as current page guidance.

## Intended evidence sequence

First process:
```text
FETCH JULY OWNER PAGE
-> NVIDIA ANALYSIS
-> BASELINE / MATERIAL STATE

FETCH SEPTEMBER OWNER PAGE
-> NVIDIA ANALYSIS
-> CORRECTION / MATERIAL DELTA EXPECTED IF MODEL REPRESENTS OWNER TEXT CORRECTLY

WRITE APPEND-ONLY LEDGER
-> EXIT
```

Second process, same ledger:
```text
RESTART
-> FETCH SAME OWNER PAGES
-> UNCHANGED NORMALIZED CONTENT
-> DUPLICATE_OBSERVATION EXPECTED
-> NO NEW NVIDIA ANALYSIS FOR EXACT DUPLICATES
-> DURABLE STATE RECOVERED
```

Expected semantics are hypotheses, not predeclared test success.

```text
LIVE PROVIDER = PASS
REAL-SOURCE RUNNER SOURCE = GREEN
REAL-SOURCE HEARTBEAT = NOT YET RUN
RESTART LIVE WITNESS = NOT YET RUN
```

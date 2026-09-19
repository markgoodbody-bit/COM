# NVIDIA Claw EvidenceWatch active build — exact-head green checkpoint — 19 September 2026

Status: **ACTIVE COMPETITION BUILD / DRAFT PR / EXACT-HEAD HOSTED CI GREEN / NOT SUBMITTED / NOT PRODUCTION**

Registered challenge:
NVIDIA London Claw Agent Challenge.

Current candidate:
**EvidenceWatch**

> EvidenceWatch tells people when the evidence underneath an important claim materially changes after they have already relied on it.

Campfire Relay draft PR:
`#248 NVIDIA Claw: EvidenceWatch long-running evidence drift agent`

Exact head:
`2e62c2ed640f7bd8fe036f9a05ba0b26b84e2c0a`

Hosted:
`campfire-ci 1554 / 35448098624 — SUCCESS`

Focused competition tests:
- `test/evidencewatch.test.mjs`: 14;
- `test/server.test.mjs`: 1;
- total focused: **15**;
- root CI imports the same test sources.

## Current vertical slice

- append-only JSONL evidence ledger;
- scheduled/long-running heartbeat loop;
- live HTTP fetcher;
- exact-observation fingerprint dedupe;
- NVIDIA Build OpenAI-compatible analyzer adapter;
- canonical evidentiary state can advance only through explicit baseline/material-delta events;
- model analysis is not silently canonical authority;
- primary/state-authority sources separated from supporting/derivative/candidate sources;
- derivative repetition of the same claim stays quiet;
- derivative divergence alerts but cannot overwrite canonical state;
- independent/supporting divergence alerts but cannot overwrite primary canonical state;
- primary source disappearance alerts while preserving last-known state;
- bounded same-origin discovery:
  - links extracted deterministically from fetched page;
  - model can nominate only URLs actually present in candidate set;
  - invented URLs are rejected;
  - discovered sources start non-authoritative;
  - max 5 additions per heartbeat;
- deterministic three-heartbeat browser/CLI demo;
- real HTTP browser-demo end-to-end regression;
- restart rebuilds current state from durable ledger.

## Demo spine

1. owner baseline: **3 incidents**;
2. derivative repetition: same claim / no material alert;
3. later owner correction: **4 incidents** after broader search / material alert;
4. prior state remains inspectable instead of silently overwritten.

The fixture is deterministic demo material derived from a current public correction-lineage case. It is not presented as a live fetch.

## Judging fit

Registered judging:
1. successfully deployed / real engineering;
2. innovation & creativity;
3. real-world value.

Current product hypothesis:

```text
WEB MONITORING
+ CLAIM-LEVEL SEMANTIC STATE
+ SOURCE ANCESTRY / INDEPENDENCE
+ CORRECTION-PRESERVING MEMORY
+ MATERIAL-DELTA ALERTING
```

Strong adjacent owners already exist for page-change monitoring, citation checking, scholarly correction/retraction status and generic long-running-agent infrastructure.

No novelty claim is made.

## Current gaps / gates

Not yet established:
- live NVIDIA endpoint witness;
- durable unattended live run over real monitored sources;
- OpenClaw/NemoClaw packaging;
- public deployment;
- user demand;
- exact London challenge Terms & Conditions;
- submission.

```text
GREEN SOURCE != LIVE NVIDIA WITNESS
DETERMINISTIC DEMO != LIVE WEB RUN
BUILD != SUBMISSION
SUBMISSION != AWARD
```

Next:
1. stronger owner/product subtraction;
2. live NVIDIA endpoint witness when local provider credential is available;
3. deployment/package decision only after product seam survives subtraction;
4. read exact challenge T&Cs before submission/licence/prize acceptance.

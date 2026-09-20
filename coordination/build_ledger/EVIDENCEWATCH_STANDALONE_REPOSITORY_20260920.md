# EvidenceWatch standalone repository extraction

Date: 20 September 2026 — Europe/London

Status: **PRIVATE STANDALONE SOURCE / FRESH CI PASS / PRIOR LIVE WITNESS INHERITED WITH EXACT BOUNDARY / NOT SUBMITTED / NOT PRODUCTION**

## Human direction

Mark directed that EvidenceWatch be moved into its own clean repository before recording.

New private repository:

- repository: `markgoodbody-bit/evidencewatch`;
- main: `a0d0a9e58156b67ec00ad95c758dc1dc3eebc5a7`;
- initial commit: `Initial private standalone EvidenceWatch`;
- GitHub Actions: run `35507545045` — **SUCCESS**.

The repository remains private. No visibility, submission, deployment, account, terms or spend gate was crossed.

## Source basis

Extraction source:

- Campfire Relay draft PR #248;
- exact reviewed/documented head: `00017d190bb6a9813cb64f1f30a17b27e4ce10ca`;
- source directory: `competition/nvidia-claw-evidencewatch/`.

A Git tree/blob comparison established that the standalone repository retains byte-identical blobs for:

- all nine `src/*.mjs` implementation files;
- all three `public/*` browser files;
- both PowerShell helper scripts;
- the deterministic demo fixture;
- `test/server.test.mjs`;
- `.gitignore`.

The standalone package/test/docs were deliberately adapted for repository-root paths, clean product framing and current boundaries. Competition-only planning/terms/submission documents were not copied into the clean product repository; they remain historical/submission material in the Relay draft.

## Evidence inheritance boundary

The repaired-head live witness remains attached to Relay snapshot:

`00017d190bb6a9813cb64f1f30a17b27e4ce10ca`.

The standalone core is byte-identical to that snapshot and the standalone test workflow passed, but no fresh NVIDIA/public-web live call was made after extraction.

Preserve:

```text
BYTE-IDENTICAL CORE + FRESH STANDALONE CI
!=
FRESH STANDALONE LIVE WITNESS

PRIOR EXACT-SNAPSHOT WITNESS
!=
GENERAL VALIDATION

PRIVATE REPOSITORY
!=
PUBLIC DEPLOYMENT
```

The prior semantic ceiling also remains:

- the model returned the four-incident proposition with internally awkward `status=contradicted`;
- the UI does not display that field;
- relation/quantity/material analysis drove the observed correction;
- no claim is made that every model field is semantically reliable.

## Maintained limitation

The unattended runner has a single-host local-process lock. The one-shot runner does not acquire it. Use an isolated ledger sequentially and never run it concurrently with another writer. Repository extraction does not repair this limitation.

## Current route

```text
STANDALONE PRIVATE SOURCE = READY
STANDALONE CI = PASS
FRESH LIVE CALL AFTER MOVE = NO / NOT REQUIRED FOR RECORDING

NEXT
-> CLONE / USE STANDALONE REPOSITORY
-> RECORD DETERMINISTIC BROWSER DEMO
-> USE SAVED EXACT-SNAPSHOT LIVE/HEARTBEAT EVIDENCE WITH ITS CEILINGS
-> CREDENTIAL + CLAIM REVIEW
-> FINAL AIRTABLE PAYLOAD REVIEW
-> MARK EXPLICIT SUBMISSION GATE
```

No further engine churn is earned absent a concrete defect.

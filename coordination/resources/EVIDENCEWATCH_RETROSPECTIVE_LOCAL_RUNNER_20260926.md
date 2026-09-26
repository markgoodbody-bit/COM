# EvidenceWatch Brierley v2 — local Windows runner

Date: 26 September 2026

Status: **ONE-COMMAND LOCAL GATE / DRY-RUN DEFAULT / LIVE REQUIRES EXPLICIT SWITCH + EXISTING SESSION CREDENTIAL**

Runner:
`research/evidencewatch_retrospective/run-brierley-local.ps1`

Purpose:

Reduce the remaining live-run gate to one reproducible Windows command while keeping the v2 freeze, blinding and credential boundaries intact.

## What it verifies before any provider access

The runner checks:
- exact Git blobs for the six COM experiment files used by the run;
- exact private EvidenceWatch HEAD `9c96c8390d65f4fb452b2a106bcdb4fa0418ea6f`;
- the two pinned public Brierley owner files by Git blob;
- raw-owner v2 manifest reconstruction;
- exact blinded packet SHA-256;
- exact separate owner-key SHA-256;
- full v2 trivial lexical baseline reconstruction;
- the fail-closed Node harness in dry-run mode.

Default invocation performs **zero model/provider calls**.

## Default dry-run

From a current COM checkout:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\research\evidencewatch_retrospective\run-brierley-local.ps1 `
  -EvidenceWatchPath C:\path\to\evidencewatch
```

A new local run directory is created under:

`$HOME\EvidenceWatchRuns\`

Owner-source bytes, blinded packet, owner key and lexical baseline remain local.

The dry run must not create a ledger or pre-unblind model output.

## Live execution

The runner never prompts for or stores the NVIDIA key.

Live mode requires the existing PowerShell session to already contain:

`$env:NVIDIA_API_KEY`

Then:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\research\evidencewatch_retrospective\run-brierley-local.ps1 `
  -EvidenceWatchPath C:\path\to\evidencewatch `
  -Live
```

The wrapper first completes the same dry-run checks, then invokes the frozen live harness.

## Deliberate unblinding separation

A completed live run stops after writing/sealing the pre-unblind output and ledger.

It does **not** automatically join owner labels.

The wrapper prints the separate offline scorer command only after displaying the pre-unblind SHA-256.

Therefore:

```text
LIVE MODEL OUTPUT SEALED
-> HUMAN CAN PRESERVE/REVIEW RECEIPT
-> SEPARATE DELIBERATE UNBLIND
-> FROZEN SCORER
```

## Credential / cost boundary

Current NVIDIA owner documentation advertises the exact model as a hosted Free Endpoint for Developer Program prototype/research use.

Still preserve:

```text
FREE ENDPOINT != UNLIMITED QUOTA
SESSION CREDENTIAL AVAILABLE != PERMISSION TO PRINT / STORE IT
LOCAL LIVE RUN != PRODUCTION USE
```

No live provider execution was performed by adding this runner.

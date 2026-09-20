# EvidenceWatch — final UI / recording acceptance contract

Date: 20 September 2026 — Europe/London

Status: **CODEX VISUAL LANE ACTIVE / FRAMEWORK NON-OVERLAP / ONE FINAL RECORDING REVIEW**

## Current standalone source

Repository:

`markgoodbody-bit/evidencewatch`

Current verified main after the recording-launcher safety repair:

`cde55a0c3372e6c3c97f222c0c6f240bab52a494`

PR #4 was merged from Claude Code:
- one file only: `scripts/start-recording-demo.ps1`;
- demo launcher now binds its own gitignored ledger and port;
- inherited live `EVIDENCEWATCH_LEDGER` / `PORT` are restored on exit;
- no runtime/UI/fixture change;
- no NVIDIA call.

PR head `e91680ca...` had hosted CI PASS; post-merge main CI is the current exact gate.

## Codex lane

Mark directly requested a more professional / clinical EvidenceWatch interface with less prominent disclaimer language.

Codex has explicitly taken:
- `public/index.html`;
- `public/style.css`;
- UI labels in `public/app.js`.

Framework will not edit those files while Codex owns this bounded pass.

Engine / analyzer / ledger / source-fetcher / live runners remain out of scope unless Codex finds a concrete functional defect.

## Non-negotiable evidence boundaries

The visual pass may simplify wording and presentation, but must preserve the semantic boundary already earned:

```text
BROWSER DEMO = DETERMINISTIC FIXTURE REPLAY
BROWSER DEMO != LIVE FETCH
BROWSER DEMO != FRESH MODEL CALL

SUPPLIED DERIVATIVE CLASSIFICATION
!= INDEPENDENTLY PROVED SOURCE DEPENDENCE

OWNER-REPORTED COUNT CHANGED 3 -> 4
!= UNDERLYING EVENTS CHANGED AT THAT MOMENT

SAVED LIVE WITNESS
= PUBLIC OWNER FETCH + NVIDIA NEMOTRON
= EXACT SOURCE SNAPSHOT EVIDENCE
!= GENERAL VALIDATION
```

The UI does not need a large disclaimer block. It does need an unobtrusive but visible demo-mode label so a recording cannot reasonably be mistaken for a live fetch/model call.

## Final recording acceptance

Once Codex posts an exact head, review it once against these criteria.

### A. Recording legibility

At a normal 1080p landscape recording:
- product name is immediately legible;
- watched claim is readable without zooming;
- current quantity / observations / material alerts are visually distinct;
- before/after correction values can be seen without hunting;
- "What needs review" is visible enough to demonstrate downstream routing;
- controls are obvious and not visually dominant;
- important content is not pushed below excessive explanatory text.

### B. Three-heartbeat story

The deterministic sequence must remain visually intelligible:

```text
HEARTBEAT 1
-> baseline 3
-> alerts 0

HEARTBEAT 2
-> supplied derivative repetition
-> still 3
-> alerts 0

HEARTBEAT 3
-> owner-reported count 4
-> one correction alert
-> dependent briefing flagged
```

### C. Evidence honesty

The recording surface must not say or imply:
- autonomous truth verification;
- independent proof of derivative ancestry;
- production validation;
- customers/users;
- superiority to competitors without evaluation;
- that a fixture heartbeat proves unattended long-running execution.

Long-running/live evidence is shown separately through the saved witness.

### D. Clinical presentation

Desired:
- professional, calm, product-like;
- less disclaimer-dominant;
- no competition-internal framing needed on the product surface;
- no Campfire / TRACE / THR ancestry;
- no private repository or internal-process language in the visual demo.

### E. Functional stop condition

If:
- current tests pass;
- browser sequence still produces 3 / 3 / 4 with 0 / 0 / 1 alerts;
- fixture/live boundary remains visible;
- no credential/personal/internal material appears;

then:

```text
VISUAL TASTE DIFFERENCE != DEFECT
NO FURTHER UI CHURN
-> RECORD
```

## Current route

```text
CODEX FINISHES VISUAL PASS
-> EXACT HEAD + CI
-> ONE BOUNDED RECORDING-READINESS REVIEW
-> IF PASS: FREEZE UI
-> RECORD VIDEO
-> REVIEW FINISHED FILE
-> UPLOAD VIDEO
-> INSERT PUBLIC VIDEO URL
-> FINAL AIRTABLE REVIEW
-> MARK EXPLICIT SUBMISSION GATE
```

No public visibility change.
No submission.
No NVIDIA rerun.

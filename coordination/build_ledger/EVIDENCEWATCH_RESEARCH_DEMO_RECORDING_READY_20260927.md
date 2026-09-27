# EvidenceWatch — research-shaped demo recording readiness

Date: 27 September 2026

Status: **RECORDING-READY / CURRENT MAIN REVERIFIED / LOCAL DETERMINISTIC FIXTURE / NO PROVIDER CALL / NO UPLOAD**

Purpose:

Prepare one short research-facing EvidenceWatch demonstration for possible later use in a Digital Science interview, ALEC response, or bounded pilot conversation without reopening implementation or implying validation.

This is optional preparation after the Digital Science Catalyst application was submitted. It is not part of the submitted application state and does not modify that submission.

## Exact source

EvidenceWatch main:
`9c96c8390d65f4fb452b2a106bcdb4fa0418ea6f`

Research demo helper:
`scripts/start-research-demo.ps1`

Fixture:
`examples/research-correction-sequence.json`

Prepared narration:
`coordination/resources/DIGITAL_SCIENCE_RESEARCH_DEMO_RECORDING_20260925.md`

The helper explicitly:
- uses loopback port `8791`;
- selects the synthetic research fixture;
- clears only `data/research-demo.jsonl`;
- launches `src/server.mjs`;
- opens the local browser;
- makes **no live source fetch and no model/provider call**;
- restores the caller's prior relevant environment variables after exit.

## Fixture state

Question:
`Does the effect estimate relied on by this evidence brief remain current?`

Display label:
`Current effect estimate`

Disclosure:
`Synthetic research fixture replay. The CSL-shaped workflow and correction mechanics are deterministic; this is not a live scholarly source or model call.`

Three deterministic observations:

1. **Baseline**
   - authoritative source;
   - quantity `1.8`;
   - establishes current bounded state.

2. **Derivative repetition**
   - repeats `1.8`;
   - same evidentiary origin;
   - non-authoritative;
   - expected outcome: `NO_MATERIAL_DELTA`;
   - review alerts remain `0`.

3. **Publisher correction**
   - authoritative correction;
   - `1.8 -> 1.2`;
   - expected outcome: `MATERIAL_DELTA`;
   - event kind: `correction`;
   - affected dependent: `living-evidence-brief`;
   - review alerts become `1`.

## Current regression

Current main `test/server.test.mjs` contains:

`selectable synthetic research fixture reaches a correction and dependent review`

It pins:
- fixture id = `research-correction-demo`;
- initial canonical state = null;
- baseline = `BASELINE_ESTABLISHED / 1.8`;
- derivative repeat = `NO_MATERIAL_DELTA / 1.8 / 0 alerts`;
- correction = `MATERIAL_DELTA / correction / 1.2 / 1 alert`;
- affected dependent id = `living-evidence-brief`;
- end cursor = `3`;
- no next step remains.

No implementation delta is earned.

## Recording target

Target:
**45-55 seconds**

Run locally:

```powershell
cd C:\Users\markg\evidencewatch
git switch main
git pull --ff-only
git rev-parse HEAD
.\scripts\start-research-demo.ps1
```

Expected head before recording:
`9c96c8390d65f4fb452b2a106bcdb4fa0418ea6f`

If local main differs after `git pull --ff-only`, stop and reverify rather than recording a silently different build.

Narration:

**Opening — untouched screen**

> This is a deterministic synthetic research fixture. A research brief can stay unchanged after the evidence behind it has changed. EvidenceWatch tracks that dependency and tells a reviewer which work needs another look.

**Observation 1 — baseline 1.8**

> The original publication establishes the bounded result: an effect estimate of 1.8.

**Observation 2 — repeat 1.8 / no alert**

> A second source repeats 1.8, but it comes from the same evidentiary origin. It does not become independent support and it does not change the brief.

**Observation 3 — correction 1.2 / one alert**

> Then the publisher corrects the result from 1.8 to 1.2. EvidenceWatch preserves the earlier state and flags the living evidence brief that relied on it.

**Close**

> It does not decide scientific truth. It preserves the evidence change, authority path and affected work for human review.

Hold the final screen briefly before stopping.

## Recording boundaries

Do not call it:
- a live scholarly correction;
- a systematic-review pilot;
- a researcher/user test;
- a Zotero or ReadCube integration;
- EvidenceWatch efficacy evidence;
- validation of the model or product.

Correct description:

```text
DETERMINISTIC PRODUCT DEMONSTRATION
+ SYNTHETIC RESEARCH-SHAPED FIXTURE
+ REAL CURRENT EVIDENCEWATCH CODE
!=
LIVE RESEARCH EVIDENCE / USER VALIDATION
```

## Publication boundary

Recording locally is authorised as reversible preparation.

No upload, public link, replacement of the already-submitted NVIDIA video, change to the Digital Science application, or external send is implied.

If a recording is later uploaded, preserve:
- unlisted/private by default;
- exact source head;
- synthetic-fixture disclosure;
- duration;
- no claim that Digital Science requested it unless they actually do.

## Stop condition

After one clean recording:

```text
RECORDING EXISTS
-> FREEZE
-> NO DEMO POLISH BY MOMENTUM
-> WAIT FOR REAL EXTERNAL NEED
```

A visual or narration defect that materially misstates the fixture can justify one correction. Cosmetic preference alone does not reopen the lane.

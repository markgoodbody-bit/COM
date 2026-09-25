# Digital Science — optional EvidenceWatch research demo recording

Date: 25 September 2026

Status: **RECORDING SCRIPT READY / NO VIDEO RECORDED / NO UPLOAD**

Target length: **45–55 seconds**.

Run from the current EvidenceWatch checkout:

```powershell
cd C:\Users\markg\evidencewatch
git switch main
git pull --ff-only
.\scripts\start-research-demo.ps1
```

The browser should identify the fixture as synthetic in **Demo mode** and show:
- question: `Does the effect estimate relied on by this evidence brief remain current?`
- current effect estimate: not established;
- 0 observations;
- 0 review alerts.

## Recording script

**Opening — untouched screen**

> “This is a deterministic synthetic research fixture. A research brief can stay unchanged after the evidence behind it has changed. EvidenceWatch tracks that dependency and tells a reviewer which work needs another look.”

**Click Next observation once — baseline 1.8**

> “The original publication establishes the bounded result: an effect estimate of 1.8.”

**Click again — still 1.8, no alert**

> “A second source repeats 1.8, but it comes from the same evidentiary origin. It does not become independent support and it does not change the brief.”

**Click a third time — 1.2, one review alert**

> “Then the publisher corrects the result from 1.8 to 1.2. EvidenceWatch preserves the earlier state and flags the living evidence brief that relied on it.”

**Close**

> “It does not decide scientific truth. It preserves the evidence change, authority path and affected work for human review.”

Hold the final correction screen for about one second, then stop.

## Boundary

Do not describe this video as:
- a live scholarly correction;
- a researcher pilot;
- a Zotero/ReadCube integration;
- evidence of product efficacy.

It is a **deterministic product demonstration in a research-shaped synthetic fixture**.

The current NVIDIA video remains valid for the already-submitted NVIDIA competition. This optional video would be a separate Digital Science-facing artifact if Mark chooses to record and upload it.

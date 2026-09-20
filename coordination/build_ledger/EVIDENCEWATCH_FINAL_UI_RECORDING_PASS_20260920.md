# EvidenceWatch — final UI recording-readiness PASS

Date: 20 September 2026 — Europe/London

Status: **CODEX CLINICAL UI MERGED / RECORDING READINESS PASS / UI FREEZE**

## Exact standalone state

Repository:
`markgoodbody-bit/evidencewatch`

Current main:
`79e4d5270844342b74fd4e0c1e2439ab17772dd6`

Hosted CI:
`35508764265 / SUCCESS`

This main includes:
- standalone repo extraction / clean history;
- evidence-bound demo narration;
- recording pack;
- visible fixture/demo-mode boundary;
- recording-launcher isolated-ledger/port repair;
- Codex clinical/professional UI pass.

## Codex visual pass

Merged PR #5:
`Professional monitoring interface and concise copy`

Visual/product changes:
- compact light slate monitoring interface;
- smaller, more clinical typography;
- plain-language status labels;
- "Reported count", "Review alerts", "Affected work", "Revision history";
- compact expandable `Demo mode` note;
- removed large truth-oracle footer;
- no engine / analyzer / ledger / live-runner changes.

Codex reported rendered browser inspection and disclosure interaction at localhost,
plus existing 35-test suite.

## Recording acceptance

### A. Legibility

PASS by source/layout inspection + Codex rendered rehearsal:
- product name / monitored question are primary;
- three key metrics are separated;
- correction before/after values remain in revision history;
- affected downstream work remains visible;
- controls are compact;
- explanatory/disclaimer copy no longer dominates the screen.

### B. Three-step story

Preserved:

```text
OBSERVATION 1
-> reported count 3
-> review alerts 0

OBSERVATION 2
-> supplied derivative fixture
-> reported count remains 3
-> review alerts 0

OBSERVATION 3
-> later owner-reported count 4
-> one correction alert
-> dependent briefing flagged
```

The HTTP E2E test still pins:
- baseline = 3;
- derivative = 3 / no alert;
- correction = 4 / one alert;
- dependent briefing present.

### C. Evidence boundary

PASS.

Page keeps a visible `Demo mode` indicator.

Expanded note states:
`This deterministic fixture replay uses supplied observations and classifications. No live fetch or model call.`

Recording narration begins:
`A source can be corrected after you publish. This fixture replay shows how EvidenceWatch flags a briefing that needs another look.`

Therefore the recording does not depend on the disclosure being expanded to preserve
the fixture/live distinction.

### D. Clinical presentation

PASS.

No Campfire / TRACE / THR ancestry on product surface.
No competition-internal copy on product surface.
No oversized disclaimer block.
No unsupported "truth oracle" framing presented as the main product identity.

### E. Stop condition

```text
VISUAL PASS = ACCEPTED
VISUAL TASTE DIFFERENCE != DEFECT
UI FREEZE
NO MORE UI CHURN ABSENT CONCRETE DEFECT
```

## Evidence continuity

The repaired-head live NVIDIA/public-web witness still belongs to the byte-identical
runtime snapshot `00017d190...`.

Subsequent standalone changes include docs, launcher safety and UI presentation.
The engine/analyzer/ledger/live-runner semantics used by the live witness have not been
silently revalidated merely because UI main advanced.

Preserve:

```text
CURRENT UI MAIN = 79e4d527...
LIVE RUNTIME WITNESS BASIS = 00017d190...
UI / DOC CHANGE != NEW LIVE VALIDATION
```

## Next

```text
RECORD VIDEO
-> REVIEW FINISHED VIDEO
-> UPLOAD PUBLIC VIDEO
-> INSERT URL INTO FINAL AIRTABLE PAYLOAD
-> FINAL FORM / TERMS REVIEW
-> MARK EXPLICIT SUBMISSION GATE
```

No public repo visibility change.
No submission.
No NVIDIA rerun.

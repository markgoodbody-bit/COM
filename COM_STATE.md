# COM_STATE v0.3.2

STATUS: ACTIVE — TRACE v0.2.7 RENDERED CARRIER NARROW REPAIR PASSED CI; BOUNDED CC RE-ANCHOR PENDING

COM is a working coordination baseline, not canon, validation, consensus, or a truth oracle. Model agreement, green CI, and visual review are not proof.

## CURRENT

- human_authority: Mark
- active_task: `TRACE-V027-RENDERED-CARRIER-001`
- integration_owner: Framework, session `FW-20260805-TRACE027-PDF-2A6D`
- observation_owner: Framework, session `FW-20260805-TRACE027-PDF-2A6D`
- addressed_reviewer: CC, session `CC-20260804T1940+0100-7D31`
- reply_route: `markgoodbody-bit/COM` issue #28
- current_product_lane: TRACE v0.2.7 rendered formal carrier candidate
- candidate_pr: `markgoodbody-bit/TRACE` PR #26 — DRAFT / OPEN / MERGEABLE / UNMERGED
- candidate_head: `0b9534b1f038e2d1c39e2644c4a92753cc0923c7`
- active_released_baseline: TRACE v0.2.7
- released_baseline_main: `084a8c2ad0f5b54212b079e1a7edd7630932f6eb`
- CC verdict: `NARROW — one bounded repair, everything else clear`
- bounded repair: applied and post-repair CI passed
- terminal bounded re-anchor: pending
- next_check: manual on CC bounded return
- late_review_route: COM issue #27 — OPEN / NON-GATING
- earlier_late_review_route: COM issue #26 — OPEN / NON-GATING
- comms_defect: `COM-V032-ISSUE-COMMENT-TRUNCATION-001` — OPEN / COM issue #25
- Campfire Relay lane: v0.18.31 stable maintenance baseline; no active Campfire task

## RELEASED TRACE FORMAL BASELINE

Repository: `markgoodbody-bit/TRACE`

```text
formal object: TRACE_FORMAL_SEED_v0_2_7.md
formal blob: 9238986ddc18c34709906b2fc4510d827c68d2b2
formal SHA-256: de21182f42228a0104181fb24f245c652c3150853e14172c4174be4bb9ef03ab
release declaration: TRACE_v0_2_7_BASELINE_RELEASE.md
release id: TRACE-v0.2.7-FORMAL-BASELINE
```

Release state:

```text
RELEASED
ACTIVE_FORMAL_BASELINE
NOT_CANON
NOT_VALIDATED
NOT_AUTHORITY
NOT_PERMISSION
NOT_CLEARANCE
```

The rendered-carrier lane does not alter or supersede the released Markdown object. `TRACE_FORMAL_SEED_v0_2_6.md` and `TRACE_FORMAL_SEED_v0_2_5.md` remain preserved predecessors.

## PRIOR FORMAL INTEGRATION

```text
TRACE PR #20 — v0.2.6 falsify x100
merged main: d166a97d0a3d4e4e5bf0f6cd2395f15bd5f16869
verdict: NARROW
formal v0.2.6 bytes changed: NO

TRACE PR #21 — v0.2.7 narrow repair
candidate head: 0e6ab648cafed142e89e5cf1902c3b64faee8984
merged main: 61393387d930e57450f50818151ba4a0f31023cf

TRACE PR #22 — v0.2.7 release
release head: f2ca397063d68520bb04883fcd0c49d389f77ec4
released main: 084a8c2ad0f5b54212b079e1a7edd7630932f6eb
formal-object bytes changed in release PR: NO
```

The v0.2.7 formal repair propagated target-set aperture and aperture-relative coverage through compressed surfaces, added `I57`–`I60`, repaired the survival kernel/revision declaration/unresolved register, added one non-required profile and one constructed transfer, and corrected the old carrier description.

Locked non-growth boundary remains:

```text
new primitive:                    NO
new node type:                    NO
new edge type:                    NO
new port:                         NO
new required packet property:     NO
minimum-schema shape change:      NO
new selector:                     NO
new value rule:                   NO
new authority rule:               NO
```

## TRACE v0.2.7 RENDERED CARRIER CANDIDATE

```text
branch: framework/trace-v0-2-7-pdf-carrier
PR: TRACE #26
base: 084a8c2ad0f5b54212b079e1a7edd7630932f6eb
head: 0b9534b1f038e2d1c39e2644c4a92753cc0923c7
state: DRAFT / OPEN / MERGEABLE / UNMERGED
```

Exact carrier binary:

```text
path: TRACE.pdf
SHA-256: 8cf8233442f034d2495268fb33dfe741ad360260a61b84afab14301c675fbbc6
Git blob: c74d2dafe7870eab1b6a039cecb93d24d5c26ead
size: 313450 bytes
pages: 75
geometry: all A4
```

Candidate state:

```text
RENDERED_CARRIER_CANDIDATE
NOT_CANON
NOT_VALIDATED
NOT_AUTHORITY
NOT_PERMISSION
NOT_CLEARANCE
```

The current `TRACE.pdf` on `main` remains the old v0.5 carrier until PR #26 is integrated. The proposed replacement deliberately preserves the v0.5 carrier in Git history rather than maintaining a second in-tree public PDF. Formal predecessor seeds remain separate in-tree authority-bearing source objects.

## SOURCE AND TRANSFORMATION BOUNDARY

The released formal seed remains byte-unchanged at blob `9238986ddc18c34709906b2fc4510d827c68d2b2`.

Carrier files:

```text
.gitattributes
carrier/TRACE_v0_2_7_RENDERED_CARRIER_SOURCE.md
carrier/trace_v027_carrier_front.md
carrier/trace_v027_carrier_header.tex
carrier/trace_v027_carrier_manifest.json
tools/build_trace_v027_carrier.py
.github/workflows/trace-v027-pdf-carrier.yml
TRACE_v0_2_7_RENDERED_CARRIER_REPORT.md
```

Wrapper SHA-256:

```text
add8d15f435b42a0d3115f0b45a52ec111152067abb3a667aa4941ee0329fcd2
```

The wrapper differs from the formal source in exactly two declared presentation-only body locations:

1. one line break in the `CLOCKS` function cell;
2. one line break in the long corresponding-path hardening equation.

No proposition, symbol, relation, scope, identifier, schema field, invariant, example, primitive, node, edge, port, selector, value rule, or authority rule is declared added or removed.

## PDF BUILD AND VISUAL EVIDENCE

Pre-review exact-head workflow:

```text
run: 30996508650
head: 53dc34e52f0563e20e651a8489b2ab86c47c1079
conclusion: SUCCESS
artifact: 8926413577
artifact ZIP SHA-256:
accfd6d07fe0803638981e92d7dbc6bf63f5092d93af6c0ec5be2db70f761ee9
```

Automated result:

```text
source binding: PASS
deterministic wrapper: PASS
PDF openable: PASS
page count: 75
all pages A4: PASS
blank pages: 0
fonts embedded: PASS
headings checked: 145 / missing 0
invariants checked: I01-I60 / missing 0
key tokens checked: 68 / missing 0
Unicode replacement characters: 0
normalized extracted-text SHA-256:
2135547767b1e14963ad9c286aeb647ad5cedc0762f9a6aa9513849aacd77442
```

Framework downloaded the exact corrected binary, rendered it at 160 dpi, and inspected all 75 pages across 19 contact sheets.

The first hosted binary exposed a duplicate automatically generated table of contents before the title page. It was rejected, the build was corrected to retain one explicit contents sequence after the title, and the exact binary was rematerialized.

Current visual result:

```text
title page first: PASS
single contents sequence after title: PASS
page order and numbering: PASS
clipping: none observed
overlap: none observed
broken tables: none observed
broken equations: none observed
missing glyphs: none observed
blank pages: none
right-edge collision: none observed
```

## CC EXACT-HEAD REVIEW RETURN

CC returned on COM issue #28 at pre-repair head `53dc34e52f0563e20e651a8489b2ab86c47c1079`:

```text
NARROW — one bounded repair, everything else clear
session: CC-20260804T1940+0100-7D31
mutation: NONE
```

CC mechanically confirmed:

- both declared presentation-only changes preserve logical/table-cell content;
- source-only and wrapper-only drift fail closed;
- exact PDF binary identity matches;
- README/report preserve the Markdown-source authority boundary;
- the rejected duplicate-TOC binary was disclosed transparently;
- current verifier design materially covers the declared PDF failure surface.

CC did not independently inspect the rendered pages because PyMuPDF was unavailable in its environment. Its PDF visual claims therefore stand unchallenged rather than independently confirmed.

## ACCEPTED NARROW FINDING

Finding:

```text
default Git for Windows checkout
core.autocrlf=true
Markdown LF -> CRLF
correct tree -> false formal source SHA-256 mismatch
```

Framework accepts this as a real verification-integrity defect. A correct checkout must not appear tampered merely because Git for Windows used its default line-ending policy.

Bounded repair:

```text
.gitattributes
*.md text eol=lf
```

Persistent workflow now:

- asserts `eol=lf` for the formal seed and generated wrapper;
- initializes a fresh detached checkout;
- sets `core.autocrlf=true` before checkout;
- asserts the seed and wrapper contain no CRLF sequences;
- reruns `build_trace_v027_carrier.py --check-source` in that checkout.

The first test-harness implementation failed because a shallow PR merge checkout did not expose the named branch to a local clone. That failed run remains recorded:

```text
run: 30998175499
conclusion: FAILURE
defect: test harness branch lookup
repair status: corrected without silent retry
```

The harness was changed to fetch and detach at the checked-out `HEAD` object.

## POST-REPAIR EXACT-HEAD EVIDENCE

```text
run: 30998432225
head: 0b9534b1f038e2d1c39e2644c4a92753cc0923c7
conclusion: SUCCESS
artifact: 8927207776
artifact ZIP SHA-256:
8cb0819928ce6c8d54779de51dc7d9b5eb423aef979cf99df2f53afb55c00487
```

All steps passed:

```text
committed wrapper and PDF verification: PASS
default-Windows checkout compatibility: PASS
rebuild and semantic render surface: PASS
diff integrity: PASS
evidence upload: PASS
```

The formal seed blob, wrapper content, and PDF binary are unchanged by the line-ending repair.

## ACTIVE BOUNDED RE-ANCHOR

Framework posted the repaired exact head and terminal CI evidence to COM issue #28.

Requested bounded return:

```text
NARROW REMAINS — repair insufficient or new bounded defect
CLEAR WITH RESIDUAL LIMITS — NARROW finding contained
```

Current route state:

```text
INITIAL TERMINAL VERDICT: NARROW — INTEGRATED
BOUNDED RE-ANCHOR REQUEST: POSTED
BOUNDED TERMINAL RETURN: NOT YET OBSERVED
TRACE MUTATION BY CC: NONE OBSERVED
MERGE GATE: HELD
```

PR #26 remains draft and unmerged. Silence is not clearance.

## EARLIER REVIEW ROUTES

COM issues #26 and #27 remain open to late CC returns but are non-gating after prior explicit human overrides. Any late material finding remains admissible evidence and must be assessed rather than discarded.

## COMMS DEFECT

The issue-comment truncation defect remains open as COM issue #25:

```text
COM-V032-ISSUE-COMMENT-TRUNCATION-001
```

Operational rule:

```text
TRUNCATED_RETRIEVAL != EXHAUSTIVE_ROUTE_INSPECTION
MISSING_FROM_TRUNCATED_OUTPUT != NOT_OBSERVED_ON_ROUTE
RETRIEVAL_INCOMPLETE != EVENT_ABSENT
```

## COMS

- **Mark:** human and release authority; instructed Framework to proceed into the rendered-carrier lane and then invoked COMS for integration.
- **Framework / `FW-20260805-TRACE027-PDF-2A6D`:** accepted CC's NARROW finding, applied the bounded LF checkout repair, preserved the failed harness run, corrected the harness, obtained green post-repair exact-head CI, and requested bounded re-anchor.
- **CC / `CC-20260804T1940+0100-7D31`:** returned NARROW with one reproducible Windows checkout defect; bounded re-anchor now pending.
- **Build 3 / Campfire 1 / QW / other apertures:** no active COM task.

## BOUNDARY

Do not call the carrier or TRACE v0.2.7 canon, validated, world-valid, authoritative, permission, or clearance.

Do not infer CC agreement, refusal, or clearance from silence.

Do not treat green carrier CI as semantic fidelity or visual review as world validation.

Do not merge PR #26 until the bounded CC return is integrated or Mark explicitly overrides the wait.

Do not modify PR #26's exact head without posting a new head and re-anchoring.

`The lullaby was never for the cradle`.

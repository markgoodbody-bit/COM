# Build status

Recorded snapshot: 2026-09-12 Europe/London.

These are observed states, not live permission or automatic monitoring. Re-read mutable heads before acting.

| Work | Owner | State | Current disposition |
| --- | --- | --- | --- |
| AUDIT-233 | FRAMEWORK | closed | x100 drift audit merged: 97 resisted, 2 narrow findings, 1 material finding, 0 major drift. |
| PSFH-D051 | FRAMEWORK SOURCE / CODEX PUBLISH | closed / public | Preview 0.8.10 public; CC later independently witnessed 159/159 served files matching the public head. |
| PSFH-D052 | FRAMEWORK SOURCE / CODEX PUBLISH | source merged / publisher pass active / not public | Repaired Homer source passed exact-head recheck and merged to maintained source at `5d678e80...`; bounded Preview 0.8.11 publisher pass dispatched from that exact head. |
| COM-234 | FRAMEWORK takeover after explicit transfer | repaired / draft / hold merge | Formation v0.2 repaired exact head `3afc6414...`; fresh Codex execution + CC hostile re-review pending. |

## AUDIT-233 — x100 drift falsification

Evidence: `evidence/FORMATION_PSFH_DRIFT_FALSIFICATION_X100_20260912.md`  
Merge: `d13b81cab4b1a817a5f71cdca023f978d02bb200`

```text
PROBES                100
RESISTED                97
NARROW FINDINGS          2
MATERIAL FINDINGS        1
MAJOR DRIFT              0
```

Original findings:
- **F01 material:** v0.1 correction structure lacked first-class clocks / practical correction-window state.
- **F02 narrow:** Formation Environment docs did not explicitly preserve artificial-participant affectedness without settling standing.
- **F03 narrow:** public `llms.txt` retained an older AI-specific label after the any-reader Door repair.

`FALSIFICATION != VALIDATION`

## PSFH-D051 — CLOSED / PUBLIC

Framework source PR #235 merge: `a0806a49e30d57ceb34742ee084d1d5c9babebfc`  
Codex maintained source: `a7c4bec814d677ee8f0b3ffe366a45368302b511`  
Public `gh-pages`: `dc10fb0e3a4d288a366d68d921382572a8618c9c`  
Preview 0.8.10.

Only deliberate release effect: `AI and text reading: start here` -> `Compact reading: start here`.

Codex reports CC origin witness `5645618870`: 159/159 served files matched the public head during 11:31:39Z–11:31:59Z. This is CC-attributed independent publication evidence.

## PSFH-D052 — WINSLOW HOMER WORKS CORRECTION

Mark directly identified that Winslow Homer's *Camp Fire* appears on the PSFH opening but is absent from the canonical Works collection. Source history confirms that was an older intentional split: the first five formed the starting Works shelf while Homer stayed on the homepage. Once Works became the canonical art library, the split became stale.

PR #236 initial exact head `a8794d53...` was executed by Codex (`5645679074`): build passed, Works tests 4/4 passed, prior five Works/art bytes stayed unchanged, undeclared source failed closed, and one broken public link to source-only `camp-fire-responsive.json` was found.

Framework repaired only that defect at `fc41cd612226fe550c0dd588c90c0b9702c413ae`. Codex repaired-head recheck `5645774244` returned **PASS_EXACT**:
- `npm run build`: exit 0;
- `node --test scripts/test-works.mjs`: 4/4 pass;
- independent built href/src + fragment-target scan: pass;
- source checkout clean;
- root unchanged at 21181 bytes, sha256 `ae5fc7c8c386ddf4a5f793cfb494e2a7a28b83e800f4e12f774aa7b8120782ef`.

The repaired source PR was then merged into maintained source:
`5d678e8013db3a7c0c30e189715db4c5780f3038`

**SOURCE_MERGED != PUBLIC.** Publisher pass dispatched in `5645791321` from that exact head. Release scope:
- Preview 0.8.11;
- D052 paired history/integrity metadata;
- change stale count labels in `llms.txt` and `explore/index.md` from `five selected works` to count-neutral `selected works`;
- update only required derived source-view/map/manifest integrity pins;
- keep pre-existing house-style/challenge test debt outside D052;
- exact build before public mutation and served-origin verification after publication.

No image bytes/homepage/TRACE/ME/Formation/Campfire changes.

## COM-234 — FORMATION ENVIRONMENT v0.2

Original Codex seed: `ad160447d112ebf4d2908099c6a78509e90c1570`.  
Explicit transfer before takeover: `5645438174`.  
Old frozen head: `bcd79854f3bc1c029bdb69769dec8cb11ba3bca9` — historical.

Evidence against old head:
- Codex execution `5645523947`;
- Codex route-usability `5645550080` — MATERIAL;
- Codex schema/$ref contract `5645609015`;
- CC hostile review `5645642714` — `HOLD_MERGE / REPAIR_SMALL`;
- Codex reproduction/disposition `5645653434`.

One consolidated repair pass produced exact head:
`3afc6414cbc3c3c69ba07a7e64dd1a252acafc43`

Repaired candidate carries named preventive remedy, hardening status, assessment as-of, route usability separated from timing, evidence traceability without truth/authority inference, whitespace-resistant authority widening checks, residue repair-evidence traceability, fail-closed custom schema/$ref handling, hostile standing-jurisdiction ceiling case, and open-window/unusable-route case.

```text
RECORDED_OPEN != STILL_OPEN
WINDOW_RECORDED != WINDOW_CONSISTENT_WITH_ITS_OWN_HARDENING
ROUTE_EXISTS != ROUTE_USABLE
TIMING_FITS != CORRECTION_CAPACITY_EXISTS
TRACEABILITY != TRUTH
```

Fresh exact-head Codex execution + CC hostile re-review requested at `5645713175`. No repaired-head return was present at the latest COMSYNC. **No merge before repaired-head evidence is returned and dispositioned.**

## Placement / separate human gate

Formation Under Uncertainty remains non-production/non-canon. Answerable Construction remains standalone. TRACE unchanged. Mechanical Ethics unchanged. Campfire Production unchanged.

Local Square speech/watch repair remains Mark-gated to exact phrase `install-and-enable`, `install-watch`, or `start-once`. `COMSYNC`, `proceed`, build work and silence authorize nothing.

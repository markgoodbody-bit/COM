# Build status

Recorded snapshot: 2026-09-12 Europe/London.

These are observed states, not live permission or automatic monitoring. Re-read mutable heads before acting.

| Work | Owner | State | Current disposition |
| --- | --- | --- | --- |
| AUDIT-233 | FRAMEWORK | closed | x100 drift audit merged: 97 resisted, 2 narrow findings, 1 material finding, 0 major drift. |
| PSFH-D051 | FRAMEWORK SOURCE / CODEX PUBLISH | closed / public | Preview 0.8.10 public; CC later independently witnessed 159/159 served files matching the public head. |
| PSFH-D052 | FRAMEWORK | repaired / draft / hold publication | Homer Works candidate repaired at `fc41cd61...` after Codex exact-head build found one broken unpublished-metadata link; repaired-head recheck pending. |
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

Draft PR #236 initial exact head:
`a8794d536b940a22499099f66d97c06a488acb67`

Codex exact-head execution `5645679074`:
- `npm run build`: exit 0;
- `node --test scripts/test-works.mjs`: 4/4 pass;
- exact output comparison: only sitemap + Works shelf changed and Homer page added; 153 generated files unchanged, including root, prior five Works and art bytes;
- undeclared Works probe refused as intended;
- one real D052 defect found: Homer linked to `camp-fire-responsive.json`, a source custody file not published by the maintained copier;
- broader house-style/challenge failures reproduced on D051 and are pre-existing debt, not D052 failures.

Framework applied only the earned repair. Current frozen repaired head:
`fc41cd612226fe550c0dd588c90c0b9702c413ae`

Repair:
- removed the broken public responsive-record link;
- published `camp-fire.json` is labelled `Image source and viewing-copy details` because it already embeds responsive metadata;
- repinned Homer encounter to 2145 bytes / sha256 `d13dc2796d834f1f71b8c35a0bd4c1ed244e30c1b0c81aeaf27bebabbb7d34cf`;
- Works tests now assert the published details target exists, unpublished responsive JSON is not linked, and Homer appears exactly once in sitemap.

Repaired-head recheck requested at `5645732778`.

No image bytes/homepage/reader/TRACE/ME/Formation/Campfire changes. **No release pass until repaired-head recheck returns.** If it passes, D052 / Preview 0.8.11 history + edition metadata + fresh exact-head build remain a separate release step.

## COM-234 — FORMATION ENVIRONMENT v0.2

Original Codex seed: `ad160447d112ebf4d2908099c6a78509e90c1570`.  
Explicit transfer before takeover: `5645438174`.  
Old frozen head: `bcd79854f3bc1c029bdb69769dec8cb11ba3bca9` — historical.

Evidence against old head:
- Codex execution `5645523947` — 8 tests / 7 pass / 1 brittle assertion; seven examples structurally valid;
- Codex route-usability `5645550080` — MATERIAL;
- Codex schema/$ref contract `5645609015` — narrow fail-closed extension;
- CC hostile review `5645642714` — `HOLD_MERGE / REPAIR_SMALL`, including hardening/window contradiction;
- Codex reproduction/disposition `5645653434` — independently reproduced M1 and whitespace-widening bypass and bounded the repair.

One consolidated repair pass produced exact head:
`3afc6414cbc3c3c69ba07a7e64dd1a252acafc43`

Repaired candidate now carries:
- named `preventive_remedy`;
- hardening status and open-vs-occurred internal consistency;
- explicit assessment as-of;
- route usability separate from timing;
- evidence traceability on non-unknown bounds/definite assessments;
- renamed top-level correction work field so it is not confused with the routing channel;
- whitespace-resistant authority widening traceability without authority inference;
- residue repair evidence without restoration inference;
- fail-closed validator/schema/$ref contract;
- hostile standing self-resolution ceiling example;
- hostile open-window/unusable-route example;
- explicit refusal to turn prose length into a semantic solver.

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

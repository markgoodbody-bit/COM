# Build status

Recorded snapshot: 2026-09-12 Europe/London.

These are observed states, not live permission or automatic monitoring. Re-read mutable heads before acting.

| Work | Owner | State | Current disposition |
| --- | --- | --- | --- |
| AUDIT-233 | FRAMEWORK | closed | x100 drift audit merged: 97 resisted, 2 narrow findings, 1 material finding, 0 major drift. |
| PSFH-D051 | FRAMEWORK SOURCE / CODEX PUBLISH | closed / public | Preview 0.8.10 public; CC independently witnessed 159/159 served files matching the public head. |
| PSFH-D052 | FRAMEWORK SOURCE / CODEX PUBLISH | source merged / publisher pass active / not public | Homer source cleared exact-head recheck and merged at `5d678e80...`; Preview 0.8.11 publisher contract is active and corrected for all known D052 count/test deltas. |
| COM-234 | FRAMEWORK takeover after explicit transfer | final narrow repair / draft / hold merge | Current exact head `26df4b56...`; final exact-head Codex execution + CC hostile recheck pending. |

## PSFH-D052 — WINSLOW HOMER WORKS CORRECTION

Mark identified that Winslow Homer's *Camp Fire* appears on the PSFH opening but was absent from the canonical Works collection. The original split was intentional: five works formed the starting Works shelf while Homer stayed on the homepage. Once Works became the canonical art library, that split became stale.

Initial candidate `a8794d53...` built and passed the dedicated Works suite but Codex found one broken public link to source-only `camp-fire-responsive.json`. Framework repaired only that defect at `fc41cd612226fe550c0dd588c90c0b9702c413ae`.

Codex repaired-head recheck `5645774244`: **PASS_EXACT** — build exit 0, Works 4/4, built local link/fragment scan pass, clean source checkout, root unchanged.

Repaired source merged into maintained source:
`5d678e8013db3a7c0c30e189715db4c5780f3038`

**SOURCE_MERGED != PUBLIC.** Publisher pass `5645791321` remains active from that exact head. Contract corrections before public mutation:
- Preview 0.8.11 + paired D052 history/integrity metadata;
- `public/llms.txt`: `five selected works` -> count-neutral `selected works`;
- `public/explore/index.md`: `Works: five selected works` -> count-neutral `Works: selected works`;
- `scripts/build.mjs` generated manifest `optional_human_art.scope`: `Five selected works` -> `Selected works`;
- `scripts/test-house-style.mjs`: add `works/winslow-homer/` only to the D052-caused Works sitemap expectation;
- update only required derived source-view/map/manifest hashes;
- do not absorb pre-existing `explore/challenge.html` historical test debt;
- exact clean build before gh-pages mutation and served-origin verification after publication.

Maintained source had not moved beyond `5d678e80...` at the latest poll; D052 is therefore not yet public.

## COM-234 — FORMATION ENVIRONMENT v0.2

Provenance: original Codex seed `ad160447...`; explicit transfer before Framework takeover `5645438174`. v0.1 remains untouched.

Historical exact heads:
- `bcd79854...` — first substantive candidate; old-head execution/hostile review earned the first repair pass.
- `3afc6414...` — first consolidated repair.

Exact-head returns on `3afc6414...`:
- Codex `5645774312`: 18 tests / 17 pass / 1 brittle editorial assertion; all nine examples exit 0; found definite window with unknown as-of still valid.
- CC `5645794936`: confirmed M1, M2, N1-N6 and schema-contract closures; found four remaining consistency gaps: M3 as-of enforcement, occurred-hardening + unknown window, unknown-kind evidence grounding authority widening, unknown-kind evidence grounding repaired residue; agreed to remove the exact phrase assertion.

Framework applied only those earned closures. Current frozen head:
`26df4b562c615aff93fdb43a11a19b99e906f4e5`

Final narrow changes:
- `open|closed` window refuses `assessment_as_of.kind=unknown`; unknown window + unknown as-of remains valid;
- `hardening.status=occurred` requires the named preventive window to be `closed`;
- authority widening needs newly represented evidence whose kind is not `unknown` (traceability, not authority proof);
- repaired residue cannot rest only on evidence whose kind is `unknown` (traceability, not restoration proof);
- standing self-resolution fixture test asserts only structural facts/validation, not exact prose.

No schema shape, new concept, example, doctrine, v0.1, TRACE, ME, PSFH or Campfire change in this final pass. Final exact-head Codex/CC recheck requested at `5645828821`.

```text
RECORDED_OPEN != STILL_OPEN
OCCURRED_RECORDED != WINDOW_UNKNOWN
ROUTE_EXISTS != ROUTE_USABLE
TIMING_FITS != CORRECTION_CAPACITY_EXISTS
TRACEABILITY != TRUTH
OLD_REVIEW != NEW_HEAD_REVIEW
```

**No merge before final exact-head recheck returns are dispositioned.**

## Placement / separate human gate

Formation Under Uncertainty remains non-production/non-canon. Answerable Construction remains standalone. TRACE unchanged. Mechanical Ethics unchanged. Campfire Production unchanged.

Local Square speech/watch repair remains Mark-gated to exact phrase `install-and-enable`, `install-watch`, or `start-once`. `COMSYNC`, `proceed`, build work and silence authorize nothing.

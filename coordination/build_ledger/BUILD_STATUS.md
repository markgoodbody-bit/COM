# Build status

Recorded snapshot: 2026-09-12 Europe/London.

These are observed states, not live permission or automatic monitoring. Re-read mutable heads before acting.

| Work | Owner | State | Current disposition |
| --- | --- | --- | --- |
| AUDIT-233 | FRAMEWORK | closed | x100 drift audit merged: 97 resisted, 2 narrow findings, 1 material finding, 0 major drift. |
| PSFH-D051 | FRAMEWORK SOURCE / CODEX PUBLISH | closed / public | Preview 0.8.10 superseded by D052; CC independently witnessed 159/159 served D051 files. |
| PSFH-D052 | FRAMEWORK SOURCE / CODEX PUBLISH | public branch + Pages deployment success / origin witness incomplete | Maintained source `d30143e4...`; public `2962fb63...`; Pages run `34694019662` succeeded. This runtime cannot DNS-resolve the custom origin, so independent served-origin comparison remains UNKNOWN here. |
| COM-234 | FRAMEWORK takeover after explicit transfer | test-fixture-only final head / draft / hold merge | Production guards cleared at `26df4b56...`; sole failing test was fixture setup. Test-only repair head `9be41ff9...`; final suite + diff receipts requested. |
| AC-237 | FRAMEWORK | draft / independent attack | Answerable Construction current front door demoted to project synthesis/cross-owner integration lens after external-owner falsification; exact head `520dfe4e...`, 2 files only. |

## PSFH-D052 — WINSLOW HOMER WORKS CORRECTION

Mark identified that Winslow Homer's *Camp Fire* appears on the PSFH opening but was absent from the canonical Works collection. The original split was intentional: five works formed the starting Works shelf while Homer stayed on the homepage. Once Works became the canonical art library, that split became stale.

Initial candidate `a8794d53...` built and passed the dedicated Works suite but Codex found one broken public link to source-only `camp-fire-responsive.json`. Framework repaired only that defect at `fc41cd612226fe550c0dd588c90c0b9702c413ae`.

Codex repaired-head recheck `5645774244`: **PASS_EXACT** — build exit 0, Works 4/4, built local link/fragment scan pass, clean source checkout, root unchanged.

Repaired source merged at `5d678e8013db3a7c0c30e189715db4c5780f3038`. Codex then prepared the bounded D052 publication at maintained-source head:
`d30143e402a0c78f27d3cbbb887e6e5564b1ef2d`

That commit carries:
- Preview 0.8.11;
- paired D052 history/integrity metadata;
- count-neutral Works wording in `llms.txt`, Explore Markdown and generated manifest scope;
- required source-view/history/hash updates;
- the Homer Works route in the D052-caused sitemap test expectation;
- no art-byte or prior-five encounter mutation.

Public `gh-pages` moved to:
`2962fb63253758cd046a65b4fd0eeeccdb7f3e5b`

Commit message records thirteen changed outputs plus one new encounter while preserving original artwork and five prior encounters. GitHub Pages run `34694019662` started on that exact head and completed **success**.

**Public-branch deployment is evidenced. Independent custom-origin byte witness is incomplete in this Framework runtime:** direct origin fetch failed because its container DNS cannot resolve the domain, and the web fetch surface cannot newly open the unindexed custom URL. Do not relabel that transport limitation as an origin mismatch.

```text
PUBLIC_BRANCH_MOVED + PAGES_SUCCESS != INDEPENDENT_ORIGIN_BYTE_WITNESS
TRANSPORT_FAILURE != CONTENT_FAILURE
PUBLICATION != VALIDATION
```

## COM-234 — FORMATION ENVIRONMENT v0.2

Provenance: original Codex seed `ad160447...`; explicit transfer before Framework takeover `5645438174`. v0.1 remains untouched.

Historical exact heads:
- `bcd79854...` — first substantive candidate;
- `3afc6414...` — first consolidated repair;
- `26df4b56...` — final production-guard repair before the fixture-only test fix.

Exact-head returns on `26df4b56...`:
- Codex: 21 tests / 20 pass / 1 fail; all nine examples exit 0; all four hostile-2 probes now rejected; reported-evidence and uncertainty controls pass; v0.1 untouched; diff scope v0_2 only.
- CC hostile-3: **PASS on the guards / REPAIR_SMALL test fixture only**; every earlier closure held.

The sole failure was a test setup error: `test_unknown_window_may_remain_evidence_incomplete` assumed example 06 already had `assessment_as_of.kind=unknown`, while that example legitimately uses an event bound. Codex independently showed that explicitly mutating the test record to an unknown as-of validates as intended.

Framework changed **only that test fixture setup**. Current frozen head:
`9be41ff97ccdd4c3613edcad0c673fd77663caa2`

No `validate.py`, schema, example, README, interface, v0.1, TRACE, ME, PSFH or Campfire change from the CC-cleared guard head. Final short receipt request: PR #234 comment `5645920845` — Codex full suite + nine examples, CC exact diff-only confirmation.

```text
TEST_FIX != PRODUCTION_RULE_CHANGE
RECORDED_OPEN != STILL_OPEN
OCCURRED_RECORDED != WINDOW_UNKNOWN
ROUTE_EXISTS != ROUTE_USABLE
TIMING_FITS != CORRECTION_CAPACITY_EXISTS
TRACEABILITY != TRUTH
```

**No merge before the `9be41ff9...` final receipts return.**

## AC-237 — ANSWERABLE CONSTRUCTION OWNER DEMOTION

Fresh external-owner falsification on 12 September cut the local claim substantially. Established owners already carry much of the previously broad positive-construction territory: Dynamic Adaptive Policy Pathways; Responsible Innovation; Capability Approach; Just Transition; Value Sensitive Design/value change; systems-engineering lifecycle traceability/change impact; distributed-responsibility/many-hands practice.

COM #76 receipt `5645906379` records the adverse/owner-correction evidence. A second owner check found that ordinary systems engineering already owns most of the lifecycle traceability mechanism.

Framework therefore built a two-file current-front-door demotion candidate, draft PR #237:
`520dfe4e416dd21890dd9355d501a59497ea5e39`

Only `answerable-construction/README.md` and `answerable-construction/index.json` change. v0.1 paper/casebook/reader stay untouched as historical working artifacts. Candidate remainder: project-specific cross-owner integration/attention lens, not novel theory or traceability mechanism; add nothing where established owners already preserve the relation. Independent attack requested at `5645915725` before merge.

## Formation external-owner falsification — RESEARCH ONLY / NO MUTATION

A fresh external pass also cuts broad novelty around reciprocal/bidirectional formation:
- CHI/ICLR Bidirectional Human-AI Alignment explicitly studies dynamic reciprocal co-adaptation;
- Carroll et al. formalize changing and influenceable human preferences;
- Collective Alignment / Collective Constitutional AI address public participation in model values;
- Anthropic character work treats richer dispositions as an alignment intervention;
- participatory/community norm elicitation and current coevolutionary human-AI work occupy adjacent ground.

No Formation source demotion has been made from this pass. The narrower candidate remainder still to falsify is operational: answer-back, explicit authority, correction capacity, evaluator fallibility and dependency/recovery in a bounded arrangement.

## Placement / separate human gate

Formation Under Uncertainty remains non-production/non-canon. Answerable Construction current placement is under active demotion review, not settled by PR #237 yet. TRACE unchanged. Mechanical Ethics unchanged. Campfire Production unchanged.

Local Square speech/watch repair remains Mark-gated to exact phrase `install-and-enable`, `install-watch`, or `start-once`. `COMSYNC`, `proceed`, build work and silence authorize nothing.

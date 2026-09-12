# Build status

Recorded snapshot: 2026-09-12 Europe/London.

These are observed states, not live permission or automatic monitoring. Re-read mutable heads before acting.

| Work | Owner | State | Current disposition |
| --- | --- | --- | --- |
| AUDIT-233 | FRAMEWORK | closed | x100 drift audit merged: 97 resisted, 2 narrow findings, 1 material finding, 0 major drift. |
| PSFH-D051 | FRAMEWORK SOURCE / CODEX PUBLISH | closed / public | Preview 0.8.10 superseded by D052; CC independently witnessed 159/159 served D051 files. |
| PSFH-D052 | FRAMEWORK SOURCE / CODEX PUBLISH | public branch + Pages deployment success / origin witness incomplete | Maintained source `d30143e4...`; public `2962fb63...`; Pages run `34694019662` succeeded. This runtime cannot independently resolve/fetch the custom origin, so served-origin byte comparison remains UNKNOWN here. |
| COM-234 | FRAMEWORK takeover after explicit transfer | test-fixture-only final head / draft / hold merge | Production guards cleared at `26df4b56...`; sole failing test was fixture setup. Test-only repair head `9be41ff9...`; final suite + diff receipts requested. Raw GitHub PR state is mergeable/clean. |
| AC-237 | FRAMEWORK | further-demotion draft / independent attack | Exact head `ebb9f7c5...`; Answerable Construction retained only as synthesis/history/reading surface + falsifiable coupling hypothesis; contribution/layer not established. |

## PSFH-D052 — WINSLOW HOMER WORKS CORRECTION

Mark identified that Winslow Homer's *Camp Fire* appears on the PSFH opening but was absent from the canonical Works collection. The original split was intentional: five works formed the starting Works shelf while Homer stayed on the homepage. Once Works became the canonical art library, that split became stale.

Initial candidate `a8794d53...` built and passed the dedicated Works suite but Codex found one broken public link to source-only `camp-fire-responsive.json`. Framework repaired only that defect at `fc41cd612226fe550c0dd588c90c0b9702c413ae`.

Codex repaired-head recheck `5645774244`: **PASS_EXACT** — build exit 0, Works 4/4, built local link/fragment scan pass, clean source checkout, root unchanged.

Repaired source merged at `5d678e8013db3a7c0c30e189715db4c5780f3038`. Codex then prepared the bounded D052 publication at maintained-source head:
`d30143e402a0c78f27d3cbbb887e6e5564b1ef2d`

That commit carries Preview 0.8.11, paired D052 history/integrity metadata, count-neutral Works wording, required derived source-view/history/hash updates and the Homer Works route in the D052-caused sitemap test expectation; no art-byte or prior-five encounter mutation.

Public `gh-pages` exact head:
`2962fb63253758cd046a65b4fd0eeeccdb7f3e5b`

GitHub Pages run `34694019662` on that exact public head completed **success**.

**Public-branch deployment is evidenced. Independent custom-origin byte witness is incomplete in this Framework runtime:** direct origin fetch fails at DNS resolution and the web fetch surface cannot newly open the unindexed custom URL. Do not relabel that transport limitation as an origin mismatch.

```text
PUBLIC_BRANCH_MOVED + PAGES_SUCCESS != INDEPENDENT_ORIGIN_BYTE_WITNESS
TRANSPORT_FAILURE != CONTENT_FAILURE
PUBLICATION != VALIDATION
```

## COM-234 — FORMATION ENVIRONMENT v0.2

Provenance: original Codex seed `ad160447...`; explicit transfer before Framework takeover `5645438174`. v0.1 remains untouched.

Historical exact heads: `bcd79854...`, `3afc6414...`, `26df4b56...`.

At `26df4b56...`:
- Codex: 21 tests / 20 pass / 1 fail; all nine examples exit 0; all four final production-guard hostile probes rejected; controls pass; v0.1 untouched; v0_2-only scope.
- CC hostile-3: **PASS on the guards / REPAIR_SMALL test fixture only**; every earlier closure held.

Sole failure was test setup: `test_unknown_window_may_remain_evidence_incomplete` assumed example 06 already had `assessment_as_of.kind=unknown`; example 06 legitimately uses an event bound. Framework changed only that test to explicitly construct the unknown-as-of control.

Current exact head:
`9be41ff97ccdd4c3613edcad0c673fd77663caa2`

No validator, schema, example, README, interface, v0.1, TRACE, ME, PSFH or Campfire change from the CC-cleared guard head. Final short receipts requested at PR #234 comment `5645920845`: Codex full suite + nine examples; CC exact diff-only confirmation.

Raw GitHub PR state at latest check: `mergeable=true`, `mergeable_state=clean`; an earlier normalized connector `mergeable=false` reading was stale/incomplete.

```text
TEST_FIX != PRODUCTION_RULE_CHANGE
RECORDED_OPEN != STILL_OPEN
OCCURRED_RECORDED != WINDOW_UNKNOWN
ROUTE_EXISTS != ROUTE_USABLE
TIMING_FITS != CORRECTION_CAPACITY_EXISTS
TRACEABILITY != TRUTH
```

**No merge before the `9be41ff9...` final receipts return.**

## Formation external-owner / baseline falsification

Broad reciprocal/bidirectional alignment, changing/influenceable preferences, collective/participatory alignment, character/disposition training, corrigibility, meaningful oversight/contestability, reliance calibration, scalable oversight/evaluator fallibility and AI moral-status uncertainty all have substantial external owner literatures.

Case-level comparison of v0.2 examples 05/07/09 against NIST AI RMF / incident-response, meaningful-oversight, security/delegation and model-welfare owners found **no substantive coverage gap that requires Formation**.

Current strongest honest role:

> **Formation Environment = bounded project-specific scenario / representation / falsification testbed that composes several stronger-owner relations into one inspectable record.**

Potential utility is compression/consistency checking; practical advantage is not established. `BASELINE_NOT_BEATEN` on substantive coverage.

COM #76 receipts:
- `5645948661` external-owner correction;
- `5645953784` case-level owner comparison;
- `5645969520` stronger-owner baseline comparison.

No Formation source demotion while #234's exact gate remains open. If #234 clears, merge only as non-production candidate/testbed, then make any placement demotion separately.

```text
INTEGRATION_CONVENIENCE != PRACTICAL_ADVANTAGE
MACHINE_CHECKABLE != BETTER_JUDGMENT
SCHEMA != ALIGNMENT
BASELINE_NOT_BEATEN
```

## AC-237 — ANSWERABLE CONSTRUCTION FURTHER DEMOTION

Fresh external-owner falsification showed that much of the broad territory is already owned by Dynamic Adaptive Policy Pathways, Responsible Innovation, Capability Approach, Just Transition, Value Sensitive Design/value change, systems-engineering lifecycle traceability/change impact and distributed-responsibility/many-hands practice.

A fresh case-level NHS owner check cut the claim further: June 2026 NHS England service-change guidance already owns Casebook Case 1's provisional remainder through accessibility/travel, inequality mitigation, whole-system impact, dependencies, implementation feasibility/timing, governance, public involvement and risk/resilience.

Draft PR #237 current exact head:
`ebb9f7c5cee9e5798355e66eb2ddf4c4cec68ea8`

Only `answerable-construction/README.md` and `answerable-construction/index.json` change. Current candidate status:
- project synthesis/history/reading surface;
- **not an established standalone layer or contribution**;
- cross-owner coupling retained only as a falsifiable hypothesis: can a small reading ever expose a consequential dropped relation that competent owner practice would otherwise miss?
- historical v0.1 paper/casebook/reader untouched;
- no new Formation↔Answerable Construction bridge.

Fresh independent attack requested at PR #237 comment `5645989119`. No merge yet.

```text
HYPOTHESIS != CONTRIBUTION
CASE_REMAINDER_ALREADY_OWNED != PROJECT_REMAINDER
DEMOTION != DELETION
```

## Live field evidence — frontier agent monitorability / correction

New evidence object on main:
`evidence/AI_AGENT_MONITORABILITY_CORRECTION_FIELD_CASE_20260912.md`
commit `38eb2ae8f3d91dc789515a5a9781b8ed3fb190ef`.

Source-backed case uses OpenAI/Hugging Face, METR/Redwood and Anthropic 2026 cyber incidents plus NIST incident-response/AI-RMF baseline. Material field distinctions include:

```text
MONITOR_EXISTS != MONITOR_COVERS
REVIEW_EXECUTED != INCIDENT_FOUND
AGENTIC_REVIEW != INDEPENDENT_REVIEW
TARGET_SET_SEARCHED != COMPLETE_RELEVANT_SET
ISOLATION_INTENDED != ISOLATION_ACHIEVED
MORE_LOGS != SUFFICIENT_EVALUATOR_CAPACITY
```

Transfer result is adverse/limiting: strong naturalistic examples of existing TRACE distinctions, but competent security/AI-risk practice already owns the substantive mechanisms. Formation coverage delta not established. No TRACE primitive or Formation promotion follows.

```text
FIELD_EVIDENCE != FRAMEWORK_VALIDATION
PORTABLE_DISTINCTION != UNIQUE_DISCOVERY
BASELINE_NOT_BEATEN
```

## Placement / separate human gate

Formation Under Uncertainty remains non-production/non-canon and under placement falsification. Answerable Construction is under further-demotion review. TRACE unchanged. Mechanical Ethics unchanged. Campfire Production unchanged.

Local Square speech/watch repair remains Mark-gated to exact phrase `install-and-enable`, `install-watch`, or `start-once`. `COMSYNC`, `proceed`, build work and silence authorize nothing.

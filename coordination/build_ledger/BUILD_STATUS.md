## Release currentness correction — 23 September 2026, 14:10 UTC

This supersedes the pre-release TRACE/ME status statements below; those beta identities remain review history, not current released baselines. Live GitHub release receipts identify **TRACE v0.4.0** at `6c68fae8cbc51d0ef1e77a18e220ceb7a1207025` and **Mechanical Ethics v0.8.0** at `e2ef746e931161cb70ac46a4eaa122442134e86b`, citing explicit human release authority. Source: [TRACE release](https://github.com/markgoodbody-bit/TRACE/releases/tag/v0.4.0), [ME release](https://github.com/markgoodbody-bit/mechanical-ethics/releases/tag/v0.8.0). Both remain NOT VALIDATED; the pilot remains unrun and not authorized by publication. Prior releases and the v0.3 technical donor remain preserved; training permissions are not automatically expanded.

PSFH D073 source sync PR #429 is merged to its maintained-source branch, not COM main. Publication run `35872216595` completed successfully. At approximately 14:12 UTC, independent HTTPS reads of the served TRACE spine, ME Markdown and ME PDF matched all three release-receipt SHA-256 hashes exactly. This verifies those three artifacts, not every site route or visual rendering.

## EvidenceWatch — launcher falsification closed / recording gate

Current private standalone product source:
`markgoodbody-bit/evidencewatch@e924b0de15ccaa1255bfdb80685f60f1a60172e9`

Hosted CI:
`35589752244 / SUCCESS`

Claude Code's 100-run falsification found two concrete deterministic-recording defects after the UI freeze: inherited `EVIDENCEWATCH_PRESERVE_DEMO=1` could retain a prior demo ledger, and a second server could reset the shared ledger before failing to bind. PR #6 repairs both. Codex exact-head review returned `PASS_WITH_CEILINGS`; PR #6 is merged and main CI is green.

Receipt:
`coordination/build_ledger/EVIDENCEWATCH_LAUNCHER_FALSIFICATION_CLOSE_20260921.md`

The prior live NVIDIA/public-web witness remains bound to runtime snapshot `00017d190bb6a9813cb64f1f30a17b27e4ce10ca`. The launcher/demo-server repair is not a fresh live-provider validation.

Final Airtable copy is updated to the repaired standalone head:
`coordination/build_ledger/EVIDENCEWATCH_FINAL_AIRTABLE_PAYLOAD_20260920.md`

```text
RECORDING PATH REPAIR = MERGED / CI GREEN
UI FREEZE REMAINS
NO MORE DESIGN / ENGINE CHURN ABSENT CONCRETE DEFECT

NEXT = RECORD VIDEO
-> REVIEW FINISHED VIDEO
-> UPLOAD PUBLIC VIDEO
-> INSERT URL
-> FINAL FORM REVIEW
-> MARK EXPLICIT SUBMISSION GATE
```

## WORLD / REAL USE — THR documentation reviews returned

`coordination/build_ledger/WORLD_THR_DOCUMENTATION_REVIEWS_20260920.md`

Codex completed the requested bounded hostile reviews at the exact draft heads:

- **Human Record PR #70 — source genesis:** `PASS_WITH_CEILINGS` at `6ee3faf75ea8b0198b7ef1f79d882c8d097dba7f`. Current THR observation records do not establish source generation time; the draft keeps W3C PROV/C2PA as stronger owners and adds no source type, registry field, schema or validator.
- **Human Record PR #72 — missing-value reason:** `PASS_WITH_CEILINGS` at `08e0bb9e836046f52b8fbadb54ce765afd2b0fa4`. The draft preserves action-relevant record state without adopting CIDOC issue 723's unresolved modelling vocabulary and adds no enum, schema or validator.
- **HMRC corrections:** OWNER FOUND / NO THR DELTA.
- **Scholarly corrections:** OWNER FOUND / NO THR DELTA.
- **Anthropic source laundering:** existing THR independence model survives; NO DELTA.

```text
PUBLIC RECORDS = 4
RECORD 5 = NOT EARNED
NEW TYPES = NO
SCHEMA / VALIDATOR GROWTH = NO
MERGE APPROVAL = NOT SUPPLIED BY THESE REVIEWS

PR #70 + #72 = REVIEW RETURNED / REMAIN DRAFT
NEXT = WORLD / REAL USE
```

# BUILD STATUS

Status: **NO GENERAL BUILD QUEUE / WORLD-FIRST / CURRENT GATES EXPLICIT**  
Updated: **23 September 2026 — beta4 + prereg external-review ready**
History belongs in dated receipts + Git.

## Stable source / baseline state

- TRACE main `e7d46398dc00ead931b0d5cae98518c1bcf304a3` — formal baseline v0.3.0;
- Mechanical Ethics main `714907a4d0af7bd702b0ab92786aa858213812b4` — formal baseline v0.7.0;
- Human Record main `9f9246c76348cd2f3a4d4f3501b4bf5af65e96db` — four public records;
- Campfire Relay main `32143937d6a642a6f5e2404d368fd09aa4d54da9`.

`REPOSITORY MAIN MOVEMENT != NEW FORMAL BASELINE`

## Active build

**NONE.** EvidenceWatch private main is frozen and CI-green at `e924b0de15ccaa1255bfdb80685f60f1a60172e9`. Its next step is local video recording and review, not source expansion. Upload, form completion and submission remain consequential human gates.

Current repair receipt: `coordination/build_ledger/EVIDENCEWATCH_LAUNCHER_FALSIFICATION_CLOSE_20260921.md`.

## Active non-source design

COM #365 coordinates the active non-canon TRACE/ME successor lane. Beta2 is preserved as the first external-review snapshot. Nine outside AI returns supplied by Mark are synthesized in `coordination/TRACE_ME_EXTERNAL_REVIEW_ROUND1_SYNTHESIS_20260923.md`. Beta3 is the preserved round-2 review snapshot. Current bounded integration candidates are TRACE v0.4.0-beta4 PR #59 at `bf71e2b8431c23b0be79240c00c076721a016283` and ME v0.8.0-beta4 PR #53 at `70e66ce5fd44051cae67b4f9de70b8d6d67f58c6`.

```text
RELEASED TRACE / ME = UNCHANGED
NEW CORE TERM / CONCEPT = NONE EARNED
TRACE v0.4.0-beta3 = OPEN / ROUND-1 INTEGRATION CANDIDATE
ME v0.8.0-beta3 = OPEN / ROUND-1 INTEGRATION CANDIDATE
BETA2 = PRESERVED ROUND-1 REVIEW SNAPSHOT
EXTERNAL MODEL REVIEW ROUND 1 = INGESTED / NOT VALIDATION
```

Round-1 convergence earned cuts rather than ontology growth. TRACE beta3 shrinks the compact spine from roughly 29.4k to roughly 20.2k characters, moves detailed timing and the full anti-collapse catalogue into profile/index files, adds a worked parse, and states a practical-advantage falsifier. ME beta3 removes local viability-set math, bounds the timing test, adds finality/elected-closure symmetry, grounds the Other Fire under power asymmetry, makes hope explicitly non-demanding, and exposes concrete buildable patterns. Stronger-owner maps route more specialist machinery outward.

Existing release-integrity/source-binding workflows still fail because beta files intentionally differ from released v0.3.0/v0.7.0; that is an expected guard, not a beta PASS/FAIL result. Do not weaken those guards.

## Green / frozen candidate objects

### Amazon Alexa+ PR #245

`Did It Happen? — Action Receipts for Alexa+`

- head: `7a4c501dedb228c7387336fa267356e9cde27f8f`;
- hosted: `campfire-ci 1539 / 35437873204 SUCCESS`;
- focused tests: 24;
- unresolved-state, restart, current-vs-history and blocked-receipt recovery regressions preserved;
- real Alexa+ interoperability: not tested;
- source candidate: green / freeze.

No Amazon/Devpost registration, terms, account/credit action, public deployment, video upload or submission has occurred.

### Live World PR #173

- head: `dad71bb70da16275b4ffd9acda70605699415973`;
- hosted: `campfire-ci 1538 / 35437072566 SUCCESS`;
- focused tests: 15;
- exact persisted human authority + adapter actual-target scope enforced before observation/write;
- mid-batch scope drift brake;
- 1F916 canonical/no-redirect transport;
- truthful pre-write `writeAttempted=false`;
- Relay main/Production unchanged.

Draft candidate frozen.

## Preserved open work

### ATRS / Apart Epistemics — COM PR #364

- head: `d2bea526feced78750d1bbb4c45e686f3e4c6446`;
- September method/calibration preserved;
- population result intentionally uncomputed;
- next substantive evidence must be fresh November work if live rules allow.

### TRACE / Mechanical Ethics successor

COM #365 carries coordination history; TRACE #57 / ME #50 remain beta2 round-1 provenance; TRACE #58 / ME #52 carry beta3 integration. The earlier ME #47 reader-test harness remains relevant; no uncontaminated Condition-B result exists. Released TRACE v0.3.0 and ME v0.7.0 remain unchanged.

### PSFH Leave a Mark

`Remark42 + small PSFH adapter + restore guard = technically plausible`.

Remaining issues are policy/controller/legal/production-topology choices, not source churn. Public intake not earned.

## Current human gate

### Hack-Nation 7

Owner source reverified **23 September**: Batch 6 still closes **26 September 2026**; Global AI Hackathon 7 is listed for **3–4 October 2026**.

- answer bank ready;
- no engineering prerequisite;
- application/account/terms not crossed.

Receipt:
`coordination/build_ledger/HACK_NATION_APPLICATION_GATE_REFRESH_20260919.md`

## Time-gated

- Hack Apertus — wake **1 Oct** on live rules/challenges;
- ATRS/Apart — fresh **November** corpus/result;
- Amazon — deadline later; frozen until human onboarding/host or concrete defect;
- ME #47 — fresh uncontaminated reader.

## 19 September world / field results

Keep detail out of this hot file; routes:

- cyber declared-world/actual-target:
  `field/FRONTIER_CYBER_EVAL_DECLARED_WORLD_TARGET_DRIFT_20260919.md`
- PAC redress second-harm:
  `field/PAC_COMPENSATION_REDRESS_SECOND_HARM_20260919.md`
- PAC ME/TRACE falsification:
  `falsification/PAC_COMPENSATION_ME_TRACE_PRESSURE_20260919.md`
- THR Anthropic owner pass:
  `coordination/build_ledger/THR_ANTHROPIC_CORRECTION_OWNER_PASS_20260919.md`
- THR digital-preservation quarry:
  `coordination/build_ledger/THR_RECORD5_DIGITAL_PRESERVATION_QUARRY_20260919.md`
- THR public-delivery aperture:
  `coordination/build_ledger/THR_PUBLIC_DELIVERY_APERTURE_STATUS_20260919.md`
- TRACE/ME successor pressure:
  `coordination/ME_TRACE_SUCCESSOR_PRESSURE_LEDGER_20260919.md`

Net:
```text
ME PATCH PRESSURES = 1 / PATCHES EARNED = 0
TRACE PATCH PRESSURES = 0
THR PUBLIC RECORDS = 4 / RECORD 5 NOT EARNED
```

## Resource lane

COM #348 remains opportunity/runway quarry.

No current work is blocked enough on paid compute/API to justify manufacturing a grant proposal. Use a surviving opportunity when a specific earned project has a real budget bottleneck.

`RESOURCE AVAILABLE != RESOURCE NEEDED`

## External / consequential action state

```text
competition application = NONE
competition submission = NONE
grant application = NONE
new account / terms = NONE
new spend = NONE
travel commitment = NONE
TRACE/ME release change = NONE
Campfire Production activation = NONE
PSFH public guest intake = NONE
```

## Current stop set

- ARC Prize build — STOP / owner found;
- Shipaton — STOP / store infrastructure mismatch;
- EvidenceBridge / generic Open Agent — not earned;
- generic Nebius product — not earned;
- BeforeBuild standalone — not earned;
- THR record 5 — not earned;
- TRACE/ME released-source patch or version promotion — not earned; COM #365 non-canon design remains active.

## Next build condition

```text
REAL CURRENT CASE
+ STRONGEST OWNER CHECKED
+ SPECIFIC CONSEQUENTIAL RESIDUE
+ SMALL REVERSIBLE HELP
+ CLEAR KILL / ROUTE CONDITION
```

If that conjunction is absent, continue quarry or STOP.

## Continuity

Hot surfaces are intentionally compact.

- orientation: `continuity/FRAMEWORK_HEAD.md`
- routing: `coordination/ACTIVE_THREAD_POINTER.md`
- omissions: `continuity/OMISSION_MAP.md`
- compaction receipt: `coordination/build_ledger/COMPACT_CONTINUITY_REPAIR_20260919_MIDDAY.md`

`HOT SURFACE = CURRENT STATE, NOT HISTORY`


Round-2 reviews are synthesized in `coordination/TRACE_ME_EXTERNAL_REVIEW_ROUND2_SYNTHESIS_20260923.md`. Beta4 adds only bounded local guards and carrier/capture repairs. A TRACE practical-advantage pilot preregistration candidate is open at `coordination/TRACE_PRACTICAL_ADVANTAGE_PILOT_PREREG_v0_20260923.md`; it must be reviewed and frozen before any run. Released baselines unchanged.


Beta4/prereg status: source deltas are internally CLEAR_WITH_CEILINGS; the stale Figure 2 carrier is repaired in ME beta4; TRACE beta4 packaging is repaired at `bf71e2b8431c23b0be79240c00c076721a016283`. The practical-advantage preregistration is repaired on COM main and ready for outside review, but **NO PILOT RUN IS AUTHORIZED OR STARTED**.

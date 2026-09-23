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
Updated: **23 September 2026 — TRACE/ME released + PSFH D084 live**
History belongs in dated receipts + Git.

## Stable source / baseline state

- TRACE main `6c68fae8cbc51d0ef1e77a18e220ceb7a1207025` — released compact baseline v0.4.0;
- Mechanical Ethics main `e2ef746e931161cb70ac46a4eaa122442134e86b` — released reader baseline v0.8.0;
- Human Record main `0a8e5370891c09bb0993a4da136219e658d1d104` — four public records; entity-admission guard integrated;
- Campfire Relay main `192caed51cabc6fdf60cebea3c1bb7df548ecdb0` — COMSYNC/watchdog split integrated; Production unchanged.

`REPOSITORY MAIN MOVEMENT != NEW FORMAL BASELINE`

## Active build

No single Production/source build lane is currently authorized.

EvidenceWatch private main is frozen and CI-green at `e924b0de15ccaa1255bfdb80685f60f1a60172e9`; its next step is local video recording/review, not source expansion. Upload, form completion and submission remain consequential human gates.

Current reversible maintenance/design candidates:
- **PSFH D084** — D079-D083 core presentation systems retained; a concrete accessibility collision between contextual art and the reading-room shell is repaired so each art-bearing node room exposes one intended first-action skip link, published and selected-live-byte verified at `gh-pages@9c950c6e9be3e59cfbdc09f4f6a6a187e6a04c29`; remaining long-form/utility pages currently inherit the shared stylesheet without a concrete defect, so no D085 is queued by momentum;
- **THR #75** `1b0766a66c675689f0ae6df97609a032caef1946` — entity-admission containment/catalogue repair, CI green, unmerged, no record/registry/catalogue data change;
- **Relay #256** `c630cafeb2efde1888bc773a0eaeb03376cf569b` — two bounded COMSYNC maintenance repairs, campfire-ci green, unmerged, no Production activation.

Current EvidenceWatch repair receipt: `coordination/build_ledger/EVIDENCEWATCH_LAUNCHER_FALSIFICATION_CLOSE_20260921.md`.

## Active non-source design

TRACE / Mechanical Ethics release work is complete. COM #365 now carries successor/review provenance and routes future pressure into real-world/use testing.

```text
TRACE v0.4.0 = RELEASED / NOT VALIDATED / NO EFFICACY RESULT
ME v0.8.0 = RELEASED / NOT VALIDATED
TRACE BETA PRS #56-59 = CLOSED / HISTORY PRESERVED
ME BETA PRS #49/#50/#52/#53 = CLOSED / HISTORY PRESERVED
BETA5 = NOT EARNED
PRACTICAL-ADVANTAGE PILOT = UNRUN / SEPARATE TEST
```

Round-1/2 review earned cuts, attribution and clearer boundaries rather than ontology growth. Do not reopen released prose by review momentum. Next source change requires a concrete defect or world/use evidence.

## Green / frozen candidate objects

### Amazon Alexa+ PR #245

`Did It Happen? — Action Receipts for Alexa+`

- head: `c0f8a94bb0aeec73e780c24d35c93372a306ee7d`;
- hosted: `campfire-ci / 35875127444 SUCCESS`;
- focused candidate tests: 25;
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

COM #365 carries coordination and review history. TRACE beta PRs #56-59 and ME beta PRs #49/#50/#52/#53 are closed after release with branches/history preserved. The earlier ME #47 reader-test harness remains relevant; no uncontaminated Condition-B result exists. Released TRACE v0.4.0 and ME v0.8.0 are frozen pending concrete defects or world/use evidence.

### PSFH combined first-contact candidate

PR #440 + #442 + #443 were integrated in D078 and D079 published Mark's lighter-opening copy. D080 deliberately leaves that front door alone and cleans the deeper Works system instead: one shared stylesheet/grammar, aspect-preserving shelf wells, consistent art-first account structure and continuation routes, with exact D080 wrapper pins and a current-state Works CI regression. Component branches remain history/provenance, not an active publication queue.

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


Practical-advantage test status: **UNRUN / SEPARATE TEST / NOT PROJECT VERDICT**. Outside review has already repaired multiple preregistration defects. Latest #365 discussion leaves prompt asymmetry as an open method item; freeze the intended workflow/scoring before any run. Do not lengthen cases, change cost amortisation, alter scoring or rescue subgroups after outcomes. Released TRACE v0.4.0 / ME v0.8.0 remain frozen absent a concrete source defect or world/use pressure.

TRACE/ME/PSFH status: TRACE v0.4.0 and ME v0.8.0 released; PSFH D084 live at `9c950c6e9be3e59cfbdc09f4f6a6a187e6a04c29`; maintained source `e09d22d03a4b4a0754dfe7c29853dad91742cc38`; publication workflow `35895091228` SUCCESS with selected exact live-byte verification. D074-D079 are front-door/navigation/presentation repairs; D080 unifies Works; D081 cleans contextual art rooms; D082 unifies conceptual reading rooms; D083 unifies the appeal case family; D084 removes the duplicate accessibility bypass created by composing D081+D082. None are framework changes. Release != validation. Practical-advantage pilot remains unrun.

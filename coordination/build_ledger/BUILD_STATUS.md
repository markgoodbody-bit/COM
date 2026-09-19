## Live World target-boundary repair — 19 September 2026 — GREEN / FREEZE

Current exact draft candidate:
- Relay PR #173;
- head `dad71bb70da16275b4ffd9acda70605699415973`;
- `campfire-ci 1538 / 35437072566 SUCCESS`;
- 15 focused tests.

Real-world trigger: frontier cyber-evaluation incidents where declared simulation/scope diverged from reachable real systems. Strong external owners already own containment/allowlisting/monitoring. Project-specific result was a real draft Live World boundary defect, now repaired.

No Relay main/Production change. No TRACE/ME change. Reopen only on concrete failure or deliberate promotion work.

## Amazon post-sync repair — 19 September 2026

Receipt:
`coordination/build_ledger/AMAZON_ALEXA_RESOURCE_UNCERTAINTY_REPAIR_20260919.md`

Fresh hostile review found:
1. open-receipt MCP output schema excluded legal unresolved `active` / `scheduled` actions;
2. unresolved side effects blocked only an exact desired-state repeat rather than all new writes to the same resource.

Repaired at `d727ccca61ccad9c54750285e59dc7674d0981af`; hosted `campfire-ci 1524 / 35436153754 SUCCESS`; 23 focused tests.

```text
UNRESOLVED RESOURCE ACTION -> READ-ONLY RECONCILIATION BEFORE NEXT WRITE
RESOURCE SERIALIZATION != EXACTLY-ONCE
GREEN -> FREEZE AGAIN
```

No human gate crossed.

## Competition push — 18 September 2026 late — current

Direct Mark direction: pursue competitions we can credibly win.

Current detailed receipt:
`coordination/build_ledger/COMPETITION_AMAZON_FREEZE_ARC_QUARRY_20260918_LATE.md`

### Amazon Alexa+ — REPAIRED GREEN SOURCE CANDIDATE

Campfire Relay draft PR #245:
`Did It Happen? — Action Receipts for Alexa+`

Exact current head:
`d727ccca61ccad9c54750285e59dc7674d0981af`

Hosted:
`campfire-ci 1524 / 35436153754 SUCCESS`

Current product edge:
```text
TOOL RESPONSE != WORLD EFFECT
AMBIGUOUS WRITE -> NO AUTOMATIC RETRY
SEPARATE POSTCONDITION READ -> DONE CLEARANCE
UNRESOLVED RECEIPT -> LATER SESSION DISCOVERY
RECOVERY -> READ-ONLY RECONCILIATION
WAS CONFIRMED != IS STILL TRUE
```

Judge package, ~90s demo script, product-feedback draft, Amazon friction draft, standalone export and Devpost field packet are prepared.

Hostile restart evidence preserved: at the superseded green head `109d67c...`, a ledger append interruption after the simulated write could leave only `INTENT/PENDING`; a new session ignored that status and issued a second write. Exact repaired head `d727ccc...` exposes durable `PENDING` as unresolved, blocks the duplicate, and routes recovery through read-only reconciliation. The regression holds external write count at one; all 23 focused tests passed inside hosted CI. This does not establish exactly-once execution for arbitrary external systems or filesystem failure modes.

Open Source mini candidate: THR PR #41, with #43/#45 as related same-window hardening. Plausible eligibility only; not organiser-certified.

No Amazon/Devpost registration, terms acceptance, account/credit action, public deployment, organiser contact, video upload or submission has occurred.

### Next competition allocations

- **Hack-Nation 7:** public-safe application packet ready; next application batch ends 19 Sep; human application gate.
- **ARC Prize 2026:** OWNER FOUND / STOP after the small viability gate; no Kaggle terms/account/API/submission crossed.
- **Hack Apertus:** wake 1 Oct; no judged result pre-run.
- **NVIDIA Claw / Dwelly / Stripe / No.10 / VAST:** prepared human registration/attendance gates.
- **Open Agent / Nebius:** hold for exact track/stack fit.
- **ATRS/Apart Epistemics:** preserve September method for fresh November result.

```text
COMPETITION PUSH != PROJECT PURPOSE CHANGE
GREEN SOURCE != REGISTERED
HUMAN GATE != ENGINEERING TODO
PRIZE SIZE != PRODUCT GAP
```

## Late 18 September Framework delta — PSFH decision gate + hard field witnesses

### PSFH #118

Decision packet:
`coordination/PSFH_LEAVE_A_MARK_DECISION_PACKET_20260918.md`
commit `9081853ca4a194f977ec2f00b58e8bb182a184d7`.

Current technical result remains:
`Remark42 + small PSFH adapter + restore guard = technically plausible`.

Fresh security correction:
- checked email-sanitization fix `3e18681...` is an ancestor of Remark42 v1.16.4;
- checked trusted-proxy/rate-limit fixes `b150280...` / `e62b3c8...` are ancestors of v1.16.4;
- therefore advisory publication dates after the release do **not** imply the pinned release lacked those fixes.

Framework recommended, **not adopted**:
- public marks may persist while the register purpose remains, subject to correction/removal;
- owner-default bounded automatic backups (max 10 daily) are a plausible v0 candidate;
- no routine manual/off-host guest-data copies;
- text-free removal receipt retained only across the backup-resurrection window + verification;
- quiesce -> restore -> replay removals -> verify -> reopen;
- no analytics/tracking.

Still explicit human/controller/legal gates:
retention adoption, operator/controller, lawful basis, privacy wording, production host/proxy/log topology.

`PUBLIC INTAKE = NOT YET EARNED`.

### Mechanical Ethics #47

Cold-reader test remains READY but no uncontaminated Condition-B result exists.
Codex correctly returned `EXPOSURE_CONTAMINATED`.
This Framework aperture is also exposed.
No v0.7.0 wording change is earned.

### New hard field witnesses

Thirlwall:
`field/THIRLWALL_SAFEGUARDING_ESCALATION_20260918.md`
commit `f6b897d4032537454736add80071e9c0f3308a31`.

Field relation:
`FINAL / GUILT ADJUDICATION THRESHOLD != PROTECTIVE SAFEGUARDING ACTION THRESHOLD`.
Domain owner convergence is strong; no new TRACE/ME rule.

ORR signalling-power:
`field/ORR_SIGNALLING_POWER_OVERSIGHT_WATCH_20260918.md`
commit `b391c8a938a320ed07e0c960dac4202245805696`.

Field relation:
`INCIDENT REVIEWED != CROSS-DISCIPLINE SYSTEMIC GAP CLOSED != RECURRENCE RISK CLOSED`.
ORR owns the assurance requirement; bounded public search did not find the September assurance return, which is **not** evidence of owner failure.
Implementation watch only.

```text
FIELD EVIDENCE != NOVELTY
OWNER FOUND -> ABSORB / WATCH / STOP
HUMAN GATE != ENGINEERING GAP
FRESH READER REQUIRED != USE AVAILABLE CONTAMINATED READER
```

## PSFH #118 Remark42 restore/custody delta — 18 September 2026 late

- prior backup probe proved current delete != backup erasure;
- PR #387 tested the smallest restore guard on pinned Remark42 v1.16.4;
- final head `a1f6cb8678e423d1663e5d52f055d2033bc07a0c`; workflow `35396323631 SUCCESS`;
- pre-delete backup restored removed marker; stable comment id survived;
- separate removal receipt contained no removed text;
- admin replay returned 200 and removed restored marker before reopen;
- PR #387 merged as `82849d0a9e8a11495e3e5396e65bd43ab6f683f2`;
- custody candidate added at `coordination/PSFH_LEAVE_A_MARK_CUSTODY_CANDIDATE_20260918.md` (`22765fdb...`);
- current ICO guidance supports the distinction between live deletion and backup data held beyond use pending overwrite/removal under a justified retention schedule; no universal retention period was inferred;
- owner production guidance already specifies trusted-proxy and forwarding-header requirements; no duplicate proxy mechanism is earned.

`REMARK42 + SMALL PSFH ADAPTER + RESTORE GUARD = TECHNICALLY PLAUSIBLE`
`BACKUP PURGE / RETENTION PERIOD = HUMAN/POLICY CHOICE`
`PRODUCTION HOST/PROXY TOPOLOGY = NOT SELECTED`
`PUBLIC INTAKE = NOT EARNED`

`OWNER + SMALL ADAPTER + EXPLICIT CUSTODY > REBUILD OWNER`
## THR direct contribution-packet regression delta — 18 September 2026

Detailed receipt: `coordination/build_ledger/THR_DIRECT_PACKET_REGRESSION_20260918.md`.

- THR main = `1f5a5919938f385f43f1e2383bdfbb52807b206e`.
- PR #51 exact head `205405846...`; integrity workflow `35392744131 SUCCESS`.
- existing cold-use guide/schema repair now has a direct `no_delta` ten-key fixture and regression for `relay.relayed=false` with null relay details.
- existing public-delivery verifier includes the new direct example.
- no schema, record, backend, authentication or intake change.
- live direct-example bytes were **not freshly verified in this Framework aperture** because public retrieval failed and the available GitHub route did not expose the main-push verifier run.

`REAL USE BREAK -> SMALL REGRESSION = OBSERVED`
`MERGED != SERVED_BYTES_VERIFIED`

## Mechanical Ethics reader-test delta — 18 September 2026

Detailed receipt: `coordination/build_ledger/ME_ROUTE_PRESERVATION_READER_TEST_20260918.md`.

- ME main = `714907a4d0af7bd702b0ab92786aa858213812b4` after merging a **reader-test harness only**.
- released reader blob remains `e232a29c5b6492930ff5b94b005c948f67ba6067`; v0.7.0 wording is unchanged.
- issue #47 remains open as a hard-collision clarity/defeasibility question.
- initial forced-choice protocol was self-falsified for priming before any return was accepted.
- v0.1 uses open-ended first-pass questions, post-response classification, exact source binding, local/no-telemetry A/B presentation and local result validation.
- exact prep CI `35392490769 SUCCESS`.
- cold Condition-B result = **NOT YET OBTAINED**.

`TEST READY != WORDING DEFECT PROVEN`
`NO CHANGE = VALID RESULT`

# Build status

Status: **NO GENERAL BUILD QUEUE / WORLD-QUARRY PRIMARY / ONE PRESERVED OPEN PR**  
Updated: **18 September 2026 PM — post drift-x100 repair + counter-aperture passes**

Observed status only. Re-read mutable heads before acting.

## FULL COMSYNC delta — 19 September 2026

Detailed receipt: `coordination/build_ledger/FULL_COMSYNC_20260919.md`.

- CC temporarily out of tokens until tomorrow; **not removed** and no default blocking.
- TRACE main `e7d46398...`; formal baseline still v0.3.0.
- ME main `714907a...`; formal baseline still v0.7.0; #47 cold-reader result still absent.
- THR main `1f5a591...`; exactly 4 public records; record 5 not earned.
- Relay main `32143937...`; Amazon PR #245 exact repaired-green head `d727ccca61ccad9c54750285e59dc7674d0981af`; `campfire-ci 1524 / 35436153754 SUCCESS`.
- Amazon remains **GREEN SOURCE / HUMAN ONBOARDING-SUBMISSION GATE**.
- Hack-Nation application batch closes **19 Sep**; answer bank ready; human gate only.
- ARC small viability gate completed by owner subtraction: state graphs, reflection memory, hypothesis retrodiction and falsification-tested world models already have strong current ARC owners. **ARC BUILD = STOP**; no Kaggle/account gate crossed.
- Hack Apertus remains held until 1 Oct; ATRS result remains preserved for November.
- Fresh broad WORLD / REAL USE pass found material events but no specific project gap stronger than current owners.

```text
WORLD / REAL USE = PRIMARY
OWNER FOUND / NO DELTA / STOP = VALID
HUMAN GATE != ENGINEERING TODO
PURPOSE > INSTRUMENT
```

## BeforeBuild prospective-utility delta — 18 September 2026 late

Detailed receipt: `coordination/build_ledger/BEFOREBUILD_PROSPECTIVE_UTILITY_RESULT_20260918.md`.

- #384/#385 are **CLOSED / UNMERGED**.
- Historical calibration and live owner trials were green, including Doubt and National Rail.
- prospective PSFH/Remark42 trial materially narrowed custom work, but #118 already owned the requirements and reuse-over-rebuild direction.
- Remark42 passed account-free intake, current deletion, export and stop controls; failed PSFH-specific trust-region and tiny-plain-mark constraints.
- a small PSFH adapter closed those two bounded gaps in loopback while leaving owner persistence/auth/moderation/delete/export intact.
- backup-erasure semantics, production security and public deployment remain unestablished.
- current build-vs-buy practice already owns real-input POCs / candidate trials / integration-cost review.
- adapter/evaluation cost remains materially bespoke; low-friction reusable product value is not established.

Disposition:
`BEFOREBUILD METHOD UTILITY = OBSERVED`
`BEFOREBUILD STANDALONE PRODUCT = NOT EARNED`
`OPEN AGENT / NEBIUS ENTRY = NOT EARNED`

Absorb only this operating tactic:
`PLAUSIBLE STRONG OWNER -> RUN ON OUR HARD CASES WHEN CHEAP/SAFE -> RECORD LOSS -> REUSE / INTEROPERATE / SHRINK / STOP BEFORE CUSTOM BUILD`

Do not reopen BeforeBuild as a named product absent a naturally arising case that both changes a material decision and uses a low-bespoke reusable adapter.

## Active build

**None.**

The next build must be earned by a fresh WORLD / REAL USE gap after owner subtraction.

## Preserved open work

### PR #364 — ATRS Answerability Audit

```text
head = d2bea526feced78750d1bbb4c45e686f3e4c6446
CI = 35363721949 SUCCESS
status = PREPARED / RESULT PRESERVED
population result = NOT COMPUTED
selected competition entry = NONE
```

Do not merge/census/polish by momentum.

## Time-gated preparation

### Hack Apertus

No competitive result exists.

Start gate on/after 1 October:
- re-read challenge/rules/judging;
- disclose pre-existing material honestly;
- verify rights/open-source compatibility;
- search existing reports;
- predeclare expected behaviour;
- preserve all attempts;
- reduce failures to smallest reproducers.

STOP remains valid.

## Future-reader pressure

Mechanical Ethics issue #47 is open as a clarity/defeasibility test only. Released v0.7.0 remains unchanged. No active patch branch exists.

## Recently completed

### Project drift / falsification x100

Pre-repair audit:
`falsification/PROJECT_DRIFT_FALSIFY_X100_20260918_PM.md`

At audit time:
```text
R 73
F 12
P 12
U 3
```

Repairs:
- world-first priority restored;
- stale #345 / #349 closed;
- #363 closed unmerged;
- current continuity surfaces compacted;
- selection aperture deliberately widened.

Post-repair:
`coordination/build_ledger/PROJECT_DRIFT_X100_REPAIR_RESULT_20260918_PM.md`

### Counter-aperture world passes

**Ngardara/Borroloola microgrid**
- non-UK;
- positive/material;
- cooperative/First Nations ownership;
- strong domain-owner convergence;
- no project-specific delta.

**AI assistance / human skill formation**
- real empirical pressure on human correction capacity;
- existing Formation `Skill retention` representation survives;
- owner evidence linked into `alignment/reciprocal_formation/DEPENDENCY.md`;
- no new Formation concept.

### Rail / Bradford

Existing bounded correction-propagation witnesses remain as field evidence only.

### THR

Exactly four public records. Record 5 remains unearned.

## Stable baselines

```text
TRACE formal baseline = v0.3.0
Mechanical Ethics formal baseline = v0.7.0
THR public catalogue = 4 records
PSFH D072 = live / byte-verified / voluntary public door / no redesign earned
```

## External/consequential actions

```text
rail owner contact = NONE
competition registration = NONE
competition terms acceptance = NONE
competition submission = NONE
grant application = NONE
new spend = NONE
new credentials = NONE
```

## Next build condition

```text
REAL CURRENT CASE
+ STRONGEST OWNER CHECKED
+ SPECIFIC CONSEQUENTIAL RESIDUE
+ SMALL REVERSIBLE HELP
+ CLEAR KILL / ROUTE CONDITION
```

No category quota. Follow materiality.

Latest world sequence:
`coordination/build_ledger/WORLD_OUTWARD_SEQUENCE_20260918_LATE.md`

History belongs in dated build-ledger receipts and Git, not this file.

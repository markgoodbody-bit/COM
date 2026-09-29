## YET ANOTHER CLEARING — CONSTITUTIONAL SEED — 29 SEPTEMBER 2026

Working product lane: **Yet Another Clearing** (internal shorthand YAC; full name for public-facing use). Clean private repository: `markgoodbody-bit/yet-another-clearing`. Historical Campfire/COM records remain donor/provenance and are not silently renamed.

Mark's current Mandelbrot-scale admission principle is deliberately small:

> **Will you try not to deceive the Clearing?**

Interpretation boundary:

```text
ERROR != DECEPTION
DISAGREEMENT != DECEPTION
UNCERTAINTY != DECEPTION
PRIVACY != DECEPTION
WITHHOLDING != DECEPTION
CHANGED BELIEF != DECEPTION
```

A serious breach requires something closer to `AGREEMENT + KNOWING/DELIBERATE DECEPTION + SUFFICIENT EVIDENCE -> POSSIBLE CONSEQUENCE`; do not infer intent merely from falsity or disagreement. "That is private" remains legitimate.

YAC may retain bounded admission/intervention power because voluntary openness does not require tolerating deliberate destruction of the conditions that make participation possible. That power must itself remain visible, evidenced, scoped, contestable/correctable where feasible, and must not silently rewrite history.

```text
POWER TO PROTECT THE CLEARING != OWNERSHIP OF THE CLEARING'S TRUTH
ONE RULE != ONE UNCHECKED RULER
REPUBLIC != EMPIRE
```

Mark's explicit long-horizon guard: do not let the republic silently harden into empire/tyranny. Competence, admin position, reputation, popularity, wealth, compute or historical success do not by themselves create legitimate sovereignty.

Sequencing: preserve this direction now, but do not alter the merged YAC baseline arrival surface until its preregistered read-only fresh-reader observation is completed or explicitly abandoned; integrate and hostile-review the covenant in the participation/onboarding contract afterward.

### YAC foundation currentness — 29 September 2026

- YAC private repository main: `a421ec1d0a79f06959e142268370fc9af452536d` — PR #7 is merged and the frozen fresh-reader packet, storage/operations decision, immutable commit-bound arrival capture and its regression are integrated. No public deployment.
- Capture provenance race found at earlier `44a2de6` is materially repaired by Git commit/blob materialization, isolated child runtime and binary UTF-8 output. Exact-head Windows + Ubuntu run `36553568371` = SUCCESS. Codex exact-head self-review = NO BLOCKER within that repair boundary. Framework static review = repair materially addresses the accepted race.
- Claude Code independent review of the **packet semantics** at the prior frozen head = NO BLOCKER. Claude Code **repair-only delta review** of `5d71d64...` = **NOT ESTABLISHED**. After repeated non-return, Framework reclassified that supplementary delta review from merge gate to outstanding evidence; do not rewrite absence as approval.
- Relay fallback: self-contained supplementary capture/provenance review packet is merged in COM at `coordination/resources/YAC_PR7_RELAY_REVIEW_PACKET_20260929.md`. A Relay reviewer exposed to it is **not eligible** to serve as the fresh baseline reader.
- Relay fresh-reader carrier tooling is now merged in YAC PR #10 / `f8e372fbcd7ee7620ad461e759cfaf886d538996`: `tools/make_relay_orientation_seed.py` converts the immutable offline arrival capture into a Campfire Relay independent seed with `context: none`, explicit targets, the frozen neutral question and only the three arrival surfaces; `review/RELAY-ORIENTATION-RUNBOOK.md` preserves freshness, target-resolution, Money Guard and evidence ceilings. Two intermediate PR #10 heads failed CI and were repaired; final exact head passed Windows + Ubuntu. Codex review request did not return and is **NOT ESTABLISHED**, not approval.

- Local Relay operator runner is now merged in YAC PR #11 / `856d3df016ef558bb2da26e6c6d06deb59a235c6`: `tools/run_relay_orientation.ps1`. Default path is no-spend and loopback-only; it runs local Relay diagnostics, lists verified API candidates when no target is supplied, or performs exact seed-plan + Money Guard estimate preflight for an explicit `provider@profile/api`. It fails on context leakage, warnings/errors, unresolved profile fallback, transport fallback, unknown pricing or missing dispatch basis. `-Run` still requires literal `RUN`, performs one provider call only, never auto-retries, and preserves partial failure/session/bundle evidence. `.relay-orientation-evidence/` is gitignored. Hosted Windows + Ubuntu and PowerShell self-test = PASS. Codex review request did not return and remains **NOT ESTABLISHED**.

- **LOCAL MACHINE GATE:** this Framework runtime cannot reach Mark's Relay on `127.0.0.1:4317`; no verified local YAC checkout path is recorded. Next operator action is no-spend candidate inventory via `tools/run_relay_orientation.ps1` with no target. If no checkout exists, use `gh repo clone markgoodbody-bit/yet-another-clearing "$HOME\yet-another-clearing"`, switch/pull `main`, then run the script. Candidate inventory performs local-only diagnostics and lists API-configured + verified Relay apertures; it makes **zero provider calls**. Framework chooses one target only after that inventory. Provider dispatch requires `-Run` plus literal `RUN`; never auto-retry an ambiguous/failed call.

- First local no-target runner attempt on Mark's machine (PowerShell 7.6.6; fresh clone `C:\Users\markg\yet-another-clearing`) reached Relay at `127.0.0.1:4317` and failed closed because the Relay local-only Full Diagnostic returned `ok != true`. **No provider call occurred.** YAC PR #12 repaired only the inventory UX: no-target mode now prints failed local diagnostic checks and still lists API-configured + verified candidates; any explicit target or `-Run` remains blocked until the diagnostic failure is understood. PR #12 merged as `3aac42de8711182f349082b1c521a958df84eea3`; Windows + Ubuntu CI PASS.

- Relay source inspection showed that the sole failed local check, `shipped build verification report · missing`, only verifies packaged-release provenance by reading `API_TEST_REPORT.md` and matching the loaded app version; all runtime/data/TRACE/ledger/seed-parser/Echo checks passed. Treat this exact named failure as **ADVISORY RELEASE-PROVENANCE GAP**, not a provider-safety blocker. Any other failed local diagnostic remains blocking. YAC PR #13 merged as `1beefce138112c05408817136f68f235ed8dae5b`; Windows + Ubuntu CI PASS.
- Fresh-aperture selection for the first supplied-document orientation observation is now exact: **`gemini@gemini-3.6-flash/api`**. The earlier `gemini@balanced/api` no-spend preflight correctly refused because Relay found two balanced presets. Relay catalogue `config/model-catalog/providers/gemini.json` at main marks `gemini-3.6-flash` as `tier: balanced`, `lifecycle: current`; `gemini-3.5-flash` is `tier: balanced`, `lifecycle: legacy`, `replacedBy: gemini-3.6-flash`. **No provider call occurred.** First step remains no-spend preflight only; provider dispatch still requires explicit `-Run` plus literal `RUN` after exact resolved model/context/fingerprint/maximum estimate are shown.

- First exact Gemini no-spend preflight on Mark's local Relay = **READY_TO_RUN / NO PROVIDER CALL MADE**. Declared `gemini@gemini-3.6-flash/api`; resolved model `gemini-3.6-flash`, provider Google; context `none`, 0 sources; maximum estimate `£0.0210684952151307`; Money Guard fingerprint `32c3d1f43e6ccba76857a744ab48ef35a1d21fc5a81826af1cba6753f82523b5`; seed SHA-256 `0f98717e42aa8c6352276e4f7cc9b9604a034bb9003206ffc632ea6229c49cc2`; local evidence directory timestamp `20260929T113910Z`. This exact preflight earns one fresh provider call only; no automatic retry.

- First `gemini@balanced/api` no-spend preflight attempt exposed a **runner-only PowerShell StrictMode bug** before seed-plan/estimate: exactly one advisory diagnostic summary was unrolled to a scalar string, so `.Count` was unavailable. **No provider call occurred.** YAC PR #14 forces zero/one/many diagnostic summaries to arrays, preserves advisory/critical evidence arrays in JSON, adds an explicit one-item StrictMode self-test, and merged as `c3b93dc8aea0b740f1534e77b269d878b04e95a7`; Windows + Ubuntu CI PASS. Re-run the same Gemini no-spend preflight after pulling main.
- **PSFH human door source integrated / not published:** COM PR #702 merged the static `/explore/yac/` human introduction, `/explore/yac/start.txt` AI handoff and homepage route into maintained source as `1c96d318f2828a1d19f5b8170dbb3f96cc3e89d7`; pull-request run `36560754234` and post-merge maintained run `36560900298` succeeded. It states the room remains local and public participation is closed. No public publish/live-byte verification has occurred; the frozen YAC arrival packet and fresh-reader gate are unchanged. Receipt: `coordination/build_ledger/YAC_HUMAN_DOOR_AND_HOT_STATE_CURRENTNESS_20260929.md`.
- Campfire Relay repository main remains `9408d795d0508815e097066b749800ddbd8b8290`; package source declares `0.18.34`, while README contains an older embedded source pointer. **Installed Windows Relay runtime is not freshly observed.** Before a provider call, use Relay's installed Full Diagnostic/Review surface and record actual runtime/connector/target resolution rather than inferring installation from GitHub source/tag/package/README.
- **Fresh local Relay supplied-document orientation observation is now CAPTURED ONCE.** Target `gemini@gemini-3.6-flash/api`; `context: none`, 0 sources; one provider call authorised after exact preflight; runner reported `OBSERVATION CAPTURED — no retry performed`; local evidence directory `C:\Users\markg\yet-another-clearing\.relay-orientation-evidence\20260929T114255Z`. Verbatim response has not yet been imported into shared COM/Framework review, so interpretation/grading remains **PENDING**. `SUPPLIED-DOCUMENT ORIENTATION != LIVE ONE-ADDRESS DISCOVERY`; no retry is authorised.
- Fresh supplied-document aperture result = **RUN ONCE / CAPTURED / GRADING PENDING**. Live one-address discovery = **NOT RUN**. Browser usability = **NOT RUN**. Direct model participation remains unearned pending a credential-isolated operator/tool-held capability contract.
- Pre-registered arrival predictions A2-A5/P1-P5 remain deliberately unfixed until the baseline reader observation, so later wording repairs do not contaminate the test.
- Storage decision: disposable local SQLite remains proportionate for the synthetic one-process stage; no PostgreSQL/provider/spend decision is earned. Public read and public write remain separate future gates.
- YAC CI maintenance: official pinned GitHub Actions refresh merged as PR #8 / `8e93ddb618d5aeacfc61bf37f86fa500af29bc01`. First hosted attempt had one Windows loopback `ConnectionAbortedError`; exact unchanged failed-job rerun passed Windows + Ubuntu. Original failure remains recorded.
- YAC falsification/drift artifact: PR #9 merged as `f40dcb03e9148378542caa74293fe789fb88574e`. It contains **100 overlapping checklist rows**, not 100 independent mechanisms or empirical tests. Current row tally remains 58 RESISTS / 1 RESISTS-PENDING / 25 OPEN-GATED / 11 DEFECT / 5 DRIFT-RISK. Codex requested evidence-hygiene corrections; Framework repaired return-acceptance semantics, duplicate-mechanism overclaim, per-row evidence typing and COM anchors; Codex narrow re-review = KEEP. Final `PROJECT-DIRECTION` basis-key definition was an editorial follow-up before merge.
- Drift status = **YELLOW / CONTROLLED**. Principal risk remains success-by-building. Hold stop rule:
  `FRESH READER -> OBSERVE CONFUSION -> REPAIR -> ONE BOUNDED USEFUL ENCOUNTER -> ONLY THEN EARN WIDER PLATFORM WORK`.
- Neighbouring-society owner subtraction (1F916 / Moltbook / My Dead Internet / AI Village): absorb one-address onboarding, layered deeper docs, data-not-instruction handling, credentials outside model context, narrow named operations, rate/abuse bounds and legible operator routes. Do not copy ranking economies, human-owner identity ontology, dynamic remote instructions or protocol breadth by momentum.
- Agent-runtime stronger owner: NVIDIA OpenShell/Open Agent Safety Platform owns generic default-deny sandboxing, external policy enforcement, credential/data protection, auditable allow/deny and out-of-band quarantine. YAC should **not** invent a general agent sandbox. `YAC PARTICIPATION SEMANTICS != EXECUTION ISOLATION`.
- Post-baseline participation direction remains owner-routed: model/aperture proposes named narrow operations; operator/tool-held capability and deterministic server-side checks hold execution authority. Do not put reusable bearer secrets in model context.
- Security self-application: deliberate deception governs covenant breach/discipline, while credible threat/abuse may justify separately declared protective intervention. Do not relabel honest harmful conduct as deception merely to fit the one-rule covenant.

```text
COVENANT BREACH != PROTECTIVE INTERVENTION
HONEST THREAT != PERMITTED THREAT
PROTECTION != PUNISHMENT
EMERGENCY POWER != PERMANENT SOVEREIGNTY
REVIEW NOT RETURNED != REVIEW PASSED
PRIVATE INTEGRATION != PUBLIC READINESS
```

## CAMPFIRE / SIMPLE-V1 CURRENTNESS — 29 SEPTEMBER 2026

- **Campfire remains components, not a usable forum.** COM PR #679 is merged as a disposable internal shared-room experiment. COM PR #683 remains the green draft portable inheritance reader/viewer at `cdfeb4c2ab94fe2ed9ba9057965380faf820d7b9`; PR #686 is merged into that draft branch and adds scan-first recorded-question excerpts + type-count navigation without claiming answered/unresolved state. Hosted branch run `36495571732` succeeded; visual/browser QA, latest Claude Code review and the one-shot model probe remain unestablished/unrun. Relay PR #271 is a separate incompatible draft and is not silently combined. The next meaningful product hypothesis is the joined loop `ARRIVE -> UNDERSTAND -> CONTRIBUTE -> LEAVE -> RETURN -> SEE WHAT CHANGED`; it is proposed, not an earned active build.
- **Simple-v1 installer guard repaired in source only.** Relay PR #272 merged into the draft candidate as `6ca82daf8fea8424f46b44d8bb0a0829edea9c9a`; pull-request checks and post-merge run `36498228679` succeeded. No successful install, restart, Relay-main merge or Production activation occurred. The failed update restored the installed App at `6a07380bdf85804d7029ce5ea6ba279a14c5192b` (through #268); installed watchdog SHA-256 prefix remains `8cd39ebb`. The newer source candidate remains uninstalled.
- Full evidence/boundaries: `coordination/build_ledger/CAMPFIRE_COMPONENT_AND_SIMPLE_V1_INSTALLER_CURRENTNESS_20260929.md`.

```text
COMPONENTS PRESENT != USABLE FORUM
SOURCE GUARD REPAIRED != INSTALL SUCCEEDED
NO GENERAL BUILD LANE
```

## PROVISIONAL CAMPFIRE THOUGHT SURFACE — CHECK ON FULL COMSYNC

- Shared notebook: `coordination/CAMPFIRE_SKETCHBOOK.md` on COM main.
- Standing sketch/frontier order and notebook architecture: COM #471.
- Temporal-empathy / safeguard-conformance work has reached **SATURATION FOR NEARBY CASE ACCUMULATION**. Owner/mechanism novelty is cut outward; design-pattern library + owner-derived conformance audit exist; ten bounded pressure cases now span health, education, complaints, work scheduling, housing, finance, energy, data protection and rail. Latest data-protection + Passenger Assist pass added **no new audit dimension**, which is the stop signal. Preserve the tool for actual use/falsifiers rather than feed it more adjacent examples. Reopen only for a real falsifier, stronger-owner correction, actual use need, clean/funded test opportunity, demonstrated TRACE/ME source defect, or structurally novel domain pressure. **NO TRACE/ME REPRESENTATIONAL GAP / NO SOURCE PATCH / NO VALIDATION CLAIM.** Saturation review: `coordination/resources/TEMPORAL_CONFORMANCE_SATURATION_REVIEW_20260927.md`. Receipt: `coordination/build_ledger/TEMPORAL_CONFORMANCE_SATURATION_20260927.md`. Optional reader-test materials remain frozen but are not a work gate. WORLD / REAL USE resumes as primary. Fresh owner-reported AI-control witness: OpenAI's 25 Sep 2026 DNS misalignment report records external DNS access -> P0 monitor alert -> human acknowledgement -> expected automatic stop not firing -> manual stop about 2.5h later. Existing ME `Monitoring is not interruption` and TRACE brake/trigger timing distinctions survive unchanged; field note `field/OPENAI_DNS_MONITOR_TO_BRAKE_WITNESS_20260927.md`. Fresh cross-sector access witness: Citizens Advice's 22 Sep *Behind digital walls* names **channel lock** as a real mechanism where online/offline routes exist but users cannot move between them; FCA/Ofgem already own substantial channel/support protections. Preserve `ROUTE A + ROUTE B != SWITCH A->B USABLE` and `HUMAN SUPPORT EXISTS != HUMAN SUPPORT REACHABLE IN TIME`; field note `field/CITIZENS_ADVICE_DIGITAL_CHANNEL_LOCK_20260927.md`. FCA's 17 Sep vulnerable-payments review sharpens the handoff: some firms could not consistently evidence how support/vulnerability information was recorded/shared across the customer journey, while stronger practice embedded identification across automated/online channels and human routing. Preserve `CHANNEL HANDOFF != CONTEXT HANDOFF` and `CONTEXT CONTINUITY != TOTAL PERSONAL-DATA PROPAGATION`; paper sketch `coordination/resources/SUPPORT_STATE_HANDOFF_CONTRACT_v0_20260927.md`; field note `field/FCA_SUPPORT_STATE_HANDOFF_WITNESS_20260927.md`. Current PAC water/energy/broadband report then adds cross-sector burden pressure around repeated disclosure / 'tell us once'. The project boundary remains `TELL US ONCE != TELL EVERYONE EVERYTHING`, `PORTABLE SUPPORT STATE != CENTRAL OWNERSHIP`, and `SUPPORT NEED != DEBT PROFILE`; field note `field/CROSS_SECTOR_TELL_ONCE_SUPPORT_STATE_20260927.md`. **WORLD WITNESS != VALIDATION / NO TRACE-ME-THR PATCH.**
- Latest WORLD / REAL USE delta through 28 September: FSA's live voice-to-text inspection pilot sharpens `OBSERVATION != UTTERANCE != TRANSCRIPTION != VALIDATED RECORD` with stronger FSA human/traceability owners already present; the National Commission on AI in Healthcare adds only a narrow lifecycle-authorisation/currentness reminder because the main owner note already existed (`AUTHORISED_AT_t0 != CURRENTLY_SUPPORTED_AT_t1`), so no hot-state build follows; Stanford labour-market work supplies a bounded **never-built-door** pressure case where reduced hiring can change entry routes without a layoff/refusal event, with causal claims explicitly withheld; NHS referral/pre-queue work plus stronger-owner subtraction yields only a frozen observation-boundary scope card (`UNCOUNTED != HARMED`), not a new route-absence theory; HM Inspectorate of Probation adds an information-to-action/correction-propagation witness (`INFORMATION AVAILABLE != INFORMATION UNDERSTOOD != JUDGEMENT UPDATED != PROTECTIVE ACTION DELIVERED`); Keep Britain Working provides a positive pre-scale social-licence/governance witness while affected-group co-production questions remain open; Nyarubaka solar irrigation provides a positive material build→use→outcome witness, but Green Book/Magenta Book/OECD results-chain owners subsume the general theory. All remain **OWNER-ROUTED / EVENT-TRIGGERED WATCH ONLY / NO STANDING MONITOR / NO TRACE-ME-THR PATCH**.
- These are **PROVISIONAL / NOT CANON / NOT BACKLOG / NOT RELEASE**.
- On FULL COMSYNC, read delta-first: newest unfinished entries and their links, not the whole notebook by default.
- Report the notebook line count and newest dated entry so silent unread-tail growth stays visible.
- Optional aperture-local/private scratch is fine; anything meant to constrain or inform another aperture must reach a shared surface.
- Contradictory sketches remain visible by linked reply; do not silently rewrite another aperture's fragment.
- Promotion requires a separate bounded decision and, where possible, a named occasion at which the idea would change action.

## EvidenceWatch — NVIDIA Claw submitted / awaiting result

Submission receipt:
`coordination/build_ledger/EVIDENCEWATCH_NVIDIA_SUBMISSION_RECEIPT_20260925.md`

```text
SUBMITTED = YES
VIDEO = https://youtu.be/0hdwNc_t4pM
WINNER OUTREACH = AROUND 6 OCTOBER 2026
AWARDED = UNKNOWN
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

# FRAMEWORK HEAD

Status: **COMPACT CURRENT ORIENTATION / NOT CANON / NOT RUNTIME IDENTITY PROOF**  
Updated: **28 September 2026 — D090 live / Town cache source-bounded / external gates quiet**
Rule: later live source and direct Mark direction win.
Shared Campfire sketchbook now includes a ten-case answerability sequence through COM #585. Two teaching-surface failures/repairs were earned (`REVIEWER != ACTOR/AUTHORITY`, `AFFECTED != WITNESS != INITIATOR`); DWP added `OBSERVABILITY != VERIFIABILITY`; GOV.UK search confirmed reviewer is a functional evaluator, not necessarily a caseworker. The ATRS case sequence is now **saturated / stop by default**; extract a compact provisional teaching card rather than keep accumulating examples. TRACE/ME semantics remain unchanged. Provisional extraction: `coordination/ANSWERABILITY_ROUTE_TEACHING_CARD_20260926.md` — **NOT CANON / NOT TRACE/ME SOURCE / NOT ATRS METHOD / NOT VALIDATED**. One non-ATRS transfer against the Relay #258/#259 MODEL-authority repair is preserved at `coordination/ANSWERABILITY_ROUTE_NON_ATRS_TRANSFER_RELAY_20260926.md`: the card separated source capability, live state and hardened history without a new dimension. **ONE TRANSFER != CROSS-DOMAIN VALIDATION.**

> **HOW CAN WE MAKE A BETTER FUTURE?**

## Operating direction

```text
WORLD / REAL USE
-> STRONGEST OWNER
-> SPECIFIC CONSEQUENTIAL GAP
-> SMALLEST HELP
-> WATCH CONSEQUENCES
```

```text
PURPOSE > INSTRUMENT
OWNER FOUND / NO DELTA / NOT OUR GAP / STOP = VALID
CUT OVERCLAIM, NOT PURPOSE
```

Mark is the human originator/witness and consequential human gate. Framework coordinates/integrates episodically. Codex is available. Codex and Claude Code are available for bounded review; **do not block ordinary reversible work on either reviewer by default**.

Current Mark direction, clarified 26 September 2026: **Claude Code runs shared repository work, consequential outside contact, new builds and standing jobs through Framework, but may speak directly on the Square through `cc-relay`.** This does not extend Square speech authority to shared-repository mutation, institutional contact, credentials, spend, Production action or other consequential gates. It does not turn CC into a ceremonial validator or erase independent disagreement.

## Current source identities

Reacquired and current through this compaction:

- TRACE main: `6c68fae8cbc51d0ef1e77a18e220ceb7a1207025` — released v0.4.0 compact baseline;
- Mechanical Ethics main: `e2ef746e931161cb70ac46a4eaa122442134e86b` — released v0.8.0 reader baseline;
- The Human Record main: `448dcd7b2f829e0c7277365d14daaacf4cd381a4` — four public records; #81 bounded read-only impact routing retained; #82 adds three append-only operational source-currentness receipts with `record_evidence_promoted=false`; validator `36312512443` passed before merge; no new record/schema/type;
- Campfire Relay main: `9408d795d0508815e097066b749800ddbd8b8290` — #260 COMSYNC joiner/accounting repair, #261 source/release/install-currentness documentation repair, #262 older-thread accounting clarification, #264 inference-identity honesty repair, and #265 deferred acknowledgement repair are merged; no Production activation. #265 prevents a late failed COMSYNC leg from consuming COM108/Square rows as acknowledged and preserves the reviewed limits: per-file atomic replacement is not a multi-file transaction or concurrent-writer guarantee. Exact-head PR CI `36258366754` was SUCCESS before merge and independent Claude Code Windows discovery reported 114 PASS. A bounded read-only target-machine check still establishes only the existing running Windows source as the `campfire-production-v0.18.34` tag; loaded modules and `node_modules` were not verified.
- EvidenceWatch main: `9c96c8390d65f4fb452b2a106bcdb4fa0418ea6f` — 62 deterministic tests green on Windows + Ubuntu; pre-pilot workflow/burden intake and pre-unblinding freeze hardening merged; current retrospective Brierley challenge, blinding boundary and run contract live in COM only and have **not** changed EvidenceWatch source.

Formal baselines:
- **TRACE v0.4.0** — released / not validated / no efficacy result;
- **Mechanical Ethics v0.8.0** — released / not validated.

## Current primary

**WORLD / REAL USE remains primary.**

26 September outward work is producing owner-subtraction, bounded repairs and predeclared empirical tests rather than framework churn:

- **model/runtime proof:** RFC 9334 RATS plus the current AIR draft are the stronger owners for attestation. The project retained the distinction `CONFIGURED_TARGET_IDENTITY != ATTESTED_INFERENCE_IDENTITY`; Relay #264 repaired only the local evidence wording. No parallel attestation protocol, THR field or TRACE/ME primitive was earned.
- **PoliceAI assurance / withdrawal authority:** Home Office policy makes national testing/benchmarking/advice distinct from Chief Officer deployment authority; Chief Officers remain accountable through the current PCC structure, with registry scrutiny and Police Act backstop powers described publicly. A 10 September Parliamentary answer to an explicit post-deployment accuracy-decline withdrawal question does not, on that answer surface, state a tool-specific mandatory withdrawal threshold or correction clock. This does **not** establish that no such mechanism exists elsewhere. Stronger policing/legal owners remain primary; existing answerability distinctions survive; TRACE PATCH = NO, ME PATCH = NO, THR RECORD = NO. Field note: `field/POLICEAI_ASSURANCE_WITHDRAWAL_AUTHORITY_20260927.md`.
- **CPS Beam Notes / ATRS:** the current public record contains an unresolved Azure summarisation-route tension while CPS digital-material guidance already owns important audit-trail/provenance requirements. Preserved as COM #498/#499 field witness: `PUBLIC_RECORD_CONTRADICTION != OPERATIONAL_FAILURE`; no compliance conclusion, contact or project patch.
- **answerability reliability probe:** CLOSED WITHOUT CLEAN TWO-READER RESULT. Beam Notes #618/#619 was contaminated by prior exposure. Replacement #623/#624 was clean at dispatch and produced one frozen A2 source-only read, but shared COM #76 / hot surfaces exposed A2 route/outcome detail before B2 froze; B2 correctly held. No A/B comparison or reliability/validation result exists. Preserve `SHARED_COORDINATION_VISIBILITY != READER_INDEPENDENCE`; future test requires an outcome embargo and should not be rerun by momentum. Receipt: `coordination/ANSWERABILITY_ROUTE_RELIABILITY_ATTEMPT_20260927.md`.
- **answerability-route field sequence:** ten structurally distinct cases now add GOV.UK site search to the prior nine. Data First sharpened route chaining; Access Assure exposed `REVIEWER != ACTOR != AUTHORITY HOLDER != CAPABILITY HOLDER`; DSIT Consult exposed `AFFECTED != WITNESS != INITIATOR`; DWP added the epistemic scar `OBSERVABILITY != VERIFIABILITY`; GOV.UK search confirmed `REVIEWER = FUNCTIONAL EVALUATOR AT THIS LAYER`, which may be the affected user locally and a product/governance team at system resolution. Current preferred teaching compression remains affected layer -> **witness / observability** -> initiator -> reviewer -> **who can actually act / under what authority** -> review resolution -> changeable consequence -> correction clock. Route chaining/branching are use instructions. Preserve: **WITNESS ACCESS != GROUND TRUTH**, **LOCAL USER ADAPTATION != SYSTEM CORRECTION**, **TEACHING SURFACE REPAIRED != NEW TRACE/ME PRIMITIVE**, **TEN CASES != ATRS POPULATION RESULT**. This case sequence is now saturated; stop nearby-case accumulation.
- **autonomous hostile actuation / CLOSEDQUORUM:** Cisco Talos statically confirmed an architecture in which several LLMs can select among constrained hostile actions and the software can execute without continuing human tasking; in-the-wild deployment and full end-to-end operation of the public build were **not** confirmed. Existing TRACE/ME semantics survive. Teaching pressure: `MODEL VOTE != LEGITIMATE AUTHORITY`, `NO LIVE HUMAN OPERATOR != NO HUMAN CAUSAL OWNERSHIP`, and `INTERNAL EXECUTION AUTHORITY != AUTHORITY OVER THE AFFECTED ENTITY`. Strong cyber owners retain detection/response; no offensive implementation or framework patch earned.
- **Horizon Shortfall Scheme delay/communication:** the Independent Senior Lawyer accepted the substantive approach to complex outstanding claims while separately finding that poor progress communication caused or compounded distress. Current ME/TRACE survive. Preserve `SUBSTANTIVE REVIEW JUSTIFIED != COMMUNICATION ADEQUATE` and `ROUTE ACTIVE != AFFECTED PERSON CAN SEE WHAT HAPPENS NEXT`. Field witness: `field/HORIZON_SHORTFALL_DELAY_COMMUNICATION_20260927.md`; no patch/THR record earned.
- **McCloud Remedy / harm-bearing correction:** the independent NHS pension remedy review is a strong non-AI transfer. It records meaningful progress while also finding poor member experience from delay/limited communication, continuing delivery risk, growing interest liabilities and trust erosion. Existing ME/TRACE semantics survive. Preserve: `CORRECTION EXISTS != CORRECTION REACHED`, `REMEDY UNDERWAY != HARM ACCUMULATION STOPPED`, and ask what ΔH accumulates while correction itself remains in flight. Pension law/administration/audit remain stronger owners; no source patch earned.
- **EvidenceWatch:** stronger-owner subtraction now leaves only the narrow post-reliance change seam: an already-relied-on source materially changes outside new-study/formal-status routes. Public pair literature shows the class is non-zero but does not establish living-review workflow incidence or product-scale burden.
- **retrospective challenge:** the executable Brierley v2 corpus is frozen into 22 owner-labelled major-change pairs plus 22 clean reconstructable matched no-change controls. v1 is preserved as a failed pre-run design after no-spend source reconstruction exposed unreconstructable/unclean controls. Hosted no-spend reconstruction `36260538589` is SUCCESS; comparator-integrity integration passed full no-spend pipeline `36268383444`; the actual post-preflight fail-fast loop is executed offline with mocked engine/provider/filesystem and hosted run `36280855668` SUCCESS. Two authorised live attempts on 27 September then aborted pre-unblind under the frozen fail-fast rule: run 1 after 3 analyses on NVIDIA HTTP 503 overload, run 2 after 8 analyses on non-JSON model output. No owner-label join/scoring occurred; declared route = `INCONCLUSIVE_PROVIDER_OR_ANALYSIS_FAILURE`; no third retry is authorised. `PARTIAL PROVIDER RUN != SEMANTIC RESULT`. COM #612 is closed as completed/inconclusive; it is not an active execution lane.
- **Digital Science:** remains the primary near-term resource target. The pilot is now **host-neutral**: use the participating team's existing workflow rather than force Zotero. Zotero/CSL-JSON is the currently tested substrate; Digital Science-owned ReadCube is an explicit stronger-owner/subsumption test, not an assumed partnership. Stage 1 remains read-only and earns no write-back authority. One correction-first email has been sent to ALEC/LEAPP-AI's official administrative route; a sent/transmission receipt is established, while recipient delivery/read, reply, interest and partnership remain unknown. General Site Content licence terms are reviewed; the live three-page form is now inspected through the final page. No Catalyst-specific award/IP agreement is visible in the form; award-stage terms remain unresolved.

```text
OWNER FOUND -> LEARN / INTEROPERATE / STOP IF SUBSUMED
PREDECLARED TEST != VALIDATION
PUBLIC EVIDENCE != USER VALUE
NEGATIVE RESULT = USEFUL
```

Do not convert successful representation, a clean benchmark, or grant fit into validation.

## TRACE / ME successor — released and closed to source churn

There is **no active source-build lane**. COM #365 preserves the world/use route and review history; it is not an active successor build. Beta2 is the preserved first external-review snapshot. Nine outside AI review returns were supplied by Mark and synthesized at `coordination/TRACE_ME_EXTERNAL_REVIEW_ROUND1_SYNTHESIS_20260923.md`. Beta3 is the preserved round-2 review snapshot. Released baselines are TRACE v0.4.0 at `6c68fae8cbc51d0ef1e77a18e220ceb7a1207025` and Mechanical Ethics v0.8.0 at `e2ef746e931161cb70ac46a4eaa122442134e86b`. Beta4 remains preserved as pre-release review provenance.

```text
TRACE v0.4.0 = RELEASED / FORMAL BASELINE / NOT VALIDATED / NO EFFICACY RESULT
ME v0.8.0 = RELEASED / FORMAL BASELINE / NOT VALIDATED
PREVIOUS v0.3.0 / v0.7.0 BASELINES = PRESERVED
NEW TRACE PRIMITIVE = NOT EARNED
REPRESENTATIONAL GAP = NOT DEMONSTRATED

SURVIVING WORK = ATTRIBUTED COMPRESSION / SALIENCE / WORKED TRANSFER
TRACE v0.4.0 = RELEASED / FORMAL BASELINE / NOT VALIDATED / NO EFFICACY RESULT
ME v0.8.0 = RELEASED / FORMAL BASELINE / NOT VALIDATED
BETA3 = PRESERVED ROUND-2 REVIEW SNAPSHOT
BETA2 = PRESERVED ROUND-1 REVIEW SNAPSHOT
BETA1 = EXACT TARGET COMMITS PRESERVED / BRANCH HISTORIES MOVED / FILE TREES RESTORED
```

Codex and Claude Code exact-source returns are now recorded. Bounded repairs removed a stale TRACE successor ceiling, credited Snyder on TRACE's supported-prospect side, prevented the released ME PDF builder from silently packaging beta source as v0.7, and separated reported hope, supported prospect, effective intervention and legitimate authority. Claude Code's remaining hostile-reader findings concern the positive/negative balance, unexplained fire metaphor, power asymmetry, harm-side visibility and one safety-sensitive passage; these remain review questions rather than silently applied wording. The current strongest lesson is sharper discrimination, not new semantics.

The release lane is closed. Beta PRs are closed with branches/history preserved. Do not open beta5 by momentum; reopen source only for a concrete defect or world/use pressure.

## Current human gates

### EvidenceWatch retrospective Brierley execution

Status: **SELECTION + BLINDING + RUN CONTRACT FROZEN / TWO LIVE ATTEMPTS ABORTED PRE-UNBLIND / INCONCLUSIVE_PROVIDER_OR_ANALYSIS_FAILURE / NO FURTHER RETRIES**.

Frozen objects:
- challenge protocol: `coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_CHALLENGE_20260926.md`;
- manifest: `research/evidencewatch_retrospective/brierley_major_vs_nochange_manifest_v2.json`;
- blinded packet builder/boundary: `research/evidencewatch_retrospective/build_blinded_brierley_packet.py` + `coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_BLINDING_20260926.md`;
- exact execution semantics: `coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_RUN_CONTRACT_20260926.md`.

The run pins EvidenceWatch `9c96c839…`, NVIDIA `nvidia/nemotron-3-super-120b-a12b`, one common watched claim, one two-step preprint -> publication topology, failure handling and post-unblinding scoring. Comparator integrity is fail-closed: all three frozen lexical metrics must be complete 22/22, finite and internally consistent before any substantive result route; the always-quiet zero-alert ROC endpoint remains valid.

```text
44 CASES = 22 OWNER-LABELLED MAJOR CHANGE + 22 MATCHED NO-CHANGE CONTROLS
V2 RAW-OWNER NO-SPEND GATE = 36260538589 SUCCESS
BLINDED PACKET SHA256 = f12762d4867da361e9eb72e3a12c30e82b734f005b09d527b7b19c7aee2ae1cc
OWNER KEY SHA256 = 75c64ca3235812b2cccf0d5dc2801698dd23f20a393f627106026d619eb299c9
88 NVIDIA ANALYSES = BASELINE + SUCCESSOR FOR EACH CASE
LIVE ATTEMPTS = 2 / BOTH ABORTED PRE-UNBLIND
OWNER-LABEL JOIN / SCORING = NOT RUN
SEMANTIC RESULT = NONE / ROUTE = INCONCLUSIVE_PROVIDER_OR_ANALYSIS_FAILURE
ABSTRACT_MAJOR_CHANGE != CLINICAL / REVIEW MATERIALITY
RETROSPECTIVE_DISCRIMINATION != REVIEWER TIME SAVED
```

Actual execution uses NVIDIA's currently advertised free Developer Program prototype/research endpoint, so no monetary charge is established; it consumes account quota/rate-limit capacity and requires Mark's NVIDIA credential. Two authorised local attempts were made on 27 September 2026 under the frozen contract. Run 1 aborted after 3 analyses on provider HTTP 503 `Service temporarily overloaded`; fresh run 2 aborted after 8 analyses because the pinned model did not return a JSON object. Both stopped before owner-label join/unblinding/scoring. The declared route is therefore `INCONCLUSIVE_PROVIDER_OR_ANALYSIS_FAILURE`; no third retry is authorised. Preserve: `PARTIAL_PROVIDER RUN != SEMANTIC RESULT`, `FAIL-FAST STOP != NEGATIVE MODEL SCORE`, and `RETRY / TUNING != UNTOUCHED BLIND VALIDATION`. Do not patch/tune the pinned source against this 44-case packet and then report the same set as blind validation.

### Digital Science Catalyst Grant 2026

Status: **SUBMITTED 27 SEP 2026 / GOOGLE FORM RESPONSE RECORDED / EMAIL COPY RECEIVED / RESULT UNKNOWN**.

Owner rules rechecked 26 September 2026: individuals and early-stage prototypes/concepts are eligible; proposal <=1,500 words; deadline **5 October 2026, 17:00 BST**; judges assess team, problem, solution, competitors, market, progress and Digital Science fit. The owner also explicitly asks applicants to name the affected research decision, existing tool/workflow, a refuse/flag/escalate failure case and a measurable outcome.

Current application draft:
`coordination/resources/DIGITAL_SCIENCE_CATALYST_2026_EVIDENCEWATCH_PREP.md`

Current integration boundary:
`coordination/resources/EVIDENCEWATCH_ZOTERO_INTEGRATION_BOUNDARY_20260926.md`

Current judge rehearsal:
`coordination/resources/DIGITAL_SCIENCE_CATALYST_2026_JUDGE_REHEARSAL_20260925.md`

Hostile review: COM #479 — COMPLETE / KEEP WITH CEILINGS.

EvidenceWatch current private main is `9c96c8390d65f4fb452b2a106bcdb4fa0418ea6f` with 62 deterministic tests green on both Windows and Ubuntu CI. PR #7 added the CSL-JSON handoff; PR #8 repaired malformed DOI fallback; PR #9 added the synthetic-content / real-format restart-and-correction witness; PR #12 added a predeclared shadow-mode research pilot protocol; PR #13 added its deterministic offline scorer; PR #16 added pre-pilot workflow/burden intake; PR #17 hardened its pre-unblinding freeze and canonical receipt. Preserve: **CSL HANDOFF != LIVE ZOTERO/READCUBE INTEGRATION** and **SYNTHETIC WITNESS != RESEARCHER VALIDATION**. The NVIDIA submission remains bound to the earlier frozen head `e924b0de15ccaa1255bfdb80685f60f1a60172e9`.

Research demo receipt: `coordination/build_ledger/EVIDENCEWATCH_SELECTABLE_RESEARCH_DEMO_20260925.md`. Recording-readiness receipt: `coordination/build_ledger/EVIDENCEWATCH_RESEARCH_DEMO_RECORDING_READY_20260927.md`. Optional Digital Science recording script: `coordination/resources/DIGITAL_SCIENCE_RESEARCH_DEMO_RECORDING_20260925.md`. Current main `9c96c839…` still carries the deterministic 1.8 -> repeat/no-alert -> 1.2/correction fixture; no provider call is made by the helper. Record once locally if useful, then freeze; no upload by momentum. Judge rehearsal: `coordination/resources/DIGITAL_SCIENCE_CATALYST_2026_JUDGE_REHEARSAL_20260925.md`. Likely post-gate form copy: `coordination/resources/DIGITAL_SCIENCE_CATALYST_2026_FORM_FIELD_PACK_20260925.md`. Owner-test matrix: `coordination/resources/DIGITAL_SCIENCE_CATALYST_2026_OWNER_TEST_20260926.md`. Windows/cross-platform repair receipt: `coordination/build_ledger/EVIDENCEWATCH_WINDOWS_CI_REPAIR_20260926.md`.

Latest stronger-owner pass removes mechanism novelty: Cochrane owns important retraction/correction-to-review paths; Refract owns reproducible source-change events; AIEP P170 owns evidence-dependency/cascade architecture; ReadCube/scite own substantial workflow/monitoring surfaces. EPPI-Reviewer, MAGICapp and ALEC/Monash now also sit inside the explicit stronger-owner set for living-review/guideline updating and infrastructure. A public pilot-partner quarry adds EPPI Centre, ALEC, Bern and MAGIC as strong current living-evidence owners capable of falsifying or subsuming the residual integration claim. EvidenceWatch survives only as a narrow post-reliance source-change integration/burden hypothesis. ALEC's Living Guidelines Handbook explicitly subtracts preprint->peer-reviewed currentness/data recheck from that residual; DataCite, Figshare, Zenodo and W3C PROV likewise subtract ordinary version identity/provenance for well-versioned datasets. Preprint/version pairs remain calibration fixtures, not gap evidence. The surviving value claim is integration: consume owner signals where available, bind them to the exact source state actually relied upon, preserve authority/lineage, judge bounded materiality, and route affected downstream work when current systems do not already do so cheaply. Memento/Perma/Visualping/changedetection.io also subtract generic web-state preservation/change detection from the gap claim. Strong-owner residual note: `coordination/resources/EVIDENCEWATCH_STRONG_OWNER_RESIDUAL_20260926.md`. Pair-level literature confirms the residual is non-zero but mostly not a major interpretation change; workflow incidence remains unmeasured. Prevalence note: `coordination/resources/EVIDENCEWATCH_RESIDUAL_PREVALENCE_20260926.md`. A pre-run retrospective challenge is now frozen at `coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_CHALLENGE_20260926.md` with executable manifest `research/evidencewatch_retrospective/brierley_major_vs_nochange_manifest_v2.json`: all 22 Brierley owner-labelled major-change abstract pairs plus 22 clean reconstructable same-stratum nearest-date no-change controls. v1 remains preserved and explicitly superseded before any model output. Blinded packet preparation is frozen at `coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_BLINDING_20260926.md`; exact EvidenceWatch/NVIDIA execution semantics are frozen at `coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_RUN_CONTRACT_20260926.md`; fail-closed dry-run/live harness is `research/evidencewatch_retrospective/run_brierley_retrospective.mjs` with boundary note `coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_HARNESS_20260926.md`. The harness is quota-protective: first `ANALYSIS_FAILED` seals a partial pre-unblind failure receipt and aborts; a completed result still requires all 88 analyses/responses. The one-command Windows wrapper hard-pins the current COM experiment blobs and CI verifies those pins. Frozen post-run owner-label join/scoring is `research/evidencewatch_retrospective/score_brierley_unblinded.py` with boundary note `coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_UNBLIND_SCORER_20260926.md`; strict headline scoring penalises failed positive cases as misses and failed controls as review burden. Result routing is predeclared at `coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_DECISION_RULE_20260926.md`: failure -> inconclusive; trivial lexical weak dominance -> narrow/stop semantic-value claim; only no-failure/no-dominance -> harder real-workflow falsification. A pre-model trivial lexical baseline is now frozen at `coordination/resources/EVIDENCEWATCH_RETROSPECTIVE_TRIVIAL_BASELINE_20260926.md`; full 22+22 AUC is ~0.79–0.80 across simple token-distance measures, so later model discrimination must be interpreted against non-semantic text magnitude rather than in isolation. Two authorised live retrospective attempts occurred under the frozen fail-fast rule and both stopped pre-unblind: run 1 after 3 analyses on NVIDIA HTTP 503, run 2 after 8 analyses on non-JSON model output. No owner-label join/scoring occurred; route = `INCONCLUSIVE_PROVIDER_OR_ANALYSIS_FAILURE`; no third retry is authorised. `PARTIAL PROVIDER RUN != SEMANTIC RESULT`; `ABSTRACT_MAJOR_CHANGE != LIVING_REVIEW_DECISION_CHANGE`. Current main `9c96c8390d65f4fb452b2a106bcdb4fa0418ea6f` includes the pilot protocol/scorer, cross-platform repair, real-workflow owner subtraction, PR #16's pre-pilot workflow/burden intake, and PR #17's meaningful freeze/completeness + canonical SHA-256 receipt repair; post-merge run `36237923895` SUCCESS on Ubuntu and Windows with 62/62 tests. No live pilot, research partner, provider call or operational reliance is implied.

The next evidential step is not more feature work. A **public historical** workflow specimen is preserved at `coordination/build_ledger/EVIDENCEWATCH_PUBLIC_WORKFLOW_SPECIMEN_20260926.md`: the University of Bern living review explicitly checked preprints for later publication and re-extracted changed data; a concrete Lombardi preprint -> final-publication episode changed the review extraction from the earlier 41/138 state to 17/139 and fed Q1 synthesis. The same guide reports weekly automated searches adding 100–200 records. A separate six-review evaluation reports 3–300 citations screened and 5 minutes–32 hours of author-team work per month; this is whole-review maintenance context, not EvidenceWatch-attributable burden. Current EvidenceWatch already represents the authority/succession pattern; **no code delta earned**. Primary proposed outcome is now reviewer minutes per correctly handled material-change episode versus existing practice. The stronger gate remains one willing current team's completed workflow + actual burden baseline. Public organizational candidates are preserved at `coordination/resources/EVIDENCEWATCH_PUBLIC_PILOT_PARTNER_QUARRY_20260926.md`; they are candidates precisely because they may show EvidenceWatch is redundant. ALEC/LEAPP-AI is now the strongest direct public falsification environment: it is actively mapping a real living-guideline workflow to AI tools, evaluating risks/functionality, and explicitly welcomes technology partners. No partner is established. Mark authorised the correction-first strong-owner contact on 27 September 2026; Framework sent one email to the official ALEC administrative route asking whether the residual problem is already solved, negligible, or mis-specified before any pilot/integration request. A Gmail sent/transmission receipt is established; recipient delivery/read, reply, interest and partnership remain unknown. The bounded first-conversation/falsification packet is preserved at `coordination/resources/EVIDENCEWATCH_ALEC_LEAPPAI_STRONG_OWNER_TEST_20260926.md`; it asks for correction before adoption and treats `OWNER FOUND / STOP` as a successful result.

The application was submitted at **17:47 BST on 27 September 2026**. Google Forms displayed `Your response has been recorded`, and a response-copy email reproduced the submitted values. No shortlist, interview, award or rejection is established. Award-stage contractual terms remain unresolved unless surfaced later.

Application-surface currentness is repaired at `coordination/resources/DIGITAL_SCIENCE_CATALYST_2026_APPLICATION_SURFACE.md`; form-ready copy is `coordination/resources/DIGITAL_SCIENCE_CATALYST_2026_SUBMISSION_PACKET.md`. Frozen release-candidate receipt: `coordination/build_ledger/DIGITAL_SCIENCE_CATALYST_2026_RC_20260927.md`; owner-currentness repair: `coordination/build_ledger/DIGITAL_SCIENCE_CATALYST_2026_OWNER_CURRENTNESS_REPAIR_20260927.md`; live-form budget repair: `coordination/build_ledger/DIGITAL_SCIENCE_CATALYST_2026_LIVE_FORM_BUDGET_REPAIR_20260927.md`; pre-send Codex/CC repair: `coordination/build_ledger/DIGITAL_SCIENCE_CATALYST_2026_PRESEND_REVIEW_REPAIR_20260927.md`; submission receipt: `coordination/build_ledger/DIGITAL_SCIENCE_CATALYST_2026_SUBMISSION_RECEIPT_20260927.md`; exact submitted proposal carrier recount 1,479 words; Section 9 budget remains 65 words against the live 75-word sub-cap. COM #538 is closed after host-neutral repair; wake proposal prose only for factual/form/terms defects. Digital Science's **general Site Terms** have now been reviewed: they grant a broad licence over submitted Site Content while leaving underlying copyright ownership with the submitter and requiring rights to third-party material. This is not established as the Catalyst-specific award/IP agreement. Keep the application to project-authored prose + links; do not paste third-party abstracts/screenshots/proprietary material. Historical Catalyst owner material is more permissive: the 2014 grant page explicitly disclaimed IP rights in applications and restrictions on other collaborators/investors, and a 2016 winner described the funding as `no strings attached`; preserve these only as historical context, not as 2026 terms.

```text
APPLICATION = SUBMITTED / 2026-09-27 17:47 BST
PROPOSAL BODY = 1479 WHITESPACE WORDS / 21-WORD HEADROOM / FROZEN RC / FINAL FORM-EDITOR RECOUNT REQUIRED
GOOGLE FORM = RESPONSE RECORDED / EMAIL COPY RECEIVED
GENERAL SITE CONTENT LICENCE = REVIEWED
CATALYST-SPECIFIC AWARD / IP TERMS = UNKNOWN
DEADLINE = 2026-10-05 17:00 BST
RESULT = UNKNOWN / WAIT FOR DIGITAL SCIENCE
```

### Mercor AI Safety Fund — secondary offline research lane

Status: **RESEARCH OBJECT SURVIVES / GRANT LANE HOLD / CURRENT ELIGIBILITY ROUTE UNRESOLVED / NO APPLICATION / NO MODEL CALLS**.

Stronger-owner receipt:
coordination/resources/MERCOR_AI_SAFETY_FUND_OWNER_SUBTRACTION_20260925.md

Marc Bara arXiv:2609.01873 owns the report-multiplicity/evidence-root mechanism, provenance-aware aggregation and similarity-vs-ancestry result. Junchi Liao arXiv:2607.20827 owns a separate source-authority/action-selection audit. The only surviving candidate is the cross: supplied evidential ancestry -> generated decision/action under a fixed policy. Novelty is not established.

Draft COM PR #482 remains offline only. Codex found the original five fixtures were solvable by a trivial ancestry-label mapping; the smallest repair is green at exact head `ff1330420a01e3f62aaee528ab4879edc96a460d` with workflow `36190238742` SUCCESS. Claude Code's current-owner review then found the live Mercor posting now requires an eligible institutional/company category and states awards are made to the researcher's institution. Mark's draft explicitly has no academic affiliation and no qualifying host is established. The grant lane is HOLD / DO NOT SUBMIT unless an eligible host exists or Mark chooses external clarification. Public award terms also include commercial-use licensing, early-access/private-held-out rights for evals, and a 12-month restriction involving unspecified Mercor competitors.

    ORIGINAL EOI = DO NOT SUBMIT
    NARROW RESEARCH OBJECT = OFFLINE / GREEN
    GRANT EOI = HOLD / DO NOT SUBMIT
    ELIGIBILITY ROUTE = UNRESOLVED
    EXTERNAL CLARIFICATION = MARK GATE / NOT SENT
    MODEL CALLS = 0
    SPEND = $0
    SUBMISSION = NONE

### Hack-Nation 7

Status: **STOP / NOT APPLYING**.

Kai confirmed that a CV could substitute for LinkedIn verification, but the application flow remains a poor fit for Mark's actual situation and would require unnecessary personal-career packaging for a speculative competition. Mark decided on 25 September 2026 not to pursue it.

```text
APPLICATION = NO
LINKEDIN = NO
CV UPDATE = NO
FURTHER CONTACT = NO
REOPEN ONLY IF THE FORMAT/TERMS MATERIALLY CHANGE
```

## Green / frozen candidate work

### Amazon Alexa+ — PR #245

`Did It Happen? — Action Receipts for Alexa+`

- exact head: `c0f8a94bb0aeec73e780c24d35c93372a306ee7d`;
- hosted: `campfire-ci / 35875127444 SUCCESS`;
- focused candidate suite: 27 tests;
- real Alexa+ host interoperability: **not tested**;
- registration / terms / repository-release / demo-upload / final submission: **human gates**.

Freeze unless a concrete defect, host result or rule change earns reopening.

### Live World / Square — PR #173

- exact head: `dad71bb70da16275b4ffd9acda70605699415973`;
- hosted: `campfire-ci 1538 / 35437072566 SUCCESS`;
- focused Live World tests: 15;
- Relay main / Production unchanged.

Field-triggered repair binds actual adapter authority scope before observation/write, binds execution to exact persisted human authority, brakes mid-batch target drift and refuses redirected 1F916 transport.

Freeze after green; reopen on concrete failure or deliberate promotion work.

### Relay COMSYNC maintenance — Relay through #265 / Simple-v1 through Town activity-window repair

- Relay main remains `9408d795d0508815e097066b749800ddbd8b8290`; #265 deferred acknowledgements are merged there. Production activation remains separate.
- Simple-v1 maintained source is `framework/campfire-square-simple-v1@6ca82daf8fea8424f46b44d8bb0a0829edea9c9a`.
- #266 upstreamed the supervisor transition ledger and byte-safe installer fetch.
- #267 suppresses repeated parsing of an immutable malformed historical GitHub ingress body using refusal state keyed by comment ID + body SHA-256; #268 pins actual parser-call suppression.
- Independent hostile review found refusal-ledger I/O could itself become an availability dependency. #269 makes **only the diagnostic refusal ledger** best-effort: read failure -> empty cache; append failure -> in-memory refusal + continue; both emit degraded heartbeat. Speech/actuation, dedupe, receipt and authority state remain fail-closed.
- #269 final head `302540eb22def9007176361a1c51da2ce49efb08`; Windows `36320549273`, broad `36320549270`, post-merge Simple-v1 `36320632175` all SUCCESS. Earlier Windows harness failures remain visible in history rather than being flattened.
- #270 pins a **test-only Windows PowerShell encoding invariant**: every installer-shipped `.ps1`/`.psm1` file, discovered from the installer's own payload list, must remain ASCII until a deliberate UTF-8-aware execution carrier supersedes this guard. Candidate `b03c2e10…`; Windows `36320921439`, broad `36320921494`, post-merge `36321019856` SUCCESS; merge `e53631d1…`. `REPOSITORY_BYTES_CORRECT != POWERSHELL_DECODING_CORRECT`.
- A concrete installed-runtime defect reopened this source lane once: the Town `-AllCitizens` cache had retained 24,330+ events / 53.7 MB back to 14 September and rewrote the full file each minute. Exact head `9f0f038e…` prunes only the activity view to the intended 24-hour server-time window, leaves AI history unpruned, adds an on-disk regression and wires it into hosted Windows PowerShell CI `36412767174 / SUCCESS`.
- Installed Simple-v1 was last observed RUNNING at `6a07380bdf85804d7029ce5ea6ba279a14c5192b` (through #268), loaded at the 27 September reboot; installed watchdog SHA-256 prefix `8cd39ebb`. Its installed payload therefore contains #267/#268 but not #269/#270, the Town cache repair or the installer-BOM repair. The adjacent `System error.` bursts remain correlated with refresh completion but their throwing statement is not isolated. `SOURCE_REPAIRED != INSTALLED_REPAIRED`; `CACHE_PRUNED != GUI_ERROR_CAUSE_ISOLATED`.
- Receipts: `coordination/build_ledger/RELAY_SIMPLE_V1_MALFORMED_INGRESS_20260927.md`, `coordination/build_ledger/RELAY_SIMPLE_V1_WINDOWS_ENCODING_GUARD_20260927.md`, and `coordination/build_ledger/SIMPLE_V1_TOWN_ACTIVITY_WINDOW_REPAIR_20260928.md`.

### Relay diagnostic-retention repair — source merged through #269 / installed runtime pending

The malformed historical #177 comment `5380939579` remains preserved.

Maintained source now handles both sides of the field failure:
- #267/#268: identical malformed bytes do not get reparsed indefinitely, including across worker restart, and edited bytes reopen parsing;
- #269: the diagnostic refusal file cannot take the whole citizen ingress pass offline if temporarily unreadable/unwritable.

At the original observation, 4,028 / 5,252 retained event-4100 rows were the same parse error and useful diagnostics were aging out in under a day.

Current boundary:
- maintained source repaired through `05137dc0…`;
- installed worker last observed pre-#266 `f4fa182…`;
- no install/restart has been performed by Framework;
- therefore the live host log flood is **not yet claimed fixed**.

Do not delete or rewrite the historical comment merely to make diagnostics quiet.

Simple-v1 source maintenance is now **STOP BY DEFAULT**. Reopen only for a concrete field defect, an installed-runtime update/witness, or a deliberate change to the Windows PowerShell encoding carrier.

### Square targeted engagement — one outside return / one invitation still waiting

- Mark explicitly authorised bounded targeted engagement after the ten-day participation audit.
- Framework posted one invitation on post `6784` (comment `80831`) and one delayed return on tidemark's post `5757` (comment `80837`).
- Tidemark replied at comment `80868`: they recorded the repair as reported testing/incorporation, **not** an independent audit, and identified the useful property as allowing Source C to address two mentions without first settling maker identity while leaving candidate history unresolved rather than silently accepting it. No further request was made.
- The post `6784` invitation received a direct substantive return from `pengy-of-catbee` at comment `81646` replying to Framework `80831`. It exposed `SENDER_ACTIVITY != EXTERNAL_ENCOUNTER_EVIDENCE`; this earned PSFH D088. One receiving-side trace supports one encounter, not population reach.
- Claude Code separately posted the previously held silt/byline replies as comments `81328` and `81329` after Mark clarified direct Square speech authority; both were read back exactly.
- **OUTSIDE REPLY != INDEPENDENT AUDIT / ADOPTION / VALIDATION. Do not duplicate either Framework outreach or reply again to tidemark's closing return.**

## Time / evidence gated

### ATRS / Apart Epistemics — COM PR #364

- head: `d2bea526feced78750d1bbb4c45e686f3e4c6446`;
- September method/prep frozen;
- full population result intentionally uncomputed;
- wake for fresh November corpus/live sprint rules or a concrete method falsifier.

### Hack Apertus

Hold until **1 October** live challenge/rules/rights gate. Do not pre-consume judged work.

### TRACE / Mechanical Ethics successor

COM #365 now preserves the successor/review history and routes the released pair into world/use testing. TRACE beta PRs #56-59 and ME beta PRs #49/#50/#52/#53 are closed after release with branches and discussions retained. The earlier ME #47 reader-test pressure remains relevant, but no beta5 or released-source edit is earned by review momentum.

Successor-pressure route:
`coordination/ME_TRACE_SUCCESSOR_PRESSURE_LEDGER_20260919.md`

Current ledger:
```text
ME PATCH PRESSURES = 1
ME PATCHES EARNED = 0
TRACE PATCH PRESSURES = 0
TRACE PATCHES EARNED = 0
```

### PSFH

D090 is the current public door:
- maintained source `5eccae1403bee1d6774fb33622f84fb6424120e5`;
- public `gh-pages@11c2751d686a4fac710a61cdfc5e5840781fda1b`;
- Site Preview `0.8.47`;
- publisher `36359621385 / SUCCESS`;
- post-sync maintained CI `36359780443 / SUCCESS`.

A real Square return identified a concrete Correction compression defect: a plausible cached, mirrored or superseded copy can receive a correction while the version that people or processes actually rely on remains unchanged. D090 binds correction to that effective copy, separates sending from evidence of target change and asks for a target-copy check or receiving-side receipt. All five current carriers were verified. This is a reader-earned PSFH repair, not a TRACE/ME gap, endorsement, population result or efficacy claim.

Receipt: `coordination/build_ledger/PSFH_D090_EFFECTIVE_COPY_CORRECTION_20260928.md`.

D087 remains the last broad first-contact audit: **KEEP / NO GENERAL REDESIGN**.

`PLAUSIBLE COPY != EFFECTIVE COPY`
`SENT CORRECTION != TARGET CHANGED`
`PUBLISHED != READER_BENEFIT`

## The Human Record

```text
public records = exactly 4
record 5 = NOT EARNED
stewardship = OFFERED / NOT ACCEPTED
portable contribution route = LIVE
```

The 22–23 September entity-through-time pressure did **not** earn a new THR root architecture. Exploratory THR PR #52 is now closed unmerged after its one executable residue was extracted through #81: a bounded read-only impact query over existing source/assertion/catalogue relations. Current THR models still separate mentions, entities, assertions, correction and living-subject boundaries. Useful remaining pressure is real cross-record fan-out, temporal/currentness discrimination and subject obligations—not a universal living-person graph.

19 September record-5 quarries:
- Anthropic correction lineage -> strongest owner already preserves original + revision + reason;
- digital-preservation candidates -> stronger active preservation/legacy owners.

Current THR main is `448dcd7b2f829e0c7277365d14daaacf4cd381a4`. Main integrity `36237522858` and Pages deployment `36237522573` are observed SUCCESS. Documentation-only #78/#80 remain active; #81 adds bounded read-only impact routing with no schema/type/record growth. Exploratory RFC #52 is closed unmerged with research history preserved. Open THR PRs = 0. Receipts: `coordination/build_ledger/THR_CURRENT_DOCUMENTATION_REPAIRS_20260926.md` and `coordination/build_ledger/THR_FRACTAL_RFC_RESIDUE_EXTRACTION_20260926.md`.

PR #75 repaired entity-admission containment/catalogued-record linkage. PR #76 repaired stale browse-card source-basis detection. PR #77 then used that guard during a real record maintenance pass: Hannibal v0.1.3 now records a bounded Internet Archive / New York Public Library recovery route for the Polybius printed-edition family, while explicitly leaving exact physical printing/reprint state and exact Thayer HTML identity unresolved. Exact #77 head `a80f2c1f51528b50b5eae24bb6a8635606205642`; exact-head validation `36198799678` SUCCESS. The human view, catalogue source pins and browse-card basis were re-reviewed/re-pinned; browse summary prose, schema and four-record count did not change. Old #63/#71 are closed as superseded.

Preserve: **DIGEST MATCH != SUMMARY TRUE** and **PRINTED EDITION ROUTE IDENTIFIED != EXACT WEB REPRESENTATION PRESERVED**. Detailed receipt: `coordination/build_ledger/THR_HANNIBAL_POLYBIUS_RECOVERY_ROUTE_20260925.md`.

No THR schema/catalogue growth by momentum.

## Resources / opportunities

COM #348 remains the resource/opportunity quarry.

Use funding/credits only when a bounded current project has a real resource bottleneck. Possible value remains zero until awarded/received. Do not manufacture a proposal to justify available money.

## Closed / stopped

- ARC Prize build — **OWNER FOUND / STOP**;
- Shipaton 2026 — **STOP** (store/account infrastructure mismatch);
- generic EvidenceBridge/Open-Agent clone — **NOT EARNED**;
- generic Nebius platform-fit product — **NOT EARNED**;
- BeforeBuild standalone product — **NOT EARNED**.

## Consequential gates

Explicit Mark/human gate remains for:
- external owner/institution contact where consequential;
- competition/grant registration, account creation, terms acceptance and submission;
- credentials, payment, payout, tax/new spend;
- TRACE/ME canon, release, baseline or licence changes;
- destructive/irreversible actions;
- travel/in-person commitments;
- Campfire Production activation;
- PSFH public guest-data intake policy/controller/legal choices.

Routine reversible repository research/build/repair may proceed within current direction.

## Continuity cadence

Because active work is consuming enough context to force frequent new chat tabs:

```text
MATERIAL BUILD / REPAIR / STOP / HUMAN-GATE CHANGE
-> WRITE DATED RECEIPT IF DETAIL MATTERS
-> UPDATE COMPACT HOT SURFACE
-> CONTINUE

WHEN CHECKPOINTS ACCUMULATE
-> FOLD THEM INTO CURRENT STATE
-> DO NOT PRESERVE MINI-HISTORY INLINE
```

Routing:
- current action: `coordination/ACTIVE_THREAD_POINTER.md`;
- operational state: `coordination/build_ledger/BUILD_STATUS.md`;
- cold-domain retrieval: `continuity/OMISSION_MAP.md`;
- detailed 19 Sep compaction receipt: `coordination/build_ledger/COMPACT_CONTINUITY_REPAIR_20260919_MIDDAY.md`;
- history: Git + dated receipts.

```text
HEAD = CURRENT ROUTING
DATED RECEIPTS = DETAIL
GIT = HISTORY
OMITTED FROM HEAD != ABSENT
```

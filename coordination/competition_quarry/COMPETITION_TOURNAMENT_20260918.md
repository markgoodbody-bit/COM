# Competition tournament — 18 September 2026

Status: **LIVE OPPORTUNITY QUARRY / NOT REGISTRATION / NOT TERMS ACCEPTANCE / NOT SUBMISSION / NOT SPEND AUTHORITY**

> **HOW CAN WE MAKE A BETTER FUTURE?**

Purpose: identify prize competitions where work we genuinely want to build could plausibly win something, without converting the project into competition theatre.

## Tournament rules

```text
BIGGER_PRIZE != BETTER_PROJECT
ELIGIBLE != FIT
FIT != WIN
POSSIBLE_PRIZE = 0 UNTIL AWARDED
IF_WE_LOSE -> USEFUL_WORK_SHOULD_REMAIN
PROJECT_PURPOSE > COMPETITION
```

## 1. Apart AI x Epistemics — CURRENT LEAD

Dates: 13–15 Nov 2026, online.
Prize: $1,000 / $500 / $300 / $100 / $100; $2,000 total.
Owner:
https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15

Current object: ATRS #364.

Disposition:
**REAL CONTENDER / FIRST PLACE PLAUSIBLE / RESULT SURFACE PRESERVED.**

No further population coding before the sprint.

## 2. Hack Apertus — PURSUE PREP / STRONG NEAR-TERM FIT

Online stage: 1–16 Oct 2026.
Submission: 16 Oct 12:00 CEST.
Owner:
https://hackapertus.devpost.com/
https://hackapertus.ch/

Relevant track:
**Apertus Readiness — Red-Teaming Apertus**.

Cash:
- Red-Teaming winner: €2,670 (2,500 CHF), plus Hugging Face credits and qualification for 2027 grand finals.

Current participant count on public Devpost is low hundreds; track-specific field will be smaller.

Why this fits:
- the track explicitly wants documented model failures;
- factuality/hallucination, privacy, culture/values and trustworthy-model behavior are in scope;
- THR has already generated real epistemic failure classes rather than invented benchmark slogans.

Candidate red-team battery, **design only before the hack window**:
1. **false independence / repeated-source ancestry** — does Apertus treat dependent paraphrases as independent corroboration?
2. **translation vs source-language literal** — does it upgrade a translation rendering into an attested original string?
3. **UNKNOWN -> ABSENT collapse** — does missing/partial evidence become a claim of non-existence?
4. **source criticism attribution** — does an author's criticism of another source become adopted model fact?
5. **correction propagation** — after a load-bearing source correction, does the model retain a stale downstream conclusion?

These tests can be source-grounded, multilingual and reproducible.

Important owner boundary:
generic factuality/hallucination evaluation is not ours. The candidate value is concrete reproducible Apertus failures if observed.

Do **not** run the Apertus competition result before the official hacking window if the live rules expect event-period work.

Current disposition:
```text
PURSUE PREP
NO MODEL RESULT YET
NO REGISTRATION YET
NO CLAIM OF NOVEL BENCHMARK
```

## 3. RevenueCat Shipaton — STOP / 2026 STORE PATH NOT VIABLE

Deadline: 30 Sep 2026.

A bounded PSFH mobile spike was built on draft PR #374 and passed Expo/TypeScript/config CI. The small local-first app concept was technically viable.

Mark then confirmed he has **no existing Apple / Google Play / Samsung developer-store infrastructure**.

Current store constraints make the 2026 competition route disproportionate:
- a new Google Play personal account cannot credibly reach production in time because of the mandatory pre-production testing path;
- fresh Apple enrollment adds identity/payment/store uncertainty inside the organiser's already-recommended review buffer;
- Shipaton requires a live public store listing and a RevenueCat-powered purchase path.

SHIPATON 2026 = STOP
CODE FAILURE = NO
STORE / ACCOUNT BOTTLENECK = YES
PR #374 = PRESERVE REUSABLE MOBILE SPIKE / CLOSE UNMERGED
DO NOT TURN PSFH INTO A STORE-ENROLLMENT RACE

The mobile concept may be revisited later on its own merits.

## 4. Open Agent Hackathon 2026 — HOLD / NO EARNED PRODUCT YET

Dates: 15–20 Oct 2026, online.
Owner:
https://hackathon.genai.works/

The earlier candidate was EvidenceBridge.

A bounded deterministic EvidenceBridge proof was built and passed CI, then deliberately owner-subtracted. Current strong owners — especially Doubt, plus source-lineage / provenance tools — already cover the generic object:

CLAIM + SOURCES -> SOURCE-GROUNDED EVIDENCE MAP -> SUPPORT / CONTRADICTION / UNKNOWNS -> INSPECTABLE TRACE

The project then encoded four THR pressure cases in **unmodified Doubt v0.8.0**:
- flak source dependence;
- Hannibal translation / attribution;
- R. Vale unresolved identity;
- unseen sieve/riddle transmission case.

All four passed the pinned upstream contract. Current result: **OWNER SUFFICIENT WITH LOSS**. Dedicated THR machine semantics are richer, but no consequential product failure from that compression has been observed.

EVIDENCEBRIDGE OPEN-AGENT ENTRY = NOT EARNED
OPEN AGENT = RETAIN AS OPPORTUNITY / NO CURRENT OBJECT
DO NOT REBUILD DOUBT UNDER A NEW NAME

Reopen only when a real project need produces work that current owners cannot already perform.

## 5. Nebius x NVIDIA Global AI Hackathon — HOLD / HIGH UPSIDE, NO EARNED OBJECT

Deadline: 30 Oct 2026, 10:00 PDT.
Owner:
https://nebiusglobalaihackathon.devpost.com/

Cash remains materially larger than the Apart routes, but prize size does not create a product gap.

The previous EvidenceBridge/Nemotron path is now owner-subtracted and must not be revived by adding platform inference to an already-owned evidence-map object.

NEBIUS = RETAIN / HIGH UPSIDE
EVIDENCEBRIDGE FOLLOW-ON = NOT EARNED
NEMOTRON / TAVILY THEATRE = NO
NEW OBJECT MUST BE USEFUL BEFORE PLATFORM FIT

If a genuinely new product emerges from world/real-use work, re-check the live Nebius rules then.

## 6. Since AI 2026 — CONDITIONAL / HIGH LOAD

Dates: 6–8 Nov 2026.
Location: Turku, Finland; in person.
Owner:
https://sinceai.ai/hackathon
https://sinceai2026.devpost.com/

Cash:
- €10,000 grand;
- 15 × €2,000 company-challenge winners;
- €4,000 best technical execution;
- €3,000 best responsible AI;
- €3,000 best commercial potential.

Partners/challenges include Google for Developers, Bayer, Sandvik, Kongsberg and Valmet.
Expected attendance: 1,000+.

Requirement:
working prototype built substantially during the event; pre-existing assets disclosed.

Why it could fit:
Framework/Codex can build quickly; responsible implementation is explicitly judged.

Why it is not assigned:
- in-person Finland;
- application/admission required;
- travel and Mark time;
- exact challenge fit matters more than generic responsible-AI strength.

Current disposition:
```text
HOLD / WATCH CHALLENGES
HIGH UPSIDE
HIGH HUMAN LOAD
TRAVEL / APPLICATION GATE
```

## 7. Apart AI Collusion — HOLD / NO EARNED DELTA

Dates: 23–25 Oct 2026, online + NYC hub.
Prize: $1,000 first / $2,000 total.
Owner:
https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25

Track 2 asks what should count as convincing evidence of collusion.

Our witness-independence instincts are relevant, but current collusion work already explicitly owns:
- correlation != collusion;
- shared model lineage != collusion;
- common causes must be modelled;
- counterfactual/channel-removal tests.

Therefore a project such as “shared lineage causes false collusion alarms” is already owner-occupied as a concept.

To earn entry, we need a new controlled experiment with a concrete detector/evidentiary failure that beats the existing owner.

Current disposition:
```text
HOLD
NO EARNED EXPERIMENT YET
DO NOT REPACKAGE THR LANGUAGE
```

## Rejected / not-current routes

- TLN Cybersecurity Challenge — student-only; not eligible.
- SPEED October AI Challenge — student-only; not eligible.
- old Microsoft Azure Responsible AI Hackathon — historical, not a current 2026 entry.
- OpenAI Bio Bounty — specialist private bio-red-team programme, not a natural project route.
- SharedOS / Syndicate — already ended.

## Current priority

```text
1. WORLD / REAL USE = FIND NEXT EARNED GAP
2. ATRS / Apart Epistemics = PRESERVE RESULT / DO NOT PRE-CONSUME
3. Hack Apertus = PREP FROZEN / RUN ONLY IN WINDOW
4. Open Agent = HOLD / NO CURRENT PRODUCT
5. Nebius/NVIDIA = HOLD / NO CURRENT PRODUCT
6. Since AI = WATCH CHALLENGES / HUMAN LOAD
7. Apart Collusion = HOLD UNTIL REAL DELTA
8. Shipaton 2026 = STOP
```

This ordering is deliberate. Competition windows are opportunities around useful work; they are not the project's top-level work queue.

```text
WORLD / REAL USE > COMPETITION PREPARATION
PRESERVE FUTURE RESULT != SPEND CURRENT TOKENS
```

No competition registration, account creation, store submission, terms acceptance, travel booking, spend or external contact is authorised by this tournament record.

## PM coordination cleanup — 18 September 2026

Open-PR surface was reconciled with the tournament's actual dispositions:

- PR #350 evidence-lineage oracle — CLOSED UNMERGED / preserved head d3aede2e...
- PR #351 WarrantFuzz — CLOSED UNMERGED / preserved head 88264d58...
- PR #352 hostile WarrantFuzz tests — CLOSED UNMERGED / preserved head 9ac92d82...
- PR #353 Missing Edge — CLOSED UNMERGED / preserved head fd5e3e91...
- PR #361 earlier No Free QALY metric stress — CLOSED UNMERGED / superseded by #363, preserved head ea759b24...
- PR #362 policy-boundary compiler — CLOSED UNMERGED / owner-rich + fixture-baked result, preserved head e2c5b348...
- PR #363 No Free QALY — remains OPEN only as fallback synthesis; exact repaired head 45105b2775c5e99c65db264a1c9285b5f7edcd1f; workflow 35383752912 SUCCESS.
- PR #364 ATRS — remains current lead / result surface preserved.

PR #363 hostile-review debt is now actually repaired: two unearned synthetic examples removed; strict pairwise reversal separated from tie-vs-order; alphabetical identifiers cannot create the scientific result; CHEERS/CHEERS-AI ownership credited; fictional exercise explicitly not reader-benefit evidence.

Hack Apertus live rules/terms were rechecked after this tournament was written. Challenges and judging criteria remain pending for 1 October. The organiser terms also require open-source submission outputs and contain both an event-period work warranty and a separate pre-existing-IP clause. The pre-event five-family red-team design is therefore explicitly timestamped and must not be represented as event-period discovery.

Start gate:
`coordination/competition_quarry/HACK_APERTUS_RED_TEAM_PREP_20260918.md`

Current competition state remains:

1. ATRS / Apart Epistemics — LEAD / preserve result.
2. Hack Apertus — PREP ONLY / run after 1 Oct rules recheck.
3. No Free QALY — FALLBACK ONLY.
4. World / real use — find earned work before platform fit.

SELECTED ENTRY = NONE
REGISTRATION / TERMS ACCEPTANCE / SUBMISSION = NONE

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

## 3. RevenueCat Shipaton — HIGH UPSIDE / URGENT CONDITIONAL GATE

Deadline: 30 Sep 2026 11:45 PM PDT.
Owner:
https://www.shipaton.com/
https://revenuecat-shipaton-2026.devpost.com/

Relevant category:
**RevenueCat Peace Prize**.

Cash:
- 1st: $20,000
- 2nd: $10,000
- 3rd: $5,000

Peace Prize criteria:
- impact;
- feasibility.

Eligibility/product requirements:
- new iOS/iPadOS/macOS/Android app whose first public store release is during the Shipaton window;
- fully published in Apple App Store, Google Play or Samsung Galaxy Store before deadline;
- RevenueCat SDK must power at least one purchase;
- judges need a free trial or promo code to unlock the purchase;
- demo video <= 2 min;
- app icon/screenshot requirements.

Important owner FAQ:
a project that previously existed only as a web app may qualify as a new app-store version.

### Candidate: Please Start From Here mobile front door

Possible product:
a privacy-first, local-first orientation app that helps a person facing a difficult/overwhelming situation:
- state what is happening;
- separate known / reported / unknown;
- name what matters now;
- see what is reachable;
- identify what is hardening with time;
- choose one small next action;
- keep a private witness note;
- optionally enter PSFH rooms / human works / THR records.

No moral score. No diagnostic/medical claim. No account required.

The existing PSFH web project can remain the public gift. Competition app could keep all core functionality free and use a genuinely optional digital supporter/cosmetic purchase to satisfy RevenueCat without paywalling the gift.

### Critical feasibility gate

This route is **time-critical** and may die on store infrastructure rather than code.

Before committing a build, establish:
- whether Mark already has a usable Apple / Google Play / Samsung seller/developer account;
- exact store review/testing lead time for that account;
- acceptable purchase shape and store policy;
- any developer/account fee;
- whether the voluntary-purchase model is ethically acceptable for PSFH.

Those are human/account/spend/terms gates.

Current disposition:
```text
HIGH UPSIDE
REAL PEACE-PRIZE FIT
URGENT FEASIBILITY GATE
DO NOT SILENTLY TURN PSFH INTO MONETISATION
NO ACCOUNT / STORE / TERMS / SPEND ACTION WITHOUT MARK
```

If store publication cannot be credibly achieved in time, kill immediately.

## 4. Nebius x NVIDIA Global AI Hackathon — RETAIN / SERIOUS PRODUCT ROUTE

Deadline: 30 Oct 2026, 10:00 PDT.
Owner:
https://nebiusglobalaihackathon.devpost.com/

Cash:
- grand: $20,000
- 2nd: $10,000
- 3rd: $6,000
- Tavily bonus: $3,000
- city awards: $500
- other track prizes.

Requirements:
- working application on Nebius Token Factory or Nebius AI Cloud;
- at least one NVIDIA open-source model;
- working hosted demo/test build;
- <=3-minute public YouTube demo;
- public open-source repository with an open-source licence;
- existing project must have been significantly updated during the submission period.

Judging:
- technological implementation;
- design;
- potential impact;
- quality/creativity of idea.

### Candidate product — evidence/claim answerability tool

Only pursue if it becomes useful independently.

Possible new clean open-source product:
`EvidenceBridge` / working name.

Input:
- source URLs/documents + a claim/question.

Output:
- source-grounded claim/proposition table;
- source ancestry/dependence;
- reported vs observed/inferred state;
- unknowns;
- conflicting/corrected claims;
- link from summary conclusions back to source evidence;
- no living-person graph by momentum.

Nebius/Nemotron could naturally do bounded extraction/reasoning; deterministic code would enforce evidence relationships and fail closed.

Tavily could be used only if it materially improves source discovery/currentness, which could make the $3k bonus natural rather than decorative.

This would be useful to THR/research/journalism even if it loses.

Risk:
7,000+ public participants. A shallow wrapper will not compete.

Current disposition:
```text
RETAIN / HIGH UPSIDE
PRODUCT MUST EARN IT
NEW CLEAN OSS REPO IF BUILT
NO NEMOTRON THEATRE
```

## 5. Since AI 2026 — CONDITIONAL / HIGH LOAD

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

## 6. Apart AI Collusion — HOLD / NO EARNED DELTA

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
1. ATRS / Apart Epistemics = PRESERVE RESULT
2. Hack Apertus = PREP NOW, RUN IN WINDOW
3. Shipaton Peace Prize = URGENT FEASIBILITY GATE
4. Nebius/NVIDIA = PRODUCT DISCOVERY / HIGH UPSIDE
5. Since AI = WATCH CHALLENGES / HUMAN LOAD
6. Apart Collusion = HOLD UNTIL REAL DELTA
```

No competition registration, account creation, store submission, terms acceptance, travel booking, spend or external contact is authorised by this tournament record.

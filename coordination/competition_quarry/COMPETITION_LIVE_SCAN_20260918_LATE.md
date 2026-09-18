# Competition live scan — 18 September 2026 late

Status: **FRESH PUBLIC-SOURCE SCAN / BUILD ROUTING / NOT REGISTRATION / NOT TERMS ACCEPTANCE / NOT SUBMISSION**

> HOW CAN WE MAKE A BETTER FUTURE?

Direct human direction for this pass: pursue competitions we can credibly win, while preserving the existing anti-drift rule that prize availability does not manufacture a useful project.

~~~text
USEFUL WITHOUT PRIZE
+ CURRENTLY ELIGIBLE / PLAUSIBLY ELIGIBLE
+ BUILD WINDOW REAL
+ PRODUCT / RESEARCH FIT
+ HONEST OWNER SUBTRACTION
-> BUILD / PREP

PRIZE EXISTS
+ NO CONSEQUENTIAL GAP
-> STOP
~~~

## 1. Amazon Developer Hackathon — ACTIVE BUILD

Official:
- https://amazonappdev2026.devpost.com/
- https://amazonappdev2026.devpost.com/rules

Current public state observed 18 Sep:
- submission period already open;
- deadline 23 Oct 2026 at 12:00 PDT;
- $138,000 cash prizes listed;
- Alexa+ first place = $25,000 cash + AWS credits;
- existing projects may enter only with significant updates during the submission period; new work now is eligible under the published timing rule;
- Alexa+ track accepts a self-hosted MCP server or Agent Skill, and the event overview permits a simulated Alexa+ experience for builders new to the platform;
- one primary-track prize plus one mini-challenge prize may be awarded to a project.

Current project candidate:
- Campfire Relay draft PR #245
- branch: framework/amazon-alexa-did-it-happen-20260918
- working title: **Did It Happen? — Action Receipts for Alexa+**
- product question: can a voice agent refuse to say "done" until the intended external effect is independently checked, while keeping ambiguous writes recoverable and non-retried?

Strong-owner correction already applied:
- MCP owns transport;
- durable execution/idempotency has mature owners;
- Postcondition MCP / Postcept / verify-action-mcp and ordinary distributed-systems practice own much of effect verification;
- Amazon itself owns Alexa+ error-recovery, schema and idempotency guidance.

Therefore candidate claim is product-level, not conceptual novelty:
**make verified / rejected / unknown / reconcile legible in ordinary Alexa+ interaction.**

Current ceiling:
- source spike only;
- simulated external services;
- no Amazon/Devpost registration;
- no terms acceptance;
- no AWS spend or credits;
- no Alexa+ production access claim.

Disposition: **BUILD / ATTACK / KEEP ONLY IF HOST-SHAPED TESTS STAY GREEN.**

## 2. Hack Apertus — PREPARED / WAKE 1 OCTOBER

Official:
- https://hackapertus.devpost.com/

Current known public schedule:
- challenge window / rules open 1 Oct;
- submission deadline 16 Oct;
- Red-Teaming challenge carries a CHF 2,500 / ~€2.67k winner prize plus associated benefits.

Existing prep:
coordination/competition_quarry/HACK_APERTUS_RED_TEAM_PREP_20260918.md

Rule remains:
do not consume judged result surfaces before the challenge/rules window.

Disposition: **HIGH PRIORITY ON 1 OCT / NO PRE-RUN NOW.**

## 3. Dwelly London AI Hackathon — STRONG IN-PERSON FIT / HUMAN APPLICATION GATE

Official event:
- https://luma.com/ja5x0m76

Current public state:
- 10 Oct 2026, London;
- invite / approval required;
- 20 teams;
- tracks: insurance claims, property management, banking/financial services, delivery/logistics;
- agents face calls, emails, documents, CRM records and operational workflows;
- "Reality Test" releases unseen escalation cases ~30 minutes before deadline: conflicting information, failed actions, missing context;
- £5,000 grand prize;
- £1,500 Best Exception Handling;
- £1,500 Best Engineering;
- £1,500 Best Voice Agent;
- £500 People's Choice;
- organisers publicly describe possible real pilot opportunity for strong teams.

This is an unusually direct fit to existing project engineering strengths:
- unknown != failure;
- ambiguous write -> no silent retry;
- source/currentness distinction;
- explicit exception state;
- correction/reconciliation;
- evidence before closure;
- human escalation where authority/evidence is insufficient.

Do not prebuild the event's track solution. Prepare failure-handling patterns and attack method; build against the supplied problem/data on the day.

Disposition: **APPLY IF MARK CHOOSES THE HUMAN / IN-PERSON GATE.**

## 4. Stripe x Briefcase London — STRONG SHORT-FORM FIT / HUMAN REGISTRATION GATE

Official event:
- https://luma.com/3k1pazop

Current public state:
- 15 Oct 2026, London, 17:15–22:00;
- 150 developers;
- two tracks revealed at opening;
- explicit hint: real money movement, autonomy, policy, auditability;
- £2,000 cash overall winner;
- Stripe-credit track prizes / side quests.

Three-hour build means prior generic reasoning discipline matters more than prebuilding a track-specific product.

Useful carry-in:
~~~text
INTENT
-> POLICY / AUTHORITY
-> IDEMPOTENCY
-> ONE WRITE
-> EFFECT READBACK
-> RECEIPT
-> UNKNOWN / RECONCILE / HUMAN
~~~

Stripe/Amazon/payment-system owners already own much of idempotency/payment safety. Use their mechanisms.

Disposition: **REGISTER / ATTEND ONLY THROUGH HUMAN GATE; NO TRACK BUILD BEFORE REVEAL.**

## 5. Future States at No.10 — HIGH PURPOSE FIT / NOT CASH-FIRST

Official event:
- https://luma.com/9vr0zktj

Current public state:
- 5–6 Oct, 10 Downing Street;
- approval required;
- external technologists + civil servants work on real state problems;
- strongest teams present to Cabinet Secretary / government leaders;
- partner credits/subscriptions rather than a stated cash pot.

Potential value is direct real-owner exposure and useful public-sector build, not cash.

Disposition: **WORTH APPLYING IF HUMAN GATE / TWO DAYS IS ACCEPTABLE; DO NOT CALL IT A CASH-PRIZE LANE.**

## 6. London AI x Science — HOLD / TRACKS NOT YET SPECIFIC

Official:
- https://luma.com/3iipivod
- https://algorithmdiscovery.org/events

3–4 Oct; teams 3–5; approval required; partner data/compute; cash + credits but exact track/prize detail not yet sufficiently specific for this project.

Disposition: **HOLD UNTIL TRACK FIT OR TEAM PATH APPEARS.**

## 7. Nebius x NVIDIA — HIGH UPSIDE / CURRENT PRODUCT GAP NOT EARNED

Official:
- https://nebius-ai-hackathon.devpost.com/

Current public state:
- deadline 30 Oct;
- $50k+ listed prize pool;
- $20k grand / $10k second / $6k third plus partner/track awards;
- project must use Nebius and at least one qualifying NVIDIA open model;
- current judging weights implementation, product design, impact and idea quality.

Fresh owner subtraction killed the obvious generic candidates:
- generic action-recovery / effect-receipt runtime -> crowded by Postcondition/Postcept/AgentLedger/Temporal/LangGraph;
- generic source-currentness / correction-propagation agent -> existing currentness/reconciliation owners already strong.

Do not add Nemotron merely to make an unrelated product eligible.

Disposition: **HOLD UNTIL A PRODUCT NATURALLY NEEDS THE REQUIRED STACK.**

## 8. Open Agent Hack — HOLD FOR TRACK-SPECIFIC FIT

Official:
- https://openagent.dev/

15–20 Oct, online; public materials describe agent work and a cash/bounty pool around ~$20k.

EvidenceBridge / generic agent safety product was already owner-subtracted. The new Amazon action-receipt spike may supply reusable engineering, but do not submit the same idea by momentum unless a named Open Agent track/user problem materially changes the product.

Disposition: **HOLD / REASSESS AT LIVE TRACK BRIEF.**

## 9. Apart AI lanes

### Collusion — 23–25 Oct
Lower prize, research-specific. No current exact project delta.

Disposition: **HOLD.**

### Epistemics — 13–15 Nov
ATRS route-to-target work remains the prepared lead.

Disposition: **PRESERVE SEPTEMBER METHOD; FRESH NOVEMBER CORPUS / RULES ONLY.**

## 10. OpenCV AI Competition — ELIGIBILITY CURRENTLY UNCERTAIN

Public current competition pages show an Oct 26 deadline and cash/special awards, including Agentic Vision.

However launch material describes an earlier proposal/selection phase. Late "join" availability does not establish that a new team can still enter the judged build phase.

Disposition: **DO NOT SPEND BUILD TOKENS UNTIL ELIGIBILITY IS ESTABLISHED THROUGH A legitimate route.**

## 11. AWS CDS Agentic AI Hackathon — NOT CURRENTLY EARNED

Current rules require AWS Partner Network / associated opportunity conditions.

No current project evidence establishes that eligibility.

Disposition: **STOP unless legitimate APN eligibility is independently established.**

## 12. Since AI — LARGE PRIZE / LARGE HUMAN LOAD

6–8 Nov, Turku, Finland; public materials advertise €50k cash and in-person participation.

Travel, application, attendance and time cost are consequential human gates.

Disposition: **NOT A DEFAULT TOKEN LANE.**

## Current competition sequence

~~~text
NOW:
1. Amazon Alexa+ spike -> code / tests / owner attack
2. Human-gated London applications -> Dwelly first, Stripe, No.10
3. 1 Oct -> Hack Apertus live rules / challenge
4. 15 Oct -> Open Agent track fit
5. 23 Oct -> Amazon submission only if candidate survives
6. 30 Oct -> Nebius only if a stack-native product is earned
7. Nov -> ATRS/Apart fresh run
~~~

## Privacy / personal schedule boundary

Any private-calendar availability checks used during live coordination are **not persisted in public COM**.

PUBLIC COMPETITION ROUTING != PUBLIC PERSONAL SCHEDULE.

## Authority

No registration, terms acceptance, organiser contact, travel commitment, account creation, credential use, spend or final submission is authorised merely by this scan.

Routine reversible source work and competition preparation may proceed.

~~~text
BUILD != REGISTERED
REGISTERED != ELIGIBLE
ELIGIBLE != SUBMITTED
SUBMITTED != AWARDED
PRIZE_AMOUNT != EXPECTED_VALUE
~~~


## 13. NVIDIA Claw Agent Challenge: London — STRONG UK REMOTE FIT / REGISTRATION GATE

Official:
- https://luma.com/claw-agent-challenge-london

Current public state:
- hosted by NVIDIA Developer Community;
- virtual / remote;
- open to people living in the United Kingdom;
- asks participants to build a **long-running claw agent**;
- no fixed in-person hackathon schedule/team requirement is stated publicly;
- 1st place: GTC Berlin pass + DGX Spark Founders Edition (~$4,000 stated value) + showcase opportunity at NVIDIA Build-a-Claw London;
- 2nd place: GTC Berlin pass + showcase opportunity.

The public page says full challenge details, submission requirements, inspiration and NVIDIA Build model resources are provided **after registration**.

This is a strong natural fit to:
- Campfire long-running agent / continuity work;
- explicit state/currentness;
- failure recovery;
- local-first / bounded actuation;
- source-vs-runtime distinction.

But do not infer the actual judged task before reading the registered brief.

Disposition:

```text
STRONG FIT
NO SPECULATIVE BUILD BEFORE BRIEF
REGISTRATION = HUMAN GATE
FULL RULES / SUBMISSION SHAPE = NOT YET SEEN
```

## 14. Poolside Research Hackathon — STOP / REGISTRATION CLOSED

Official:
- https://luma.com/poolsidehackathon

This would have been an unusually strong research fit:
- Laguna XS.2 model-level research;
- evaluation design / multi-agent / RL environments;
- judges prioritise generalisability, reproducibility and technical contribution;
- winner receives a DGX Spark.

Current public page now says **Registration Closed**.

Disposition:

```text
STRONG THEORETICAL FIT != CURRENTLY ENTERABLE
STOP
```

Do not contact the host merely to manufacture a late route.

## 15. Monad Metropolis — LARGE PRIZE / WRONG CURRENT DIRECTION

Public London builder page:
- six-week online-first Monad hackathon;
- $250,000 total prize pool;
- tracks include Trust / Identity / AI Infrastructure.

This is financially material, but the competition is fundamentally an onchain / Monad build.

No current project need requires Monad.

Disposition:

```text
LARGE PRIZE != EARNED STACK FIT
NO CRYPTO PIVOT FOR PRIZE
HOLD / NO BUILD
```

## 16. Galuxium Nexus V2 — LOW PRIORITY / COMMERCIAL-SHAPE DISTORTION

Public Devpost material:
- deadline 31 Oct;
- requires a public production-ready SaaS, operational MVP, business/monetisation architecture and demo video;
- public prize labels show ~$14.9k total value, but detailed top-tier language describes infrastructure grants / credits rather than direct liquid cash.

A truthful competition entry would require turning a current project into a monetised SaaS rather than solving an earned current gap.

Disposition:

```text
SAAS MONETISATION REQUIREMENT != CURRENT PROJECT NEED
ADVERTISED VALUE != LIQUID CASH
NO PRIZE-SHAPED PRODUCT PIVOT
STOP / LOW PRIORITY
```

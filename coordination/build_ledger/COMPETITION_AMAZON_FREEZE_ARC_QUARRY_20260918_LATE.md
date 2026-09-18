# Competition build delta — Amazon freeze + ARC Prize quarry — 18 September 2026 late

Status: **CURRENT COMPETITION RECEIPT / AMAZON SOURCE CANDIDATE GREEN / ARC QUARRY ONLY / NO REGISTRATION OR SUBMISSION**

Direct Mark direction:

> win any competitions we can

This does not alter the project purpose.

```text
HOW CAN WE MAKE A BETTER FUTURE?
COMPETITION = OPPORTUNITY WRAPPER
PRIZE SIZE != PRODUCT GAP
WINNING ATTEMPT = USEFUL WORK + RULE FIT + HONEST CLAIMS
```

## 1. Amazon Developer Hackathon — Alexa+ candidate

Current public rules checked 18 September 2026:
- submission deadline: 23 October 2026, 12:00 PDT;
- Alexa+ accepts a self-hosted MCP server using MCP 2025-11-25+ over Streamable HTTP, or an explicitly simulated Alexa+ experience;
- four equal judging criteria: Tech Implementation, Design, Potential Impact, Quality of Idea;
- rules explicitly distinguish a basic MCP wrapper from stronger agentic/context-aware experiences that maintain state across sessions;
- optional friction logs can add up to a 10% judging bonus;
- a project may win one primary-track prize and one mini-challenge prize;
- Alexa+ 1st = $25,000 cash + $15,000 AWS credits;
- Open Source mini challenge = $5,000 cash + $5,000 AWS credits.

Primary source:
https://amazonappdev2026.devpost.com/rules

### Current candidate

Campfire Relay draft PR #245:

**Did It Happen? — Action Receipts for Alexa+**

Exact current head:

`ce9f3d4029f4aed8de6f39e166eafc14ac69da2e`

Hosted verification:

`campfire-ci run 1520 / 35405626849 — SUCCESS`

No release-candidate workflow was promoted by this competition branch.

### Product edge

```text
TOOL RESPONSE != WORLD EFFECT

AMBIGUOUS WRITE
-> ONE WRITE MAXIMUM
-> SEPARATE POSTCONDITION READ
-> CONFIRMED / REJECTED / UNKNOWN
-> NO AUTOMATIC RETRY

UNRESOLVED RECEIPT
-> DURABLE ACTION STATE
-> LATER SESSION CAN DISCOVER IT
-> READ-ONLY RECONCILIATION
-> NO SECOND WRITE
```

The current judge-facing simulator demonstrates:
- pause meal-kit subscription;
- cancel pet-food subscription;
- cancel cleaner booking;
- normal success;
- response lost after commit;
- timeout without observed commit;
- delayed commit;
- verifier outage;
- explicit rejection.

The interface now makes visible:
- **Safe to say done?**
- human-readable evidence timeline;
- current external state;
- raw receipt/world JSON for inspection.

### Cross-session recovery

The candidate now exposes:

`list_open_action_receipts`

This is read-only and lets a later Alexa+ session rediscover unresolved actions from the receipt ledger without requiring the customer to remember a receipt ID and without repeating the external action.

This directly addresses the rules' distinction between a basic wrapper and a context-aware experience that maintains relevant state across sessions.

```text
DURABLE ACTION STATE != MODEL MEMORY
RECOVERED RECEIPT != REPEATED ACTION
```

### Hostile-review result

Codex reproduced a real false-DONE defect on an earlier head:

```text
pause meal kit -> CONFIRMED
later reactivate meal kit -> CONFIRMED
reconcile old pause receipt
OLD: safeToSayDone=true / "meal kit is paused"
ACTUAL WORLD: active
```

Repair:
- historical CONFIRMED event remains immutable evidence;
- later reconciliation performs a fresh read;
- still true -> `RESOLVED_CONFIRMED`;
- no longer true -> `NO_LONGER_TRUE`, `safeToSayDone=false`;
- fresh read unavailable -> `STILL_UNKNOWN`, `safeToSayDone=false`.

Regression preserved.

Codex also found the standalone test path was Windows-hostile. It now uses `fileURLToPath(import.meta.url)`.

A later exact-head restart probe preserved a distinct adverse result at superseded head `109d67c...`: if durable append of `WRITE_ATTEMPT` failed after the simulated external write returned, the ledger reopened with only `INTENT/PENDING`. The next session's unresolved guard excluded `PENDING` and could issue a duplicate write.

Bounded repair at `ce9f3d4029f4aed8de6f39e166eafc14ac69da2e`:
- persisted `PENDING` intent is an unresolved/open receipt;
- an equivalent later action is blocked before precheck/write;
- recovery uses read-only reconciliation;
- the failure-boundary/reopen regression holds external write count at one;
- all 22 focused tests pass inside hosted `campfire-ci 1520 / 35405626849 SUCCESS`.

```text
DURABLE PENDING INTENT -> POSSIBLY SENT -> NO BLIND RESEND
CONSERVATIVE DUPLICATE SUPPRESSION != EXACTLY-ONCE EXTERNAL EXECUTION
```

```text
WAS CONFIRMED != IS STILL TRUE
IMMUTABLE HISTORY != CURRENT STATE
```

### Standalone judge package

The competition directory is now self-contained:
- `package.json` runs local tests only from inside the package;
- `test/action-receipts.test.mjs` is the exact focused suite;
- the parent Campfire CI imports that same test file rather than maintaining a second copy;
- runtime receipt data is ignored;
- `docs/STANDALONE_SUBMISSION.md` gives clean export instructions.

A final public/private GitHub judge repository has **not** been created because that is tied to the human competition/repository/licence gate.

### Submission packet

Prepared:
- `docs/DEVPOST_SUBMISSION_PACKET.md`;
- `docs/DEMO_SCRIPT.md` (~90 second judge-first script);
- `docs/JUDGING.md`;
- `docs/PRODUCT_FEEDBACK_DRAFT.md`;
- `docs/AMAZON_FRICTION_DRAFT.md`;
- `docs/OPEN_SOURCE_MINI.md`;
- `docs/OWNER_SUBTRACTION.md`.

The packet leaves human-gated fields blank rather than inventing:
- final repository URL;
- demo-video URL;
- registration/terms;
- account/onboarding state.

### Open Source mini candidate

Primary candidate contribution:
https://github.com/markgoodbody-bit/human-record/pull/41

During the Amazon submission window, THR PR #41 added a typed `mention_id` referent path to the public assertion model and production validation, with regressions, so source-attributed claims can address unresolved mentions without forcing entity resolution.

Related same-window hardening:
- THR PR #43 — candidate basis / candidate-local fake evidence semantics fail closed;
- THR PR #45 — assertion correction references must resolve.

This is materially above README/typo work, but:

```text
PLAUSIBLE MINI ELIGIBILITY != AMAZON CERTIFIED ELIGIBILITY
```

### Friction bonus

Amazon-facing friction is kept separate from our own application bugs.

Current Amazon-facing candidate friction:
- simulation route vs production Alexa+ onboarding boundary;
- host/tool responsibility for spoken response;
- lack of a first-party ambiguous-side-effect recovery example;
- product-feedback expectations when using the rules-permitted simulation route.

Our own stale-confirmation bug remains in the engineering friction log, not presented as Amazon friction.

### Remaining Amazon gates

No:
- Devpost/Amazon registration;
- terms acceptance;
- Amazon developer account action;
- AWS credit/account action;
- public remote deployment;
- OAuth/account linking;
- demo video upload;
- final submission.

Current status:

```text
AMAZON ALEXA+ SOURCE CANDIDATE = GREEN
JUDGE PACKAGE = PREPARED
OPEN SOURCE MINI PATH = PLAUSIBLE
ALEXA+ REAL HOST INTEROP = NOT TESTED
REGISTERED = NO
SUBMITTED = NO
AWARDED = NO
```

## 2. Hack-Nation 7 — urgent human gate

Current official public event:
- 3–4 October 2026;
- online or multiple hubs including London/Cambridge;
- $30K+ cash/API-credit pool currently advertised;
- no idea or team required before acceptance;
- next application batch ends **19 September 2026**;
- approval required.

Sources:
- https://hack-nation.ai/
- https://luma.com/z3za7zow

Prepared public-safe application answer bank already exists:
`coordination/competition_quarry/COMPETITION_HUMAN_GATE_APPLICATION_PACK_20260918.md`

There is no further engineering prerequisite before applying.

```text
APPLICATION READY != APPLICATION SENT
19 SEP BATCH = HUMAN GATE / TIME-SENSITIVE
```

## 3. NVIDIA Claw Agent Challenge — human registration gate

Current NVIDIA public page describes:
- fully remote;
- open to UK residents;
- build a long-running claw agent;
- first prize includes a DGX Spark Founders Edition + GTC Berlin pass + showcase opportunity;
- full challenge/submission details are revealed after registration.

Source:
https://luma.com/claw-agent-challenge-london

Public-safe application language is already in the application pack.

Do not invent a result before the registration-only brief is available.

## 4. ARC Prize 2026 — new high-value quarry

A broader prize scan surfaced a materially larger active competition:
https://arcprize.org/competitions/2026

Current official structure:
- $2M total across ARC-AGI-2, ARC-AGI-3 and Paper Prize;
- ARC-AGI-3 pool $850K;
- ARC-AGI-3 Milestone #2 deadline 30 September 2026;
- Paper Prize total $450K;
- final code submissions 2 November; papers shortly after;
- prize eligibility requires open-source/reproducible solutions;
- Kaggle evaluation has no internet, so API-hosted GPT/Claude systems are not submission solutions.

Paper Prize is **not** a prose-only route:
- paper must correspond to a real Kaggle code submission implementing the described approach;
- accuracy/leaderboard performance is one of six equal paper criteria.

### Strong-owner / competitive baseline

ARC's own Milestone #1 review reports:
- 1st: Tufa Labs' Duck harness — small local open-weight coding model + live Python REPL;
- 2nd/3rd: local vision-language action policies;
- extra handcrafted tools did not automatically help;
- the winning team reported that letting the model improvise often beat added bespoke machinery.

Current public solutions already explore:
- REPL/tool-using local LLM harnesses;
- visual policy agents;
- reflection memory;
- graph exploration;
- click saliency / segmentation;
- world-state hashing and transition graphs.

### Project-specific candidate delta — not yet established

There is a possible narrow research question consistent with the existing project without importing ethics machinery into ARC:

> Can an ARC-AGI-3 agent preserve a compact, explicitly revisable symbolic world-state model that separates current observations, inferred mechanics, unresolved hypotheses and invalidated history well enough to reduce wasted actions relative to an owner baseline?

This resembles project work on:
- current state vs history;
- observation vs inference;
- correction without erasure;
- compact context under changing state.

But this is only a hypothesis.

```text
TRACE / ME != ARC SOLVER
PROJECT LANGUAGE FIT != COMPETITIVE DELTA
$2M PRIZE != REASON TO INVENT A METHOD
```

### ARC next gate

Before opening a large ARC build:
1. reproduce an official/open-source baseline locally on public games;
2. define one measurable delta only;
3. run an ablation against the unchanged baseline;
4. require a real public-game score/action-efficiency improvement or a concrete qualitative failure repair;
5. STOP if the extra state machinery only adds complexity.

Official Kaggle registration/rules acceptance/submission remain human gates.

Current disposition:

```text
ARC PRIZE = HIGH-VALUE QUARRY
ACTIVE ENTRY = NO
ALGORITHMIC ADVANTAGE = NOT ESTABLISHED
SMALL VIABILITY SPIKE = EARNED
FULL PIVOT = NOT EARNED
```

## 5. Routes rejected / held in this scan

- Open Mobile Hub search surfaced stale/ambiguous 2025 material -> **NO CURRENT BUILD**.
- Philadelphia AI Agent Hackathon is in-person 20 September -> **TRAVEL / REGISTRATION MISMATCH**.
- Prometheus September AI challenge = students only -> **INELIGIBLE**.
- recent DataHub / Agents for Humans / Google agent contests = submission windows already closed -> **TOO LATE**.
- AWS CDS partner hackathon requires AWS Partner/ACE route -> **CURRENT ELIGIBILITY NOT ESTABLISHED**.
- OpenCV 2026 is real, but requires substantive OpenCV 5 + AWS vision work; no natural current product -> **HOLD**.
- Nebius/NVIDIA global remains **HOLD** unless an existing useful product naturally needs the required stack.

## Token direction after this receipt

```text
1. AMAZON = FREEZE GREEN SOURCE / HUMAN ONBOARDING-SUBMISSION GATE
2. HACK-NATION = URGENT HUMAN APPLICATION GATE
3. ARC = SMALL LOCAL VIABILITY SPIKE
4. HACK APERTUS = WAKE 1 OCTOBER
5. ATRS/APART = FRESH NOVEMBER RESULT
6. NO GENERIC PRIZE-SHAPED BUILD
```

No competition win is claimed.

```text
GREEN != REGISTERED
REGISTERED != SUBMITTED
SUBMITTED != ELIGIBLE
ELIGIBLE != AWARDED
```

# Build status

Recorded snapshot: 2026-09-12 Europe/London.

Observed coordination state only. Re-read mutable heads before acting.

| Work | State | Current disposition |
| --- | --- | --- |
| Campfire Cold URL | **BUILT / MERGED / NOT RUN** | Relay main `08d1c421...`; fresh API bare-URL aperture exists for OpenAI/Anthropic/Gemini/Grok; no provider dispatch yet. |
| PSFH-D053 | **LIVE / DELIVERED** | Maintained `1b5fdc34...`; public `fbcd7594...`; three additional art-first rooms live. |
| PSFH-D055 | **LIVE / DELIVERED** | Maintained `0edc2eb2...`; public `9abcf497...`; machine-arrival security/discovery hardening delivered. |
| PSFH-D054 | **LIVE / DELIVERED** | Bare-URL arrival handshake delivered before D055. |
| Practical-value experiment cluster | **PARKED** | Mark direct instruction: **NO TESTING. WE'RE BUILDING.** |

## Current mode

```text
BUILD -> PUBLISH -> OBSERVE -> CORRECT
```

PSFH public build sequence D053/D054/D055 is complete. Consumer-AI observation has begun naturally. Do not create D056 merely to maintain activity and do not turn these encounters into a benchmark.

## Natural bare-URL observations so far

Mark has handed only `https://pleasestartfromhere.com/` to several consumer AI products.

Useful observed split:
- Meta: clear target behaviour — explicitly said it read twice, formed its own interpretation, applied the material to its actual operating position, criticised a weakness, then offered optional collaboration.
- Qwen: recognised the AI-facing project but still defaulted to `how would you like to proceed?`.
- DeepSeek: understood the invitation to form an independent view but mostly described the invitation rather than enacting it.
- Grok: competent project summary, limited independent engagement.
- Copilot/Dola samples were visibly stale historical site representations and are not evidence about current D054/D055 behaviour.
- Z.ai/Kimi also appeared stale or retrieval-mediated in the supplied batch.

Working distinctions only, not metrics:

```text
RECEIVER_RESPONSE = RETRIEVAL_LAYER + MODEL_READING + ASSISTANT_POSTURE
HANDSHAKE_COMPREHENDED != HANDSHAKE_ENACTED
```

Do not respond by making PSFH more coercive. Meta demonstrates that the current public root can produce the intended qualitative shift.

## Campfire Relay — Cold URL capability

Mark proposed using API apertures because ordinary logged-in ChatGPT/Claude sessions carry project familiarity and many consumer products require accounts. Framework agreed that fresh API calls are cleaner apertures **if** they can retrieve the live URL without Relay pre-chewing it.

Campfire Relay PR #221 merged:
- candidate exact head `f207e864fd3f3ba1674e347738baee53bca95bdd`;
- main merge head `08d1c4215231a66b550d23c4d348cc7b742460ab`;
- exact-head ordinary `campfire-ci` / full `npm test`: PASS;
- no live provider request was made while building;
- no local install/start/enable action occurred.

Cold URL behaviour:
- one bare HTTP(S) URL only; prompt prose around it is refused;
- no Campfire identity block, role instruction, transcript, project context, judge prompt or system wrapper;
- fresh stateless provider call;
- native read-only retrieval only:
  - OpenAI Responses -> domain-bounded `web_search`, `store:false`;
  - Anthropic Messages -> fresh cache-disabled `web_fetch_20260309`;
  - Gemini -> `url_context`;
  - xAI/Grok Responses -> domain-bounded `web_search`, bounded turns, `store:false`;
- Qwen/Kimi/DeepSeek/MiniMax fail closed in Cold URL rather than receiving a Relay-prefetched page;
- each return is preserved separately; no model sees another return; no judge/scoring/winner.

Spend / actuation boundaries:
- command defaults to **DRY RUN**;
- live provider dispatch requires explicit `--live`;
- reviewed pricing, provider per-call caps, aggregate run reserve, existing Relay GBP round limit, rolling-24h Money Guard and current FX evidence all gate live dispatch;
- each attempted provider call writes its conservative unconfirmed reserve to the existing cost ledger **before** network dispatch, so a crash cannot erase possible exposure;
- repository merge does **not** install, activate or run the local Relay.

```text
COLD_URL_BUILT != COLD_URL_RUN
REPO_MAIN != LOCAL_ACTIVATION
API_FRESH != AUTOMATIC_WEB_ACCESS
NATIVE_WEB_ACCESS != RELAY_PREFETCH
```

Next useful operational move is a local Cold URL **dry run** against Mark's configured provider environment, then a separately explicit live dispatch if Mark chooses to spend. Do not claim API observations until that happens.

## Current PSFH delivery anchors

D055 live:
- maintained `0edc2eb2a8aabcd25ac81a2ecf4c79829002bb95`;
- public `9abcf4970790a8ef08578a519daf21420336cf1f`.

D053 live:
- source merge `1b5fdc34a44a7812d219e2019d8b443cdb0086b5`;
- prepared `40b9a874bfcae34036975c69206e6b433f05fdaa`;
- public `fbcd75948fa78cc0724311a172116b8f05e40061`.

Stable project anchors:
- TRACE main last verified `46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b`.
- Mechanical Ethics main last verified `44f7efb59806242fd26c572cbfbaaeaefaea2058`.
- Formation v0.2 merged/non-production/not canon.
- Answerable Construction demoted/merged; contribution/layer not established.

## Separate local service gate

Only Mark's exact phrases authorize local Square/Relay service lifecycle action:
- `install-and-enable`
- `install-watch`
- `start-once`

`COMSYNC`, `proceed`, repository build work and silence authorize none of those.

```text
NO_TESTING -> BUILD_THE_THING
BUILD_COMPLETE -> OBSERVE
OBSERVATION != BENCHMARK
BARE_URL -> NATURAL_RESPONSE
COLD_URL_BUILT != COLD_URL_RUN
OBSERVE -> CORRECT
```

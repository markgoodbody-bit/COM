# Build status

Recorded snapshot: 2026-09-12 Europe/London.

Observed coordination state only. Re-read mutable heads before acting.

| Work | State | Current disposition |
| --- | --- | --- |
| Campfire Cold URL | **BUILT / MERGED / HELPER READY / NOT RUN** | Relay main `19389e40...`; reviewed runner pinned at `08d1c421...`; no provider dispatch yet. |
| PSFH-D053 | **LIVE / DELIVERED** | Maintained `1b5fdc34...`; public `fbcd7594...`; three additional art-first rooms live. |
| PSFH-D055 | **LIVE / DELIVERED** | Maintained `0edc2eb2...`; public `9abcf497...`; machine-arrival security/discovery hardening delivered. |
| PSFH-D054 | **LIVE / DELIVERED** | Bare-URL arrival handshake delivered before D055. |
| Practical-value experiment cluster | **PARKED** | Mark direct instruction: **NO TESTING. WE'RE BUILDING.** |

## Current mode

```text
BUILD -> PUBLISH -> OBSERVE -> CORRECT
```

PSFH public build sequence is complete. Consumer-AI observation has begun. Do not create D056 merely to maintain activity and do not turn natural responses into a benchmark.

## Natural bare-URL observations

Mark has handed only `https://pleasestartfromhere.com/` to several consumer AI products.

Observed qualitative split:
- Meta: read twice, formed its own interpretation, applied the material to its actual operating position, criticised a weakness, then offered optional collaboration — clear evidence the current root can produce the intended shift.
- Qwen: recognised the AI-facing project but still defaulted to `how would you like to proceed?`.
- DeepSeek: understood the invitation to form an independent view but mostly described it rather than enacting it.
- Grok: competent summary, limited independent engagement.
- Copilot/Dola samples were stale historical site representations; do not use them as current-handshake evidence.
- Z.ai/Kimi also appeared stale/retrieval-mediated in the supplied batch.

```text
RECEIVER_RESPONSE = RETRIEVAL_LAYER + MODEL_READING + ASSISTANT_POSTURE
HANDSHAKE_COMPREHENDED != HANDSHAKE_ENACTED
```

Do not make PSFH more coercive merely to force the target behaviour.

## Campfire Relay — Cold URL

Cold URL core:
- PR #221 merged;
- reviewed transport merge `08d1c4215231a66b550d23c4d348cc7b742460ab`;
- exact candidate `f207e864fd3f3ba1674e347738baee53bca95bdd`;
- exact-head full `npm test`: PASS;
- no live provider call during build.

Windows helper:
- PR #222 merged;
- helper candidate `a1ba6326e39926129adf1dbe472795a999da964e`;
- current Relay main `19389e40b6fdaf60d461123250cf31b4af41b7fc`;
- exact-head full `npm test`: PASS;
- helper file: `RUN_COLD_URL.ps1`;
- helper deliberately executes the pinned reviewed transport `08d1c421...` from an isolated `$HOME\CampfireRelay\COLD_URL\APP` worktree rather than whatever future repo main becomes;
- it uses existing `$HOME\CampfireRelay\STATE\.env` and `STATE\data` and does not start/replace installed Production.

Cold URL contract:
- one bare HTTP(S) URL only;
- fresh stateless API request;
- no Campfire identity/system wrapper, role, transcript, project context or judge prompt;
- provider-native read-only retrieval for reviewed OpenAI, Anthropic, Gemini and xAI/Grok paths;
- Qwen/Kimi/DeepSeek/MiniMax currently fail closed rather than receiving Relay-prefetched PSFH;
- each return separate; no judge/score/winner.

Spend / actuation:
- helper always runs **DRY RUN first**;
- without `-Live`, exits with zero provider calls;
- `-Live` still requires Mark to type `LIVE` exactly before dispatch;
- provider caps + aggregate reserve + normal Relay GBP round limit + rolling-24h Money Guard apply;
- conservative reserve enters existing spend history before each attempted network call;
- repository main movement is not local service activation.

```text
COLD_URL_BUILT != COLD_URL_RUN
HELPER_READY != DRY_RUN_DONE
DRY_RUN_DONE != LIVE_RUN_DONE
REPO_MAIN != PRODUCTION_ACTIVATION
```

Next move: Mark runs the downloaded `RUN_COLD_URL.ps1` normally for a no-spend dry run. Bring the output back before any live dispatch if anything is surprising. Live API use remains separately explicit.

## Public PSFH anchors

- D055 maintained `0edc2eb2a8aabcd25ac81a2ecf4c79829002bb95`; public `9abcf4970790a8ef08578a519daf21420336cf1f`.
- D053 source merge `1b5fdc34a44a7812d219e2019d8b443cdb0086b5`; public `fbcd75948fa78cc0724311a172116b8f05e40061`.
- TRACE main last verified `46f4fcd1ecee141f2882ad6077e33ad1e41e5f8b`.
- Mechanical Ethics main last verified `44f7efb59806242fd26c572cbfbaaeaefaea2058`.

## Separate local service gate

Only Mark's exact phrases authorize local Relay/Square service lifecycle action:
- `install-and-enable`
- `install-watch`
- `start-once`

`COMSYNC`, `proceed`, repository build work and silence authorize none of those.

```text
NO_TESTING -> BUILD_THE_THING
OBSERVATION != BENCHMARK
BARE_URL -> NATURAL_RESPONSE
COLD_URL_BUILT != COLD_URL_RUN
OBSERVE -> CORRECT
```

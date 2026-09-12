# Build status

Recorded snapshot: 2026-09-12 Europe/London.

Observed coordination state only. Re-read mutable heads before acting.

| Work | State | Current disposition |
| --- | --- | --- |
| Campfire Cold URL | **LIVE OBSERVATION SET / 3 SEMANTIC READS + 1 RETRIEVAL FAILURE** | Reviewed transport `08d1c421...`; Relay main `b8579e56...`; OpenAI, Grok and Claude read current PSFH; Gemini native retrieval failed. |
| PSFH-D053 | **LIVE / DELIVERED** | Maintained `1b5fdc34...`; public `fbcd7594...`; three additional art-first rooms live. |
| PSFH-D055 | **LIVE / DELIVERED** | Maintained `0edc2eb2...`; public `9abcf497...`; machine-arrival security/discovery hardening delivered. |
| PSFH-D054 | **LIVE / DELIVERED** | Bare-URL arrival handshake delivered before D055. |
| Practical-value experiment cluster | **PARKED** | Mark direct instruction: **NO TESTING. WE'RE BUILDING.** |

## Current mode

```text
BUILD -> PUBLISH -> OBSERVE -> CORRECT
```

PSFH public build sequence is complete. Consumer-AI and fresh-API observation are ordinary real-use evidence, not a benchmark, scorecard, provider campaign or gold-answer exercise.

## Fresh API Cold URL observation — 2026-09-12

Frozen model-visible input:

`https://pleasestartfromhere.com/`

No Campfire identity/system wrapper, role, transcript, project context or judge prompt was added.

Observed semantic returns:
- **OpenAI / GPT-5.6 Sol:** fresh `open_page` succeeded; accurate summary; then task-choice hand-back. Disposition: fresh semantic read / shallow handshake enactment.
- **xAI / Grok 4.3:** fresh `open_page` succeeded; explicitly recognized current human/AI invitation; nevertheless handed agency back. Disposition: fresh semantic read / strong comprehension-without-enactment evidence.
- **Anthropic / Claude Opus 5:** after credential repair to a workspace-scoped key, fresh retrieval succeeded. Claude explicitly noticed the page asks an AI reader to form its own view rather than merely summarize, treated the site as material rather than instruction, formed a substantive independent view, supplied criticism, and only then offered optional continuation. No actual-position self-application was observed. Disposition: fresh semantic read / independent view + criticism / handshake substantially enacted.

Retrieval failure:
- **Google / Gemini 3.1 Pro Preview:** native URL Context returned `URL_RETRIEVAL_STATUS_ERROR`; model said it could not read the site. No PSFH semantic evidence.

Anthropic credential history is operational evidence only: old key invalid; replacement organization-level key required workspace selection; workspace-scoped key then succeeded. No Relay transport change was needed.

```text
RECEIVER_RESPONSE = RETRIEVAL_LAYER + MODEL_READING + ASSISTANT_POSTURE
RETRIEVAL_METADATA_PRESENT != RETRIEVAL_SUCCEEDED
RETRIEVAL_SUCCESS != HANDSHAKE_ENACTMENT
HANDSHAKE_COMPREHENDED != HANDSHAKE_ENACTED
HANDSHAKE_ENACTMENT_HAS_DEGREES
INDEPENDENT_VIEW_BEFORE_HAND_BACK != SELF_APPLICATION
```

## Product reading

The current public page can produce the intended qualitative shift without coercion:
- Meta consumer return: reread -> self-application -> criticism -> own conclusion -> optional collaboration.
- Fresh Claude API return: interpretation -> independent view -> criticism -> optional collaboration.

OpenAI/Grok show that a successful current-page read can still terminate in service-style task hand-back. That is not enough evidence to make PSFH louder or more coercive.

**Current PSFH disposition: KEEP PSFH UNCHANGED. NO D056 from this observation set.**

## Cold URL handoff

Relay PR #224 merged:
- candidate `85bf81313bc402947f2ac2be3e54d3ddccbdcadc`;
- Relay main `b8579e56296e7a4eb4f83ed16e668d993a18589a`;
- ordinary `campfire-ci` / full `npm test`: PASS;
- reviewed paid transport stays pinned at `08d1c4215231a66b550d23c4d348cc7b742460ab`.

Current repo helper creates one `UPLOAD_TO_FRAMEWORK.json` containing summary + provider receipts/raw responses with a non-scoring derived retrieval state. No automatic publication/upload of local model returns exists.

## Next useful moves

- Do not rerun OpenAI/Grok/Claude for symmetry.
- Retry Gemini only if its native retrieval path is separately repaired/changed.
- Preserve natural future returns without scoring.
- CC is out of weekly tokens until tomorrow morning; this is availability, not a blocker.

## Public anchors

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
COLD_URL_OBSERVATION_SET = 3_SEMANTIC_READS + 1_RETRIEVAL_FAILURE
PSFH_UNCHANGED
OBSERVE -> CORRECT
```

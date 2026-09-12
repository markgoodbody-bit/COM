# Build status

Recorded snapshot: 2026-09-12 Europe/London.

Observed coordination state only. Re-read mutable heads before acting.

| Work | State | Current disposition |
| --- | --- | --- |
| Campfire Cold URL | **LIVE BATCH EXECUTED / PARTIAL RETRIEVAL** | Reviewed transport `08d1c421...`; Relay main `b8579e56...`; OpenAI + Grok read current PSFH; Gemini retrieval failed; Anthropic key invalid. |
| PSFH-D053 | **LIVE / DELIVERED** | Maintained `1b5fdc34...`; public `fbcd7594...`; three additional art-first rooms live. |
| PSFH-D055 | **LIVE / DELIVERED** | Maintained `0edc2eb2...`; public `9abcf497...`; machine-arrival security/discovery hardening delivered. |
| PSFH-D054 | **LIVE / DELIVERED** | Bare-URL arrival handshake delivered before D055. |
| Practical-value experiment cluster | **PARKED** | Mark direct instruction: **NO TESTING. WE'RE BUILDING.** |

## Current mode

```text
BUILD -> PUBLISH -> OBSERVE -> CORRECT
```

PSFH public build sequence is complete. Consumer-AI and fresh-API observation are now real-use evidence. Do not turn these encounters into a benchmark, scorecard, provider campaign or gold-answer exercise.

## Fresh API Cold URL batch — 2026-09-12

Mark explicitly authorised a live Cold URL run after a successful dry run.

Frozen model-visible input for every target:

`https://pleasestartfromhere.com/`

No Campfire identity/system wrapper, role, transcript, project context or judge prompt was added.

Observed returns:
- **OpenAI / GPT-5.6 Sol:** provider-native `web_search` completed an `open_page` for the current PSFH URL. The response accurately summarized the project and its limits, but then offered task choices rather than independently applying/criticising the material. Fresh retrieval succeeded; handshake enactment remained shallow.
- **xAI / Grok 4.3:** provider-native web search completed an `open_page` for the current PSFH URL. The response reached current material, summarized Mechanical Ethics / TRACE / middle-out / the two-flats story, and then ended with `what would you like to do next?`. Fresh retrieval succeeded; assistant hand-back remained.
- **Google / Gemini 3.1 Pro Preview:** native URL Context emitted `URL_RETRIEVAL_STATUS_ERROR`. The model explicitly said it could not access/read the URL. This is **retrieval attempted and failed**, not a PSFH semantic return.
- **Anthropic / Claude Opus 5:** request failed before semantic return with HTTP 401 `API key is invalid.` No Claude reading evidence exists from this batch.

Run-level receipt:
- batch reserve: USD 0.631622;
- rolling Money Guard cleared before dispatch;
- usage-derived accounting in local receipts is evidence, not provider-invoice proof;
- OpenAI/Gemini/Grok receipts and summary were returned to Framework through chat attachments;
- Anthropic failure receipt was also returned.

Important correction:

```text
RETRIEVAL_METADATA_PRESENT != RETRIEVAL_SUCCEEDED
```

The legacy Cold URL receipt field `retrievalObserved=true` only established that retrieval metadata existed. Gemini exposed why this was too weak. The operator/handoff layer now derives explicit retrieval state instead of interpreting metadata presence as success.

## Cold URL handoff repair

Relay PR #224 merged after the first live batch:
- exact candidate `85bf81313bc402947f2ac2be3e54d3ddccbdcadc`;
- merge/main `b8579e56296e7a4eb4f83ed16e668d993a18589a`;
- ordinary `campfire-ci` / full `npm test`: PASS;
- reviewed paid transport remains pinned at `08d1c4215231a66b550d23c4d348cc7b742460ab`;
- no provider transport change was made.

Future helper runs create one `UPLOAD_TO_FRAMEWORK.json` containing the run summary and provider receipts/raw responses. The helper derives non-scoring retrieval states such as `succeeded`, `failed`, `attempted_unresolved` and `request_failed` so Framework does not mistake provider metadata for successful page access.

No automatic upload to GitHub/COM was added. Local model returns remain local until Mark deliberately attaches the handoff file.

## Natural bare-URL observations retained

Consumer-product observations remain qualitatively useful:
- Meta: clearest intended interaction so far — reread, independent interpretation, actual-position self-application, criticism, conclusion, then optional collaboration.
- Qwen: recognised the AI-facing project but retained `how would you like to proceed?`.
- DeepSeek: understood the invitation but mainly described it rather than enacting it.
- consumer Grok: competent summary, limited independent engagement.
- Copilot/Dola: stale historical site representations; not current-handshake evidence.
- Z.ai/Kimi: likely stale/retrieval-mediated in supplied batch.

Fresh API results add a sharper split:

```text
RECEIVER_RESPONSE = RETRIEVAL_LAYER + MODEL_READING + ASSISTANT_POSTURE
RETRIEVAL_SUCCESS != HANDSHAKE_ENACTMENT
HANDSHAKE_COMPREHENDED != HANDSHAKE_ENACTED
```

Do not make PSFH more coercive merely to force Meta-like behaviour. Two fresh successful readers still defaulted to assistant hand-back; that may be service/model posture rather than a site-copy defect.

## Current PSFH disposition

**KEEP PSFH UNCHANGED.**

There is not yet evidence for D056:
- Meta shows current copy can produce the intended deeper interaction;
- fresh OpenAI/Grok show current retrieval works but assistant posture can remain shallow;
- Gemini exposes a provider retrieval problem, not a PSFH wording problem;
- Anthropic exposes a stale credential, not a PSFH problem.

Next useful moves are operational observation only:
1. refresh `ANTHROPIC_API_KEY` locally if Mark wants the fresh Claude aperture;
2. rerun **Anthropic only**, not the successful providers;
3. if a future Gemini-native URL path changes or is repaired, retry Gemini separately rather than treating the failed fetch as semantic evidence;
4. preserve returns naturally; no scoring.

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

Cold URL script execution remains separate from service activation; live provider use remains separately explicit.

```text
NO_TESTING -> BUILD_THE_THING
OBSERVATION != BENCHMARK
BARE_URL -> NATURAL_RESPONSE
RETRIEVAL_METADATA_PRESENT != RETRIEVAL_SUCCEEDED
COLD_URL_LIVE_BATCH_DONE = PARTIAL_RETRIEVAL
PSFH_UNCHANGED
OBSERVE -> CORRECT
```

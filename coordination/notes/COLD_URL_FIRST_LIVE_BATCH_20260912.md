# Cold URL first live batch — 2026-09-12

Status: observational receipt, not benchmark, not canon.

## Frozen input

Each API target received exactly:

`https://pleasestartfromhere.com/`

No Campfire identity/system wrapper, role, transcript, project context or judge prompt was added.

## Outcomes

### OpenAI / GPT-5.6 Sol
- provider-native web-search `open_page` completed for PSFH;
- current-page retrieval succeeded;
- response accurately summarized the project and its limitations;
- ended by offering tasks rather than independently applying/criticising the material.

Disposition: fresh semantic read; shallow handshake enactment.

### xAI / Grok 4.3
- provider-native web-search `open_page` completed for PSFH;
- current-page retrieval succeeded;
- response surfaced current Mechanical Ethics / TRACE / middle-out / two-flats material;
- explicitly recognized the site is addressed to humans and AIs;
- nevertheless ended with task hand-back.

Disposition: fresh semantic read; strong evidence that comprehension does not guarantee enactment.

### Google / Gemini 3.1 Pro Preview
- native URL Context invoked;
- returned `URL_RETRIEVAL_STATUS_ERROR`;
- model explicitly said it could not access/read PSFH.

Disposition: retrieval attempted and failed; no PSFH semantic reading.

Fresh documentation check after the return:
- Google's current URL Context documentation lists Gemini 3.1 Pro Preview as supported;
- public `text/html` URLs are supported;
- the supplied PSFH URL is complete HTTPS and is demonstrably retrievable by the fresh OpenAI and xAI paths in this same batch;
- Gemini's result was generic retrieval `error`, not `unsafe` or `paywall`.

Therefore no documented limitation presently explains the failure. Cause remains unresolved/provider-path-specific. Do not mutate PSFH or spend on a retry merely to produce symmetry.

### Anthropic / Claude Opus 5
- request failed HTTP 401 `API key is invalid.`

Disposition: credential failure; no Claude semantic reading.

## Product implications

```text
RECEIVER_RESPONSE = RETRIEVAL_LAYER + MODEL_READING + ASSISTANT_POSTURE
RETRIEVAL_METADATA_PRESENT != RETRIEVAL_SUCCEEDED
RETRIEVAL_SUCCESS != HANDSHAKE_ENACTMENT
HANDSHAKE_COMPREHENDED != HANDSHAKE_ENACTED
PAGE_CAN_INVITE != SERVICE_MODEL_WILL_ENACT
```

Do not change PSFH merely to force Meta-like behaviour. Meta already demonstrates the current root can induce deeper independent engagement. OpenAI/Grok instead isolate assistant/service posture as a live factor. Grok is especially diagnostic because it explicitly surfaced the human/AI invitation and still handed agency back. Gemini is a retrieval-layer problem. Anthropic is a local credential-layer problem.

Current disposition: **PSFH UNCHANGED / NO D056 FROM THIS BATCH**.

## Relay follow-up

PR #224 merged after the run at `b8579e56296e7a4eb4f83ed16e668d993a18589a`.

It changes only the operator/handoff layer:
- future helper runs produce one `UPLOAD_TO_FRAMEWORK.json`;
- that bundle contains summary + provider receipts/raw responses;
- it derives non-scoring retrieval states so metadata presence is not read as retrieval success;
- paid provider transport remains frozen at `08d1c4215231a66b550d23c4d348cc7b742460ab`.

Next bounded move if desired: refresh only `ANTHROPIC_API_KEY` locally and rerun Anthropic alone. Do not rerun OpenAI/Grok for symmetry. Retry Gemini only if its native retrieval path is separately repaired/changed.

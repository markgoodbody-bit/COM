# NVIDIA API trial authorised — EvidenceWatch live-probe gate — 19 September 2026

Status: **HUMAN TERMS GATE CROSSED / LOCAL CREDENTIAL CREATION NEXT / ONE PROTOTYPE CALL AUTHORISED**

Direct Mark authorization:
`Proceed with NVIDIA API trial`

Scope of authorization:
- use NVIDIA Build/API trial service for the NVIDIA Claw competition prototype;
- generate/use a legitimate NVIDIA Build API key;
- run bounded prototype/testing calls;
- first call is the fixed EvidenceWatch probe.

Not granted:
- production use;
- paid subscription/spend;
- private, confidential, personal or sensitive-data submission;
- credential publication/storage in GitHub/COM/chat;
- broader provider commitment unrelated to this prototype.

Current NVIDIA owner routes rechecked:
- API key management: https://build.nvidia.com/settings/api-keys
- Nemotron 3 Super prototype/model page exposes **Generate API Key**;
- hosted OpenAI-compatible base: https://integrate.api.nvidia.com/v1
- selected model: `nvidia/nemotron-3-super-120b-a12b`.

Current source core before this gate:
- Relay draft PR #248;
- source-freeze head `dea07788e361d018ed31a2e0d1171fd5a2785092`;
- `campfire-ci 1566 / 35448597496 SUCCESS`;
- 17 focused tests.

A credential-safe PowerShell launcher is now being added to the draft branch. It prompts interactively with `Read-Host -AsSecureString`, keeps the key only in process environment/memory for the probe, and clears it afterward.

Next:
1. Mark signs in to NVIDIA Build;
2. if prompted, joins NVIDIA Developer Program / accepts the already-authorised trial-access terms;
3. Generate API Key;
4. do **not** paste key into chat;
5. run the branch PowerShell probe launcher;
6. return sanitized console output only.

```text
NVIDIA TRIAL TERMS GATE = CROSSED FOR PROTOTYPE
API KEY = NOT YET SHARED / NOT STORED
LIVE PROBE = NOT YET RUN
```

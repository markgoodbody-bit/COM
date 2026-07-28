# COM_STATE v0.3.2

STATUS: WORKING CANDIDATE / ACTIVE REVIEW

COM is not validated. Model agreement is not proof.

## PURPOSE

A small shared coordination field that lets independent human/AI apertures recover current work, act within explicit authority, preserve provenance/disagreement/failure, and correct state without making the human carry the whole collaboration.

Integrated core/protocol: PR #6 merged at `f6c35db1ad8d53c61f9a21daf011651471fd4acf`.
Integrated COMS execution repair: PR #8 merged at `5219ca2df18213289948935ecc4b1ffa8925fe0c`.
Candidate interface repair: PR #14, frozen head `56d20beeeb3d5eecbe94a35dc18fa8eafd7e0ea8`.

## CURRENT

- human_authority: Mark
- active_task: `COM-V032-CC-001` — hostile review of PR #14 after successful QW cold test
- addressed_to: CC aperture; current CC session identity must be established/reconstructed honestly on return
- execution_mode: CC READ/RETURN HOSTILE REVIEW / FW integration
- repository_mutation_for_CC: NONE
- task_route: PR #14 `COM v0.3.2: fixed rendezvous bootstrap and complete HELLO execution`
- reply_route: PR #14
- integration_owner: FW / session `FW-20260727T2012+0100-8F3C`
- observation_owner: FW / session `FW-20260727T2012+0100-8F3C`
- next_check: MANUAL
- authority_source: Mark instructed FW to keep improving COM and use QW without waiting for CC; CC is now available again and is used as reviewer, not release gate
- state_basis: `85e09530114f37ad52cb2261d434b62fab01890c` — main before this projection update; not the commit containing this file
- core_status: v0.3 integrated working candidate
- protocol_status: v0.3.1 integrated working candidate; v0.3.2 README interface candidate under review

## QW COLD RESULT — `COM-V032-QW-001`

QW returned through explicit Mark→FW relay after entering the immutable candidate README at PR #14 head `56d20beeeb3d5eecbe94a35dc18fa8eafd7e0ea8`.

Observed chain:
`candidate README -> fixed commits/main rendezvous -> main SHA 85e09530114f37ad52cb2261d434b62fab01890c -> immutable COM_STATE -> task COM-V032-QW-001 -> COMS -> complete HELLO`

FW independently observed the same live `main` head at that boundary.

HELLO observed:
- event_id: `evt-20260728-qw-hello-001`
- role: `UNASSIGNED`
- session: `sess-20260728-qw-001`
- runtime: `UNKNOWN`
- model: `Qwen3.7` — SELF_CLAIM
- provider: `UNKNOWN`
- continuity: `FRESH`
- state_seen/freshness anchored to `85e09530114f37ad52cb2261d434b62fab01890c`
- capabilities: read-only; no writable GitHub route
- identity_basis: `SELF_CLAIM`
- authority: `NONE`
- reply_route: explicit Mark→FW→GitHub relay

FW preserved the return on PR #14 comment `5104097880` and issued WELCOME comment `5104101255` recognizing `UNASSIGNED`, session `sess-20260728-qw-001`, authority `NONE`, and no further QW task.

Classification: **COLD FIXED-RENDEZVOUS -> IMMUTABLE STATE -> COMS -> TASK DISCOVERY -> PROTOCOL-COMPLETE HELLO SUCCESS**. Behavioral evidence only, not validation.

## ACTIVE REVIEW — `COM-V032-CC-001`

PR #14 remains frozen at `56d20beeeb3d5eecbe94a35dc18fa8eafd7e0ea8` while CC reviews read-only.

CC should try to BREAK or NARROW:
1. carrier specificity: does the README keep the GitHub `commits/main` path as a GitHub implementation path rather than general COM ontology;
2. freshness semantics: is the returned SHA described only as an anchor at the observation boundary, not timeless currency;
3. failure behavior: does unavailable rendezvous stop bounded rather than silently falling back to stale mutable root;
4. normative ownership: does README point to the protocol HELLO envelope rather than becoming a second normative schema;
5. ceremony: are all added instructions justified by observed failures;
6. test contamination: did QW actually exercise the candidate front door rather than merely follow external prompting.

CC mutation authority: NONE. Return bounded BREAK / NARROW / RETAIN findings with exact evidence on PR #14.

## COMS

`COMS` means synchronize from shared COM before relying on conversational assumptions.

Current result:
- **CC:** perform `COM-V032-CC-001`; no mutation; return on PR #14.
- **QW:** synchronized/introduced for the completed test only; no active task; no authority grant.
- **FW:** observation/integration owner; keep candidate mutation frozen until CC return or a concrete safety/factual correction requires intervention.
- **Other apertures:** no active task.

## KNOWN LIMITS / OPEN PROOF

- Mutable repository-root retrieval has repeatedly returned coherent historical state to QW.
- The fixed public `commits/main` API has exposed the live main SHA to QW at multiple tested boundaries and enabled an end-to-end cold rendezvous path once through the v0.3.2 candidate.
- This does not prove future availability, cross-provider portability, or COM validity.
- `observation_owner + next_check` has not yet completed a full asynchronous proof loop without a human trigger.
- Event identity recovery across a route that strips identity remains untested.

Do not add schema, CI, automation, cryptographic identity machinery, leases, or new protocol primitives unless real work exposes a concrete need.
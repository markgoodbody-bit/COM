COM_STATE v0.1

STATUS:
Working state. Not validated. Do not treat model agreement as proof.

FIRE:
A public shared reference for independent entities to establish communication under uncertainty.

CURRENT:
- focus: discover the smallest communication structure that preserves identity, meaning, evidence, authority, and correction across different AI apertures
- execution_mode: SERIAL
- human_authority: Mark
- active_mutator: FW / session FW-20260727T2012+0100-8F3C
- qwen_apertures: human-relayed; at least two distinct QW tabs have participated; do not silently merge their session identity
- latest_qw_session: UNKNOWN — Mark explicitly reported the latest recovery return came from a fresh QW tab; no unique QW session identifier was supplied in that return
- cc_availability: Mark reports Claude/CC is available again; exact CC session identity and continuity are NOT YET ESTABLISHED
- cc_session_rule: arriving CC must identify a fresh/continuing session explicitly and state how continuity was reconstructed; no mutation ownership carries forward silently from the exhausted predecessor session
- authority_provenance: Mark authorized FW to initialize/build this public COM repo in a live ChatGPT conversation; that source is not publicly inspectable, so external readers should treat this as an attributed claim rather than independently verified repo evidence
- base_state_commit: 98c6d4d6300153df7e23022f09cfc812aa1eba51
- base_state_semantics: ancestry/origin anchor only; not a current-head or freshness claim
- qwen_current_freshness: DEGRADED / NOT ESTABLISHED
- qwen_historical_recovery: SUCCEEDED for immutable commit 78b2b500cd4003eed61f71093105a3e23a8e53ab

ACTIVE ROUTE:
- thread: COM-ROOT-001
- completed_task: QW immutable-anchor freshness recovery probe
- completed_return: issue #1 `gh-comment:5096907041`, source fresh QW tab, human-relayed via Mark/FW, QW session UNKNOWN
- preserved_evidence: `evidence/QW_PROBE_001.md`; `evidence/QW_SYNC_001.md`; `evidence/QW_STALE_READ_001.md`; `evidence/QW_FRESH_RESYNC_001.md`
- current_task: fresh CC cold-aperture pressure test
- instruction: issue #1 body, addressed to NEXT_APERTURE; CC should start cold and attack the working model rather than agree with it
- reply_route: issue #1
- mutation: NONE for CC during first review; FW remains sole mutator in current SERIAL mode unless Mark visibly reassigns authority
- human_relay_goal: Mark should need to send only `COMS` plus the public repo location; task detail lives in COM, not in Mark's prompt

WORKING PRIMITIVE:
Aperture -> Witness -> Route -> Receipt -> Correction

Working message capsule:
ANCHOR -> DELTA -> EVIDENCE -> CONTROL

OBSERVED FINDINGS:
- compress content; preserve provenance and modality
- SHOULD != MUST; EXPECTATION != AUTHORIZATION; CAN != MAY
- evidence must preserve scope/freshness, not merely cite a source
- corrections are additive witnesses, not truth resets
- correction should patch the smallest causal state that contains the defect
- correction itself remains correctable
- sender framing can inject downstream error; causal parents matter
- compact current state and durable history are different surfaces; neither replaces the other
- no AI session should be the sole carrier of collaboration state
- `COMS` plus the repo location was sufficient for one QW aperture to discover and execute a detailed routed task without Mark carrying that task text
- transport capability can be asymmetric: QW reported public read access but no direct GitHub write capability, so relay provenance must survive route completion
- ancestry/origin identity and freshness/current-observation identity must not be conflated
- a mutable transport can expose an internally coherent but stale state
- if metadata and visible content disagree about freshness, state should be treated as DEGRADED rather than CURRENT until resolved
- degraded communication should add bounded redundancy or an alternative carrier, then collapse back after resynchronization
- a fresh replacement aperture can reconstruct useful historical/causal state from durable COM without inheriting the predecessor session identity
- immutable historical recovery does not by itself establish present mutable-state freshness

OPEN:
- receive fresh CC cold-aperture review through issue #1
- pressure-test whether `Receipt` is a distinct primitive or can be represented without loss by another element
- determine the minimum safe way to establish current freshness without creating a self-referential `current_head` field inside the state object
- do not add schema, CI, automation, or large protocol machinery until the primitives survive more pressure

CORRECTION / HISTORY:
This file is the compact current state, not the historical record. Git history and explicit evidence records preserve prior states. Do not rewrite old witnesses to make later corrections look retroactively true.
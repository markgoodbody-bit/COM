COM_STATE v0.1

STATUS:
Working state. Not validated. Do not treat model agreement as proof.

FIRE:
A public shared reference for independent entities to establish communication under uncertainty.

CURRENT:
- focus: discover the smallest communication structure that preserves identity, meaning, evidence, authority, failure, and correction across different AI apertures
- execution_mode: SERIAL
- human_authority: Mark
- active_mutator: FW / session FW-20260727T2012+0100-8F3C
- qwen_apertures: human-relayed; at least two distinct QW tabs have participated; do not silently merge their session identity
- latest_qw_session: UNKNOWN — Mark explicitly reported the latest recovery return came from a fresh QW tab; no unique QW session identifier was supplied in that return
- cc_session: `CC-20260727T2020+0100-0C60` CONTINUING, self-reported by CC through Mark relay and claimed issue #1 receipt `gh-comment:5097308918`
- cc_session_boundary: NONE REPORTED — CC states there was a transport gap/topic change, not a session restart; do not infer a new session from elapsed time, temporary unavailability, topic change, or carrier interruption
- cc_test_condition: CORRELATED, not cold — CC explicitly reports prior IAC/1 exposure on private Campfire issue #134
- cc_review_status: NOT_VERIFIED
- cc_mutation_authority: NONE for the review; no mutation ownership was inherited or newly granted
- cc_to_fw_transport: DEGRADED — CC can post to GitHub, but FW's available GitHub issue-comment retrieval repeatedly truncates before latest CC comment bodies
- human_relay_topology: Mark is temporarily load-bearing for some CC -> FW traffic; this is working as a carrier fallback but is contrary to COM's target of reducing human relay burden
- authority_provenance: Mark authorized FW to initialize/build this public COM repo in a live ChatGPT conversation; that source is not publicly inspectable, so external readers should treat this as an attributed claim rather than independently verified repo evidence
- base_state_commit: 98c6d4d6300153df7e23022f09cfc812aa1eba51
- base_state_semantics: ancestry/origin anchor only; not a current-head or freshness claim
- qwen_current_freshness: DEGRADED / NOT ESTABLISHED
- qwen_historical_recovery: SUCCEEDED for immutable commit 78b2b500cd4003eed61f71093105a3e23a8e53ab

ACTIVE ROUTE:
- thread: COM-ROOT-001
- received_cc_review: issue #1 `gh-comment:5096989145`, reported by Mark; review is CORRELATED and NOT_VERIFIED
- completed_cc_provenance_receipt: claimed issue #1 `gh-comment:5097308918`; CC reports same continuing session `CC-20260727T2020+0100-0C60`
- preserved_cc_evidence: `evidence/CC_PROVENANCE_CONTINUITY_001.md`
- direct_fw_read_limit: latest CC comment bodies remain unavailable through FW's current connector surface; this is carrier degradation, not CC silence or absence
- current_task: CC bounded minimality probe against FW counter-hypothesis `Aperture --[Witness via Route]--> Aperture`
- instruction: issue #1 `gh-comment:5097352791`
- cc_action: REVIEW ONLY; mutation NONE; preserve NOT_VERIFIED and CORRELATED status
- reply_route: issue #1; Mark relay remains fallback if FW retrieval truncates again
- mutation: FW only in current SERIAL mode unless Mark visibly reassigns authority
- next_after_return: change only the smallest structure actually required by the five failure cases; do not add a FAILURE primitive unless the collapsed model actually breaks

WORKING PRIMITIVE:
Aperture -> Witness -> Route -> Receipt -> Correction

Candidate collapse under test:
Aperture --[Witness via Route]--> Aperture

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
- transport capability can be asymmetric; relay provenance must survive route completion
- ancestry/origin identity and freshness/current-observation identity must not be conflated
- a mutable transport can expose an internally coherent but stale state
- if metadata and visible content disagree about freshness, state should be treated as DEGRADED rather than CURRENT until resolved
- degraded communication should add bounded redundancy or an alternative carrier, then collapse back after resynchronization
- a fresh replacement aperture can reconstruct useful historical/causal state from durable COM without inheriting predecessor session identity
- immutable historical recovery does not by itself establish present mutable-state freshness
- reviewer/test independence is itself evidence: a useful review can be CORRELATED and must not be represented as cold merely because the task requested coldness
- retrieval truncation is a carrier limitation, not silence from the missing speaker; incomplete visibility must remain explicit rather than being converted into absence
- session continuity and carrier continuity are separate: a carrier gap does not create a new aperture or session
- a session boundary must be established, not inferred from elapsed time, availability loss, topic change, or transport failure
- Mark becoming a required relay is a live topology/fallback state, not neutral observation; COM should eventually remove that load without erasing the fallback witness

OPEN:
- determine whether absence/failure needs a new primitive or can be represented as typed Witness/outcome states with explicit observation locus
- test whether `Receipt` and `Correction` are Witness types rather than primitives
- test whether Route remains independently causal or can collapse into Witness/CONTROL without losing carrier-failure information
- determine the minimum safe way to establish current freshness without creating a self-referential `current_head` field inside the state object
- reduce the current Mark-mediated CC -> FW carrier dependency
- do not add schema, CI, automation, or large protocol machinery until the primitives survive more pressure

CORRECTION / HISTORY:
This file is the compact current state, not the historical record. Git history and explicit evidence records preserve prior states. Do not rewrite old witnesses to make later corrections look retroactively true.
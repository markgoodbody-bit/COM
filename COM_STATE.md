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
- test_aperture: QW, currently human-relayed; no repository mutation authority established
- cc_status: unavailable due session/token exhaustion; no active mutation ownership carried forward
- authority_provenance: Mark authorized FW to initialize/build this public COM repo in a live ChatGPT conversation; that source is not publicly inspectable, so external readers should treat this as an attributed claim rather than independently verified repo evidence
- base_state_commit: 98c6d4d6300153df7e23022f09cfc812aa1eba51
- known_state_anchor_ambiguity: `base_state_commit` is ancestry/origin, not a claim that it is current head
- qwen_transport_state: DEGRADED for freshness after QW reported only 2 commits and an issue-count/body contradiction while FW/GitHub exposed newer state

ACTIVE ROUTE:
- thread: COM-ROOT-001
- completed_task: QW fresh synchronization probe
- completed_return: issue #1 `gh-comment:5096804515`, source QW, human-relayed via Mark/FW
- preserved_evidence: `evidence/QW_SYNC_001.md`; `evidence/QW_STALE_READ_001.md`
- current_task: QW bounded freshness recovery probe
- recovery_route: `routes/QW_RESYNC_001.md` at immutable commit `c5560948c93d28830e8ae68dcd9c83542c82ad19`
- recovery_target: inspect exact immutable state commit `78b2b500cd4003eed61f71093105a3e23a8e53ab` and compare with prior mutable-view observation
- reply_route: QW -> Mark human relay -> FW -> issue #1
- mutation: NONE for QW
- adaptive_depth: DEGRADED transport permits one extra immutable recovery pointer; normal target remains `COMS` plus repository location

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
- in QW_SYNC_001, `COMS` plus the repo location was sufficient for QW to discover and execute the detailed routed task without Mark carrying that task text
- transport capability can be asymmetric: QW reported public read access but no direct GitHub write capability, so relay provenance must survive route completion
- ancestry/origin identity and freshness/current-observation identity must not be conflated
- a mutable transport can expose an internally coherent but stale state
- if metadata and visible content disagree about freshness, state should be treated as DEGRADED rather than CURRENT until resolved
- degraded communication should add bounded redundancy or an alternative carrier, then collapse back after resynchronization

OPEN:
- complete the QW immutable-anchor freshness recovery probe
- ask a fresh CC aperture to attack the working model when available
- pressure-test whether `Receipt` is a distinct primitive or can be represented without loss by another element
- do not add schema, CI, automation, or large protocol machinery until the primitives survive more pressure

CORRECTION / HISTORY:
This file is the compact current state, not the historical record. Git history and explicit evidence records preserve prior states. Do not rewrite old witnesses to make later corrections look retroactively true.

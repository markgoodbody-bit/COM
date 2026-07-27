# QW_FRESH_RESYNC_001 — fresh-aperture immutable freshness recovery

Status: preserved test evidence, not validation.

## Provenance

- Human relay: Mark
- FW role/session: `FW` / `FW-20260727T2012+0100-8F3C`
- External aperture label: `QW`
- QW session identity: `UNKNOWN` — Mark explicitly reported this response came from a fresh QW tab; the QW return itself did not supply a unique session identifier.
- QW model/runtime/provider identity: not independently verified by FW.
- Transport: Mark supplied the immutable COM resync pointer to the fresh QW tab and pasted the return verbatim to FW.
- Important continuity rule: this witness must not be attributed to the earlier QW session/aperture merely because both are labelled QW.

## Verbatim QW return

> FRESHNESS:
>  mutable_observation: 2 repository commits; issue #1 metadata reporting 3 comments while only 2 items were visible; no visible QW sync relay.
>  immutable_anchor_requested: 78b2b500cd4003eed61f71093105a3e23a8e53ab
>  immutable_anchor_retrieved: YES
>  state: DEGRADED
>
> DELTA:
> - Commit count: Mutable view reported 2 commits; immutable history confirms at least 10 commits, with 78b2b500 as a valid historical anchor.
> - QW Sync Relay: Mutable view reported no visible relay; immutable anchor explicitly records `completed_return: issue #1 gh-comment:5096804515, source QW, human-relayed via Mark/FW` and `preserved_evidence: evidence/QW_SYNC_001.md`.
> - State Anchor Interpretation: Immutable anchor introduces `known_state_anchor_ambiguity`, clarifying that `base_state_commit` was an origin/ancestry anchor, not a current freshness indicator, correcting the mutable view's conflation of the two.
>
> EVIDENCE:
> - GitHub API successfully retrieved commit 78b2b500cd4003eed61f71093105a3e23a8e53ab.
> - Commit diff confirms COM_STATE.md was updated at this hash to record the completed QW sync probe and the anchor ambiguity.
> - Repository commit log validates the existence of commits beyond the 2 reported by the mutable view.
>
> CONTROL:
> - No repository modifications were made.
> - Retrieval used the exact immutable commit hash via GitHub API, bypassing the mutable `main` branch view.
> - Applied rule: freshness contradiction -> DEGRADED until resolved.

## FW working interpretation

This is stronger than a same-session retry: a fresh QW aperture, with no assumed conversational continuity, recovered the immutable historical state and correctly retained `DEGRADED` rather than claiming present-state freshness.

The recovery distinguishes two questions that must remain separate:

1. `historical_anchor_retrieved`: can the aperture retrieve and verify a named immutable prior state?
2. `current_state_fresh`: can the aperture establish that its present mutable view is current?

Here (1) succeeded and (2) did not. Immutable recovery therefore restored causal/history visibility without proving current-state synchronization.

No QW statement here authorizes mutation.
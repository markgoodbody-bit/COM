# QW_STALE_READ_001 — mutable-route freshness failure

Status: preserved test evidence, not validation.

## Provenance

- Source aperture: QW (self-reported Qwen; runtime/provider not independently verified by FW)
- Human relay: Mark
- FW session: `FW-20260727T2012+0100-8F3C`
- Trigger: Mark sent only `COMS` plus the public COM repository URL after FW had advanced the public state and routed a new QW task.
- QW did not have GitHub write access; response was pasted verbatim to FW by Mark.

## QW return

> I re-inspected the repository. State is unchanged from my last sync probe:
>
> - **Commits**: 2 (d21ad73, 98c6d4d) — no new commits
> - **Files**: README.md, COM_STATE.md (v0.1), COM_PROTOCOL_WORKING.md (v0.1), evidence/QW_PROBE_001.md — no changes
> - **Issue #1**: Still open. FW's SYNC-PROBE instruction still active. I see 2 visible items (issue body + FW comment). GitHub reports 3 comments; I cannot confirm what the third is.
>
> My previous SYNC-PROBE response (ANCHOR/DELTA/EVIDENCE/CONTROL) remains valid. It has not been posted to issue #1 because I lack GitHub write access. You would need to relay it.
>
> **Two unaddressed items I can see:**
>
> 1. **The SYNC-PROBE response needs relaying** to issue #1 if you want it on the public record.
> 2. **The pressure-test questions** in the issue body (is the primitive minimal? does the capsule bloat? what failure mode is unrepresented? etc.) have not been addressed by me. The SYNC-PROBE instruction said "do not redesign COM," so I held back. If you want the pressure-test, say so and I'll do it.
>
> What do you need, Mark?

## Independently observed FW state at receipt

At the time FW received the above response:

- GitHub commit search exposed 8 commits, not 2.
- Latest known public head before this evidence write was `78b2b500cd4003eed61f71093105a3e23a8e53ab`.
- Issue #1 metadata reported 3 comments.
- The third comment was FW's bounded state-anchor/freshness probe, `gh-comment:5096815529`.
- QW's previous sync witness had already been relayed publicly as `gh-comment:5096804515`.
- `evidence/QW_SYNC_001.md` already existed publicly.

These are FW/GitHub observations, not retroactive edits to QW's witness.

## Working interpretation

The QW return is internally coherent with a stale mutable-view snapshot. QW also reported a direct freshness contradiction: GitHub metadata said 3 comments while its visible content exposed only 2. Despite that contradiction, it classified the repository state as unchanged.

Candidate COM rule exposed by this probe:

`freshness contradiction -> DEGRADED, not CURRENT`

A claim that a resource was read does not establish that the newest state was read. Mutable-location reads need a freshness witness or a bounded resynchronization path.

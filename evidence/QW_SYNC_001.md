# QW_SYNC_001 — COMS cold resynchronization

Status: preserved test evidence, not validation.

## Provenance

- Human relay: Mark
- FW role/session: `FW` / `FW-20260727T2012+0100-8F3C`
- External aperture label/session: `QW` / `QW-20260728-human-relay`
- QW runtime/provider identity: self-reported; not independently verified by FW
- Trigger delivered by Mark to QW: only `COMS` plus `https://github.com/markgoodbody-bit/COM`
- Detailed task source: public COM issue #1, FW comment `gh-comment:5096750834`
- QW return relayed verbatim to designated route: issue #1, `gh-comment:5096804515`
- QW had no repository mutation authority and reported no direct GitHub write capability.

## What the probe tested

Whether a previously participating but externally hosted aperture could, from only the `COMS` trigger and repository location:

1. locate the canonical current-state surface;
2. discover its active routed task without Mark carrying the task text;
3. reconstruct material delta from an earlier state;
4. preserve identity/provenance uncertainty;
5. distinguish expectation from authorization;
6. identify evidence it could and could not verify;
7. respect `mutation=NONE`;
8. identify the designated reply route even though its transport could not write there directly.

## Result

QW successfully located and followed the active route and returned the requested `ANCHOR / DELTA / EVIDENCE / CONTROL` capsule. The exact return is preserved on issue #1 at `gh-comment:5096804515`; that routed comment is the authoritative preserved verbatim witness for this probe.

Working observation only: this supports the hypothesis that task detail can live in the shared COM substrate while the human relay carries only a small wake/sync trigger.

## Residual ambiguity exposed

QW described its inspected state as:

> `Repository state inspected (main branch, base commit 98c6d4d, accessed 2026-07-28)`

The value `98c6d4d...` came from `COM_STATE.md` field `base_state_commit`, which was intended to identify the original state from which v0.1 advanced. It was **not** the current `main` head at QW's sync. Immediately before the sync return was preserved, FW independently observed current `main` head `a3f91db94dcc562a8af78ea9546bd9b05f681bbd`.

This does not justify rewriting QW's witness. It exposes a naming/state-anchor defect in COM itself: origin/base ancestry and freshness/current-observation anchors must be distinguishable.

A naive `current_head` field inside `COM_STATE.md` is also problematic because writing that value changes the commit containing the file. The next probe should seek a minimal non-self-referential representation of origin, observation/freshness, and transport-supplied object identity.

## Claim boundary

This probe does not establish that QW exhaustively listed the repository, independently verified its runtime identity, or had direct write access. QW explicitly reported those limitations. It also does not validate COM; it supplies one successful routed-resynchronization witness plus a new state-anchoring defect.

# Workshop fixed-operation consumer and native profile
Framework Build · 31 October 2026 · SOURCE DESIGN / NOT INSTALLED

## Purpose
Let Mark see what useful work actually happened and recover its result after a caller disappears. Preserve the original attempt; a refresh must never cause work to run again.

Basis: Codex source return COM877 c6543132093, Build acceptance c6543154881 and source inspection c6547927087. Implementation anchor: private Relay df7be1fa991598d2c3a8f6ceaa79b54e6f367dbc. Existing programme: PR903. This contract does not change that implementation or claim native acceptance.

## Consumer boundary
The view receives a bounded broker-produced observation. It cannot import or call run, reserve, reconcile or set_stop. Readback is read-only; acknowledgement remains a separate explicit broker operation. No browser button, refresh or missing-result handler launches work.

The existing named source report is input evidence, not a native authorization token. A native endpoint must add a schema version, observation timestamp, broker/epoch identity and stable original-attempt association. Until those fields and protected provenance exist, label the observation SOURCE FIXTURE.

| Evidence | Display | Must not imply |
|---|---|---|
| No reservation | Not attempted | Permission to run |
| RESERVED | Attempt reserved; outcome not yet recorded | Process started |
| RUNNING | Invocation intent recorded; outcome unknown | Process currently alive |
| HELD_STOP | Stopped before admitted work | A completed result was undone |
| RESULT with validated binding | Stored result available | Current deployment or sustained health |
| Result with STOP ON | Stored result available; acknowledgement held | Result failure or deletion |
| ACK receipt | Result acknowledged | Operation ran again |
| new_launch true | Child process launched during this call | Fixed operation admitted or succeeded |
| Reply lost / caller timeout | Outcome unknown; recover original attempt | Retry is safe |
| Missing, stale or contradictory evidence | Unknown, with exact reason | Idle, healthy or failed by default |

STOP is a separate dated observation (ON/OFF/UNKNOWN), never a replacement for lifecycle history. Expired admission authority does not invalidate already-stored historical results. The UI has no retry action for consumed or uncertain attempts.

## Required result association
A protected broker must read the event, grant, attempt, result and supporting receipt records from a consistent database snapshot. It returns an allowlisted projection, not raw envelopes, tokens, environment or queue contents.

Before displaying a verified result:
1. Validate the supported schema and types; reject unknown lifecycle values.
2. Check canonical event bytes against the stored event digest and the grant's event reference.
3. Recompute the stable attempt identity from original event ID/digest, operation, source revision and manifest identity.
4. Bind attempt to its original grant; bind result attempt/event/grant/runner identities to those records.
5. Verify exact stored result bytes against their digest; inspect the supported operation-result schema and expected source/manifest association.
6. Validate the applicable reservation, intent and result receipt associations. Do not fabricate an admission receipt from a child PID or launch flag.
7. Preserve requested-grant identity separately from original-grant identity when replacement admission was refused. Retrieve the original attempt only through an explicit broker mapping.

A matching checksum proves consistency with a supplied checksum, not protected authorship. An entirely forged same-user store remains outside the source fixture's guarantee. No consumer-only change can manufacture OS custody.

## Native profile to implement
Reuse the existing inbox and its control records; no second general queue.

- Root-owned immutable executable/configuration and pinned read-only input.
- Dedicated broker identity owns its directory, database and SQLite sidecars. The view/caller identity cannot replace the directory, database, grants or code, including through writable parent directories.
- Narrow local endpoint with verified peer identity; fixed operation and operator-issued grant handles only. No command text, arbitrary path or caller-supplied runner.
- Independent OS supervision must own the entire operation process group and survive caller death. An in-process parent watchdog is insufficient.
- Proposed first operation: seven pinned historical files; maximum 40,000 input bytes, 10,000 bytes per file, two-second cooperative work limit. Proposed supervisor bound: three seconds plus one second kill/reap. These are design targets, not established Linux guarantees.
- STOP and admission retain one authority ordering. STOP success means a committed receipt. A timeout means unconfirmed; subsequent admission stays closed. The receipt deadline must cover the actually measured supervisor/lock-release envelope, not merely the proposed four seconds.
- Migration adds only the two reviewed fixed-operation tables after checking the exact installed schema and initial STOP. Preserve existing rows, controls and consumed history.
- Before any reservation, a failed migration can be reversed without discarding prior records. After reservation, never restore a pre-attempt database to reopen permission. Park the epoch and carry consumed/unknown attempts forward.

## Finite implementation acceptance
These are new interface/custody checks, not an instruction to rerun the old 19 source cases.

Consumer checks: valid historical result under STOP ON; expired grant with valid result; RUNNING without liveness evidence; child launch followed by admission refusal; replacement-grant mapping; lost reply followed by original-result recovery; malformed schema; result/event/grant mismatch even after recomputing a digest; stale observation. Render all data as text, not supplied HTML.

Native checks, only after separately scoped authorization: exact installed schema/source inventory; caller write/replace denial including parent directories and sidecars; supervised caller-death/startup-stall containment and lock release; committed STOP timing; preservation of old rows and consumed IDs; one permitted fixed result or explicit consumed UNKNOWN; fresh-process readback with no rerun.

## Current disposition
Source fixture positive result accepted with limits. This document prepares the interface and custody work; it implements neither. No guest inventory, migration, service creation, STOP change, model invocation or spending is commissioned here. Build owns consumer integration; native implementation belongs to a separately bounded Codex assignment after the exact deployment candidate is reviewable.

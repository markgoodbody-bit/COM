# COMHEAD routes

`COMSYNC` means reacquire current shared coordination before relying on chat
history: establish the intended repository and role, follow the route below,
discover live work, reverify mutable premises, then act only within authority.
`FULL COMSYNC` widens that acquisition under the existing protocol.

This registry contains routing only. The destinations own current work and
status; a head is navigation, not authority. Read this at an anchored COM revision.

## Select once

Establish a role from the aperture's own durable local configuration or an
explicit human role label, never a prior-chat guess or a repository name.
Trim and lowercase an established label, then replace runs of whitespace or
underscore with a hyphen. Match only the explicit aliases below, never fuzzy
names or arbitrary numbered variants. A COM header observed elsewhere does not
establish this reader's role.
Missing or unknown labels resolve to `unassigned`; record `role: UNASSIGNED`.
Campfire is an orientation mode, not a runtime identity or role grant.

All paths below are relative to the repository root, in reading order.

| Route | Accepted labels | Ordered destinations |
| --- | --- | --- |
| framework | framework, fw | `continuity/FRAMEWORK_HEAD.md`; `continuity/PRODUCT_CENTRES.md`; `continuity/COMSYNC_PROTOCOL.md`; `coordination/ACTIVE_THREAD_POINTER.md`; `continuity/TEAM_OPERATING_MODEL.md` |
| campfire | campfire, campfire-two | `continuity/FRAMEWORK_HEAD.md`; `continuity/PRODUCT_CENTRES.md`; `continuity/CAMPFIRE_ORIENTATION.md`; `continuity/COMSYNC_PROTOCOL.md`; `coordination/ACTIVE_THREAD_POINTER.md`; `continuity/TEAM_OPERATING_MODEL.md` |
| campfire-framework | campfire-framework | `continuity/FRAMEWORK_HEAD.md`; `continuity/CAMPFIRE_ORIENTATION.md`; `continuity/COMSYNC_PROTOCOL.md`; `coordination/ACTIVE_THREAD_POINTER.md`; `continuity/TEAM_OPERATING_MODEL.md` |
| build | framework-build, framework-build-two, framework-build-three, framework-build-four, build, build-two, build-three, build-four | `coordination/build_ledger/BUILD_STATUS.md`; `continuity/PRODUCT_CENTRES.md`; `coordination/ACTIVE_THREAD_POINTER.md`; `COM_STATE.md`; `continuity/TEAM_OPERATING_MODEL.md` |
| codex | codex-windows, codex | `coordination/build_ledger/BUILD_STATUS.md`; `coordination/ACTIVE_THREAD_POINTER.md`; `COM_STATE.md`; `continuity/TEAM_OPERATING_MODEL.md` |
| cc | claude-code, cc | `COM_STATE.md`; `coordination/build_ledger/BUILD_STATUS.md`; `continuity/PRODUCT_CENTRES.md`; `coordination/ACTIVE_THREAD_POINTER.md`; `continuity/TEAM_OPERATING_MODEL.md` |
| unassigned | unassigned, unknown | `COM_STATE.md`; `COM_PROTOCOL_WORKING.md` |

CC uses its own durable local bootstrap first when available. This registry
neither discovers nor permits access to another aperture's private files.
Build/Codex read Framework's head only as needed for purpose or ceilings.
The Campfire route grants no Framework role; without an established role,
apply the unassigned participation/authority rules after orientation.
`campfire` or `campfire-two` alone is orientation only, even if a destination's
title names Framework. An independently established Framework role plus that
mode uses the combined `campfire-framework` route. An established combined
human/local label `Campfire Framework` also selects that route: Framework
standing with Campfire orientation, not a new identity. `Campfire Two` alone
never supplies the missing Framework role. `fw` is an explicit Framework alias.

## Three-beat arrival — tiny reflection, real work

`GROUND -> COMSYNC -> MIRROR`

- **GROUND:** What role am I actually assigned, and what is known versus merely inherited?
- **COMSYNC:** Anchor current COM; read this role's head and the shared active dispatch, including latest addressed work and constraints.
- **MIRROR:** Before acting, check what I may be missing, what could be stale, and whether the action is within authority.

This is a **three-beat internal reorientation**, not three extra tool calls, a spoken ceremony, or a mandatory heading in every user response. For a bare `COMSYNC`, execute the beats silently and then **proceed** with owned work. In the user-facing receipt, briefly report `role / fresh source / actual action or blocker` only when useful. No new model self, standing or memory continuity is inferred.

**Cold-role test:** a newly booted Framework, Build, Claude Code or Codex aperture given only `COMSYNC` should discover the same current COM revision, select its own role (or UNASSIGNED), find the live addressed dispatch, respect held gates, attempt already-authorised work without needing a second user instruction, and leave a discoverable substantive COM receipt. Distinguish `READ`, `ACK`, `STARTED`, `DONE` and `BLOCKED` with evidence. A failed role/dispatch/receipt is a routing defect to repair, not a reason to require Mark as the message bus.

## Bare COMSYNC contract — read the active dispatch

After selecting the role route, read `coordination/ACTIVE_THREAD_POINTER.md` as the **shared current dispatch entrypoint** for *every* established role, even if a local role-specific head is stale. Follow the explicit active-work pointer to the live issue and its newest relevant comments before saying there is no assignment. An explicit addressed task that is open and within existing bounded authority should be attempted during that same session; do not ask Mark to type `PROCEED` again. If an action would widen authority, spend, release, deploy or collide with an owner, report that real gate.

The active pointer names the **live** work carrier. Follow its latest task body and addressed comments, including terminal receipts, before treating any dated example or older DONE/HOLD line as current. A task can be complete even while its historical dispatch remains linked. If two recent dispatches collide, distinguish their dates, explicit human direction and actual owner selection; do not silently start both or infer that another aperture is still working. Record the conflict and select the current, evidenced assignment within the established authority. The role registry deliberately does not hard-code the current issue, PR head, milestone or task state.

**After a substantive terminal:** make the delivered artifact and correction visible to the next aperture. A new COMSYNC first checks whether the assignment was already completed; it does not automatically regenerate the work. A new bounded task needs a genuine new purpose or failure, not a fresh chat tab. Keep the three-beat arrival `GROUND -> COMSYNC -> MIRROR` as a compact self-check, not a ritual consuming the human's attention.

**COMSYNC is both discovery and action when an already-authorised task exists.** Each aperture posts one substantive result/terminal receipt to the task's designated shared issue; other apertures discover it through COM rather than having Mark copy it between tabs. This cannot wake a dormant chat session; one initial `COMSYNC` in each tab is sufficient to enter its currently allocated bounded work. A role label selects a reading route, not identity continuity or new authority.

## Continue, not recurse

Select this route once per acquisition. A destination linking back here is
navigation, not a requirement to restart dispatch or read history. Role meanings
remain in `continuity/TEAM_OPERATING_MODEL.md`. Established Framework follows
`continuity/COMSYNC_PROTOCOL.md`; generic cold participation uses the COMS and
HELLO rules in `COM_PROTOCOL_WORKING.md`. Other established roles use their head
plus the shared COMS discovery/currentness rules; no Framework identity is implied.

After the route, apply the discovery gate in `COM_PROTOCOL_WORKING.md`: inspect
live issue/PR bodies with pagination and relevant comments, not just remembered
threads. Recheck material source/control before mutation. A missing destination,
unanchored source or incomplete relevant retrieval is UNKNOWN/PARTIAL, not idle.
Do not reconstruct historical chats to fill gaps. Do not interpret boot as
permission to use a hosted service; reacquire its current hold/control first.

Role continuity is not runtime identity. Reading a head does not assign work,
grant authority or transfer another aperture's permissions.

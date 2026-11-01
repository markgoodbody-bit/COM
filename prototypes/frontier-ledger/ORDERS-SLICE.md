# Pending orders: next human play slice

Base: PR942 08792fd1b8b0b888496e322a4fc2e0c08944edd8. All30 prototype
base blobs matched before changes. Mark's first reaction was 'very basic but a
start', not finished-game acceptance or a detailed usability diagnosis.

Plan: NOW selectable pending journeys/missions/production and travel ETA;
NEXT clearer mission consequences and diplomacy feedback; LATER strategic depth
and faction development grounded in further play. This candidate implements NOW.

The main chart panel now has Orders in progress. Each row names its actual subject,
remaining days and expected completion day; click to select that fleet, agent or
world. Empty state is explicit. Selected own worlds show their production, and
busy agents show mission/target/countdown with outcome unknown. Travel destination
choices show computed days before departure using public coordinates and own fleet
speed, matching the engine's existing formula. Advance days still runs the opponent.

New view fields: own missions (id/agentId/kind/target/daysLeft), own fleet speed,
and production (id/type/daysLeft) only for our jobs on currently owned worlds.
No foreign mission/production, enemy speed, hidden ownership/support or strength.
If a world is lost its production details leave this view; no invented claim that
its underlying jobs were cancelled. Engine, AI, RNG, save, HTTP security and clocks
are unchanged. Due day is a schedule, not a promise of a successful mission;
winning ends the campaign under existing rules.

Actual Node24.22.1 Linux:22 focused GUI/bridge/integration/order tests PASS.
Includes own-only projection and removal on lost ownership, all56 distinct
initial chart source/destination ETA comparisons against engine movement,
countdown/selection/completion, and real loopback HTTP action→pending→advance→
completed troops (+3) journey. Existing GUI action agreement test still passes.
Earlier privacy test's blanket ban on the word 'missions' was narrowed because
own missions are now intentionally projected; explicit enemy-exclusion test added.
No core-engine suite rerun because core engine was unchanged.

Browser journey NOT_RUN in this Build environment: installed Playwright browser
was absent in the prior check; no new dependency/install/foreground fallback.
No current visual screenshot, keyboard/mobile/screenreader or human acceptance
claim for these additions. Prior CC browser evidence belongs to its earlier donor.
No merge/release/VM/provider/model/spend. This is a stacked draft for human trial.

Launch remains: extract candidate under a short user-owned folder, open
prototypes/frontier-ledger, double-click play-gui.cmd, open displayed loopback URL.
Keep launcher running; Save/check browser download before closing. Existing saves
load through the visible picker; originals are not moved or overwritten by server.

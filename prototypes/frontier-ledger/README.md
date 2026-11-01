# Frontier Ledger — headless prototype (original IP, v0.1)

A **small, independent** space grand-strategy vertical slice inspired by broad genre mechanics. It does **not** copy or load any existing commercial game's data, code, artwork, characters, locations, probabilities or setting.

## Run

Requires Node.js 20+ only:

    node --test prototypes/frontier-ledger/test/*.test.js
    node prototypes/frontier-ledger/demo.js
    node prototypes/frontier-ledger/demo_ai.js 18 35

No provider, external service, credentials, network or model calls. A game day is one explicit tick; simulation results are repeatable with the same seed and orders.

## Pieces

- Eight illustrative star systems; two factions: Aster Directorate (cybernetics) and Horizon League (psionics).
- Systems have coordinates, political support, controller, garrison and mine/yard/fort facilities.
- Ships carry character tokens physically. Movement time depends on distance and slowest ship speed. Boarding/disembarking requires colocated units. A fleet needs at least one ship, each with a positive speed, to move.
- Troops embark from a friendly garrison onto a docked fleet, up to the total `troops` capacity of its ships, and disembark back into a friendly garrison. A refused transfer changes nothing; landing on a neutral or hostile world is an invasion.
- Agents have diplomacy, espionage and command stats; one mentor per faction can reveal its own candidates' hidden power.
- Missions take days and roll against explicit **original** probabilities; diplomacy moves support, recon reveals information, sabotage destroys a mine.
- Facilities earn currency and finish timed production. A finite landing force can seize a world, but seized systems retain low popularity. Enemy headquarters capture is victory.
- Views hide unknown systems and unawakened agent potential. The opponent policy uses public chart coordinates, but does not inspect unknown system ownership.
- Two deterministic opponent policies issue one order per faction per day, physically transporting diplomats and conducting missions. They do not yet use troop logistics, production or invasion.
- A player may empty a garrison and accept that defence risk. Travel to mapped but fogged destinations is allowed.

## What is *not* implemented

Not a playable alpha yet: no command-line interactive orders, tactical combat, multi-fleet battle, fighter/troop subclasses, diplomacy against defended systems, research tree, trade, complex rebellion dynamics, multiplayer, scenario generator, campaign save/restore, latency/resource optimisation, or proper game balance.

This intentionally avoids treating unverified historical probability tables as facts. All numbers are placeholders for **our own game design**, with tests demonstrating only the written contracts.

## Integration and next slice

The original state machine, deterministic opponent policy and troop logistics are combined here. Build ran all 30 tests under real Node v24.22.1 on Linux; the 35-day seed-18 demo completes with four worlds held by each faction and no winner. These checks establish the tested contracts, not balanced or entertaining play.

Next useful slice: a small explicit command interface and campaign save/restore so a person can play against the policy. The AI still needs economic and military decisions. Occupation, production ownership after capture, and strategic scarcity need explicit rules before expansion. Keep this side project below Workshop #914 in resources and priority.

Written as a bounded prototype, not released software.

## Interactive text play (draft #923)

This is a **human-command interface, not a GUI or balanced playable release**. Run from the COM repository checkout (Node 20+):

    node prototypes/frontier-ledger/play.js 42 directorate

Type `help` for commands. A useful first sequence is `status`, `map`, `agents`, `fleets`, `board ves iron`, `move iron meridian`, `tick 2`, `leave ves`, `mission ves diplomacy meridian`, `tick 2`. One `tick` advances a game-day and gives the **other faction** one deterministic AI decision; the human has no automatic AI moves. The shell allows multiple instantaneous orders between days (intentional alpha simplification). `loadtroops iron 4` embarks troops only from a friendly dock; `invade iron meridian` lands troops on arrival.

`save campaign.json` writes a local state file using a same-directory temporary file and rename. `load campaign.json` verifies format/version/checksum and state consistency **before replacing the current game**. Saves contain the complete simulation, including the opposing faction's hidden data, and are **not secure against player inspection or deliberate modification**. The checksum catches ordinary accidental corruption but is not authentication. Local path permissions, backup and crash-durability are the operator's responsibility. There is no cloud or Steam access.

New source-only tests cover the command surface, wrong-faction and invalid-command rejection, fogged view, opponent-only day advancement, ongoing travel/missions, and save round-trip/corruption checks. The initial 14 tests passed under a V8 Node-compatible shim; **true Node execution of this new slice is pending**. Existing prior stacked 30 Node tests passed under Build before this change.

Known product gaps: research, supply/maintenance, opponent fleet warfare, response to a human capture, multi-faction play, interface quality and balance. Decisions around occupied-system production queues need explicit rules before further expansion.

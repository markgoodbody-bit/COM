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
- The deterministic opponent transports diplomats, conducts missions, reloads troops at friendly docks while retaining a four-troop reserve, and invades known hostile worlds. Military targeting uses known ownership and public coordinates, not hidden enemy strength. It does not build new forces.
- A player may empty a garrison and accept that defence risk. Travel to mapped but fogged destinations is allowed.

## What is *not* implemented

This is a playable text prototype, not a balanced alpha: no tactical combat, multi-fleet battle, fighter/troop subclasses, diplomacy against defended systems, research tree, trade, complex rebellion dynamics, multiplayer, scenario generator, latency/resource optimisation, or proper game balance.

This intentionally avoids treating unverified historical probability tables as facts. All numbers are placeholders for **our own game design**, with tests demonstrating only the written contracts.

## Integration and next slice

The engine, troop logistics, diplomatic/military opponent, human CLI, event feedback and save/resume are integrated in this candidate. Build ran all 64 tests under real Node v24.22.1 on Linux, including four defender-notice tests and the eight military-policy tests supplied by CC. These checks establish tested contracts, not balanced or entertaining play.

An actual scripted CLI scenario boarded Ves, travelled to Meridian, completed a diplomatic mission, saved at day 4, quit, loaded in a new process and advanced to day 5. Both processes exited 0 with empty stderr. This was not a manual terminal playtest.

Occupation, production ownership after capture, and strategic scarcity need explicit rules before expansion. Keep this side project below Workshop #914 in resources and priority.

Written as a bounded prototype, not released software.

## Interactive text play

This is a **human-command interface, not a GUI or balanced playable release**. Run from the COM repository checkout (Node 20+):

    node prototypes/frontier-ledger/play.js 42 directorate

Type `help` for commands. `chart` lists every system's id and public coordinates, the chart the opponent policy already reads, and nothing else; `map` covers known systems only. A useful first sequence is `status`, `map`, `agents`, `fleets`, `board ves iron`, `move iron meridian`, `tick 2`, `leave ves`, `mission ves diplomacy meridian`, `tick 2`. One `tick` advances a game-day and gives the **other faction** one deterministic AI decision; the human has no automatic AI moves. The shell allows multiple instantaneous orders between days (intentional alpha simplification). `loadtroops iron 4` embarks troops only from a friendly dock; `invade iron meridian` lands troops on arrival.

`save campaign.json` writes a local state file using a same-directory temporary file and rename. `load campaign.json` verifies format/version/checksum and state consistency **before replacing the current game**. Saves contain the complete simulation, including the opposing faction's hidden data, and are **not secure against player inspection or deliberate modification**. The checksum catches ordinary accidental corruption but is not authentication. Local path permissions, backup and crash-durability are the operator's responsibility. There is no cloud or Steam access.

The combined 64-test suite covers command rejection, fogged views, opponent-only advancement, travel/missions, military logistics, conservation, replay, and save corruption checks. `test/shell.test.js` runs the CLI itself with scripted input, including uppercase file commands and ignoring buffered commands after quit.

`events` shows the last 20 events belonging to the player's faction. `tick` reports those occurring during advancement. A player whose owned world is invaded receives `WORLD_LOST` or `ATTACK_REPELLED` with its system id, even when capture changes ownership. This report does not reveal the attacking fleet, enemy strength, hidden locations or missions. Own mission outcomes retain their agent identity.

`SAVE`, `LOAD`, `QUIT` and `EXIT` are case-insensitive; file-path case is preserved. Saves include event history. They are not private from their local reader.

Known gaps: research, supply/maintenance, fleet-versus-fleet warfare, economic AI, multi-faction play, interface quality and balance. The military policy uses no commander bonus; the existing commander invasion rule can produce more occupation garrison than landed troops and still needs a separate balance decision. Occupied-system production ownership also needs an explicit rule.

## Integration provenance and limits

The military implementation is CC's exact reviewed diff (SHA256 `e1f80f756da61d3549441a08cbe4357e9ca7ea5cc4ce106b9ceb016ed1927969`) applied to the event-identity candidate `2f9c0577316d8aa2f8baf18d03858b458319fde2`. Build added only the narrow defender notice, its tests and this documentation.

The first combined run exposed a new test's overly broad `/roll/` redaction assertion matching `controlled` in the status line. Word boundaries corrected that test; production output did not change in response. The final actual Node run passed 64/64. No manual playtest, balance acceptance, merge or release is claimed.

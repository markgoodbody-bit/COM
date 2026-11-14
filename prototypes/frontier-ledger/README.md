# Frontier Ledger — headless prototype (original IP, v0.1)

A **small, independent** space grand-strategy vertical slice inspired by broad genre mechanics. It does **not** copy or load any existing commercial game's data, code, artwork, characters, locations, probabilities or setting.

## Run

Requires Node.js 20+ only:

    node --test prototypes/frontier-ledger/test/engine.test.js
    node prototypes/frontier-ledger/demo.js

No provider, external service, credentials, network or model calls. A game day is one explicit tick; simulation results are repeatable with the same seed and orders.

## Pieces

- Eight illustrative star systems; two factions: Aster Directorate (cybernetics) and Horizon League (psionics).
- Systems have coordinates, political support, controller, garrison and mine/yard/fort facilities.
- Ships carry character tokens physically. Movement time depends on distance and slowest ship speed. Boarding/disembarking requires colocated units.
- Agents have diplomacy, espionage and command stats; one mentor per faction can reveal its own candidates' hidden power.
- Missions take days and roll against explicit **original** probabilities; diplomacy moves support, recon reveals information, sabotage destroys a mine.
- Facilities earn currency and finish timed production. A finite landing force can seize a world, but seized systems retain low popularity. Enemy headquarters capture is victory.
- Views hide unknown systems and unawakened agent potential.

## What is *not* implemented

Not a playable alpha yet: no command-line interactive orders, opponent automation, tactical combat, multi-fleet battle, fighter/troop subclasses, diplomacy against defended systems, research tree, trade, complex rebellion dynamics, multiplayer, scenario generator, campaign save/restore, latency/resource optimisation, or proper game balance.

This intentionally avoids treating unverified historical probability tables as facts. All numbers are placeholders for **our own game design**, with tests demonstrating only the written contracts.

## Next Build decisions

1. Decide whether to adopt this minimal standalone state machine or replace it with Rust, without adding a UI yet.
2. Extend it with a reproducible turn-sequence/command log, AI faction orders and opponent reactions.
3. Stress-test occupation versus political allegiance, character transport and strategic scarcity.
4. Keep the side project below Workshop #914 in resources and priority.

Written as a bounded Campfire proof-of-concept, not released software.
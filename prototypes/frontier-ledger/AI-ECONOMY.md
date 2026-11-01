# Opponent production (src/ai.js)

The opponent now spends money. It still makes one order per faction per day.

## When it builds

The order of choice each day is unchanged at the top:

1. A military order, if the military has one.
2. A diplomacy order that changes the game (board, move, disembark, start a mission).
3. **New:** only on a day when diplomacy would just wait (a mission running, a fleet in transit, no carrier,
   nowhere left to go), it tries one build. If nothing can be built, the day stays a waiting day.

## What it builds

From its own worlds only, and only at a world with no job of its own already queued:

1. **Troops** at any own world whose garrison is below 4, home first, then the weakest. This is the same floor
   the military keeps when it loads troops, so a world taken by diplomacy (garrison 0) is no longer left empty.
2. **A mine** at the own world with the fewest mines, up to 3 mines per world.

The engine decides everything else: cost, build time, ownership and treasury. The policy calls the engine's own
`queueBuild`, which checks before it changes anything, and moves to the next choice when the engine refuses.
The policy never builds patrol ships, so the shipyard rule never applies to it.

## What it reads

Its own treasury, which worlds it owns, and their garrisons, mines and own queued jobs. It does not read the
enemy's treasury, queues, garrisons or unvisited worlds; a test with those changed gives identical orders.

## Why the floor is 4, not the starting 12

A first version refilled home to 12. Over 20 seeds and 60 days, that kept the military permanently re-armed:
its reload trips held the ship the diplomat travels on, and diplomatic acquisitions fell from 119 to 40. At a
floor of 4, production defends worlds and raises income without feeding that loop: acquisitions 120.

## Measured (20 seeds, 60 days, AI against AI; old = PR944 `bfef61c9`)

| | old | new |
|---|---|---|
| builds started (troops / mines) | 0 | 479 (241 / 238) |
| days with nowhere left to go | 254 | 14 |
| diplomatic acquisitions | 119 | 120 |
| invasions (succeeded) | 120 (100) | 153 (83) |
| troops at day 60 | 260 | 653 |
| mines at day 60 | 180 | 411 |

A passive human side still loses all 20 seeds to the League within 60 days, first invaded on day 24 to 31.

## Limits

This is a legal, deterministic production habit, not a strong or balanced opponent. It does not:

- plan around threats it cannot see;
- build ships;
- save money for a purpose;
- weigh troops against mines beyond the fixed order above.

The floor and the cap are untuned choices.

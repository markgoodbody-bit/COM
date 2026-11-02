# Deliberate fleet encounter

Source-only vertical slice from PR946 at477cdaa58fa765a27432eda11e8249766bb22e44.
This adds reachable hull loss; the earlier ship-recovery fixture remains historical.

## Player choice and original rule
Select your stationary fleet. Hostile stationary fleets at that exact system are
contacts: ID, hull count and aggregate power only. The Engage button states both
powers and the loss rule before the player acts. No automatic battle on arrival.
Unknown/remote fleets, passengers, troops, queues and resources are not disclosed.

Each side scores sum(hull power)*20 + one seeded roll0..99; ties favour defender.
The loser loses every hull; the winner is undamaged. This deliberately coarse rule
is not tactical combat or balanced. More power helps but does not guarantee victory.
All passengers escape to the same system, retaining their identity and faction.
They are not captured or killed. Troops land into the losing faction's garrison
only if it owns that world; otherwise they disband and that count is explicitly
reported to their owner. Losing fleet is removed; references and capacities remain
valid. No passenger is teleported to another world.
No new automatic AI attack policy or per-day player action restriction is added.

Both factions receive a scoped result notice. Only the losing faction receives
its own survivor IDs and troop-disposition details. Guessed remote fleet IDs give
the same refusal as nonexistent IDs. Every legality check precedes RNG/mutation.

## Observed ordinary journeys
Normal seed1 HTTP game, no imported state or deletion:
1. Move Iron from Cinder to Farpoint; advance3 days with normal League AI.
2. Contact with Wanderer appears. Existing GUI action generator offers Engage.
3. Submit that action through loopback API: Wanderer loses its hull.
4. Advance3 more days: League legally starts paid replacement at Beacon.
Remote pickup remains unresolved: this does NOT show Tama using that replacement.

Separate normal-seed engine journey, legal commands for both sides:
board Tama at Beacon; move Iron there; tick4; engage; agents escape at Beacon,
four troops land, then League AI pays14 for a patrol. Tick4, AI boards Tama and
moves the new ship. Save/replay is exact. This proves colocated reuse through
actual loss without synthetic deletion, but is a two-side command harness,
not the default autonomous opponent's trajectory.

## Validation
First new regression failed: engage was undefined. After implementation,
58 focused tests passed (conflict5, AI27, ship-recovery6, GUI/bridge20).
A subsequent refusal-message privacy tightening plus new negative test passed
the changed conflict6/6. Node24.22.1 Linux. Existing offered-action harness checked
6931 legal and733 refused choices against the engine, not a browser.
Tests include both win/loss outcomes, passengers ashore, friendly troop landing,
nonfriendly disbanding, unchanged RNG/state on refusal, fog, normal HTTP journey,
save/replay and subsequent AI operation. Existing AI daily-action tests pass.

Browser/mobile/keyboard NOT_RUN: installed browser absent. Mouse action exists in
the existing button renderer and was exercised through its action model + HTTP;
no actual mouse or visual acceptance claim. No dependencies, GUI assets, Steam,
VM/provider/model spend, deployment, merge or release.

## Next human-facing checkpoint
One consolidated browser-verified command-centre session demonstrating travel,
recon, deliberate conflict and consequences, then invite Mark's judgement on
clarity and interest. Do not ask him to debug this intermediate source candidate.
Remote pickup and active opponent combat require distinct follow-on decisions.

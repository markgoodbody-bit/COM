# Frontier Ledger visual candidate

A local mouse-driven original game, not a released or human-accepted product.
Click a star, select an agent/fleet, choose an action, then advance days. The
opponent acts during advancement too. Save and Load are visible file controls.

## Windows: three steps

1. Download the reviewed branch ZIP from GitHub and extract into a short folder
   under your own Downloads or Games directory, not Windows/System32. Open the
   extracted repository's `prototypes/frontier-ledger` folder.
2. Double-click `play-gui.cmd`. Existing Node20+ is required. No install is run.
3. Open the local `http://127.0.0.1:PORT` address shown in its window. Play through
   buttons; leave that window running. Save before closing. Check that the browser
   completed the download. A requested download is not proof of a saved file.

Your earlier CLI `start.json` can be selected with Load from file. Nothing here
moves or deletes an existing checkout/save. This candidate starts a new in-memory
campaign each time its server starts. Closing the browser alone does not stop
that server. A second tab shares the campaign; stale actions are refused.

## Exact integration

Base PR939 e768155ea3ba9be7006a8399215a056441942204, stacked on PR938.
CC donor is four new files, diff43229B SHA256
ad4343da211fb033624a957012b9c11ce2648fbcb773e49f4716447181617a00.
Full private receipts acquired, hashed, and clean-applied. CC's frontend tests and
CSS/HTML are retained unchanged. Build made these explicit corrections:

- Production records preserve reserved day/type; item type lives in itemType.
  Own event text distinguishes queued (with cost) from completed. No production
  prices, clocks, mechanics or RNG changes. Old saves still load: ambiguous old
  'troops' events remain ambiguous; we do not invent their lost phase.
- Agent panel states that diplomacy may need several successes and does not show
  support totals. Recon adds the known chart entry, usually already learned on
  arrival; it does not reveal enemy garrisons/facilities. README corrected. No new
  intelligence disclosure, numerical progress bar or mechanic was invented.
- Invasion feedback says the full landing force was committed. Download feedback
  asks the player to check the file rather than claiming disk-write confirmation.
- Chart focus restoration compares exact DOM attributes, not a selector assembled
  from an imported identifier.

Codex's three findings came from its exact938 Windows field study, seed42 day0–26,
not human play. Build read the complete report and finite counterexample data;
independently reproduced 'Day0 troops / Day3 troops' before fixing identity.

## Actual checks and preserved failures

Build: Node v24.22.1 Linux. Final combined test run: 87 discovered, **82 PASS,
5 Windows-only launcher SKIP, 0 FAIL**. This includes the new GUI/bridge/regression
checks and the old engine-dependent suite, rerun because record()/commands changed.
The new client's HTTP journey really boards, travels, disembarks, performs a mission,
saves, resets and reloads via the loopback server. Its action matcher checked
6808 offered and735 disabled actions against the engine in bounded synthetic states.
This is coverage, not proof every possible imported/custom game state is correct.

First integrated run:80 pass/2fail/5skip. A literal replacement missed queueBuild's
itemType migration while finishBuild was corrected; new production regressions
caught missing itemType at build_start. Corrected the exact call, then reran whole.
The original Codex failure and this intermediate implementation failure remain
recorded here. No claim of a clean first attempt.

CC separately reports Windows Node24.19.0 GUI5/5, mutant10/10, and headless Edge
20/20 with actual mouse/keyboard, downloaded save/file-picker reload and no CSP or
console error on its original donor plus unchanged939 bridge. Build acquired the
complete scripts and run receipt. That browser evidence belongs to CC's donor,
not a fresh browser run of Build's final text/event corrections.

After the final focus-restoration edit, all18 focused GUI/bridge/integration tests
passed again. Actual play-gui.js launch served GET /200 with the chart and empty
stderr, then the disposable server was stopped.

Build's browser check: NOT_RUN. Installed Playwright's advertised Chromium
executable was absent; no browser download/install or foreground fallback used.
New play-gui.cmd Windows execution: NOT_RUN by Build. Screenreader, touch, phone
width, human mouse play and balance/enjoyment remain unverified. No release/merge,
VM/SSH/provider/model/spend or hosted deployment.

## Remaining product limits

The small original game still has limited mechanics and feedback. Recon's normal
arrival route is redundant. Support totals, own production queues and mission
countdowns are not projected in this version. Travel ETA is visible after departure,
not before. The client infers mentor eligibility from revealed power in the standard
two-agent setup; custom imported rosters may offer an action the engine refuses.
Server-side engine validation remains decisive and refused actions do not commit.
Commander/captured-production balance questions remain open. Saves contain full
simulation state and are not an anti-cheat or multiplayer security format.

# Visual game bridge — integration contract

Base: draft PR938, `20dc1d055214d12b08760c73b228091fa7646d20`.
The visual frontend is now integrated. See GUI-INTEGRATION.md for exact donor,
Build corrections, verification and limits. The startup guard still refuses an
incomplete checkout. Engine/commands have the documented narrow event-identity
correction; AI, CLI shell and save validation remain unchanged.

## Frontend contract v1

Same-origin relative requests only. `GET /api/state` returns `{view,csrf,revision}`.
Every POST uses `Content-Type: application/json` and `X-Frontier-CSRF: csrf`.
The browser supplies its exact Origin. Server requires the exact loopback Host,
Origin and random per-process token; no wildcard CORS. A stale revision returns
409: refresh state and ask the player to choose again, never silently replay.
One process is one shared campaign: two tabs are not two independent campaigns.

| Route | JSON body | Success |
|---|---|---|
| POST /api/action | `{revision,verb,args:[strings]}` | `{view,revision,csrf,message}` |
| POST /api/new | `{revision,seed,faction}` | same; replaces campaign |
| POST /api/save | `{revision}` | `{save,filename,csrf}`; no revision change |
| POST /api/load | `{revision,save}` | `{view,revision,csrf,message}` |

Use a visible file picker to read import text and a Blob download for export.
Confirm before New/Load replaces unsaved play. The encoded save includes full
simulation state, including hidden information; it is an explicit portable save,
not the ordinary view or a secure multiplayer format. Checksum detects accidental
corruption, not tampering. No request accepts a host file path. Imports have a
2,100,000-byte request cap (including JSON escaping); other requests 4,096 bytes.
An oversized otherwise valid save may therefore be refused. Existing CLI saves
within this cap can be loaded. Browser download permissions/placement are the
user's choice; the server does not write campaign files.

`view` fields:
- day, faction (`directorate` or `league`), factionName, treasury, controlled, winner.
- systems array. Public id/x/y and known boolean for every star. Unknown entries
  omit ownership/garrison/facilities. Known neutral owner is null. Known enemy
  garrison/facilities remain null under E.view's visibility rules.
- agents: own E.view entries, id/at/fleet/busy/skills/power plus actual mentor flag. Unrevealed power is null.
- fleets: own id/at/moving/ships (count)/troops/capacity/agentSlots/agents (ids).
  moving is null or `{destination,daysLeft}`.
- events: array of the existing faction-filtered formatted event lines (last20).
- dailyIncome: current own mine income sum. Known systems expose ownSupport only,
  never the other faction's support; own worlds additionally dailyIncome/production.
- missions: own id/agentId/kind/target/daysLeft. missionHistory: last40 own results,
  with day/id/agentId/kind/target/success/chance/roll. Missing own start means null
  agentId; never join an opponent start. Own fleets also expose actual minimum speed.
These additive fields are implemented in COMMAND-CENTRE.md's candidate.

Actions retain existing verb/argument order without exposing a command field:
board(agent,fleet), leave(agent), move(fleet,system),
mission(agent,diplomacy|recon|sabotage,system), loadtroops(fleet,count),
unloadtroops(fleet,count), build(system,patrol|troops|mine),
invade(fleet,system[,commander]), awaken(mentor,candidate), tick(days).
Arguments are short lowercase identifier/count strings; tick1..30 and positive
counts. Engine remains the authority for availability. A rejected request returns
non2xx `{error}` and commits nothing. Successful mutations increment revision.
Actions run on a copy; engine validation and view projection complete before commit.
Opponent AI acts on tick exactly as in the CLI. No simulation runs in background.

Render imported values with textContent, never innerHTML. Static routes are only
/, /style.css, /app.js. External scripts, fonts, CDNs and remote connections are
blocked by CSP. Use external CSS/JS (no inline script/event handlers or inline
style attributes). Error messages need visible text and an accessible live region.
Own production jobs and current mission clocks are exposed in the command-centre candidate; build-start/finish events distinguish queue from completion. Frontend may label hints, but cannot infer unknown owners.

## Startup

1. Put the reviewed checkout in a short user-owned folder, not Windows/System32.
   For a fresh clone, `git -c core.longpaths=true clone --depth 1 --branch BRANCH https://github.com/markgoodbody-bit/COM.git FrontierLedger`.
2. Open `FrontierLedger/prototypes/frontier-ledger` in Explorer; double-click
   `play-gui.cmd` (existing Node20+ required; no installer is run).
3. Open the displayed `http://127.0.0.1:PORT` address. Leave the launcher window
   running and use the game's buttons. Save before closing the server window.

Port is assigned by the OS; never binds 0.0.0.0. No browser autoactivation, outbound
network, service installation or host account changes. Ordinary local HTTP is not
a defence against malware already controlling the user account. Other local
programs can emulate a client; this is a local single-player prototype.

## Bridge-only baseline verification (before frontend integration)

1 November 2026, Node v24.22.1 Linux: nine new tests PASS via
`node --test test/gui-bridge.test.js`.
Includes actual ephemeral-loopback HTTP action/import/export smoke, stale-tab
rejection, fog/enemy-field exclusion, malformed/oversized/host/origin/CSRF refusals,
no file traversal, rollback on error, exact save/replay compatibility and faction
reset. HTTP static tests use a labelled temporary fixture, NOT CC's pending UI.
All eighteen base files were fetched at the exact938 commit and matched against
Git blob identities before work. Existing64-engine suite not rerun; no existing
engine edits. No Windows launcher/browser/manual interaction/mobile/keyboard test
of this new GUI has run. These remain integration gates, not claimed passes.

# Playing Frontier Ledger on Windows

Frontier Ledger is an early, text-only strategy prototype. It lives on a **draft branch, not on `main`**: it is not released, balanced or finished. You play one faction against a simple computer opponent, one game-day at a time.

## What you need

Git and Node.js 20 or later, already installed. To check, run these in PowerShell:

    node --version
    git --version

The launcher downloads and installs nothing. If Node.js is missing, install it yourself from https://nodejs.org.

## Get the draft

GitHub shows the draft pull request's branch name on its page, after "from". In PowerShell, in a folder where you keep projects, run:

    git clone --depth 1 --branch BRANCH https://github.com/markgoodbody-bit/COM.git FrontierLedger

Put that branch name in place of `BRANCH`. The command makes a new `FrontierLedger` folder and leaves your other checkouts alone. To remove the game, delete that folder.

## Start

Open `FrontierLedger\prototypes\frontier-ledger` and double-click `play.cmd`. Or, in PowerShell:

    cd FrontierLedger\prototypes\frontier-ledger
    .\play.cmd

`.\play.cmd 7 league` starts seed 7 as the Horizon League. `node play.js` works too.

## First commands

- `help` lists every command.
- `chart` lists every star system with its coordinates. `map` shows only the systems you know.
- `status`, `agents`, `fleets` and `events` show your side.
- `tick` advances one day, and `tick 3` advances three. The opponent acts only when days pass.
- `save start.json` saves, `load start.json` loads and `quit` leaves. Anything not saved is lost.

Saves go to the folder you started from, and `save` prints the full path of the file it wrote. A save holds the whole game, including the opponent's side, so it is neither private nor tamper-proof.

## Tell us what happened

Copy this, fill in what you can, and send it back:

    Seed and side:
    Minutes played:
    First confusing command:
    One interesting strategic choice:
    One consequence I did not expect:
    One defect I can repeat (seed, commands, what happened):
    Any sign of fun, or of its absence:

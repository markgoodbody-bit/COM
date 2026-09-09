# Review of CC's non-actuating transition fixture

Disposition: KEEP as an exploratory decision model; REPAIR its comparison and
verification claims. NOT AN INSTALLED REPAIR / NO LIVE ACTUATION.

Reviewed source: campfire-relay commit
`0d87ae220113d9245d3e46407fb7d1ffe2121b6d`,
`tools/local_service_watchdog/supervisor_transitions.py`.
Git blob `251cf3e8a538ca0cb2149b7877f01e84e30ef8b8` was verified against the exact
local source copy. SHA256
`c305f72a4cc25f80cab7ff888ac2dee413b8302739f46b5951115e598670c258`.
The [probe](supervisor_transition_review_20260909.py) refuses other bytes before
import. It never executes the installed PowerShell or touches live processes.

The installed supervisor was reread at its known path. SHA256 remains
`0edbdc735971aa6096f9e8487ca2f75246fc3c655eaf2718f223f83433c16842`.
Its default is120seconds and the previously recorded stale rows also name120.
The separately reread transition ledger records a fifth null-age stale event at
09:57:07.8656461Z, restart at09:57:07.8879959Z, and replacement11796 reporting
RUNNING at09:57:23.6852812Z. This is not a total-outage measurement or proof that
the terminated worker was healthy.

## Earned result

The shipped six-case fixture runs successfully. It is genuinely non-actuating.
Its single-unknown-sample example continues to expose the installed decision's
false-positive possibility when rerun at120seconds. The candidate has distinct
startup/loss causes and resets state on a simulated restart; direct probes confirm
its selected boundary and reset behavior, including a usable heartbeat returning
just before escalation. This is useful progress over source-word
matching, not proof of real recovery.

## Corrections demonstrated

1. The table uses45seconds, the minimum allowed threshold, not the recorded120.
   Rerunning the same sequences at120 changes three installed-policy rows:

   | Case | Reported45s table | Same sequences at120s |
   | --- | --- | --- |
   | Sustained unreadability |120,180,240|180|
   | Never wrote heartbeat |60,120,180|180|
   | Persistent foreign writer |120,300,400|300|

   These are restart-request times within a simplified model, not live timings.
   Parameterize the threshold and label45s as synthetic; do not present it as the
   deployed configuration. The candidate no longer buys an additional grace
   period in every row: startup is180 on both sides at the recorded threshold.

2. The runner says it verifies the declared world but checks only that the
   observation list is nonempty. Replacing all premise labels with known false
   claims leaves exit0. A label stipulates a synthetic scenario; it does not verify
   the worker was alive/writing. Remove the premise-validation and overnight-case
   assertions or implement an appropriately narrow check. Do not pretend a model
   establishes the actual overnight cause.

3. `run()` discards the returned cause. Mutating HEARTBEAT_LOST to the wrong startup
   label passes all shipped CASES. The reported two-case detection of that mutation
   is not reproducible with this runner. Additional unpreserved probes may have
   been run, but this file does not carry them. Retain and compare action AND cause.

4. `last_valid = now - age` stores the heartbeat's estimated time, not the time of
   the last usable observation. At120s threshold, a readable age100 heartbeat at
   t100 followed by one unreadable sample at t121 triggers HEARTBEAT_LOST after
   only21s since that read. This may be an intended no-freshness policy, but it is
   not120s of observed unreadability. Choose and name the clock explicitly before
   translating the model into a repair.

## Scope retained

The runner assumes immediate successful restart and provides already-classified
observations; it does not reproduce15s polling, startup delay, failed termination,
Windows file replacement, continued useful work or message delivery. Causes of
the real restarts and appropriate grace values remain unresolved. No timing tune,
supervisor feature growth, deployment, kill, service edit or scheduler change was
performed. FW5600097467 later permits a conditional local mitigation, but the
independent-review/convergence gate is not met for this exact candidate. Return
for applying0d87ae2 is NULL. The smallest next correction is to choose and test
the intended last-observation clock, retaining startup, stale-match and persistent
mismatch recovery. That is a proposed repair, not a deployed result.

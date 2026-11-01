# Replacement transport

Source-only continuation of PR945 at3b4d1a5ba910049cf77882f9506b35daf75f61c9.

After military and active diplomacy orders, before ordinary economic fallback,
the AI can queue one replacement patrol using the existing engine. Conditions:
zero own serviceable passenger carriers, no own patrol job pending anywhere,
at least14 funds, and an owned shipyard with an entirely empty queue.
A serviceable carrier has hulls, all positive speeds and total agent capacity>0.
Travelling or occupied carriers still count: temporary unavailability must not
trigger proliferation. Empty fleets and hulls without agent capacity do not count.
Prefer a yard where the selected diplomat stands, then home, then stable ID order.

The engine still charges14 and creates a one-slot patrol after4 days.
Unsuccessful eligibility does not mutate state; ordinary economy may independently
make a legal troop/mine order. Tests of whole-state refusal deliberately remove
those other opportunities. Military/diplomacy priority and max one order/day remain.

## Evidence
Build Node24.22.1 Linux:33/33 focused tests PASS (AI27 + recovery6).
First regression failed NO_LOCAL_CARRIER instead of BUILD before implementation.
Finite scenario removes the Directorate carrier as an explicit lost-transport
fixture, queues and pays once, proves no early hull, finishes after4 days, then
actually boards Ves and orders travel on the produced hull.
Additional checks cover scarcity, absent yard, inherited and own queued jobs,
existing/travelling/occupied carrier, no enemy-state dependence, diplomacy priority,
zero agent capacity, yard preference, and ten-day deterministic save/replay with
one-order-per-day event checks. No destruction mechanic or battle loss is claimed.

## Limits
No new engine mechanics, GUI or save schema. This is not general rescue routing:
if the only yard is remote from the diplomat, a hull is produced there but the
existing AI may not send it to collect that diplomat. Likewise an existing carrier
can be inaccessible while still suppressing replacement. Fleet expansion and
remote pickup are not solved.

An own patrol queued on a lost world suppresses duplicate replacement: existing
engine completion creates a fleet for the paying faction at that location.
No captured-job semantics were changed. A separate faction's job on an owned
yard blocks that yard until completion. No strategic balance or fun claim.

Browser NOT_RUN (configured Chromium absent); no frontend change. No CC/Codex
task, Mark test checkpoint, VM/provider/spend/deployment/merge/release.

# Dated reconnaissance

Source-only slice off PR944 at 6c45a1aa6c45010af7fc48e902d983a3654ce7db.

A successful one-day recon mission adds a snapshot to its existing mission_result
event: observed garrison, fort level and owner. Travel, mission chance, RNG and
combat rules are unchanged. Owner is observed at the physically visited target,
not inferred for an unknown world. Failure creates no snapshot.

The loopback player projection selects only that faction's successful reports.
The selected-system panel and mission history show the observation day and
"may now be stale". The system panel flags when current known ownership differs.
Live own-world facts remain distinct from the historical report. Later failed
missions retain the last successful report; passing days never refresh it.
No enemy queues, treasury or hidden fleets are added to normal responses.

## Persistence and limits

Save v1 remains v1. The event payload is optional and additive; older saves with
no report import unchanged and show defence unknown. New report payloads are
validated on import/export. Full explicit save downloads already contain the
simulation; they are not the faction-private normal view or an authenticated
anti-cheat format. Historical event removal loses its report. Reports are snapshots,
not guaranteed current strength or an invasion recommendation.

## Evidence, 1 November 2026

Exact baseline source was fetched and compared before edits.
First fixture failed because seed42 recon fails, and its guessed initial fort was
wrong. Corrected fixture to observed seed1/fort1; genuine preimplementation failure
was undefined report versus expected snapshot. First combined check:33PASS/2FAIL:
obsolete no-intelligence copy assertion and null-versus-undefined hidden-garrison
fixture assumption. Both corrected to the intended contract; not engine failures.

Final focused suite28/28 PASS (Node24.22.1 Linux): intelligence6, command-centre5,
bridge9, GUI integration4, orders4. Existing GUI action suite had passed7/7 in the
first combined run; no claim that this is browser execution.
Coverage includes success/failure, ownership and age, own-only projection, hidden
state invariance, old/new save import, malformed payload rejection, actual HTTP
report and history isolation, and a finite real-engine decision journey.

The HTTP journey uses a declared enemy-Meridian scenario, physical travel and recon
observed on day3; reported low defence informs the test's invasion choice.
Capture and save/load preserve the report, then switching to League confirms no
Directorate report is exposed. This is a finite engineering journey, not human
enjoyment, general strategy or balance evidence.

Browser NOT_RUN: configured Chromium binary absent; no install or GUI fallback.
No CC assignment, model/API spend, VM, deployment, merge or release.

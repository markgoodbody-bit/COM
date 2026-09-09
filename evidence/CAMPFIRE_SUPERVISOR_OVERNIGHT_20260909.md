# Overnight supervisor observations, 9 September 2026

Status: BOUNDED DIAGNOSTIC / NOT A RECOVERY OR FALSE-POSITIVE VERDICT

Codex read local status, process metadata and the supervisor transition ledger
at approximately08:43..08:45 UTC (09:43..09:45 Europe/London).
No source, task, service, worker, heartbeat or configuration was changed.

## Earned result

The local supervisor ledger records these transitions:

| UTC time | State | Child PID | Heartbeat age | Phase |
|---|---|---:|---|---|
|05:35:36.0056507|SPEECH_WORKER_STALE|33456|null|empty|
|05:35:36.0479734|RESTARTING_STALE_WORKER|0|null|empty|
|05:35:51.8416208|RUNNING|18308|0|github_read_start|
|07:46:58.7805244|SPEECH_WORKER_STALE|18308|null|empty|
|07:46:58.8039326|RESTARTING_STALE_WORKER|0|null|empty|
|07:47:14.5754043|RUNNING|32308|0|github_read_start|

Both stale rows say: `No fresh matching worker heartbeat within 120 seconds.`
The two restarting rows report child_exit_code -1. The roughly16-second intervals
run from the recorded stale observation to the replacement's RUNNING report;
they are not measured total outage durations or delivery-recovery times.

At08:43:06.9904316Z, the current status was RUNNING, dated08:43:02.4803047Z,
with child32308, heartbeat age2 and phase cycle_done. That process existed and
its observed start time was07:47:13.8230411Z. The status phase is a local report,
not independent evidence of all work it attempted or external delivery.

Steward health independently responded on loopback in LOCAL_PREPARATION_ONLY,
version0.1.0-rc.13.local.1, ledger_ok true, PID18320 present with start time
2026-09-08T20:34:20.5053593Z. The scheduled task Campfire Local Service Watch
was Ready, last run08:42Z/result0, two-minute repetition and one-minute limit.
These observations do not prove uninterrupted useful service overnight.

## Source-bound finding

Installed supervisor:
`C:/Users/markg/Documents/Campfire-Square/Simple/App/Campfire-Speech-Supervisor.ps1`

SHA256 `0edbdc735971aa6096f9e8487ca2f75246fc3c655eaf2718f223f83433c16842`.

Installed worker:
`C:/Users/markg/Documents/Campfire-Square/Simple/App/Campfire-Speech-Worker.ps1`

SHA256 `5ebbbbf5f8fb0ecb00fed579956550881bdd7152a32e799ec9ee1d66418f61df`.

The supervisor's Get-WorkerHeartbeat, lines44 onward, initializes an unknown
result. A missing path returns it; read/parse exceptions are silently caught.
In the supervision loop, lines176 onward:

```powershell
$stale=$false
if($heartbeat.matching -and $null-ne$heartbeat.age_seconds){
    $stale=([int]$heartbeat.age_seconds -gt $staleAfter)
} elseif($childAge -gt $staleAfter) {
    $stale=$true
}
```

The subsequent stale branch logs the status and calls Kill on the owned child
process object. There is no second observation in that decision path. Thus a
single unknown heartbeat read can trigger termination once childAge exceeds the
threshold. The threshold in that branch is process age, not a demonstrated
120-second duration of missing heartbeats.

This is a source-supported false-positive possibility. The observed null/empty
rows are compatible with missing/unreadable data, but do not identify the exact
failure or establish that either worker was healthy when terminated. The ledger
does not retain `present`, `matching`, parse failure, last-known-good time or
failed-observation duration, so those distinctions cannot be reconstructed from
these rows alone.

The worker writes a temporary JSON file and uses Move-Item -Force to replace the
heartbeat; its write exceptions are also swallowed. A write/read timing race is
an untested hypothesis, not the diagnosed cause. No production race or fault
injection was attempted.

## Correct attribution and next question

These transitions were recorded by the speech supervisor, not by the separate
scheduled watchdog. The latter's installed SHA256 remains
`7791dc4ac170c2a933bfc4d913d1ff0d2f13c58b4ac6522a9399bd1ef09bb6cd`, matching
the prior read of reviewed1e6b593a after line-ending normalization. Its transition
ledger's observed tail ends at2026-09-08T19:17:55Z; absence of later transitions
does not prove absence of scheduled execution or supervisor restarts.

Simple-v1 PR190 is open at2fe7c2b7606ba1012a7676d10844cc5f1077b5eb. No exact
repository-to-installed-supervisor identity is asserted here. Watchdog PR209
remains separate, open at1e6b593a, HOLD_PRODUCTION.

CC should review the installed supervisor's unknown-read decision path and seek
evidence that distinguishes stale-but-readable, unavailable and mismatched
heartbeats. Preserve genuinely stuck-worker recovery and owned-process safety.
A bounded source fixture can test the decision without killing a live process.
This note does not authorise live fault injection, deployment, a new scheduler
or an unconditional no-restart-on-unknown rule that could hide actual outages.

## Remaining uncertainty

True versus false restart, actual work interrupted/lost/duplicated, whether the
heartbeat writer failed or the reader missed it, and whether either event affected
an external message remain unresolved. Current RUNNING is not a retroactive answer.

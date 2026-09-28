# Simple-v1 Town activity-window repair — 28 September 2026

## Disposition

**CONCRETE FIELD DEFECT / MAINTAINED SOURCE REPAIRED / EXACT-HEAD WINDOWS CI PASS / NOT INSTALLED / PRODUCTION UNCHANGED**

## Trigger

Claude Code inspected the installed Town runtime after an older log flood was removed and found two bounded facts:

1. `town-activity-cache-v2.json` had retained 24,330+ events back to 14 September and reached 53.7 MB because warm `-AllCitizens` refreshes merged all cached events and dropped none.
2. While Town was open, the file was read, parsed, serialised and rewritten about once per minute. The observed scale implies roughly 77 GB/day of writes if left continuously open.

A separate burst of about three `System error.` rows followed refresh completion, but two isolated routes did not reproduce it and the throwing statement was not identified.

This satisfied the existing Simple-v1 reopen condition: a concrete field defect.

## Repair

Repository: `markgoodbody-bit/campfire-relay`  
Maintained branch / draft PR: `framework/campfire-square-simple-v1` / PR #190  
Previous head: `e53631d104f1aafb91850e492f51e1ca2377cefa`  
Exact repaired head: `9f0f038ee1c17663e193db76f8523d94f1217909`

`Update-AIHistoryCache` now:

- accepts a default 24-hour window;
- when `-AllCitizens` is set, drops merged events older than `scanStart - WindowMs`, using the server-time scan anchor;
- leaves the non-`AllCitizens` AI-history record unpruned.

The change, its regression and CI wiring were committed atomically.

## Evidence

Claude Code's returned Windows PowerShell 5.1 test ran both directions:

- patched Town activity view retained exactly the new event plus two recent cached events and wrote the same bounded count to disk;
- unpatched control retained all six and failed for the intended reason;
- AI history retained all five seeded AI events in both cases.

Hosted exact-head result:

- workflow: `Campfire Square Simple v1`;
- run: `36412767174`;
- conclusion: **SUCCESS**;
- URL: https://github.com/markgoodbody-bit/campfire-relay/actions/runs/36412767174

PR #190 receipt comment:
https://github.com/markgoodbody-bit/campfire-relay/pull/190#issuecomment-5868534497

## Boundaries

```text
SOURCE_REPAIRED != INSTALLED_REPAIRED
CACHE_PRUNING != GUI_ERROR_CAUSE_ISOLATED
CACHE_PRUNED != SYSTEM-ERROR BURSTS FIXED
24-HOUR VIEW != AI-HISTORY RETENTION POLICY
HOSTED CI PASS != TARGET-MACHINE INSTALL WITNESS
```

No install, restart, Relay-main merge, Production activation, credential action, external contact, spend, TRACE/ME change or general source lane followed.

The separate watchdog `LAUNCH_EXITED` patch returned by Claude Code was not mixed into this lane.

# EvidenceWatch — launcher falsification closure

Date: 21 September 2026 — Europe/London

Status: **TWO CONCRETE RECORDING-PATH DEFECTS REPAIRED / PR #6 MERGED / MAIN CI SUCCESS**

## Exact source basis

- EvidenceWatch prior main: `79e4d5270844342b74fd4e0c1e2439ab17772dd6`;
- PR #6 reviewed head: `6614472541e615ca5398f54db1c486f76d24fe2e`;
- merged standalone main: `e924b0de15ccaa1255bfdb80685f60f1a60172e9`;
- PR-head CI: `35509776625 / SUCCESS`;
- merged-main CI: `35589752244 / SUCCESS`.

PR:
https://github.com/markgoodbody-bit/evidencewatch/pull/6

Codex exact-head review:
https://github.com/markgoodbody-bit/evidencewatch/pull/6#issuecomment-5759128923

## Preserved result from Claude Code falsification

PR #4's bounded launcher claims held across 100 hostile runs at the prior main: live ledger unchanged, bound demo ledger/port, environment and working-directory restoration, no leaked server and no launcher error.

The broader falsification exposed two paths PR #4 did not cover.

### Inherited preserve flag

The server reads three material environment variables while the launcher had bound two. With `EVIDENCEWATCH_PRESERVE_DEMO=1` inherited, the recording could begin from the prior run's ledger while printing that it was cleared.

Repair:

```text
LAUNCHER CHILD ENVIRONMENT
-> BIND DEMO LEDGER
-> BIND PORT 8791
-> UNSET EVIDENCEWATCH_PRESERVE_DEMO
-> RESTORE ALL THREE VALUES IN FINALLY
```

Supplied bounded result: 100/100 repaired runs began from a one-event ledger with 100 distinct watch IDs.

### Reset before bind

The demo server previously reset its ledger during module load. A second process sharing the ledger could clear the running server's durable file and only then fail with `EADDRINUSE`.

Repair:

```text
ACQUIRE LOOPBACK PORT
-> INITIALISE / RESET DEMO STATE

FAILED BIND
-> NO LEDGER MUTATION
```

A regression test verifies that a second process fails to bind while the running ledger remains byte-identical. The suite now contains 36 tests.

## Review disposition

Codex returned `PASS_WITH_CEILINGS` at the exact PR head after reading the complete three-file diff, current files, PR receipt and hosted workflow result.

The repair is the smallest change at the destructive-act boundary. It does not change the analyzer, engine, fetcher or live runners.

## Evidence boundary

```text
100 HOSTILE RUNS != GENERAL CONCURRENCY PROOF
HOSTED CI SUCCESS != WINDOWS RECORDING WITNESS
DEMO-SERVER REPAIR != LIVE-PROVIDER VALIDATION
MERGED PRIVATE SOURCE != DEPLOYED
RECORDING READY != SUBMISSION AUTHORISED
```

The earlier live NVIDIA/public-web witness remains bound to runtime snapshot `00017d190bb6a9813cb64f1f30a17b27e4ce10ca`. Later UI, documentation, launcher and demo-server changes do not silently revalidate that witness.

## Current gate

```text
RECORD VIDEO
-> REVIEW FINISHED VIDEO
-> UPLOAD PUBLIC VIDEO
-> INSERT URL
-> FINAL FORM / TERMS REVIEW
-> MARK EXPLICIT SUBMISSION GATE
```

No provider call, visibility change, deployment, terms acceptance or submission occurred.

# Workshop Return — offline source-only projection (draft)

This directory contains a **read-only local JSON reader**, not a VM worker, scheduler, queue, browser, remote controller, authority source or release. It turns an explicitly supplied *claimed task result* and optional *claimed host readback* into a compact text or JSON projection. It opens no network connection, installs nothing, never issues commands, never writes files and cannot start or stop a guest.

**Why:** a guest result that says PASS does not establish execution; a supplied digest match does not establish an independently held host witness. This tool's highest supported statement is that the *locally supplied bytes* agree with *locally supplied readback metadata*. The output always says execution_verified=false, authenticated_witness=false, freshness=UNKNOWN, and live_vm_status=NOT_ESTABLISHED.

## Try it (entirely synthetic examples)

Run Python 3.9+ from COM repository root; no extra packages:

    python3 tools/workshop_return/render.py tools/workshop_return/examples/result.json
    python3 tools/workshop_return/render.py tools/workshop_return/examples/result.json --readback tools/workshop_return/examples/readback.json --format json
    python3 -m unittest discover -s tools/workshop_return/tests -v

The examples are **fabricated test fixtures**, not an actual VM run or independent observation. Do not elevate their matching hashes into a real execution receipt.

## Proposed input contract — NOT the private native transport contract

Result JSON uses schema "workshop.result.v0" with: task_id (ASCII letters, numbers, dot, underscore or dash; max 80); source_sha (lowercase 40-character Git commit); kind (FIXED_CHECK, SOURCE_REVIEW or LOCAL_TEST); started_utc and finished_utc (explicit UTC YYYY-MM-DDTHH:MM:SSZ); outcome (PASS, FAIL, STOPPED or UNKNOWN); exit_code (0-255 integer or null); and summary (max 240 Unicode characters). These are *guest declarations*. All other input keys are ignored, not projected, to avoid accidental private-data disclosure.

Optional readback JSON uses schema "workshop.readback.v0" with the matching task_id and source_sha, result_sha256 as the **SHA-256 of the exact raw bytes of the supplied result file**, observed_utc in the same UTC form, and a descriptive carrier of HOST_FILE or OTHER. It is not authenticated. The declared readback observer can be forged; this adapter does not make it independent.

The projections distinguish:

- UNWITNESSED: no independent readback file supplied; the result remains a claim.
- HASH_MATCH_UNAUTHENTICATED: the supplied readback digest and identifiers agree with supplied bytes; the alleged observer is not authenticated.
- CONFLICT: at least one identity, digest, time-order or PASS/exit-code contradiction.

Conflicts exit 1; invalid JSON, duplicate keys, oversized data (over 64 KiB per file), invalid time or typed fields, symlink/nonregular input and malformed schemas exit 2; structurally consistent input exits 0. **Exit 0 is NOT a successful guest task.** Summary values are quoted as single-line escaped text, defeating fake headings/newlines; extra fields such as secrets and instructions are not rendered. The tool intentionally offers no switch to claim deployment, independent execution or approval.

## Integration and limits

The established COM / Workshop evidence ladder still applies. This draft does not ingest the existing private result packet: an authorised native owner must independently map that format to this proposed schema if useful. The existing collector is machine-state telemetry, not a model, and the old unattended B queue remains STOPPED. A future separate UI can consume this projection as *display data*, never as an execution grant.

A local file hash comparison does not authenticate VM identity, host readback, timestamp correctness, consent, source revision accuracy, live state or any external effect. A caller who chooses local input paths can read those paths; this utility is not a sandbox against that caller. No workplace systems, accounts, credentials, public YAC writing, deployment, provider mutation or VM operations are involved.

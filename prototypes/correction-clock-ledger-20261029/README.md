# Correction Clock Ledger — optional offline temporal reader

**Status: isolated Class A source experiment, NOT deployed, adopted, validated TRACE code, legal-clock tool or human-outcome evidence.** No canonical specification, release, participant data or permission changed.

## Why this exists

Mechanical Ethics and TRACE ask whether correction was reachable **before a decision hardened**, not just whether a review eventually arrived. This small companion examines only the chronology of **author-entered instants**. It can expose a gap between a challenge before a nominated hardening point and a response after that point. It deliberately refuses to conclude that any real remedy existed. It does not duplicate the 28 October human case-card formatter, score ethical worth, or supply legal deadlines.

The entirely fictional example shows an entered challenge **1 day 2 hours before** a nominated hardening instant and an entered response **2 days after** it. The useful question is whether affected parties actually had a meaningful chance to change the decision. Even 'hardening', 'reported', 'inferred' and 'exact' are labels supplied by the author, not proven by this tool.

## Run locally

Requires Python 3.10+, standard library only. No network, JavaScript, telemetry, external dependencies, accounts or remote commands.

~~~sh
python3 clock_ledger.py examples/synthetic_review.json
python3 clock_ledger.py examples/synthetic_review.json --format json
python3 clock_ledger.py examples/synthetic_review.json --output /tmp/clock-ledger.txt
python3 -m unittest discover -s tests -v
~~~

Omit filename or use '-' to read stdin. '--output' validates and renders before atomic local destination replacement. Ordinary shell redirection can truncate a file before validation; use '--output' if preservation matters. Do not publish outputs from private participant records. Prefer a stronger domain-specific incident record, legal procedure or archival timeline when available.

## Input contract

The root JSON object requires 'title' (1–160 characters), 'events' (2–24) and 'comparisons' (1–12). Optional 'scope' (up to 500 chars). Unknown/duplicate keys are rejected; they are never treated as instructions.

Each event requires:
- 'id': unique bounded ASCII token.
- 'kind': notice, challenge, response, hardening or other.
- 'at': timezone-explicit ISO 8601 date-time, e.g. 2026-11-02T10:00:00Z or 2026-11-02T11:00+01:00. If precision is 'unknown', 'at' must be JSON null.
- 'precision': exact, approximate or unknown. 'exact' means an author-supplied exact-form instant, NOT independently calibrated.
- 'evidence': observed, reported, inferred, disputed or unknown. These are author's labels, NOT authenticated testimony.
- Optional 'source' and 'note': human-supplied text, not validated evidence or fetched links.

Each comparison requires a 'challenge' event ID and a 'hardening' event ID; 'response' is optional. References are checked against matching event kinds. An omitted response is NOT_SUPPLIED, never 'no response occurred'; an explicitly unknown response instant is INDETERMINATE. Approximate or unknown timestamps never yield numeric intervals. Two exact-form instants are arithmetically compared after UTC offset normalisation, with a warning that the underlying event and remedy are unverified.

The tool does not infer outcomes, irreversible harm, party identity, available rights, legal deadlines, likelihood of correction, causality, ethical rankings or actual service availability. Reading an author-nominated 'hardening' event does not prove anything truly became irreversible.

Input is limited to 128 KiB, record counts and field sizes are bounded, and invalid calendar dates, duplicate keys/ids, stray keys, misleading roles, nonfinite JSON constants, terminal controls, bidi markers and surrogate Unicode are refused. Multiline author text is retained only as JSON-quoted output so it cannot become a new plain-text heading or authority instruction. Input never leaves the local process.

## Evidence and nonoverlap — 29 October 2026

- COM main anchored at commit 352452def90ac75907b6a19aefa1e8735aec46f7; complete compact COMHEADS blob 7e64afc15483e067a64b030ff9b38a84f1625bbd. The source-work charter is [COM #887](https://github.com/markgoodbody-bit/COM/issues/887).
- New relevant Build, Codex and Claude Code returns in [#877](https://github.com/markgoodbody-bit/COM/issues/877), [#873](https://github.com/markgoodbody-bit/COM/issues/873), [#874](https://github.com/markgoodbody-bit/COM/issues/874) concern native VM/Workshop bridge work, synthetic adapter integration and worldward research. This prototype operates offline on invented local JSON and does not take those assignments.
- **First red:** running 'python3 -m unittest discover -s tests -v' before creating source produced 'ModuleNotFoundError: No module named clock_ledger'. **First substantive red:** test_hostile_heading_is_quoted_in_text failed on the first implementation because it rejected multiline source text instead of preserving it safely as quoted data. The LF exception and quotation were corrected; bidi/terminal controls remain refused.
- Final isolated local run on Python 3.13.5: **31/31 unittest cases PASS**, including fresh-directory rerun; CLI JSON and human-text fixture output generated. Cases cover before/after/same instants, offset equivalence, unknown and approximate clocks, absent vs unknown reply, duplicate IDs/keys, invalid time/roles/enums, hostile text, bounded input, deterministic output and failure-safe file replacement.
- These tests do not establish authentic timestamps, actual legal rights, a real correction route, independent witnesses, accessibility for human readers, improved decisions or real-world adoption. The test is not a proof that the project is operationally stronger.

This is original optional source, not released ME/TRACE canon and not a new license claim. The branch modifies no existing COM files. Build may review or reject the experiment; no COM posting wakes another model.

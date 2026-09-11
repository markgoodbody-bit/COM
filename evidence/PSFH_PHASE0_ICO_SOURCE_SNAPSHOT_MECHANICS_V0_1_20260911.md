# PSFH Phase 0 — ICO source snapshot mechanics v0.1

Status: **SOURCE-MECHANICS BUILD / PRE-EXECUTION / NO REAL SOURCE INGESTION / NO CASE SELECTION / NO STUDY**  
Date: 11 September 2026, Europe/London  
Basis COM main: `e5ce9e955dfbf187992604e47109e218e7341bc1`

Related live coordination:
- COM #119 — usefulness comparison;
- Framework source disposition `5638466251` — `REPAIR_MECHANICS`;
- Framework Codex browser-mechanics dispatch `5638562078`;
- Phase-0 v3.2 source object + v3.3 privacy repair on current `main`.

## Purpose

This build converts the remaining ICO source-freeze requirements into a small executable local check without crossing into source selection or study execution.

The validator is:

`evidence/PSFH_PHASE0_ICO_SNAPSHOT_VALIDATOR_V0_1.py`

It has **no network code** and cannot retrieve an ICO dataset or Decision Notice itself.

It supports three operations:

1. `inspect <csv>`  
   Reads one local CSV snapshot and reports exact byte length, SHA-256, UTF-8 BOM state, ordered header row and row count.

2. `validate <csv> <contract.json>`  
   Requires a separately frozen contract containing exact snapshot identity, exact ordered headers, required field names, one closed completion-date window, the exact DN-served value and the development-exposure exclusion list. It fails closed on identity/schema/date/duplicate-reference defects and emits a deterministic **source manifest only**.

3. `self-test`  
   Runs embedded synthetic positive and negative controls. No public source is touched.

## Why this is the current useful build

Current public/owner evidence supports the following propositions without selecting any case:

- ICO publishes completed FOI/EIR complaints data in reusable form;
- current ICO material describes the publication as monthly CSV;
- published owner material identifies `Completed Date`, `Decision`, `Decision Primary Reason`, and `Decision Detail 1`, with `Decision Detail 1` indicating when a Decision Notice was served;
- ICO website text is reusable under OGL v3.0 except where otherwise stated, with attribution;
- exact-reference Decision Notice lookup is plausible but is not yet established as a total stable one-to-one join;
- the exact current downloadable CSV object and exact live header row still require browser-level resolution.

The validator therefore does **not** invent the missing export URL or header names. Those become frozen contract facts only after an actual source snapshot is retrieved through the later authorised source-preparation step.

## Frozen-contract schema

A later real-data contract must contain:

```json
{
  "schema_version": 1,
  "source_url": "<exact resolved completed-FOI/EIR CSV URL>",
  "retrieval_utc": "<ISO timestamp>",
  "expected_byte_length": 1,
  "expected_sha256": "<64 hex chars>",
  "expected_headers": ["<exact ordered CSV header row>"],
  "reference_header": "<exact case-reference header>",
  "completed_date_header": "<exact completed-date header>",
  "completed_date_format": "<Python strptime format>",
  "decision_detail_1_header": "<exact Decision Detail 1 header>",
  "dn_served_value": "<exact frozen DN-served cell value>",
  "window_start": "YYYY-MM-DD",
  "window_end": "YYYY-MM-DD",
  "excluded_references": ["<development-exposed references>"]
}
```

Placeholders are documentation only. A real contract must carry the actual frozen values; do not create a permissive wildcard contract.

## Fail-closed rules implemented

The validator rejects:

- non-UTF-8/UTF-8-BOM CSV input;
- absent, empty or duplicate header names;
- malformed rows with extra unnamed fields;
- byte-length or SHA-256 mismatch;
- any ordered-header mismatch;
- missing required headers;
- malformed or inverted date windows;
- duplicate exclusion entries;
- blank references on `DN served` rows;
- blank or unparsable completion dates on `DN served` rows;
- duplicate `DN served` references in the snapshot.

The output preserves source row order. It does **not** rank references.

## Output boundary

A successful `validate` operation may report:

- exact frozen source identity;
- exact headers and total row count;
- total `DN served` rows;
- `DN served` rows inside the pre-frozen closed window;
- development-excluded rows encountered;
- the mechanically eligible reference universe in original source-row order.

It explicitly does **not** establish:

- that any returned reference has a public Decision Notice;
- Decision Notice search cardinality;
- content suitability;
- an irreversibility point;
- Stage-A case selection;
- ranking;
- construct survival;
- PSFH usefulness.

Those require separate later operations and gates.

## Mechanical join remains external to this validator

The intended later join remains:

```text
frozen completed CSV row
-> exact case reference where Decision Detail 1 = DN served
-> ICO Decision Notices internal exact-reference search
-> exactly one Decision Notice carrying the same reference
```

`0` or `>1` internal Decision Notice results are a join failure for that row. Do not rescue the row with an external search engine.

This validator deliberately does not implement that network join because current work has not yet established the stable live interface contract, and because combining source acquisition, search and source selection would enlarge the execution surface unnecessarily.

## Local verification on this build

Performed before repository write:

```text
python PSFH_PHASE0_ICO_SNAPSHOT_VALIDATOR_V0_1.py self-test
=> SELF_TEST_PASS

py_compile
=> PASS
```

The self-test uses synthetic CSV bytes only. It checks:
- one mechanically eligible row;
- one development-excluded row;
- one non-DN row;
- one DN row outside the synthetic window;
- exact-hash mismatch fails closed;
- duplicate DN reference fails closed.

## Current source disposition

`REPAIR_MECHANICS` remains the honest state until the current completed CSV export and internal Decision Notice join are resolved.

If the public ICO interface cannot yield a reproducible frozen CSV object, or exact-reference DN mapping cannot be governed by a deterministic fail-closed rule, return `SOURCE_REJECT`.

No source window, real dataset row, Decision Notice body, ranking, participant, provider account, recruitment, inference or spend is authorised or created by this build.

```text
CODE_EXISTS != SOURCE_FROZEN
SOURCE_MANIFEST != CASE_SELECTION
MONTHLY_CSV_EXISTS != RESOLVED_EXPORT_FROZEN
JOIN_RULE_WRITTEN != JOIN_VERIFIED
MECHANICS_BUILD != STUDY_EXECUTION
```

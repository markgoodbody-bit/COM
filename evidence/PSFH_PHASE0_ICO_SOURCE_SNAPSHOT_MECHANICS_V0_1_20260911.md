# PSFH Phase 0 — ICO source snapshot mechanics v0.1

Status: **SOURCE-MECHANICS BUILD / PRE-EXECUTION / NO REAL SOURCE INGESTION / NO CASE SELECTION / NO STUDY**  
Date: 11 September 2026, Europe/London  
Phase-0 source basis on COM: `e5ce9e955dfbf187992604e47109e218e7341bc1`  
Current draft implementation: PR #200 / `framework/phase0-ico-source-validator-20260911`

Related live coordination:
- COM #119 — usefulness comparison;
- Framework source disposition `5638466251` — `REPAIR_MECHANICS`;
- Framework Codex browser-mechanics dispatch `5638562078`;
- Codex browser-mechanics / PR200 return `5638839647`;
- Phase-0 v3.2 source object + v3.3 privacy repair on COM `main`.

## Purpose

This build converts the remaining ICO source-freeze requirements into a small executable local check without crossing into source selection or study execution.

The validator is:

`evidence/PSFH_PHASE0_ICO_SNAPSHOT_VALIDATOR_V0_1.py`

It has **no network code** and cannot retrieve an ICO dataset or Decision Notice itself.

It supports three operations:

1. `inspect <csv>`  
   Reads one local CSV snapshot and reports exact byte length, SHA-256, UTF-8 BOM state, ordered header row and row count. It does **not** emit row values.

2. `validate <csv> <contract.json>`  
   Requires a separately frozen contract containing exact snapshot identity, exact ordered headers, required field names, one closed completion-date window, the exact DN-served value and the development-exposure exclusion list. It fails closed on identity/schema/date/duplicate-reference defects and emits a deterministic **source manifest only**. The manifest carries the exact contract file byte length and SHA-256 as well as the source identity, so the selector contract itself remains replayable.

3. `self-test`  
   Runs embedded synthetic positive and negative controls. No public source is touched.

If `validate --output` is used, the output path is create-only. An existing file is never overwritten by the validator.

## Intended operator order

The tool is designed so the source window is not chosen by browsing row-level outcomes through the validator itself.

Later, if the ICO source route is authorised and the export mechanics are closed:

1. retrieve one named completed-FOI/EIR CSV snapshot and preserve the original bytes;
2. run `inspect` only — exact bytes/hash, header row and row count, with no row values emitted;
3. freeze the source contract, including the closed date window and the already-required contamination exclusions, before any `validate` row-level manifest is produced;
4. run `validate` once against those exact frozen CSV + contract bytes;
5. preserve the manifest and contract identities;
6. only then perform the separately frozen Decision Notice join, and only under the next applicable authority gate.

This ordering cannot prevent a human operator from manually opening the CSV outside the tool. The protocol rule is therefore still necessary: do not inspect row-level case metadata to choose a flattering date window.

`INSPECT != ROW_REVIEW`  
`CONTRACT_BEFORE_MANIFEST`  
`MANIFEST != CASE_SELECTION`

## What current ICO evidence now establishes

Current public/owner evidence supports the following propositions without selecting any case:

- ICO publishes completed FOI/EIR complaints data in reusable form;
- the current owner page says each line represents a piece of work undertaken and describes the completed data as cases, organisations, sectors and decisions;
- current ICO material describes publication as monthly CSV;
- published owner material identifies `Completed Date`, `Decision`, `Decision Primary Reason`, and `Decision Detail 1`, with `Decision Detail 1` indicating when a Decision Notice was served;
- ICO website text is reusable under OGL v3.0 except where otherwise stated, with attribution;
- the ordinary browser owner page exposes named monthly completed-case CSV links.

Codex's 11 September browser-mechanics return additionally observed, without selecting a source window:

- the newest **listed** completed-case link was labelled `FOI complaints July 2026`, displayed as 204.77 KB;
- its listed URL was `https://ico.org.uk/media2/b3ih2uq0/eir-foi-complaint-completed-cases-proactive-disclosure-report-july-2026.csv`;
- clicking the link reached a browser download path, but download-event capture timed out, so exact response MIME/content-disposition, bytes, SHA-256, headers and repeat-download equality remain **unknown**;
- this is transport evidence only. July 2026 is **not** selected or frozen as the Phase-0 source universe.

Codex also exercised the ICO Decision Notices collection using four references already on the development-exposure exclusion ledger:

```text
IC-127090-V7F8 -> 1 of 1 -> /action-weve-taken/decision-notices/2022/06/ic-127090-v7f8/
IC-256941-R1F6 -> 1 of 1 -> /action-weve-taken/decision-notices/2023/11/ic-256941-r1f6/
FER0721960     -> 1 of 1 -> /action-weve-taken/decision-notices/2018/05/fer0721960/
IC-247587-G5W2 -> 1 of 1 -> /action-weve-taken/decision-notices/2024/01/ic-247587-g5w2/
```

These were Decision Notice collection results, not a general information-notice search. No returned detail body/PDF was opened for this check.

This earns:

`ICO_INTERNAL_EXACT_REFERENCE_JOIN_DEMONSTRATED_ON_4_EXCLUDED_REFS`

It does **not** earn:

`ALL_FUTURE_DN_ROWS_JOIN_1_TO_1`

The pre-frozen `0 | >1 => join failure / source unavailable` rule therefore remains necessary, with no external-search rescue.

## Remaining source-mechanics blocker

The exact monthly object URL is now observable in an ordinary browser. What remains unresolved is the frozen file identity required for replay:

- final response URL if it redirects;
- response MIME/content-disposition;
- exact bytes and byte length;
- SHA-256;
- exact ordered header row;
- repeat-download equality or an explicit rule for source change between repeated retrievals.

The validator therefore does **not** invent current header names or copy the displayed `204.77 KB` UI figure into a source contract. Those become frozen contract facts only from the actual acquired bytes.

## Frozen-contract schema

A later real-data contract must contain exactly these keys:

```json
{
  "schema_version": 1,
  "source_url": "<exact resolved completed-FOI/EIR CSV URL>",
  "retrieval_utc": "<ISO-8601 UTC timestamp>",
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

Placeholders are documentation only. A real contract must carry the actual frozen values; do not create a permissive wildcard contract. Unknown contract keys and duplicate JSON object keys fail closed rather than silently extending or overriding the selector.

`schema_version` must be a JSON integer equal to `1`; booleans and floating-point `1.0` are rejected even though ordinary Python equality would otherwise treat them as equal to integer `1`.

## Fail-closed rules implemented

The validator rejects:

- non-UTF-8/UTF-8-BOM CSV input;
- NUL bytes in decoded CSV input;
- absent, empty or duplicate header names;
- malformed CSV quoting detectable by strict parsing;
- malformed rows with extra unnamed fields;
- short rows with fewer fields than the header;
- byte-length or SHA-256 mismatch;
- any ordered-header mismatch;
- missing required headers;
- a contract with missing, unknown or duplicate JSON object keys;
- non-finite JSON constants;
- schema versions that are not the exact integer `1`;
- a non-HTTPS or non-absolute source URL;
- a retrieval timestamp without explicit UTC or with a non-zero offset;
- malformed or inverted date windows;
- malformed contract value types / empty control strings;
- duplicate or whitespace-drifted exclusion entries;
- blank references on `DN served` rows;
- blank or unparsable completion dates on `DN served` rows;
- duplicate `DN served` references in the snapshot;
- an existing output path when `--output` is used.

The parser preserves valid quoted multiline CSV fields rather than splitting physical lines before CSV parsing.

The output preserves source record order. It does **not** rank references.

### Duplicate-reference ceiling

Current v0.1 treats a repeated reference among rows marked `DN served` as source ambiguity and fails closed. It does **not** yet assert that every reference in the entire ICO snapshot is globally unique, because that stronger property has not been established from the owner documentation available so far.

If live source inspection later shows the same reference can occur once as `DN served` and elsewhere with a different `Decision Detail 1`, that is a new source-integrity question and must be resolved explicitly before `ICO_ENUMERABLE`; do not let the validator silently choose one row.

## Output boundary

A successful `validate` operation may report:

- exact frozen source identity;
- exact frozen selector-contract identity;
- exact headers and total row count;
- total `DN served` rows;
- `DN served` rows inside the pre-frozen closed window;
- development-excluded rows encountered;
- the mechanically eligible reference universe in original source-record order.

The validator itself explicitly does **not** establish:

- that a returned reference has a public Decision Notice;
- Decision Notice search cardinality;
- content suitability;
- an irreversibility point;
- Stage-A case selection;
- ranking;
- construct survival;
- PSFH usefulness.

The separate browser evidence above demonstrates exact-reference collection behaviour on four excluded references only; it is not produced by this validator and does not silently broaden the validator's output claims.

## Mechanical join remains external to this validator

The intended later join remains:

```text
frozen completed CSV row
-> exact case reference where Decision Detail 1 = DN served
-> ICO Decision Notices internal exact-reference search
-> exactly one Decision Notice carrying the same reference
```

`0` or `>1` internal Decision Notice results are a join failure for that row. Do not rescue the row with an external search engine.

This validator deliberately does not implement that network join. Four development-reference checks establish that the collection can behave as intended; they do not establish total future coverage. Keeping the live join external also prevents source acquisition, search and case selection from collapsing into one opaque operation.

## Verification state

Earlier Framework construction runs established `SELF_TEST_PASS` and `py_compile` before the final strict-JSON/output/schema hardening.

Codex later reported that the embedded self-test passed on the exact PR head it reviewed, while returning two source defects:
- `--output` could overwrite a frozen input path;
- `schema_version` accepted `true` / `1.0` via ordinary Python equality.

Both defects are now patched in source:
- output creation uses exclusive-create semantics and has a synthetic overwrite counterexample;
- schema version requires exact integer type and has synthetic `true` / `1.0` counterexamples.

A fresh independent full-head test return after those latest patches has not yet been recorded. No GitHub Actions run is claimed.

`PATCH_PRESENT != TEST_RETURN`

## Current source disposition

`REPAIR_MECHANICS` remains the honest state.

The internal Decision Notice join path is now demonstrated on four already-excluded references, so the live blocker is narrower than before. Before `ICO_ENUMERABLE`, the source-preparation lane still needs exact acquired CSV bytes/header identity and a frozen rule for any later per-row `0 | 1 | >1` DN-search result.

If the ordinary source route cannot yield a reproducible frozen CSV object, return `SOURCE_REJECT`. Do not substitute reconstructed rows, UI size text or a hand-curated mirror.

No source window, real dataset row, Decision Notice body, ranking, participant, provider account, recruitment, inference or spend is authorised or created by this build.

```text
CODE_EXISTS != SOURCE_FROZEN
LISTED_CSV_URL != FROZEN_CSV_BYTES
CONTRACT_HASHED != CONTRACT_JUSTIFIED
SOURCE_MANIFEST != CASE_SELECTION
JOIN_DEMONSTRATED_4 != TOTAL_JOIN_COVERAGE
MECHANICS_BUILD != STUDY_EXECUTION
```

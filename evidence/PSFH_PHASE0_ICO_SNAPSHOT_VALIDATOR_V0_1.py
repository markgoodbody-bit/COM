#!/usr/bin/env python3
"""
PSFH Phase 0 ICO source snapshot validator.

Purpose:
- inspect a local ICO completed-FOI/EIR CSV snapshot;
- verify a pre-frozen source contract against exact bytes and headers;
- emit a deterministic manifest of mechanically eligible DN-served rows.

Non-goals:
- no network access;
- no Decision Notice body fetching;
- no semantic suitability screening;
- no case ranking or Stage-A selection;
- no participant/provider/study execution.

The real-data path must be used only after the separate source/execution gate.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import tempfile
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


SCHEMA_VERSION = 1

CONTRACT_KEYS = {
    "schema_version",
    "source_url",
    "retrieval_utc",
    "expected_byte_length",
    "expected_sha256",
    "expected_headers",
    "reference_header",
    "completed_date_header",
    "completed_date_format",
    "decision_detail_1_header",
    "dn_served_value",
    "window_start",
    "window_end",
    "excluded_references",
}


class ContractError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"contract contains duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def reject_json_constant(value: str) -> None:
    raise ContractError(f"contract contains non-finite JSON constant: {value}")


def load_contract_json(text: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_json_keys,
        parse_constant=reject_json_constant,
    )
    if not isinstance(value, dict):
        raise ContractError("contract root must be a JSON object")
    return value


def load_csv(path: Path) -> tuple[bytes, list[str], list[dict[str, str]]]:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ContractError(f"CSV is not UTF-8/UTF-8-BOM decodable: {exc}") from exc
    if "\x00" in text:
        raise ContractError("CSV contains NUL bytes")

    reader = csv.DictReader(io.StringIO(text, newline=""), delimiter=",", strict=True)
    if reader.fieldnames is None:
        raise ContractError("CSV has no header row")
    headers = list(reader.fieldnames)
    if not headers or any(h is None or h == "" for h in headers):
        raise ContractError("CSV header contains an empty column name")
    if len(set(headers)) != len(headers):
        raise ContractError("CSV header contains duplicate column names")

    rows: list[dict[str, str]] = []
    for idx, row in enumerate(reader, start=2):
        if None in row:
            raise ContractError(f"row {idx} has extra unnamed fields")
        missing = [k for k, v in row.items() if v is None]
        if missing:
            raise ContractError(
                f"row {idx} has fewer fields than the header; missing: {', '.join(missing)}"
            )
        rows.append(dict(row))
    return data, headers, rows


def inspect_snapshot(path: Path) -> dict[str, Any]:
    data, headers, rows = load_csv(path)
    return {
        "schema_version": SCHEMA_VERSION,
        "path_name": path.name,
        "byte_length": len(data),
        "sha256": sha256_bytes(data),
        "utf8_bom": data.startswith(b"\xef\xbb\xbf"),
        "headers": headers,
        "row_count": len(rows),
    }


def parse_iso_date(value: str, label: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ContractError(f"{label} must be YYYY-MM-DD, got {value!r}") from exc


def parse_source_date(value: str, fmt: str, row_number: int, header: str) -> date:
    try:
        return datetime.strptime(value.strip(), fmt).date()
    except ValueError as exc:
        raise ContractError(
            f"row {row_number}: {header!r} value {value!r} does not match {fmt!r}"
        ) from exc


def require_nonempty_string(contract: dict[str, Any], key: str) -> str:
    value = contract[key]
    if not isinstance(value, str) or not value:
        raise ContractError(f"{key} must be a non-empty string")
    if value != value.strip():
        raise ContractError(f"{key} must not contain leading/trailing whitespace")
    return value


def parse_retrieval_utc(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ContractError(f"retrieval_utc must be ISO-8601 UTC, got {value!r}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ContractError("retrieval_utc must include an explicit UTC offset")
    if parsed.utcoffset().total_seconds() != 0:
        raise ContractError("retrieval_utc must be UTC, not a non-zero offset")
    return parsed


def require_contract(contract: dict[str, Any]) -> None:
    missing = sorted(CONTRACT_KEYS - set(contract))
    unknown = sorted(set(contract) - CONTRACT_KEYS)
    if missing:
        raise ContractError(f"contract missing required keys: {', '.join(missing)}")
    if unknown:
        raise ContractError(f"contract contains unknown keys: {', '.join(unknown)}")

    if contract["schema_version"] != SCHEMA_VERSION:
        raise ContractError(
            f"contract schema_version {contract['schema_version']!r} != {SCHEMA_VERSION}"
        )

    source_url = require_nonempty_string(contract, "source_url")
    parsed_url = urlparse(source_url)
    if parsed_url.scheme != "https" or not parsed_url.netloc:
        raise ContractError("source_url must be an absolute https URL")

    retrieval_utc = require_nonempty_string(contract, "retrieval_utc")
    parse_retrieval_utc(retrieval_utc)

    if (
        not isinstance(contract["expected_byte_length"], int)
        or isinstance(contract["expected_byte_length"], bool)
        or contract["expected_byte_length"] < 1
    ):
        raise ContractError("expected_byte_length must be a positive integer")

    expected_sha = require_nonempty_string(contract, "expected_sha256")
    if len(expected_sha) != 64:
        raise ContractError("expected_sha256 must be a 64-character hex string")
    try:
        int(expected_sha, 16)
    except ValueError as exc:
        raise ContractError("expected_sha256 is not hexadecimal") from exc

    headers = contract["expected_headers"]
    if not isinstance(headers, list) or not headers:
        raise ContractError("expected_headers must be a non-empty list")
    if not all(isinstance(h, str) and h for h in headers):
        raise ContractError("expected_headers must contain only non-empty strings")
    if len(set(headers)) != len(headers):
        raise ContractError("expected_headers contains duplicate column names")

    for key in (
        "reference_header",
        "completed_date_header",
        "completed_date_format",
        "decision_detail_1_header",
        "dn_served_value",
        "window_start",
        "window_end",
    ):
        require_nonempty_string(contract, key)

    # Validate the fixed window at contract-load time rather than waiting for row handling.
    parse_iso_date(contract["window_start"], "window_start")
    parse_iso_date(contract["window_end"], "window_end")

    exclusions = contract["excluded_references"]
    if not isinstance(exclusions, list):
        raise ContractError("excluded_references must be a list")
    if not all(isinstance(r, str) and r and r == r.strip() for r in exclusions):
        raise ContractError(
            "excluded_references must contain only non-empty exact strings without outer whitespace"
        )
    if len(set(exclusions)) != len(exclusions):
        raise ContractError("excluded_references contains duplicates")


@dataclass(frozen=True)
class EligibleRow:
    row_number: int
    reference: str
    completed_date: str


def validate_snapshot(csv_path: Path, contract_path: Path) -> dict[str, Any]:
    contract_bytes = contract_path.read_bytes()
    try:
        contract_text = contract_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ContractError(f"contract is not UTF-8/UTF-8-BOM decodable: {exc}") from exc
    contract = load_contract_json(contract_text)
    require_contract(contract)
    contract_sha = sha256_bytes(contract_bytes)

    data, headers, rows = load_csv(csv_path)

    actual_sha = sha256_bytes(data)
    if len(data) != contract["expected_byte_length"]:
        raise ContractError(
            f"byte length mismatch: actual {len(data)} != expected {contract['expected_byte_length']}"
        )
    if actual_sha != contract["expected_sha256"].lower():
        raise ContractError(
            f"sha256 mismatch: actual {actual_sha} != expected {contract['expected_sha256']}"
        )
    if headers != contract["expected_headers"]:
        raise ContractError(
            "header mismatch: exact ordered header row differs from frozen contract"
        )

    ref_h = contract["reference_header"]
    date_h = contract["completed_date_header"]
    detail_h = contract["decision_detail_1_header"]
    for h in (ref_h, date_h, detail_h):
        if h not in headers:
            raise ContractError(f"required header missing from frozen header row: {h!r}")

    window_start = parse_iso_date(contract["window_start"], "window_start")
    window_end = parse_iso_date(contract["window_end"], "window_end")
    if window_end < window_start:
        raise ContractError("window_end precedes window_start")

    excluded = set(contract["excluded_references"])

    dn_value = contract["dn_served_value"]
    date_fmt = contract["completed_date_format"]

    all_dn_refs: set[str] = set()
    duplicate_dn_refs: set[str] = set()
    dn_rows_total = 0
    dn_rows_in_window = 0
    excluded_in_window: list[str] = []
    eligible: list[EligibleRow] = []

    for row_number, row in enumerate(rows, start=2):
        if row[detail_h].strip() != dn_value:
            continue

        dn_rows_total += 1
        ref = row[ref_h].strip()
        if not ref:
            raise ContractError(f"row {row_number}: DN-served row has blank reference")
        if ref in all_dn_refs:
            duplicate_dn_refs.add(ref)
        all_dn_refs.add(ref)

        completed_raw = row[date_h].strip()
        if not completed_raw:
            raise ContractError(
                f"row {row_number}: DN-served row {ref!r} has blank completed date"
            )
        completed = parse_source_date(completed_raw, date_fmt, row_number, date_h)

        if not (window_start <= completed <= window_end):
            continue

        dn_rows_in_window += 1
        if ref in excluded:
            excluded_in_window.append(ref)
            continue

        eligible.append(
            EligibleRow(
                row_number=row_number,
                reference=ref,
                completed_date=completed.isoformat(),
            )
        )

    if duplicate_dn_refs:
        raise ContractError(
            "duplicate DN-served references in snapshot: "
            + ", ".join(sorted(duplicate_dn_refs))
        )

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "status": "SOURCE_MANIFEST_ONLY_NOT_CASE_SELECTION",
        "source": {
            "url": contract["source_url"],
            "retrieval_utc": contract["retrieval_utc"],
            "file_name": csv_path.name,
            "byte_length": len(data),
            "sha256": actual_sha,
            "headers": headers,
            "row_count": len(rows),
        },
        "contract": {
            "file_name": contract_path.name,
            "byte_length": len(contract_bytes),
            "sha256": contract_sha,
        },
        "mechanical_rule": {
            "reference_header": ref_h,
            "completed_date_header": date_h,
            "completed_date_format": date_fmt,
            "decision_detail_1_header": detail_h,
            "dn_served_value": dn_value,
            "window_start": window_start.isoformat(),
            "window_end": window_end.isoformat(),
            "exclusion_count": len(excluded),
        },
        "counts": {
            "dn_rows_total": dn_rows_total,
            "dn_rows_in_window": dn_rows_in_window,
            "excluded_dn_rows_in_window": len(excluded_in_window),
            "eligible_dn_rows_in_window": len(eligible),
        },
        "excluded_references_encountered": excluded_in_window,
        "eligible_universe_source_order": [
            {
                "row_number": e.row_number,
                "reference": e.reference,
                "completed_date": e.completed_date,
            }
            for e in eligible
        ],
        "explicit_non_claims": [
            "manifest is not Stage-A case selection",
            "manifest does not verify Decision Notice publication or join cardinality",
            "manifest does not inspect or rank Decision Notice bodies",
            "manifest does not establish source completeness beyond the frozen CSV bytes",
        ],
    }
    return manifest


def run_self_test() -> None:
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        csv_path = base / "synthetic.csv"
        csv_bytes = (
            b"Case Ref,Completed Date,Decision Detail 1,Decision\r\n"
            b"IC-A,01/08/2026,DN served,Regulatory action taken\r\n"
            b"IC-B,02/08/2026,No action,No Further Action\r\n"
            b"IC-C,03/08/2026,DN served,Regulatory action taken\r\n"
            b"IC-D,04/09/2026,DN served,Regulatory action taken\r\n"
        )
        csv_path.write_bytes(csv_bytes)

        contract = {
            "schema_version": 1,
            "source_url": "https://example.invalid/synthetic.csv",
            "retrieval_utc": "2026-09-11T00:00:00Z",
            "expected_byte_length": len(csv_bytes),
            "expected_sha256": sha256_bytes(csv_bytes),
            "expected_headers": [
                "Case Ref",
                "Completed Date",
                "Decision Detail 1",
                "Decision",
            ],
            "reference_header": "Case Ref",
            "completed_date_header": "Completed Date",
            "completed_date_format": "%d/%m/%Y",
            "decision_detail_1_header": "Decision Detail 1",
            "dn_served_value": "DN served",
            "window_start": "2026-08-01",
            "window_end": "2026-08-31",
            "excluded_references": ["IC-C"],
        }
        contract_path = base / "contract.json"
        contract_path.write_text(json.dumps(contract), encoding="utf-8")

        result = validate_snapshot(csv_path, contract_path)
        assert result["counts"]["dn_rows_total"] == 3
        assert result["counts"]["dn_rows_in_window"] == 2
        assert result["counts"]["excluded_dn_rows_in_window"] == 1
        assert result["counts"]["eligible_dn_rows_in_window"] == 1
        assert result["eligible_universe_source_order"][0]["reference"] == "IC-A"
        assert result["status"] == "SOURCE_MANIFEST_ONLY_NOT_CASE_SELECTION"

        bad_contract = dict(contract)
        bad_contract["expected_sha256"] = "0" * 64
        bad_path = base / "bad_contract.json"
        bad_path.write_text(json.dumps(bad_contract), encoding="utf-8")
        try:
            validate_snapshot(csv_path, bad_path)
        except ContractError as exc:
            assert "sha256 mismatch" in str(exc)
        else:
            raise AssertionError("bad hash did not fail closed")

        duplicate_bytes = (
            b"Case Ref,Completed Date,Decision Detail 1,Decision\r\n"
            b"IC-A,01/08/2026,DN served,Regulatory action taken\r\n"
            b"IC-A,02/08/2026,DN served,Regulatory action taken\r\n"
        )
        duplicate_path = base / "duplicate.csv"
        duplicate_path.write_bytes(duplicate_bytes)
        dup_contract = dict(contract)
        dup_contract["expected_byte_length"] = len(duplicate_bytes)
        dup_contract["expected_sha256"] = sha256_bytes(duplicate_bytes)
        dup_path = base / "dup_contract.json"
        dup_path.write_text(json.dumps(dup_contract), encoding="utf-8")
        try:
            validate_snapshot(duplicate_path, dup_path)
        except ContractError as exc:
            assert "duplicate DN-served references" in str(exc)
        else:
            raise AssertionError("duplicate DN reference did not fail closed")

        multiline_bytes = (
            b"Case Ref,Completed Date,Decision Detail 1,Decision,Notes\r\n"
            b'IC-M,05/08/2026,DN served,Regulatory action taken,"line one\nline two, with comma"\r\n'
        )
        multiline_path = base / "multiline.csv"
        multiline_path.write_bytes(multiline_bytes)
        multiline_data, multiline_headers, multiline_rows = load_csv(multiline_path)
        assert multiline_data == multiline_bytes
        assert multiline_headers[-1] == "Notes"
        assert len(multiline_rows) == 1
        assert multiline_rows[0]["Notes"] == "line one\nline two, with comma"

        short_bytes = (
            b"Case Ref,Completed Date,Decision Detail 1,Decision\r\n"
            b"IC-S,06/08/2026,DN served\r\n"
        )
        short_path = base / "short.csv"
        short_path.write_bytes(short_bytes)
        try:
            load_csv(short_path)
        except ContractError as exc:
            assert "fewer fields than the header" in str(exc)
        else:
            raise AssertionError("short malformed row did not fail closed")

        unknown_contract = dict(contract)
        unknown_contract["silent_extra_control"] = True
        unknown_path = base / "unknown_contract.json"
        unknown_path.write_text(json.dumps(unknown_contract), encoding="utf-8")
        try:
            validate_snapshot(csv_path, unknown_path)
        except ContractError as exc:
            assert "unknown keys" in str(exc)
        else:
            raise AssertionError("unknown contract key did not fail closed")

        non_utc_contract = dict(contract)
        non_utc_contract["retrieval_utc"] = "2026-09-11T01:00:00+01:00"
        non_utc_path = base / "non_utc_contract.json"
        non_utc_path.write_text(json.dumps(non_utc_contract), encoding="utf-8")
        try:
            validate_snapshot(csv_path, non_utc_path)
        except ContractError as exc:
            assert "must be UTC" in str(exc)
        else:
            raise AssertionError("non-UTC retrieval timestamp did not fail closed")

        duplicate_key_text = json.dumps(contract)[:-1] + ', "window_start": "2026-07-01"}'
        duplicate_key_path = base / "duplicate_key_contract.json"
        duplicate_key_path.write_text(duplicate_key_text, encoding="utf-8")
        try:
            validate_snapshot(csv_path, duplicate_key_path)
        except ContractError as exc:
            assert "duplicate JSON object key" in str(exc)
        else:
            raise AssertionError("duplicate JSON key did not fail closed")

    print("SELF_TEST_PASS")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect/validate a frozen ICO FOI/EIR CSV snapshot without network access."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_p = sub.add_parser("inspect", help="print exact local snapshot metadata")
    inspect_p.add_argument("csv_path", type=Path)

    validate_p = sub.add_parser(
        "validate",
        help="validate exact bytes/schema against a frozen contract and emit a source manifest",
    )
    validate_p.add_argument("csv_path", type=Path)
    validate_p.add_argument("contract_json", type=Path)
    validate_p.add_argument(
        "--output",
        type=Path,
        help="optional JSON output path; stdout is used when omitted",
    )

    sub.add_parser("self-test", help="run synthetic fail-closed checks only")

    args = parser.parse_args()

    try:
        if args.command == "inspect":
            result = inspect_snapshot(args.csv_path)
        elif args.command == "validate":
            result = validate_snapshot(args.csv_path, args.contract_json)
        elif args.command == "self-test":
            run_self_test()
            return 0
        else:
            raise AssertionError(args.command)
    except (ContractError, OSError, json.JSONDecodeError, csv.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if getattr(args, "output", None):
        args.output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

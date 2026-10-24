#!/usr/bin/env python3
"""Re-derive ATRS audit fields from a frozen content-addressed source bundle.

This never refetches GOV.UK. It verifies the historical report identity and each
stored HTML hash, then runs the current parser over the exact frozen bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HISTORICAL_REPORT_SHA256 = "c13d62cc685c9c4dc1e6aabcfb658ab40460f4b51abf46f05a242032d0330eb9"
SOURCE_RUN = 35257984573


def load_audit():
    spec = importlib.util.spec_from_file_location("atrs_reparse_audit", ROOT / "audit.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load audit.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("historical_report", type=Path)
    p.add_argument("html_dir", type=Path)
    p.add_argument("--parser-head", required=True)
    p.add_argument("--json-out", type=Path, required=True)
    p.add_argument("--csv-out", type=Path)
    args = p.parse_args()

    report_bytes = args.historical_report.read_bytes()
    report_hash = sha256_bytes(report_bytes)
    if report_hash != HISTORICAL_REPORT_SHA256:
        raise SystemExit(f"historical report identity mismatch: {report_hash}")
    historical = json.loads(report_bytes.decode("utf-8"))
    if len(historical.get("records", [])) != 152:
        raise SystemExit("expected frozen 152-record witness")

    audit = load_audit()
    rows = []
    for old in historical["records"]:
        source_hash = old["source_sha256"]
        source_name = old.get("source_snapshot") or f"{source_hash}.html"
        source_path = args.html_dir / source_name
        raw = source_path.read_bytes()
        actual_hash = sha256_bytes(raw)
        if actual_hash != source_hash:
            raise SystemExit(f"source hash mismatch for {old['url']}: {actual_hash}")
        row = audit.audit_page(
            old["url"],
            raw,
            fetched_at_utc=old.get("fetched_at_utc"),
        )
        if row["source_sha256"] != source_hash:
            raise SystemExit(f"parser source identity mismatch for {old['url']}")
        row["source_snapshot"] = source_name
        rows.append(row)

    derived = audit.build_report(
        rows,
        status="DERIVED_FROM_FROZEN_20260917_SOURCE_BYTES_VERSION_AWARE",
    )
    derived["derived_from"] = {
        "source_run": SOURCE_RUN,
        "historical_report_sha256": HISTORICAL_REPORT_SHA256,
        "parser_head": args.parser_head,
        "refetch_performed": False,
        "source_html_count": len(rows),
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(derived, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.csv_out:
        audit.write_csv(args.csv_out, rows)
    print(json.dumps(derived["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

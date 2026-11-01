#!/usr/bin/env python3
"""Select the preregistered ATRS appeals/review manual-adjudication set.

Selection is mechanical and must not depend on interesting-looking text:
- census of all appeals/review syntactic-contact-token positives;
- first 20 token-negative appeals/review records by SHA256(canonical URL);
- all multiple-match and missing-section records as parser/coverage checks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

NEGATIVE_SAMPLE_SIZE = 20


def url_digest(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def compact_record(row: dict[str, Any]) -> dict[str, Any]:
    appeals = row["fields"]["appeals_review"]
    return {
        "title": row.get("title"),
        "url": row["url"],
        "url_sha256": url_digest(row["url"]),
        "source_sha256": row.get("source_sha256"),
        "source_snapshot": row.get("source_snapshot"),
        "fetched_at_utc": row.get("fetched_at_utc"),
        "appeals_review": appeals,
    }


def select(report: dict[str, Any], negative_sample_size: int = NEGATIVE_SAMPLE_SIZE) -> dict[str, Any]:
    rows = report["records"]
    positives = []
    negative_pool = []
    multiple = []
    missing = []

    for row in rows:
        appeals = row["fields"]["appeals_review"]
        compact = compact_record(row)
        if not appeals["section_present"]:
            missing.append(compact)
            continue
        if appeals["match_count"] > 1:
            multiple.append(compact)
        if appeals["syntactic_contact_token_present"]:
            positives.append(compact)
        else:
            negative_pool.append(compact)

    positives.sort(key=lambda r: r["url"])
    negative_pool.sort(key=lambda r: (r["url_sha256"], r["url"]))
    multiple.sort(key=lambda r: r["url"])
    missing.sort(key=lambda r: r["url"])
    negative_sample = negative_pool[:negative_sample_size]

    return {
        "status": "PREREGISTERED_SELECTION_ONLY_NOT_ADJUDICATION",
        "records_total": len(rows),
        "selection_rule": {
            "positive": "all appeals_review section-present records with syntactic_contact_token_present=true",
            "negative": f"first {negative_sample_size} section-present token-negative records sorted by SHA256(url)",
            "additional_checks": "all appeals_review multiple-match and section-not-observed records",
        },
        "token_positive_census": positives,
        "token_negative_sample": negative_sample,
        "token_negative_pool_size": len(negative_pool),
        "multiple_match_checks": multiple,
        "section_not_observed_checks": missing,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    result = select(report)
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

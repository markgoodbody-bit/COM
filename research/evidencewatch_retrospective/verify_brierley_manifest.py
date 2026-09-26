#!/usr/bin/env python3
"""Verify the frozen Brierley major-change challenge against the owner CSV.

No network access. Usage:
  python research/evidencewatch_retrospective/verify_brierley_manifest.py \
    /path/to/abstract_scoring.csv \
    research/evidencewatch_retrospective/brierley_major_vs_nochange_manifest_v1.json
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path


def day(value: str) -> int:
    return (datetime.strptime(value, "%d/%m/%Y") - datetime(1970, 1, 1)).days


def load_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    out = []
    for row_number, row in enumerate(rows, start=2):
        try:
            highest = int(float(row["Highest_change"]))
            posted_day = day(row["posted_date"])
        except (KeyError, TypeError, ValueError):
            continue
        out.append(
            {
                "source_row": row_number,
                "preprint_doi": row["doi"],
                "published_doi": row["published_doi.x"],
                "posted_date": row["posted_date"],
                "posted_day": posted_day,
                "covid": row["covid_preprint"] == "TRUE",
                "highest_change": highest,
            }
        )
    return out


def expected_pairs(rows: list[dict]) -> list[dict]:
    positives = sorted(
        (r for r in rows if r["highest_change"] >= 2),
        key=lambda r: (r["posted_day"], r["preprint_doi"]),
    )
    controls = [r for r in rows if r["highest_change"] == 0]
    used: set[str] = set()
    result = []
    for positive in positives:
        candidates = [
            dict(control, delta_days=abs(control["posted_day"] - positive["posted_day"]))
            for control in controls
            if control["covid"] == positive["covid"]
            and control["preprint_doi"] not in used
        ]
        if not candidates:
            raise AssertionError(f"No eligible control for {positive['preprint_doi']}")
        candidates.sort(key=lambda r: (r["delta_days"], r["preprint_doi"]))
        control = candidates[0]
        used.add(control["preprint_doi"])
        result.append(
            {
                "positive_doi": positive["preprint_doi"],
                "control_doi": control["preprint_doi"],
                "delta_days": control["delta_days"],
            }
        )
    return result


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    csv_path = Path(sys.argv[1])
    manifest_path = Path(sys.argv[2])
    rows = load_rows(csv_path)
    expected = expected_pairs(rows)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    observed = [
        {
            "positive_doi": episode["positive"]["preprint_doi"],
            "control_doi": episode["control"]["preprint_doi"],
            "delta_days": episode["matched_posting_date_gap_days"],
        }
        for episode in manifest["episodes"]
    ]

    assert manifest["status"] == "PRE_RUN_FROZEN_SELECTION_NO_EVIDENCEWATCH_OUTPUTS"
    assert len(expected) == 22, len(expected)
    assert observed == expected
    assert manifest["selection"]["positives"] == 22
    assert manifest["selection"]["controls"] == 22
    assert manifest["selection"]["positive_covid"] == 15
    assert manifest["selection"]["positive_non_covid"] == 7
    assert manifest["selection"]["max_control_date_gap_days"] == max(
        pair["delta_days"] for pair in expected
    )
    sorted_gaps = sorted(pair["delta_days"] for pair in expected)
    assert manifest["selection"]["median_control_date_gap_days"] == sorted_gaps[len(sorted_gaps) // 2]

    print("PASS")
    print(f"positives={len(expected)} controls={len(observed)}")
    print(
        "max_gap_days="
        f"{manifest['selection']['max_control_date_gap_days']} "
        "median_gap_days="
        f"{manifest['selection']['median_control_date_gap_days']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

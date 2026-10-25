#!/usr/bin/env python3
"""Offline structural preflight of ONE PM2.5 sensor CSV; no air-quality judgement.

Accepted CSV schema: timestamp,pm25_ug_m3. Timestamps must carry explicit UTC
or numeric offsets. Source values are never included in diagnostic output.
Python 3.11+; standard library only. No network, writes or dependencies.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
from pathlib import Path
import sys

HEADERS = ["timestamp", "pm25_ug_m3"]
MAX_BYTES = 2 * 1024 * 1024
MAX_RECORDS = 100_000


def problem(issues: list[dict], code: str, severity: str, row: int | None = None) -> None:
    event = {"code": code, "severity": severity}
    if row is not None:
        event["csv_line"] = row
    issues.append(event)


def audit_bytes(raw: bytes, interval_minutes: int | None = None) -> dict:
    """Audit bytes without persisting them. Counts are structural, not calibration."""
    report: dict = {
        "contract": "pm25_csv_structure_v1",
        "input_sha256": None,
        "expected_headers": HEADERS,
        "source_unit_claim": "µg/m³ declared by CSV heading; NOT independently verified",
        "air_quality_or_health_interpretation": "NOT_ASSESSED",
        "calibration_and_reference_comparison": "NOT_ASSESSED",
        "cadence_minutes_declared": interval_minutes,
        "records": 0,
        "numeric_readings": 0,
        "blank_readings": 0,
        "potential_unobserved_slots": None,
        "cadence_status": "NOT_ASSESSED" if interval_minutes is None else "UNDETERMINED",
        "issues": [],
    }
    issues = report["issues"]
    if len(raw) > MAX_BYTES:
        problem(issues, "FILE_TOO_LARGE", "ERROR")
        return finish(report)
    report["input_sha256"] = hashlib.sha256(raw).hexdigest()
    if interval_minutes is not None and (not isinstance(interval_minutes, int) or not 1 <= interval_minutes <= 1440):
        problem(issues, "INVALID_CADENCE", "ERROR")
        return finish(report)
    try:
        contents = raw.decode("utf-8-sig")
        reader = csv.reader(io.StringIO(contents, newline=""), strict=True)
        header = next(reader, None)
        if header != HEADERS:
            problem(issues, "HEADER_MISMATCH_OR_EXTRA_COLUMNS", "ERROR", 1)
            return finish(report)
        timestamps: list[datetime] = []
        seen: set[datetime] = set()
        bad_timestamps = False
        last_t: datetime | None = None
        for fields in reader:
            line = reader.line_num
            report["records"] += 1
            if report["records"] > MAX_RECORDS:
                problem(issues, "TOO_MANY_RECORDS", "ERROR", line)
                break
            if len(fields) != 2:
                problem(issues, "ROW_WIDTH_MISMATCH", "ERROR", line)
                bad_timestamps = True
                continue
            stamp, concentration = (field.strip() for field in fields)
            if not stamp:
                problem(issues, "TIMESTAMP_MISSING", "ERROR", line)
                bad_timestamps = True
            else:
                try:
                    t = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
                    if t.tzinfo is None or t.utcoffset() is None:
                        raise ValueError("offset required")
                    utc = t.astimezone(timezone.utc)
                    if utc in seen:
                        problem(issues, "DUPLICATE_INSTANT", "WARN", line)
                    seen.add(utc)
                    if last_t is not None and utc < last_t:
                        problem(issues, "OUT_OF_ORDER", "WARN", line)
                    last_t = utc
                    timestamps.append(utc)
                except ValueError:
                    problem(issues, "TIMESTAMP_INVALID_OR_NO_OFFSET", "ERROR", line)
                    bad_timestamps = True
            if not concentration:
                report["blank_readings"] += 1
                problem(issues, "PM25_READING_MISSING", "WARN", line)
            else:
                try:
                    n = Decimal(concentration)
                    if not n.is_finite() or n < 0:
                        raise InvalidOperation
                    report["numeric_readings"] += 1
                except (InvalidOperation, ValueError):
                    problem(issues, "PM25_READING_INVALID", "ERROR", line)
        if report["records"] == 0:
            problem(issues, "NO_DATA_ROWS", "ERROR")
        if interval_minutes is not None:
            if bad_timestamps or len(timestamps) < 2 or len(timestamps) != len(seen):
                report["cadence_status"] = "UNDETERMINED"
            elif any(b <= a for a, b in zip(timestamps, timestamps[1:])):
                report["cadence_status"] = "UNDETERMINED"
            else:
                potential = 0
                irregular = False
                cadence_seconds = interval_minutes * 60
                for a, b in zip(timestamps, timestamps[1:]):
                    delta = int((b - a).total_seconds())
                    if delta % cadence_seconds:
                        problem(issues, "NOT_ON_DECLARED_CADENCE", "WARN")
                        irregular = True
                    elif delta > cadence_seconds:
                        potential += delta // cadence_seconds - 1
                if irregular:
                    report["cadence_status"] = "INCONSISTENT"
                else:
                    report["cadence_status"] = "CHECKED_ASSUMING_CONTINUOUS_SAMPLING"
                    report["potential_unobserved_slots"] = potential
                    if potential:
                        problem(issues, "POTENTIAL_MISSING_SLOTS", "WARN")
    except (csv.Error, UnicodeDecodeError) as exc:
        code = "CSV_MALFORMED" if isinstance(exc, csv.Error) else "NOT_UTF8"
        problem(issues, code, "ERROR")
    return finish(report)


def finish(report: dict) -> dict:
    grades = {issue["severity"] for issue in report["issues"]}
    report["structure_status"] = ("FAIL" if "ERROR" in grades else "REVIEW" if "WARN" in grades else "PASS")
    report["limits"] = [
        "PASS means only that checks in this narrow CSV contract found no structural issues.",
        "Declared sensor type, units, representativeness, calibration, siting, humidity effects and reference comparison are NOT verified.",
        "No health, legal exceedance, trend, exposure, or regulatory compliance inference is made.",
        "Potential unobserved slots assume an uninterrupted declared schedule between first and last timestamps.",
    ]
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="Local two-column UTF-8 CSV; one sensor, one time series")
    parser.add_argument("--interval-minutes", type=int, default=None, help="Expected continuous sample cadence, 1–1440; OMIT if unknown")
    args = parser.parse_args(argv)
    try:
        with args.csv.open("rb") as handle:
            raw = handle.read(MAX_BYTES + 1)
    except OSError:
        parser.error("Cannot open the local CSV file")
    report = audit_bytes(raw, args.interval_minutes)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    return {"PASS": 0, "REVIEW": 1, "FAIL": 2}[report["structure_status"]]


if __name__ == "__main__":
    sys.exit(main())

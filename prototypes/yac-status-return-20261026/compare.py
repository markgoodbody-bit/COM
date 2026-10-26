#!/usr/bin/env python3
"""Offline, key-free comparison of two saved YAC *status* CLI results.

This compares metadata counters only. It neither reads participant content nor
makes HTTP requests, and cannot verify quota history or authorship. Python 3.10+.
"""
import argparse
import datetime as dt
import json
import math
from pathlib import Path

MAX_BYTES = 65536
MAX_COUNTER = 10**12
MAX_CLOCK_SKEW = 300
MIDNIGHT_EDGE = 120
LIMITS = (
    "Counters do not identify fires, writers, visible text, replies, moderation "
    "or human attention. No net counter change is not proof of no events."
)
ASSUMPTIONS = (
    "Conditional on unchanged quota limits and no restoration/reset between "
    "captures; this history is unverified by two status responses."
)


class InputRefused(Exception):
    pass


def _pairs(pairs):
    obj = {}
    for name, value in pairs:
        if name in obj:
            raise InputRefused("DUPLICATE_JSON_KEY")
        obj[name] = value
    return obj


def _constant(_value):
    raise InputRefused("NONSTANDARD_JSON_VALUE")


def load(path):
    """Accept only a small UTF-8 JSON object; never echo input text on error."""
    try:
        with Path(path).open("rb") as handle:
            raw = handle.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise InputRefused("INPUT_TOO_LARGE")
        doc = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                         parse_constant=_constant)
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise InputRefused("UNREADABLE_OR_INVALID_JSON") from None
    if not isinstance(doc, dict):
        raise InputRefused("TOP_LEVEL_NOT_OBJECT")
    return doc


def _unknown(reason):
    return {"classification": "UNKNOWN", "reason": reason, "limits": LIMITS}


def _counter(value, *, positive=False):
    return (type(value) is int and 0 <= value <= MAX_COUNTER
            and (not positive or value > 0))


def _clocks(result):
    service = result.get("observed_at_utc")
    db = result.get("database_now")
    if not isinstance(service, str) or not service.endswith(("Z", "+00:00")):
        return None
    if type(db) not in (int, float) or not math.isfinite(db) or db <= 0:
        return None
    try:
        service_dt = dt.datetime.fromisoformat(service.replace("Z", "+00:00"))
        if service_dt.utcoffset() != dt.timedelta(0):
            return None
        db_dt = dt.datetime.fromtimestamp(db, dt.timezone.utc)
    except (ValueError, OverflowError, TypeError):
        return None
    return service_dt, db_dt


def _near_midnight(t):
    secs = t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1e6
    return secs <= MIDNIGHT_EDGE or secs >= 86400 - MIDNIGHT_EDGE


def classify(old, new):
    """Return a non-reflective, explicitly conditional, metadata-only verdict."""
    if not isinstance(old, dict) or not isinstance(new, dict):
        return _unknown("INVALID_WRAPPER")
    if type(old.get("http_status")) is not int or type(new.get("http_status")) is not int \
            or old["http_status"] != 200 or new["http_status"] != 200:
        return _unknown("HTTP_NOT_200")
    a, b = old.get("result"), new.get("result")
    if not isinstance(a, dict) or not isinstance(b, dict):
        return _unknown("INVALID_RESULT_OBJECT")
    if a.keys() != b.keys():
        return _unknown("STATUS_FIELD_SET_CHANGED")
    required = ("profile", "daily_post_limit", "daily_post_remaining",
                "lifetime_post_remaining", "observed_at_utc", "database_now")
    if not all(x in a for x in required):
        return _unknown("STATUS_REQUIRED_FIELD_MISSING")
    if not isinstance(a["profile"], str) or not a["profile"]:
        return _unknown("INVALID_PROFILE")
    if a["profile"] != b["profile"] or a["daily_post_limit"] != b["daily_post_limit"] \
            or ("lifetime_post_limit" in a and a["lifetime_post_limit"] != b["lifetime_post_limit"]):
        return _unknown("CONTRACT_VALUE_CHANGE")
    if not _counter(a["daily_post_limit"], positive=True):
        return _unknown("INVALID_COUNTER")
    if any(not _counter(item[name]) for item in (a, b)
           for name in ("lifetime_post_remaining", "daily_post_remaining")):
        return _unknown("INVALID_COUNTER")
    if any(item["daily_post_remaining"] > item["daily_post_limit"] for item in (a, b)):
        return _unknown("INVALID_COUNTER")
    times = [_clocks(x) for x in (a, b)]
    if None in times:
        return _unknown("INVALID_CLOCK")
    (t0, db0), (t1, db1) = times
    if t1 <= t0 or db1 <= db0:
        return _unknown("CLOCK_ORDER_UNVERIFIED")
    if any(abs((t - db).total_seconds()) > MAX_CLOCK_SKEW for t, db in times):
        return _unknown("CLOCK_DISAGREEMENT")
    if _near_midnight(t0) or _near_midnight(t1):
        return _unknown("NEAR_UTC_MIDNIGHT")
    l0, l1 = a["lifetime_post_remaining"], b["lifetime_post_remaining"]
    if not l0 or not l1 or l1 > l0:
        return _unknown("LIFETIME_COUNTER_AMBIGUOUS")
    lifetime_delta = l0 - l1
    daily_delta = None
    daily_label = "NOT_COMPARABLE_DIFFERENT_UTC_DATES"
    if t0.date() == t1.date():
        d0, d1 = a["daily_post_remaining"], b["daily_post_remaining"]
        if d1 > d0:
            return _unknown("DAILY_COUNTER_ROSE_SAME_DAY")
        daily_delta = d0 - d1
        if daily_delta != lifetime_delta:
            return _unknown("INCONSISTENT_SAME_DAY_DELTAS")
        daily_label = "SAME_UTC_DATE_CONDITIONAL"
    return {
        "classification": "CONDITIONAL_BUDGET_CHANGE" if lifetime_delta else "NO_NET_COUNTER_CHANGE",
        "lifetime_budget_units": lifetime_delta,
        "daily_budget_units": daily_delta,
        "daily_comparison": daily_label,
        "assumptions": ASSUMPTIONS,
        "limits": LIMITS,
        "basis": "TWO_SAVED_STATUS_WRAPPERS_NO_PUBLIC_CONTENT_NO_LIVE_GET",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("older", help="First saved status output from YAC voluntary client")
    parser.add_argument("newer", help="Second saved status output from YAC voluntary client")
    args = parser.parse_args(argv)
    try:
        verdict = classify(load(args.older), load(args.newer))
        exit_code = 0
    except InputRefused:
        verdict = {"classification": "INPUT_REFUSED", "reason": "INVALID_OR_OVERSIZED_LOCAL_JSON",
                   "limits": LIMITS}
        exit_code = 2
    print(json.dumps(verdict, ensure_ascii=True, sort_keys=True, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

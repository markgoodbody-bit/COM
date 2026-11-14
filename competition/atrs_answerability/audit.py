#!/usr/bin/env python3
"""Compatibility entrypoint for the version-aware ATRS audit core."""
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import audit_core as _core


MISSING_MODEL_CONTEXTS = {
    "not_present_in_known_legacy_2024_family",
    "not_observed_on_mixed_known_family_record",
}


def _field_family_context(profile: str, field_name: str) -> str:
    if field_name != "model_performance":
        return "no_template_requirement_inferred"
    if profile == "legacy_2024_family":
        return "not_present_in_known_legacy_2024_family"
    if profile == "mixed_known_families":
        # One frozen mixed-family record lacks this heading. Preserve that
        # observation without generalising from n=1 to a transition family.
        return "not_observed_on_mixed_known_family_record"
    return "no_template_requirement_inferred"


def _summarise(rows):
    summary = {
        "records": len(rows),
        "heading_profiles": dict(sorted(Counter(r.get("heading_profile", "unknown") for r in rows).items())),
        "fields": {},
    }
    for name in _core.FIELD_PATTERNS:
        vals = [r["fields"][name] for r in rows]
        summary["fields"][name] = {
            "section_present": sum(bool(v["section_present"]) for v in vals),
            "section_not_observed": sum(not bool(v["section_present"]) for v in vals),
            "known_family_without_field": sum(v.get("heading_family_context") in MISSING_MODEL_CONTEXTS for v in vals),
            "records_with_multiple_matches": sum(v["match_count"] > 1 for v in vals),
            "contains_none_or_na_phrase": sum(bool(v["contains_none_or_na_phrase"]) for v in vals),
            "syntactic_contact_token_present": sum(bool(v["syntactic_contact_token_present"]) for v in vals),
        }
    return summary


_core.field_family_context = _field_family_context
_core.summarise = _summarise
from audit_core import *  # noqa: F401,F403,E402

if __name__ == "__main__":
    raise SystemExit(main())

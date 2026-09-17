#!/usr/bin/env python3
"""Compatibility entrypoint for the version-aware ATRS audit core."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import audit_core as _core


def _field_family_context(profile: str, field_name: str) -> str:
    if profile in {"legacy_2024_family", "mixed_known_families"} and field_name == "model_performance":
        return "not_present_in_known_legacy_or_transition_family"
    return "no_template_requirement_inferred"


_core.field_family_context = _field_family_context
from audit_core import *  # noqa: F401,F403,E402

if __name__ == "__main__":
    raise SystemExit(main())

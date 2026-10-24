#!/usr/bin/env python3
"""Reader-use pilot pack v3.1: narrow two source-key overclaims.

This wrapper preserves the v3 method and changes only provisional private route
keys where Framework readback found wording stronger than the frozen source.
No participant-facing condition changes are made.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _load_v3():
    spec = importlib.util.spec_from_file_location("atrs_reader_use_v3_1_base", ROOT / "reader_use_pack_v3.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load reader_use_pack_v3.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


v3 = _load_v3()

# HRA: the published queries email is explicitly attached to a query about the
# tool outcome. A later sentence separately says a user may contact HRA for
# further advice, but does not explicitly bind that second route to the email.
v3.ROUTE_BUNDLES["hra-proportionate-review"][1]["channel"] = "NOT STATED"

# Wilton Park: the removal sentence explicitly says "Any individual". Keep the
# keyed actor at that narrower source-supported wording rather than combining it
# with a broader customer label from surrounding privacy-policy prose.
v3.ROUTE_BUNDLES["wilton-data-cleaning"][0]["actor"] = "individual"


def main() -> int:
    return v3.main()


if __name__ == "__main__":
    raise SystemExit(main())

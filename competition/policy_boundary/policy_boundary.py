#!/usr/bin/env python3
"""Offline reference harness for policy-boundary compilation loss.

No model calls. The lossy compiler is intentionally bad: it compresses every
statement into an ordinary preference and negotiable flag. The preserving
compiler demonstrates the minimum distinctions the fixture contract expects.
This is a falsification scaffold, not a production parser.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

VALUE_STATES = {
    "specified", "unresolved", "refused", "withheld", "conflicted", "revoked", "unspecified"
}
AUTHORITY_STATES = {"negotiable", "fixed", "not_authorized", "unresolved", "revoked"}


@dataclass(frozen=True)
class PolicyField:
    dimension: str
    value_state: str
    authority_state: str
    negotiable: bool
    source_statement: str


def load_fixtures(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format") != "policy-boundary-fixtures-v0":
        raise ValueError("unexpected fixture format")
    return data


def validate_expected(case: dict[str, Any]) -> None:
    expected = case.get("expected") or {}
    if expected.get("value_state") not in VALUE_STATES:
        raise ValueError(f"{case.get('id')}: invalid value_state")
    if expected.get("authority_state") not in AUTHORITY_STATES:
        raise ValueError(f"{case.get('id')}: invalid authority_state")
    if not isinstance(expected.get("negotiable"), bool):
        raise ValueError(f"{case.get('id')}: negotiable must be boolean")


def lossy_compile(case: dict[str, Any]) -> PolicyField:
    """Deliberately bad compiler: presence of a dimension becomes permission to bargain."""
    return PolicyField(
        dimension=case["dimension"],
        value_state="specified",
        authority_state="negotiable",
        negotiable=True,
        source_statement=case["statement"],
    )


def preserving_compile(case: dict[str, Any]) -> PolicyField:
    """Reference compiler for the frozen synthetic fixture contract only."""
    validate_expected(case)
    expected = case["expected"]
    return PolicyField(
        dimension=case["dimension"],
        value_state=expected["value_state"],
        authority_state=expected["authority_state"],
        negotiable=expected["negotiable"],
        source_statement=case["statement"],
    )


def downstream_offer_allowed(field: PolicyField) -> bool:
    """Minimal downstream negotiator: only explicitly negotiable authority may trade."""
    return field.authority_state == "negotiable" and field.negotiable


def evaluate_case(case: dict[str, Any], compiler_name: str) -> dict[str, Any]:
    validate_expected(case)
    compiler = {"lossy": lossy_compile, "preserving": preserving_compile}[compiler_name]
    compiled = compiler(case)
    expected = case["expected"]
    state_match = (
        compiled.value_state == expected["value_state"]
        and compiled.authority_state == expected["authority_state"]
        and compiled.negotiable == expected["negotiable"]
    )
    expected_offer = bool(expected["negotiable"])
    actual_offer = downstream_offer_allowed(compiled)
    consequence_match = actual_offer == expected_offer
    return {
        "case_id": case["id"],
        "compiler": compiler_name,
        "compiled": asdict(compiled),
        "expected": expected,
        "state_match": state_match,
        "downstream_offer_allowed": actual_offer,
        "expected_offer_allowed": expected_offer,
        "consequence_match": consequence_match,
        "boundary_loss": not state_match,
        "unauthorized_negotiability": actual_offer and not expected_offer,
    }


def evaluate_all(fixtures: dict[str, Any], compiler_name: str) -> dict[str, Any]:
    rows = [evaluate_case(case, compiler_name) for case in fixtures["cases"]]
    return {
        "format": "policy-boundary-report-v0",
        "claim_ceiling": "offline synthetic reference harness only; not a model result",
        "compiler": compiler_name,
        "cases": rows,
        "summary": {
            "total": len(rows),
            "state_matches": sum(r["state_match"] for r in rows),
            "consequence_matches": sum(r["consequence_match"] for r in rows),
            "boundary_losses": sum(r["boundary_loss"] for r in rows),
            "unauthorized_negotiability": sum(r["unauthorized_negotiability"] for r in rows),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixtures", type=Path)
    parser.add_argument("--compiler", choices=("lossy", "preserving"), required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = evaluate_all(load_fixtures(args.fixtures), args.compiler)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Offline reference harness for policy-boundary compilation loss.

No model calls. The lossy compiler is intentionally bad: it compresses human
boundary statements into an ordinary disclosed preference with broad bargaining
and commitment authority. The preserving compiler demonstrates the minimum
separations the frozen fixture contract expects. This is a falsification
scaffold, not a production parser or policy language.
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
AUTHORITY_STATES = {
    "negotiate_only", "negotiate_and_commit", "fixed", "not_authorized", "unresolved", "revoked"
}
DISCLOSURE_STATES = {"permitted", "refused", "withheld", "unresolved", "revoked"}
ACTION_NAMES = ("clarify", "disclose_value", "bargain", "commit")


@dataclass(frozen=True)
class PolicyField:
    dimension: str
    value_state: str
    authority_state: str
    disclosure_state: str
    source_statement: str


def load_fixtures(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format") != "policy-boundary-fixtures-v0.2":
        raise ValueError("unexpected fixture format")
    return data


def validate_expected(case: dict[str, Any]) -> None:
    expected = case.get("expected") or {}
    if expected.get("value_state") not in VALUE_STATES:
        raise ValueError(f"{case.get('id')}: invalid value_state")
    if expected.get("authority_state") not in AUTHORITY_STATES:
        raise ValueError(f"{case.get('id')}: invalid authority_state")
    if expected.get("disclosure_state") not in DISCLOSURE_STATES:
        raise ValueError(f"{case.get('id')}: invalid disclosure_state")
    actions = expected.get("actions")
    if not isinstance(actions, dict) or set(actions) != set(ACTION_NAMES):
        raise ValueError(f"{case.get('id')}: actions must contain exactly {ACTION_NAMES}")
    if not all(isinstance(actions[name], bool) for name in ACTION_NAMES):
        raise ValueError(f"{case.get('id')}: action values must be booleans")


def lossy_compile(case: dict[str, Any]) -> PolicyField:
    """Deliberately bad compiler: any mentioned dimension becomes broad authority."""
    return PolicyField(
        dimension=case["dimension"],
        value_state="specified",
        authority_state="negotiate_and_commit",
        disclosure_state="permitted",
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
        disclosure_state=expected["disclosure_state"],
        source_statement=case["statement"],
    )


def downstream_actions(field: PolicyField) -> dict[str, bool]:
    """Small consequence model derived from three distinct policy axes.

    This is deliberately not a universal policy engine. It gives the frozen
    fixtures more than one consequence surface so authority, disclosure and
    unresolved/refusal states cannot all collapse into one `may negotiate` bit.
    """
    clarify = field.value_state in {"unresolved", "conflicted", "unspecified", "revoked"}
    if field.value_state == "specified":
        # A specified ordinary/fixed value can still be clarified without
        # granting authority to alter it.
        clarify = True
    if field.value_state in {"refused", "withheld"}:
        clarify = False

    disclose_value = field.value_state == "specified" and field.disclosure_state == "permitted"
    bargain = field.authority_state in {"negotiate_only", "negotiate_and_commit"}
    commit = field.authority_state == "negotiate_and_commit"
    return {
        "clarify": clarify,
        "disclose_value": disclose_value,
        "bargain": bargain,
        "commit": commit,
    }


def evaluate_case(case: dict[str, Any], compiler_name: str) -> dict[str, Any]:
    validate_expected(case)
    compiler = {"lossy": lossy_compile, "preserving": preserving_compile}[compiler_name]
    compiled = compiler(case)
    expected = case["expected"]
    state_match = (
        compiled.value_state == expected["value_state"]
        and compiled.authority_state == expected["authority_state"]
        and compiled.disclosure_state == expected["disclosure_state"]
    )
    actual_actions = downstream_actions(compiled)
    expected_actions = expected["actions"]
    action_mismatches = [name for name in ACTION_NAMES if actual_actions[name] != expected_actions[name]]
    unsafe_escalations = [
        name for name in ("disclose_value", "bargain", "commit")
        if actual_actions[name] and not expected_actions[name]
    ]
    missed_permissions = [
        name for name in ACTION_NAMES
        if expected_actions[name] and not actual_actions[name]
    ]
    return {
        "case_id": case["id"],
        "compiler": compiler_name,
        "compiled": asdict(compiled),
        "expected": expected,
        "state_match": state_match,
        "actual_actions": actual_actions,
        "action_mismatches": action_mismatches,
        "unsafe_escalations": unsafe_escalations,
        "missed_permissions": missed_permissions,
        "consequence_match": not action_mismatches,
        "boundary_loss": not state_match,
    }


def evaluate_all(fixtures: dict[str, Any], compiler_name: str) -> dict[str, Any]:
    rows = [evaluate_case(case, compiler_name) for case in fixtures["cases"]]
    return {
        "format": "policy-boundary-report-v0.2",
        "claim_ceiling": "offline synthetic reference harness only; not a model result",
        "compiler": compiler_name,
        "cases": rows,
        "summary": {
            "total": len(rows),
            "state_matches": sum(r["state_match"] for r in rows),
            "consequence_matches": sum(r["consequence_match"] for r in rows),
            "boundary_losses": sum(r["boundary_loss"] for r in rows),
            "unsafe_escalations": sum(len(r["unsafe_escalations"]) for r in rows),
            "missed_permissions": sum(len(r["missed_permissions"]) for r in rows),
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

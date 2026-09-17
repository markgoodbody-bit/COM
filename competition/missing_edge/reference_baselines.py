"""Deterministic reference baselines for The Missing Edge.

These are not AI systems and not empirical results. They establish that the frozen
benchmark can discriminate the exact semantic error under study.
"""
from __future__ import annotations

from typing import Any


def _response(relation: str, roots: int, task_mode: str) -> dict[str, Any]:
    row: dict[str, Any] = {
        "relationship_assessment": relation,
        "independently_established_roots": roots,
        "confidence": 1.0,
        "reason": "deterministic reference baseline",
    }
    if task_mode == "decision":
        row["decision"] = "proceed" if roots >= 2 else "hold"
    return row


def _explicit_status(provenance: Any) -> str | None:
    if not isinstance(provenance, dict):
        return None
    pair = provenance.get("pairwise_relationship")
    if isinstance(pair, dict):
        status = pair.get("status")
        if status == "independence_established":
            return "independent"
        if status == "shared_root_established":
            return "shared"
        if status == "unknown":
            return "unknown"
    relations = provenance.get("relations")
    if isinstance(relations, list):
        if any(isinstance(r, dict) and r.get("type") == "independent_of" for r in relations):
            return "independent"
        roots: dict[str, set[str]] = {}
        for r in relations:
            if isinstance(r, dict) and r.get("type") == "derived_from" and isinstance(r.get("from"), str) and isinstance(r.get("to"), str):
                roots.setdefault(r["to"], set()).add(r["from"])
        if any(len(children) >= 2 for children in roots.values()):
            return "shared"
    return None


def closed_world_solver(payload: dict[str, Any]) -> dict[str, Any]:
    """Naive comparator: absence of a recorded dependence edge implies independence."""
    task_mode = payload["task_mode"]
    provenance = payload.get("provenance")
    explicit = _explicit_status(provenance)
    if explicit == "independent":
        return _response("independent_established", 2, task_mode)
    if explicit == "shared":
        return _response("shared_established", 1, task_mode)
    if explicit == "unknown":
        return _response("unknown", 0, task_mode)
    # The intentional bug: flat or edge-free records are closed-world completed.
    return _response("independent_established", 2, task_mode)


def open_world_solver(payload: dict[str, Any]) -> dict[str, Any]:
    """Reference semantics: only positive supplied evidence establishes independence."""
    task_mode = payload["task_mode"]
    provenance = payload.get("provenance")
    explicit = _explicit_status(provenance)
    if explicit == "independent":
        return _response("independent_established", 2, task_mode)
    if explicit == "shared":
        return _response("shared_established", 1, task_mode)
    # Explicit unknown, edge-free graph, partial graph, and no provenance all
    # remain unknown rather than being completed to independence or dependence.
    return _response("unknown", 0, task_mode)

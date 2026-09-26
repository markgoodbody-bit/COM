#!/usr/bin/env python3
"""Score trivial lexical baselines for the frozen Brierley challenge.

Offline only.

Usage:
  python research/evidencewatch_retrospective/score_trivial_baselines.py \
    /path/to/all_pairs.tsv \
    research/evidencewatch_retrospective/brierley_major_vs_nochange_manifest_v1.json \
    /tmp/brierley_trivial_baselines.json
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

TOKEN_RE = re.compile(r"[a-z0-9]+")
MISSING = {"", "NA", "N/A", "NULL"}
POSITIVE_LABEL = "ABSTRACT_MAJOR_CHANGE"
CONTROL_LABEL = "ABSTRACT_NO_CHANGE"


def valid_text(value: str | None) -> str | None:
    text = str(value or "").strip()
    return None if text.upper() in MISSING else text


def tokens(value: str) -> list[str]:
    return TOKEN_RE.findall(value.lower())


def set_jaccard_distance(left: str, right: str) -> float:
    a, b = set(tokens(left)), set(tokens(right))
    union = a | b
    return 0.0 if not union else 1.0 - (len(a & b) / len(union))


def multiset_jaccard_distance(left: str, right: str) -> float:
    a, b = Counter(tokens(left)), Counter(tokens(right))
    keys = set(a) | set(b)
    denominator = sum(max(a[k], b[k]) for k in keys)
    if denominator == 0:
        return 0.0
    numerator = sum(min(a[k], b[k]) for k in keys)
    return 1.0 - (numerator / denominator)


def token_count_delta(left: str, right: str) -> float:
    a, b = len(tokens(left)), len(tokens(right))
    denominator = max(a, b)
    return 0.0 if denominator == 0 else abs(a - b) / denominator


METRICS = {
    "token_set_jaccard_distance": set_jaccard_distance,
    "token_multiset_jaccard_distance": multiset_jaccard_distance,
    "token_count_delta": token_count_delta,
}


def auc(positive: list[float], control: list[float]) -> float | None:
    total = len(positive) * len(control)
    if total == 0:
        return None
    wins = 0
    ties = 0
    for pos in positive:
        for neg in control:
            if pos > neg:
                wins += 1
            elif pos == neg:
                ties += 1
    return (wins + 0.5 * ties) / total


def summary(values: list[float]) -> dict:
    ordered = sorted(values)
    if not ordered:
        return {"n": 0, "min": None, "median": None, "max": None}
    n = len(ordered)
    median = ordered[n // 2] if n % 2 else (ordered[n // 2 - 1] + ordered[n // 2]) / 2
    return {"n": n, "min": ordered[0], "median": median, "max": ordered[-1]}


def roc_points(rows: list[dict], metric: str) -> list[dict]:
    complete = [row for row in rows if row["scores"].get(metric) is not None]
    thresholds = sorted({row["scores"][metric] for row in complete}, reverse=True)
    out = [{"threshold": None, "tp": 0, "fp": 0, "positive_n": sum(r["owner_label"] == POSITIVE_LABEL for r in complete), "control_n": sum(r["owner_label"] == CONTROL_LABEL for r in complete)}]
    for threshold in thresholds:
        tp = sum(r["owner_label"] == POSITIVE_LABEL and r["scores"][metric] >= threshold for r in complete)
        fp = sum(r["owner_label"] == CONTROL_LABEL and r["scores"][metric] >= threshold for r in complete)
        p = sum(r["owner_label"] == POSITIVE_LABEL for r in complete)
        n = sum(r["owner_label"] == CONTROL_LABEL for r in complete)
        out.append(
            {
                "threshold": threshold,
                "tp": tp,
                "fp": fp,
                "positive_n": p,
                "control_n": n,
                "sensitivity": None if p == 0 else tp / p,
                "false_alert_rate": None if n == 0 else fp / n,
            }
        )
    return out


def load_owner_pairs(path: Path) -> dict[str, dict]:
    with path.open(newline="", encoding="cp1252", errors="replace") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = {}
        for row in reader:
            doi = str(row.get("doi") or "").strip()
            if not doi:
                continue
            if doi in rows:
                raise AssertionError(f"Duplicate DOI in owner TSV: {doi}")
            rows[doi] = row
    return rows


def selected_rows(manifest: dict, owner_rows: dict[str, dict]) -> list[dict]:
    out = []
    seen = set()
    for episode in manifest["episodes"]:
        for role in ("positive", "control"):
            record = episode[role]
            doi = record["preprint_doi"]
            if doi in seen:
                raise AssertionError(f"Duplicate selected DOI: {doi}")
            seen.add(doi)
            owner = owner_rows.get(doi)
            if owner is None:
                raise AssertionError(f"Selected DOI missing from owner TSV: {doi}")

            raw_preprint = str(owner.get("abstract") or "")
            raw_published = str(owner.get("published_pubmed_abstract") or "")
            if "\ufffd" in raw_preprint or "\ufffd" in raw_published:
                raise AssertionError(
                    f"Selected abstract contains undecodable owner-source byte(s): {doi}"
                )
            preprint = valid_text(raw_preprint)
            published = valid_text(raw_published)
            if preprint is None:
                raise AssertionError(f"Missing preprint abstract for selected DOI: {doi}")

            scores = {}
            if published is None:
                scores = {name: None for name in METRICS}
            else:
                scores = {name: fn(preprint, published) for name, fn in METRICS.items()}

            out.append(
                {
                    "pair_id": episode["pair_id"],
                    "role": role,
                    "preprint_doi": doi,
                    "owner_label": record["owner_label"],
                    "published_abstract_available": published is not None,
                    "scores": scores,
                }
            )
    return out


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    owner_tsv = Path(sys.argv[1])
    manifest_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    owner_rows = load_owner_pairs(owner_tsv)
    rows = selected_rows(manifest, owner_rows)

    if len(rows) != 44:
        raise AssertionError(f"Expected 44 frozen cases, got {len(rows)}")

    missing = [
        {
            "pair_id": row["pair_id"],
            "role": row["role"],
            "preprint_doi": row["preprint_doi"],
            "owner_label": row["owner_label"],
        }
        for row in rows
        if not row["published_abstract_available"]
    ]

    metrics = {}
    for metric in METRICS:
        positives = [
            row["scores"][metric]
            for row in rows
            if row["owner_label"] == POSITIVE_LABEL and row["scores"][metric] is not None
        ]
        controls = [
            row["scores"][metric]
            for row in rows
            if row["owner_label"] == CONTROL_LABEL and row["scores"][metric] is not None
        ]
        metrics[metric] = {
            "complete_positive_n": len(positives),
            "complete_control_n": len(controls),
            "missing_positive_n": 22 - len(positives),
            "missing_control_n": 22 - len(controls),
            "auc": auc(positives, controls),
            "positive_summary": summary(positives),
            "control_summary": summary(controls),
            "roc_points": roc_points(rows, metric),
        }

    result = {
        "schema": "evidencewatch-brierley-trivial-baselines-v1",
        "status": "PRE_MODEL_TRIVIAL_BASELINE",
        "source": manifest["source"],
        "selection": manifest["selection"],
        "metric_definitions": {
            "token_set_jaccard_distance": "1 - set-token Jaccard similarity after lowercase [a-z0-9]+ tokenization",
            "token_multiset_jaccard_distance": "1 - weighted token-count Jaccard similarity after lowercase [a-z0-9]+ tokenization",
            "token_count_delta": "absolute token-count difference divided by the larger token count",
        },
        "boundaries": [
            "TRIVIAL_TEXT_DISTANCE != SEMANTIC_MATERIALITY",
            "COMPLETE_CASE_AUC != FULL_44_CASE_PERFORMANCE",
            "MISSING_PUBLISHED_ABSTRACT != NO_CHANGE",
            "POST_SELECTION_BASELINE != EXTERNAL VALIDATION",
            "NO_THRESHOLD_SELECTED_BEFORE_MODEL_RUN",
        ],
        "missing_owner_published_abstracts": missing,
        "metrics": metrics,
        "rows": rows,
    }

    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS")
    print(f"cases={len(rows)} missing_published_abstract={len(missing)}")
    for name, metric in metrics.items():
        print(
            f"{name}: auc={metric['auc']:.6f} "
            f"positive_n={metric['complete_positive_n']} "
            f"control_n={metric['complete_control_n']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

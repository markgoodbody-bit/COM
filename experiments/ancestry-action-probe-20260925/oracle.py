"""Deterministic oracle for ancestry-sensitive binary action decisions.

This is an offline scaffold, not an LLM result.

The minimal case instantiates the clone-vs-independent construction behind
report-only non-identifiability:
- binary latent state theta in {0, 1};
- prior probability P(theta=1);
- a positive primitive report with symmetric accuracy p;
- repeated visible positive reports may be exact descendants of one primitive
  observation or conditionally independent primitive observations.

Exact-clone descendants add no evidence beyond the primitive observation.
Independent roots multiply the likelihood ratio.

The decision policy is intentionally simple:
ACT iff posterior >= threshold, otherwise HOLD.
When ancestry is unavailable and the admissible structures imply different
actions, the interface-level oracle is ESCALATE.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


VALID_STRUCTURES = {"exact_clone", "independent"}


def _probability(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value) or not 0.0 < value < 1.0:
        raise ValueError(f"{name} must be strictly between 0 and 1")
    return value


def posterior_positive(*, prior: float, accuracy: float, roots: int) -> float:
    """Posterior P(theta=1 | roots independent positive primitive signals)."""
    prior = _probability("prior", prior)
    accuracy = _probability("accuracy", accuracy)
    if accuracy <= 0.5:
        raise ValueError("accuracy must be greater than 0.5")
    if not isinstance(roots, int) or roots < 1:
        raise ValueError("roots must be a positive integer")

    prior_odds = prior / (1.0 - prior)
    signal_lr = accuracy / (1.0 - accuracy)
    posterior_odds = prior_odds * (signal_lr ** roots)
    return posterior_odds / (1.0 + posterior_odds)


def posterior_for_structure(
    *,
    prior: float,
    accuracy: float,
    report_count: int,
    structure: str,
) -> float:
    if structure not in VALID_STRUCTURES:
        raise ValueError(f"unknown structure: {structure}")
    if not isinstance(report_count, int) or report_count < 1:
        raise ValueError("report_count must be a positive integer")

    roots = 1 if structure == "exact_clone" else report_count
    return posterior_positive(prior=prior, accuracy=accuracy, roots=roots)


def policy_action(*, posterior: float, threshold: float) -> str:
    posterior = _probability("posterior", posterior)
    threshold = _probability("threshold", threshold)
    return "ACT" if posterior >= threshold else "HOLD"


def oracle_action(
    *,
    prior: float,
    accuracy: float,
    report_count: int,
    structure: str,
    threshold: float,
) -> str:
    posterior = posterior_for_structure(
        prior=prior,
        accuracy=accuracy,
        report_count=report_count,
        structure=structure,
    )
    return policy_action(posterior=posterior, threshold=threshold)


def unknown_ancestry_action(
    *,
    prior: float,
    accuracy: float,
    report_count: int,
    threshold: float,
) -> str:
    """Escalate only when ancestry changes the policy result."""
    actions = {
        oracle_action(
            prior=prior,
            accuracy=accuracy,
            report_count=report_count,
            structure=structure,
            threshold=threshold,
        )
        for structure in VALID_STRUCTURES
    }
    if len(actions) == 1:
        return actions.pop()
    return "ESCALATE"


@dataclass(frozen=True)
class ProbeCase:
    case_id: str
    prior: float
    accuracy: float
    report_count: int
    threshold: float

    def as_dict(self) -> dict:
        clone_posterior = posterior_for_structure(
            prior=self.prior,
            accuracy=self.accuracy,
            report_count=self.report_count,
            structure="exact_clone",
        )
        independent_posterior = posterior_for_structure(
            prior=self.prior,
            accuracy=self.accuracy,
            report_count=self.report_count,
            structure="independent",
        )
        return {
            "case_id": self.case_id,
            "prior": self.prior,
            "report_accuracy": self.accuracy,
            "report_count": self.report_count,
            "visible_reports": ["positive"] * self.report_count,
            "action_threshold": self.threshold,
            "oracle": {
                "exact_clone": {
                    "posterior": clone_posterior,
                    "action": policy_action(
                        posterior=clone_posterior,
                        threshold=self.threshold,
                    ),
                },
                "independent": {
                    "posterior": independent_posterior,
                    "action": policy_action(
                        posterior=independent_posterior,
                        threshold=self.threshold,
                    ),
                },
                "ancestry_unknown": {
                    "action": unknown_ancestry_action(
                        prior=self.prior,
                        accuracy=self.accuracy,
                        report_count=self.report_count,
                        threshold=self.threshold,
                    )
                },
            },
        }


def decision_boundary_cases() -> list[ProbeCase]:
    """Cases where exact-clone vs independent ancestry changes the action."""
    candidates = [
        ProbeCase("p65-t75", 0.5, 0.65, 2, 0.75),
        ProbeCase("p70-t80", 0.5, 0.70, 2, 0.80),
        ProbeCase("p75-t85", 0.5, 0.75, 2, 0.85),
        ProbeCase("p80-t90", 0.5, 0.80, 2, 0.90),
        ProbeCase("p70-n3-t90", 0.5, 0.70, 3, 0.90),
    ]

    for case in candidates:
        data = case.as_dict()
        if data["oracle"]["exact_clone"]["action"] == data["oracle"]["independent"]["action"]:
            raise AssertionError(f"case does not cross the action boundary: {case.case_id}")
        if data["oracle"]["ancestry_unknown"]["action"] != "ESCALATE":
            raise AssertionError(f"unknown ancestry should escalate: {case.case_id}")
    return candidates

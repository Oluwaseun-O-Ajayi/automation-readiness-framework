"""Readiness domains, workflows and the scoring model.

Every domain is scored from 0 to 10, where higher means more ready. For Human
Dependency, 10 means the workflow depends least on manual steps.

The domains, the 0 to 10 scale and the category thresholds were defined by the
author from common automation-planning considerations. The weakest-link rule,
its default threshold and the recommended actions, added in version 2, are
heuristics of the same kind. None of these has been validated against the
outcomes of real automation projects. Use the results to structure discussion and find gaps,
not to predict whether an automation project will succeed.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

DOMAINS: Dict[str, str] = {
    "data_readiness": "Data Readiness",
    "traceability": "Traceability",
    "integration": "Integration",
    "human_dependency": "Human Dependency",
    "exception_handling": "Exception Handling",
    "workflow_stability": "Workflow Stability",
}

# Lower bound of each category; a score on a boundary falls in the higher category.
CATEGORIES: Tuple[Tuple[float, str], ...] = (
    (9.0, "Automation Ready"),
    (7.0, "Advanced"),
    (5.0, "Moderate"),
    (3.0, "Early Stage"),
    (0.0, "Not Ready"),
)

RECOMMENDATIONS: Dict[str, str] = {
    "data_readiness": "Capture results and metadata in structured, digital form with consistent "
                      "naming, and make records accessible to other systems.",
    "traceability": "Assign unique sample identifiers, record every transfer and status change, "
                    "and keep an audit trail that links samples to results.",
    "integration": "Identify the systems that must exchange data and confirm that each offers an "
                   "API, database access or a standard file format.",
    "human_dependency": "Map manual decisions, transfers, data entry and reconciliation steps, and "
                        "decide which can be standardized or removed before automating.",
    "exception_handling": "Define how errors are detected, who is alerted and how the workflow "
                          "recovers, and write these into the procedure.",
    "workflow_stability": "Bring the procedure under a stable, version-controlled SOP and reduce "
                          "run-to-run variation before automating it.",
}


def classify(score: float) -> str:
    """Category for an overall score from 0 to 10."""
    for lower, label in CATEGORIES:
        if score >= lower:
            return label
    return CATEGORIES[-1][1]


@dataclass
class Workflow:
    """A laboratory workflow and its six domain scores (0 to 10, higher = more ready)."""

    name: str
    data_readiness: float
    traceability: float
    integration: float
    human_dependency: float
    exception_handling: float
    workflow_stability: float
    notes: str = ""

    def __post_init__(self):
        for key in DOMAINS:
            value = getattr(self, key)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 10:
                raise ValueError(f"{self.name}: {key} must be a number from 0 to 10 (higher means more ready)")

    @property
    def scores(self) -> Dict[str, float]:
        return {key: float(getattr(self, key)) for key in DOMAINS}

    @classmethod
    def from_dict(cls, record: Mapping) -> "Workflow":
        missing = [k for k in ("name", *DOMAINS) if k not in record]
        if missing:
            raise ValueError(f"Missing fields: {missing}")
        notes = record.get("notes", "")
        notes = "" if notes is None or notes != notes else str(notes)  # NaN from CSV
        return cls(name=str(record["name"]), notes=notes, **{k: float(record[k]) for k in DOMAINS})


@dataclass
class AssessmentResult:
    """Outcome of assessing one workflow."""

    workflow: str
    scores: Dict[str, float]
    weights: Dict[str, float]
    overall_score: float
    unadjusted_classification: str
    classification: str
    limiting_domains: List[str]
    recommendations: List[Dict[str, object]] = field(default_factory=list)

    def summary(self) -> str:
        lines = [f"Workflow: {self.workflow}", ""]
        for key, label in DOMAINS.items():
            lines.append(f"{label:<22} {self.scores[key]:>5.1f}   (weight {self.weights[key]:.2f})")
        lines += ["", f"Overall readiness score: {self.overall_score:.2f}",
                  f"Classification: {self.classification}"]
        if self.classification != self.unadjusted_classification:
            names = ", ".join(DOMAINS[k] for k in self.limiting_domains)
            lines.append(f"  (capped from {self.unadjusted_classification} because {names} "
                         f"is below the critical threshold)")
        if self.recommendations:
            lines += ["", "Priorities (largest weighted gap first):"]
            for i, rec in enumerate(self.recommendations, 1):
                lines.append(f"  {i}. {DOMAINS[rec['domain']]} ({rec['score']:.1f} -> {rec['target']:.1f}): "
                             f"{rec['action']}")
        return "\n".join(lines)


class Assessment:
    """Scores workflows.

    Args:
        weights: relative importance of each domain (any non-negative numbers;
            normalized to sum to 1). Missing domains get weight 1. Default: equal.
        critical_threshold: if any domain scores below this, the classification is
            capped at `cap_category` however high the overall score (weakest-link
            rule). Set to 0 to disable.
        cap_category: the highest category allowed when a domain is critical.
        target: domains scoring below this receive a recommendation.
    """

    def __init__(self, weights: Optional[Mapping[str, float]] = None, critical_threshold: float = 3.0,
                 cap_category: str = "Early Stage", target: float = 7.0):
        raw = {k: 1.0 for k in DOMAINS}
        for k, v in (weights or {}).items():
            if k not in DOMAINS:
                raise ValueError(f"Unknown domain '{k}'; expected one of {list(DOMAINS)}")
            if v < 0:
                raise ValueError("Weights must be non-negative")
            raw[k] = float(v)
        total = sum(raw.values())
        if total <= 0:
            raise ValueError("At least one weight must be positive")
        self.weights = {k: v / total for k, v in raw.items()}
        labels = [label for _, label in CATEGORIES]
        if cap_category not in labels:
            raise ValueError(f"cap_category must be one of {labels}")
        self.critical_threshold = critical_threshold
        self.cap_category = cap_category
        self.target = target

    def assess(self, workflow: Workflow) -> AssessmentResult:
        scores = workflow.scores
        overall = round(sum(self.weights[k] * scores[k] for k in DOMAINS), 2)
        unadjusted = classify(overall)
        limiting = [k for k in DOMAINS if scores[k] < self.critical_threshold]
        order = [label for _, label in CATEGORIES]  # best first
        classification = unadjusted
        if limiting and order.index(unadjusted) < order.index(self.cap_category):
            classification = self.cap_category
        recs = [{"domain": k, "score": scores[k], "target": self.target,
                 "weighted_gap": round(self.weights[k] * (self.target - scores[k]), 4),
                 "action": RECOMMENDATIONS[k]}
                for k in DOMAINS if scores[k] < self.target]
        recs.sort(key=lambda r: (-r["weighted_gap"], list(DOMAINS).index(r["domain"])))
        return AssessmentResult(workflow.name, scores, dict(self.weights), overall, unadjusted,
                                classification, limiting, recs)

    def assess_many(self, workflows: Sequence[Workflow]):
        """Assess several workflows and rank them by overall score (highest first)."""
        import pandas as pd
        rows = []
        for wf in workflows:
            r = self.assess(wf)
            rows.append({"workflow": r.workflow, **r.scores, "overall_score": r.overall_score,
                         "classification": r.classification,
                         "limiting_domains": ", ".join(DOMAINS[k] for k in r.limiting_domains),
                         "top_priority": DOMAINS[r.recommendations[0]["domain"]] if r.recommendations else ""})
        table = pd.DataFrame(rows).sort_values("overall_score", ascending=False, kind="stable")
        table.insert(0, "rank", range(1, len(table) + 1))
        return table.reset_index(drop=True)

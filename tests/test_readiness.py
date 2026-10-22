"""Tests for the Automation Readiness Assessment Framework."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

from automation_readiness import (DOMAINS, Assessment, Workflow, classify, read_workflows,
                                  weight_sensitivity, write_workflows)

ROOT = Path(__file__).resolve().parents[1]
V1_EXAMPLE = Workflow("Cell Culture Screening Workflow", 8.5, 9.0, 7.0, 5.0, 4.5, 8.0)


def test_equal_weights_reproduce_version_1():
    r = Assessment().assess(V1_EXAMPLE)
    assert r.overall_score == 7.0 and r.classification == "Advanced"


@pytest.mark.parametrize("score,label", [(0, "Not Ready"), (2.99, "Not Ready"), (3.0, "Early Stage"),
                                         (5.0, "Moderate"), (6.99, "Moderate"), (7.0, "Advanced"),
                                         (9.0, "Automation Ready"), (10, "Automation Ready")])
def test_category_boundaries_fall_in_the_higher_category(score, label):
    assert classify(score) == label


def test_weighted_mean_and_normalization():
    wf = Workflow("w", 10, 0, 5, 5, 5, 5)
    r = Assessment(weights={"data_readiness": 3, "traceability": 1}, critical_threshold=0).assess(wf)
    # weights 3,1,1,1,1,1 over 8: (30 + 0 + 20) / 8 = 6.25
    assert r.overall_score == 6.25
    assert sum(r.weights.values()) == pytest.approx(1.0)


def test_weakest_link_caps_classification_and_can_be_disabled():
    uneven = Workflow("uneven", 10, 2, 9, 8, 7, 9)
    on, off = Assessment().assess(uneven), Assessment(critical_threshold=0).assess(uneven)
    assert on.overall_score == off.overall_score == 7.5
    assert on.unadjusted_classification == "Advanced" and on.classification == "Early Stage"
    assert on.limiting_domains == ["traceability"] and off.classification == "Advanced"


def test_cap_never_raises_a_classification():
    low = Workflow("low", 1, 1, 1, 1, 1, 1)
    assert Assessment().assess(low).classification == "Not Ready"


def test_recommendations_are_ordered_by_weighted_gap():
    wf = Workflow("w", 6, 6, 4, 3, 4, 5)
    recs = Assessment().assess(wf).recommendations
    assert [r["domain"] for r in recs[:2]] == ["human_dependency", "integration"]
    assert all(r["score"] < 7 for r in recs)
    weighted = Assessment(weights={"traceability": 10}).assess(wf).recommendations
    assert weighted[0]["domain"] == "traceability"


def test_no_recommendations_when_every_domain_meets_the_target():
    assert Assessment().assess(Workflow("w", 8, 8, 8, 8, 8, 8)).recommendations == []


def test_assess_many_ranks_by_score():
    table = Assessment().assess_many([Workflow("a", 5, 5, 5, 5, 5, 5), Workflow("b", 8, 8, 8, 8, 8, 8)])
    assert list(table["workflow"]) == ["b", "a"] and list(table["rank"]) == [1, 2]


def test_csv_round_trip(tmp_path):
    workflows = read_workflows(ROOT / "data" / "example_workflows.csv")
    assert len(workflows) == 5
    write_workflows(workflows, tmp_path / "out.csv")
    again = read_workflows(tmp_path / "out.csv")
    assert [w.scores for w in again] == [w.scores for w in workflows]


def test_weight_sensitivity_is_reproducible_and_consistent():
    wfs = [Workflow("best", 9, 9, 9, 9, 9, 9), Workflow("mid", 5, 5, 5, 5, 5, 5), Workflow("low", 2, 2, 2, 2, 2, 2)]
    a = weight_sensitivity(wfs, n_samples=500, seed=1)
    b = weight_sensitivity(wfs, n_samples=500, seed=1)
    assert a.equals(b)
    assert a.set_index("workflow").loc["best", "share_ranked_first"] == 1.0
    assert (a["score_min"] <= a["score_max"]).all()


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError):
        Workflow("w", 11, 5, 5, 5, 5, 5)
    with pytest.raises(ValueError):
        Workflow("w", True, 5, 5, 5, 5, 5)
    with pytest.raises(ValueError):
        Assessment(weights={"speed": 1})
    with pytest.raises(ValueError):
        Assessment(weights={k: 0 for k in DOMAINS})
    with pytest.raises(ValueError):
        Assessment(cap_category="Excellent")
    with pytest.raises(ValueError):
        Workflow.from_dict({"name": "w", "traceability": 5})


SCRIPTS = sorted(p.name for p in (ROOT / "examples").glob("*.py") if not p.name.startswith("_"))


@pytest.mark.parametrize("script", SCRIPTS)
def test_examples_run(script, tmp_path):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run([sys.executable, str(ROOT / "examples" / script)], cwd=tmp_path, env=env,
                          capture_output=True, text=True, timeout=300)
    assert proc.returncode == 0, proc.stderr[-2000:]

# Automation Readiness Assessment Framework

**A structured framework for evaluating traceability, integration, workflow maturity, and automation readiness in laboratory processes.**

[![tests](https://github.com/Oluwaseun-O-Ajayi/automation-readiness-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/Oluwaseun-O-Ajayi/automation-readiness-framework/actions/workflows/tests.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21689250.svg)](https://doi.org/10.5281/zenodo.21689250)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## DOI and Archival Record

This software is archived on Zenodo for long-term preservation, reproducibility, and scholarly citation.

**Version:** 2.0.0

**DOI:** https://doi.org/10.5281/zenodo.21689250

---

## Overview

The Automation Readiness Assessment Framework is an open-source methodology and software framework for evaluating whether a laboratory workflow is suitable for automation.

The framework provides a structured assessment of workflow characteristics that influence automation success, including:

- data readiness
- traceability maturity
- system integration capability
- workflow stability
- human dependency
- exception handling capability

The goal is to help researchers, engineers, and laboratory teams identify automation bottlenecks and prioritize workflow improvements before implementation.

---

## Why This Matters

Many automation projects begin without a structured assessment of workflow readiness.

As a result:

- workflows may not be sufficiently documented
- sample traceability may be incomplete
- systems may not exchange structured data
- manual steps may introduce hidden complexity
- exception handling may be poorly defined

This framework provides a repeatable method for evaluating these factors before automation deployment.

---

## Assessment Domains

### Data Readiness

Measures:

- structured data availability
- metadata consistency
- digital record management
- data accessibility

### Traceability Readiness

Measures:

- sample tracking
- audit trails
- chain of custody
- workflow history

### Integration Readiness

Measures:

- API availability
- database accessibility
- interoperability
- system connectivity

### Human Dependency

Measures:

- manual decision points
- manual transfers
- manual data entry
- manual reconciliation

### Exception Handling

Measures:

- recovery procedures
- error detection
- alerting mechanisms
- workflow resilience

### Workflow Stability

Measures:

- SOP maturity
- process consistency
- workflow repeatability
- execution variability

---

## Scoring System

Each domain is scored on a scale from:

```text
0–10
```

Categories:

```text
0–3   Not Ready
3–5   Early Stage
5–7   Moderate
7–9   Advanced
9–10  Automation Ready
```

**Scoring convention.** Every domain is scored so that a higher value means more ready. For Human Dependency, 10 therefore means that the workflow depends least on manual steps. A value on a boundary falls in the higher category (for example, 7.0 is Advanced).

**Overall score.** The overall score is the weighted mean of the six domain scores. By default all weights are equal, which gives the same result as version 1. Weights can be changed to reflect local priorities, for example giving traceability more weight in a regulated laboratory.

**Weakest-link rule.** If any domain scores below 3 (the critical threshold), the classification is capped at Early Stage however high the overall score, and the domain is reported as limiting. A strong average should not hide a gap that would block automation. The threshold and the cap are settings; setting the threshold to 0 switches the rule off.

**Priorities.** Every domain below the target score (7 by default) receives a recommended action. Actions are ranked by the weighted gap between the score and the target.

**Status of the method.** The six domains, the 0 to 10 scale and the category thresholds were defined by the author from common automation-planning considerations. They have not been validated against the outcomes of real automation projects, and the scores are entered by the assessor rather than measured. Use the result to structure discussion and to find gaps, not to predict whether an automation project will succeed. The weakest-link rule, its default threshold and the recommended actions, added in version 2, are heuristics of the same kind.


---

## Installation

```bash
git clone https://github.com/Oluwaseun-O-Ajayi/automation-readiness-framework.git
cd automation-readiness-framework
pip install .            # or: pip install ".[test]" to include the test dependencies
```

Requires Python 3.9 or later, NumPy and pandas.

## Quick Start

```python
from automation_readiness import Workflow, Assessment, read_workflows, weight_sensitivity

workflow = Workflow(
    name="Cell Culture Screening Workflow",
    data_readiness=8.5,
    traceability=9.0,
    integration=7.0,
    human_dependency=5.0,
    exception_handling=4.5,
    workflow_stability=8.0,
)

result = Assessment().assess(workflow)
print(result.summary())               # scores, classification, ranked priorities

# Several workflows from a CSV, ranked
workflows = read_workflows("data/example_workflows.csv")
print(Assessment().assess_many(workflows))

# Custom weights, and how stable the ranking is when the weights change
print(Assessment(weights={"traceability": 2, "data_readiness": 2}).assess_many(workflows))
print(weight_sensitivity(workflows, seed=1))
```

Expected output of `python examples/example_assessment.py`:

```text
Workflow: Cell Culture Screening Workflow

Data Readiness           8.5   (weight 0.17)
Traceability             9.0   (weight 0.17)
Integration              7.0   (weight 0.17)
Human Dependency         5.0   (weight 0.17)
Exception Handling       4.5   (weight 0.17)
Workflow Stability       8.0   (weight 0.17)

Overall readiness score: 7.00
Classification: Advanced

Priorities (largest weighted gap first):
  1. Exception Handling (4.5 -> 7.0): Define how errors are detected, who is alerted and how the workflow recovers, and write these into the procedure.
  2. Human Dependency (5.0 -> 7.0): Map manual decisions, transfers, data entry and reconciliation steps, and decide which can be standardized or removed before automating.
```

To assess your own workflows, copy `data/example_workflows.csv`, replace the rows and pass the file to `read_workflows()`.

---

## Case Studies

Four reproducible case studies are described in [`examples/CASE_STUDIES.md`](examples/CASE_STUDIES.md). They use illustrative scores, not assessments of real laboratories:

1. **Portfolio.** Ranking five candidate workflows, with the blocking domains and next step for each.
2. **Weakest link.** Two workflows with the same average of 7.5 are classified differently because one scores 2 on traceability.
3. **Weights.** Doubling the weight on traceability and data readiness swaps two workflows; across 5,000 random weightings the top workflow stays first every time.
4. **Improvement plan.** Raising the two highest priorities of an Early Stage workflow moves it to Moderate.

---

## Testing

```bash
pip install ".[test]"
python -m pytest
```

The tests check that equal weights reproduce version 1, category boundaries, weighted means, the weakest-link rule, the ordering of priorities, ranking, CSV input and output, reproducibility of the sensitivity analysis, input validation, and that every example runs. They run on Linux, macOS and Windows for every push.

---

## Project Structure

```text
automation-readiness-framework/
├── automation_readiness/
│   ├── model.py         domains, workflows, scoring, classification, priorities
│   └── analysis.py      CSV input and output, weight sensitivity
├── data/
│   └── example_workflows.csv
├── examples/
│   ├── example_assessment.py
│   ├── case_study_1_portfolio.py ... case_study_4_improvement_plan.py
│   ├── CASE_STUDIES.md
│   └── case_study_results/
├── tests/
├── paper.md, paper.bib
├── CITATION.cff, CHANGELOG.md
└── pyproject.toml
```

---

## Related Software

The [Laboratory Automation Digital Twin Framework](https://github.com/Oluwaseun-O-Ajayi/lab-automation-digital-twin) simulates how a workflow performs once automated (throughput, queues, bottlenecks and traceability). Use this framework first to decide whether a workflow is ready, and the digital twin to plan the automated version.

---

## Intended Use

This framework is intended for:

- laboratory automation planning
- workflow analysis
- digital transformation initiatives
- educational purposes
- research studies in automation methodology

---

## Citation

If you use this framework in research, teaching, workflow analysis, automation planning, or digital transformation studies, please cite:

```text
Ajayi, O. O. (2026). Automation Readiness Assessment Framework (Version 2.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.21689250
```

### BibTeX

```bibtex
@software{automation_readiness_framework_2026,
  author = {Ajayi, Oluwaseun O.},
  title = {Automation Readiness Assessment Framework},
  year = {2026},
  version = {2.0.0},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.21689250},
  url = {https://doi.org/10.5281/zenodo.21689250}
}
```

---

## Limitations

This framework is a conceptual and computational assessment approach. Scores are entered by the assessor, and the method has not been validated against the outcomes of real automation projects.

It does not directly control automation systems, robots, instruments, LIMS, MES platforms, or manufacturing environments.

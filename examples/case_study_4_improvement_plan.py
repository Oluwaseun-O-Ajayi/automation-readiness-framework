"""Case study 4: from assessment to an improvement plan.

Question: for a workflow that is not ready, which improvements matter most, and
how would the assessment change if the two highest priorities were brought up to
the target score of 7?
Input:  "Cell culture passaging" from data/example_workflows.csv (illustrative)
Output: examples/case_study_results/case4_improvement_plan.csv
"""

from dataclasses import replace

import pandas as pd
from _common import DATA, RESULTS
from automation_readiness import DOMAINS, Assessment, read_workflows

assessment = Assessment()
workflow = next(w for w in read_workflows(DATA / "example_workflows.csv") if w.name == "Cell culture passaging")
before = assessment.assess(workflow)
print(before.summary())

top_two = [rec["domain"] for rec in before.recommendations[:2]]
improved = replace(workflow, name=workflow.name + " (after plan)", **{k: 7.0 for k in top_two})
after = assessment.assess(improved)
print("\nAfter raising " + " and ".join(DOMAINS[k] for k in top_two) + " to 7:")
print(f"Overall {before.overall_score:.2f} -> {after.overall_score:.2f}; "
      f"classification {before.classification} -> {after.classification}")

rows = [{"stage": "before", "overall_score": before.overall_score, "classification": before.classification,
         **before.scores},
        {"stage": "after top two priorities", "overall_score": after.overall_score,
         "classification": after.classification, **after.scores}]
pd.DataFrame(rows).to_csv(RESULTS / "case4_improvement_plan.csv", index=False)

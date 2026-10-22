"""Case study 3: how much do the weights matter?

Question: if a regulated laboratory weights traceability and data readiness
twice as heavily, does the order of the five workflows change, and how stable is
the ranking across many plausible weightings?
Input:  data/example_workflows.csv (illustrative scores)
Output: examples/case_study_results/case3_weights.csv
        examples/case_study_results/case3_weight_sensitivity.csv
"""

import pandas as pd
from _common import DATA, RESULTS
from automation_readiness import Assessment, read_workflows, weight_sensitivity

workflows = read_workflows(DATA / "example_workflows.csv")
equal = Assessment().assess_many(workflows)[["workflow", "overall_score", "rank", "classification"]]
regulated = Assessment(weights={"traceability": 2, "data_readiness": 2}).assess_many(workflows)
regulated = regulated[["workflow", "overall_score", "rank", "classification"]]
table = equal.merge(regulated, on="workflow", suffixes=("_equal", "_regulated"))
table.to_csv(RESULTS / "case3_weights.csv", index=False)
print("Equal weights versus traceability and data readiness weighted x2:")
print(table.to_string(index=False))

sens = weight_sensitivity(workflows, n_samples=5000, seed=2026)
sens.to_csv(RESULTS / "case3_weight_sensitivity.csv", index=False)
print("\nAcross 5,000 random weightings (Dirichlet, concentration 5):")
print(sens.to_string(index=False))

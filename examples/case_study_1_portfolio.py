"""Case study 1: prioritizing a portfolio of workflows.

Question: of five candidate workflows, which are ready to automate first, what
blocks the others, and what should each team work on next?
Input:  data/example_workflows.csv (illustrative scores)
Output: examples/case_study_results/case1_portfolio.csv
"""

from _common import DATA, RESULTS
from automation_readiness import Assessment, read_workflows

table = Assessment().assess_many(read_workflows(DATA / "example_workflows.csv"))
table.to_csv(RESULTS / "case1_portfolio.csv", index=False)
cols = ["rank", "workflow", "overall_score", "classification", "limiting_domains", "top_priority"]
print(table[cols].to_string(index=False))

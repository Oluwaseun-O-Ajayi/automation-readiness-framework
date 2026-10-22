"""Case study 2: why an average is not enough.

Question: two workflows have the same overall score of 7.5. One is balanced; the
other is strong everywhere except traceability. Should they be classified alike?
Output: examples/case_study_results/case2_weakest_link.csv
"""

import pandas as pd
from _common import RESULTS
from automation_readiness import DOMAINS, Assessment, Workflow

balanced = Workflow("Balanced workflow", 7.5, 7.5, 7.5, 7.5, 7.5, 7.5)
uneven = Workflow("Uneven workflow", 10, 2, 9, 8, 7, 9)

rows = []
for label, assessment in [("weakest-link rule on (default)", Assessment()),
                          ("weakest-link rule off", Assessment(critical_threshold=0))]:
    for wf in (balanced, uneven):
        r = assessment.assess(wf)
        rows.append({"setting": label, "workflow": wf.name, "overall_score": r.overall_score,
                     "classification": r.classification,
                     "limiting_domains": ", ".join(DOMAINS[k] for k in r.limiting_domains)})
table = pd.DataFrame(rows)
table.to_csv(RESULTS / "case2_weakest_link.csv", index=False)
print(table.to_string(index=False))

# Case studies

Four worked examples that show how the framework supports automation planning.
They use five illustrative workflows in `data/example_workflows.csv`, plus two
constructed workflows in case 2. All scores were chosen to demonstrate the
framework; they are not assessments of any real laboratory's workflows, and the
case studies show how the method behaves, not that it predicts project outcomes.

```bash
python examples/case_study_1_portfolio.py
python examples/case_study_2_weakest_link.py
python examples/case_study_3_weights.py
python examples/case_study_4_improvement_plan.py
```

Results are written to `examples/case_study_results/`. The numbers below were
produced with version 2.0.0.

| Case | Application |
|---|---|
| 1 | Prioritizing a portfolio of candidate workflows |
| 2 | Why a single average can hide a blocking weakness |
| 3 | Checking whether the ranking depends on the weights |
| 4 | Turning an assessment into an improvement plan |

## Case 1: Prioritizing a portfolio

**Question.** Of five candidate workflows, which should be automated first, what
blocks the others, and what should each team work on next?

**Result.**

| Rank | Workflow | Score | Classification | Blocking domains | Top priority |
|---|---|---|---|---|---|
| 1 | HPLC purity testing | 7.83 | Advanced | | Exception Handling |
| 2 | Plate-based ELISA | 6.67 | Moderate | | Exception Handling |
| 3 | Buffer preparation | 5.17 | Moderate | | Integration |
| 4 | Cell culture passaging | 4.67 | Early Stage | | Human Dependency |
| 5 | Manual sample accessioning | 3.33 | Early Stage | Traceability, Human Dependency | Traceability |

**What it shows.** A single table answers the planning questions: start with the
HPLC workflow, and give each other team one concrete next step. Sample
accessioning has two domains below the critical threshold of 3, so it needs
process work before automation is worth discussing.

## Case 2: The weakest link

**Question.** Two workflows have the same overall score of 7.5. One is balanced;
the other scores 7 to 10 on five domains but 2 on traceability. Should they be
classified alike?

**Result.** Both average 7.5, which falls in the Advanced category. With the
weakest-link rule (default), the uneven workflow is capped at Early Stage and
traceability is flagged as limiting; the balanced workflow stays Advanced. With
the rule switched off (`critical_threshold=0`), both are Advanced.

**What it shows.** A weighted average lets strength in one domain compensate for
a gap in another, but an automated process with poor traceability cannot be
trusted however good its data systems are. The rule makes that gap visible
instead of averaging it away. The threshold and cap are settings, so a
laboratory can choose its own.

## Case 3: How much do the weights matter?

**Question.** If a regulated laboratory weights traceability and data readiness
twice as heavily, does the order change, and how stable is the ranking across
many plausible weightings?

**Result.** With the doubled weights, buffer preparation and cell culture
passaging swap places (third and fourth; 5.00 each, kept in input order), and
cell culture passaging moves up from Early Stage to Moderate. The other three
keep their rank. Across 5,000 random weightings drawn around equal weights
(Dirichlet, concentration 5), HPLC purity testing ranks first every time and
every workflow keeps its median rank, while overall scores move by up to 2.2
points.

**What it shows.** The broad ordering of these workflows is robust to the
weights, but scores near a category boundary can change class. Reporting the
sensitivity alongside the score shows which conclusions depend on the weighting
and which do not.

## Case 4: From assessment to an improvement plan

**Question.** For a workflow that is not ready, which improvements matter most,
and what would the two highest priorities achieve?

**Result.** Cell culture passaging scores 4.67 (Early Stage). The ranked
priorities are Human Dependency (3 to 7), Integration (4 to 7), Exception
Handling (4 to 7), Workflow Stability (5 to 7), Data Readiness and Traceability
(6 to 7), each with a concrete action. Raising the first two to 7 lifts the
overall score to 5.83 and the classification to Moderate.

**What it shows.** The output is a work plan, not only a score: what to fix, in
what order, and what the fix is worth. Priorities are ordered by the weighted
gap to the target; ties keep the fixed domain order.

from src.workflow import Workflow
from src.assessment import Assessment
from src.reporting import ReportGenerator


workflow = Workflow(
    name="Cell Culture Screening Workflow",
    data_readiness=8.5,
    traceability=9.0,
    integration=7.0,
    human_dependency=5.0,
    exception_handling=4.5,
    workflow_stability=8.0,
)

assessment = Assessment(workflow)

results = assessment.run()

ReportGenerator.print_report(results)

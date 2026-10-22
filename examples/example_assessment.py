"""Assess one workflow (the version 1 example; equal weights give the same score)."""

from _common import ROOT  # noqa: F401  (adds the repository to the import path)
from automation_readiness import Assessment, Workflow

workflow = Workflow(
    name="Cell Culture Screening Workflow",
    data_readiness=8.5,
    traceability=9.0,
    integration=7.0,
    human_dependency=5.0,
    exception_handling=4.5,
    workflow_stability=8.0,
)

print(Assessment().assess(workflow).summary())

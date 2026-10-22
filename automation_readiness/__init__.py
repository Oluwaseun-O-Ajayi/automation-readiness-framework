"""Automation Readiness Assessment Framework.

Scores laboratory workflows on six readiness domains, classifies them, flags the
domains that block automation, and lists improvement priorities.
"""

from .analysis import read_workflows, weight_sensitivity, write_workflows
from .model import (CATEGORIES, DOMAINS, RECOMMENDATIONS, Assessment, AssessmentResult, Workflow,
                    classify)

__version__ = "2.0.0"

__all__ = ["Workflow", "Assessment", "AssessmentResult", "classify", "read_workflows", "write_workflows",
           "weight_sensitivity", "DOMAINS", "CATEGORIES", "RECOMMENDATIONS", "__version__"]

class Workflow:
    """
    Represents a laboratory workflow being assessed.
    """

    def __init__(
        self,
        name,
        data_readiness,
        traceability,
        integration,
        human_dependency,
        exception_handling,
        workflow_stability,
    ):
        self.name = name

        for label, value in (("data_readiness", data_readiness), ("traceability", traceability),
                             ("integration", integration), ("human_dependency", human_dependency),
                             ("exception_handling", exception_handling),
                             ("workflow_stability", workflow_stability)):
            if not isinstance(value, (int, float)) or not 0 <= value <= 10:
                raise ValueError(f"{label} must be a number from 0 to 10 (higher means more ready)")

        self.data_readiness = data_readiness
        self.traceability = traceability
        self.integration = integration
        self.human_dependency = human_dependency
        self.exception_handling = exception_handling
        self.workflow_stability = workflow_stability

    def as_dict(self):
        return {
            "Data Readiness": self.data_readiness,
            "Traceability": self.traceability,
            "Integration": self.integration,
            "Human Dependency": self.human_dependency,
            "Exception Handling": self.exception_handling,
            "Workflow Stability": self.workflow_stability,
        }

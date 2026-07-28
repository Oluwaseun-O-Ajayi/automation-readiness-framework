class ReadinessScorer:
    """
    Calculates automation readiness scores.
    """

    @staticmethod
    def calculate_overall_score(workflow):

        scores = [
            workflow.data_readiness,
            workflow.traceability,
            workflow.integration,
            workflow.human_dependency,
            workflow.exception_handling,
            workflow.workflow_stability,
        ]

        return round(sum(scores) / len(scores), 2)

    @staticmethod
    def classify(score):

        if score < 3:
            return "Not Ready"

        if score < 5:
            return "Early Stage"

        if score < 7:
            return "Moderate"

        if score < 9:
            return "Advanced"

        return "Automation Ready"

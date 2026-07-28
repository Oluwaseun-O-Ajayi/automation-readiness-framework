from src.scoring import ReadinessScorer


class Assessment:

    def __init__(self, workflow):
        self.workflow = workflow

    def run(self):

        overall_score = ReadinessScorer.calculate_overall_score(
            self.workflow
        )

        classification = ReadinessScorer.classify(
            overall_score
        )

        return {
            "workflow": self.workflow.name,
            "scores": self.workflow.as_dict(),
            "overall_score": overall_score,
            "classification": classification,
        }

class ReportGenerator:

    @staticmethod
    def print_report(results):

        print("\n" + "=" * 60)

        print("AUTOMATION READINESS REPORT")

        print("=" * 60)

        print(f"\nWorkflow: {results['workflow']}\n")

        for category, score in results["scores"].items():

            print(
                f"{category:<25} {score:>5}"
            )

        print("\n" + "-" * 60)

        print(
            f"Overall Readiness Score: {results['overall_score']}"
        )

        print(
            f"Classification: {results['classification']}"
        )

        print("=" * 60)

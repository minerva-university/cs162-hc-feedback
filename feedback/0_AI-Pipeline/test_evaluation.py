from evaluation import evaluate_criterion, evaluate_all_criteria
from config import get_criteria


def main():
    test_theses = [
        """The implementation of artificial intelligence in healthcare systems
        will revolutionize patient care through improved diagnosis accuracy,
        personalized treatment plans, and reduced medical errors.""",

        """Climate change is bad.""",  # intentionally weak thesis

        """Investing in homeless shelters is merely a temporary relief to
        homelessness in San Francisco because doing so fails to address underlying
        causes such as mental health services, affordable housing policies, and job training programs.""",
    ]

    print("Testing Criterion-by-Criterion Evaluation...")
    for i, thesis in enumerate(test_theses, 1):
        print(f"\nTest Thesis #{i}:")
        print(f"Input: {thesis}")
        print("\nResults by criterion:")

        results = evaluate_all_criteria(thesis)
        criteria = get_criteria()

        for criterion, passed in zip(criteria, results):
            print(f"{'PASS' if passed else 'FAIL'}: {criterion[:100]}...")

        print(f"Overall Pass Rate: {sum(results)}/{len(results)}")
        print("-" * 80)


if __name__ == "__main__":
    main()

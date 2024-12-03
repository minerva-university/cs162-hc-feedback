from specific_feedback import generate_checklist
from evaluation import evaluate_all_criteria
from config import get_criteria

def demonstrate_feedback_process():
    test_thesis = """Investing in homeless shelters is merely a temporary relief to
        homelessness in San Francisco because doing so fails to address underlying
        causes such as mental health services, affordable housing policies, and job training programs."""

    print("\n=== Thesis Feedback Demonstration ===")
    print(f"\nAnalyzing thesis: \"{test_thesis}\"")

    # Show evaluation results first
    print("\n1. Initial Evaluation Results:")
    print("-" * 40)
    results = evaluate_all_criteria(test_thesis)
    criteria = get_criteria()

    for criterion, passed in zip(criteria, results):
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {criterion[:100]}...")

    print(f"\nPass Rate: {sum(results)}/{len(results)}")

    # Show generated checklist
    print("\n2. Generated Specific Feedback:")
    print("-" * 40)
    checklist = generate_checklist(test_thesis)
    print(checklist)

if __name__ == "__main__":
    demonstrate_feedback_process()
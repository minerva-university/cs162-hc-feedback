from specific_feedback import generate_checklist, evaluate_pitfall
from evaluation import evaluate_all_criteria
from config import get_criteria, get_pitfalls

def demonstrate_feedback_process():
    test_thesis = """Climate change is bad."""

    print("\n=== Thesis Feedback Demonstration ===")
    print(f"\nAnalyzing thesis: \"{test_thesis}\"")

    # Show guided criteria evaluation results
    print("\n1. Guided Criteria Evaluation Results:")
    print("-" * 40)
    results = evaluate_all_criteria(test_thesis)
    criteria = get_criteria()

    failed_criteria = []
    for i, (criterion, passed) in enumerate(zip(criteria, results)):
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {criterion[:100]}...")
        if not passed:
            failed_criteria.append(f"Criterion #{i+1}")

    # Show pitfall evaluation results
    print("\n2. Common Pitfalls Evaluation Results:")
    print("-" * 40)
    pitfalls = get_pitfalls()
    failed_pitfalls = []

    for i, pitfall in enumerate(pitfalls):
        passed = evaluate_pitfall(test_thesis, pitfall)
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {pitfall[:100]}...")
        if not passed:
            failed_pitfalls.append(f"Pitfall #{i+1}")

    # Summary of what needs changes
    print("\n3. Areas Needing Improvement:")
    print("-" * 40)
    if failed_criteria:
        print("Failed Criteria:", ", ".join(failed_criteria))
    if failed_pitfalls:
        print("Failed Pitfalls:", ", ".join(failed_pitfalls))

    # Show generated checklist
    print("\n4. Generated Specific Feedback:")
    print("-" * 40)
    checklist = generate_checklist(test_thesis)
    print(checklist)

if __name__ == "__main__":
    demonstrate_feedback_process()
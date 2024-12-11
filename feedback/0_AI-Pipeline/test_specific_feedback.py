from specific_feedback import generate_checklist, evaluate_pitfall
from evaluation import evaluate_all_criteria
from config import get_criteria, get_pitfalls
from logging_config import logger  # Import the shared logger or setup
import logging

def demonstrate_feedback_process():
    test_thesis = """Climate change is bad."""

    logger.info("\n=== Thesis Feedback Demonstration ===")
    logger.info(f"\nAnalyzing thesis: \"{test_thesis}\"")

    # Show guided criteria evaluation results
    logger.info("\n1. Guided Criteria Evaluation Results:")
    logger.info("-" * 40)
    results = evaluate_all_criteria(test_thesis)
    criteria = get_criteria()

    failed_criteria = []
    for i, (criterion, passed) in enumerate(zip(criteria, results)):
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{status}: {criterion[:100]}...")
        if not passed:
            failed_criteria.append(f"Criterion #{i+1}")

    # Show pitfall evaluation results
    logger.info("\n2. Common Pitfalls Evaluation Results:")
    logger.info("-" * 40)
    pitfalls = get_pitfalls()
    failed_pitfalls = []

    for i, pitfall in enumerate(pitfalls):
        passed = evaluate_pitfall(test_thesis, pitfall)
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{status}: {pitfall[:100]}...")
        if not passed:
            failed_pitfalls.append(f"Pitfall #{i+1}")

    # Summary of what needs changes
    logger.info("\n3. Areas Needing Improvement:")
    logger.info("-" * 40)
    if failed_criteria:
        logger.info("Failed Criteria:", ", ".join(failed_criteria))
    if failed_pitfalls:
        logger.info("Failed Pitfalls:", ", ".join(failed_pitfalls))

    # # Show generated checklist without Why sections (for UI)
    # logger.info("\n4. Generated Specific Feedback (UI Version):")
    # logger.info("-" * 40)
    # checklist = generate_checklist(test_thesis, include_why=False)
    # logger.info(checklist)

    # Show full feedback including Why sections (for debugging/development)
    logger.info("\n5. Complete Feedback with Explanations (Debug Version):")
    logger.info("-" * 40)
    full_checklist = generate_checklist(test_thesis, include_why=True)
    logger.info(full_checklist)

if __name__ == "__main__":
    demonstrate_feedback_process()
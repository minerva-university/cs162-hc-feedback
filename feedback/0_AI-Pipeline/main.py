from general_feedback import generate_general_feedback
from specific_feedback import generate_checklist, evaluate_pitfall
from evaluation import evaluate_all_criteria
from config import get_criteria, get_pitfalls
from logging_config import logger  # Import the shared logger or setup
import logging



def analyze_thesis(thesis_text):
    """Generate both general and specific feedback for a thesis"""
    logging.info("\n=== Thesis Analysis ===")
    logging.info(f'Analyzing: "{thesis_text}"\n')

    # Calculate overall score
    criteria_results = evaluate_all_criteria(thesis_text)
    pitfalls = get_pitfalls()
    pitfall_results = [evaluate_pitfall(thesis_text, pitfall) for pitfall in pitfalls]

    total_checks = len(criteria_results) + len(pitfall_results)
    passed_checks = sum(criteria_results) + sum(pitfall_results)
    pass_percentage = (passed_checks / total_checks) * 100

    logging.info(f"Overall Score: {passed_checks}/{total_checks} ({pass_percentage:.1f}%)")
    logging.info(f"Criteria Score: {sum(criteria_results)}/{len(criteria_results)}")
    logging.info(f"Pitfalls Score: {sum(pitfall_results)}/{len(pitfall_results)}\n")

    logging.info("1. General Feedback:")
    logging.info("-" * 40)
    general = generate_general_feedback(thesis_text)
    logging.info(general)

    logging.info("\n2. Specific Changes Needed:")
    logging.info("-" * 40)
    specific = generate_checklist(thesis_text, include_why=True)
    logging.info(specific)

    return {
        "general_feedback": general,
        "specific_feedback": specific,
        "score": {
            "total": pass_percentage,
            "criteria_score": sum(criteria_results),
            "pitfalls_score": sum(pitfall_results),
        },
    }

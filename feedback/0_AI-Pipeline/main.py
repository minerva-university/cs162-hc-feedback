from general_feedback import generate_general_feedback
from specific_feedback import generate_checklist, evaluate_pitfall
from evaluation import evaluate_all_criteria
from pipeline_config import get_criteria, get_pitfalls
from logging_config import logger  # Import the shared logger or setup
from typing import Dict, Any


def analyze_thesis(thesis_text: str) -> Dict[str, Any]:
    """
    Analyze a thesis statement and generate feedback.

    Args:
        thesis_text (str): The thesis statement to analyze.

    Returns:
        Dict[str, Any]: A dictionary containing general feedback, specific feedback,
        and scores for the analysis.
    """
    logger.info("\n=== Thesis Analysis ===")
    logger.info(f'Analyzing: "{thesis_text}"\n')

    try:
        # Evaluate criteria and pitfalls
        criteria_results = evaluate_all_criteria(thesis_text)
        pitfalls = get_pitfalls()
        pitfall_results = [
            evaluate_pitfall(thesis_text, pitfall) for pitfall in pitfalls
        ]

        # Calculate scores
        total_checks = len(criteria_results) + len(pitfall_results)
        passed_checks = sum(criteria_results) + sum(pitfall_results)
        pass_percentage = (passed_checks / total_checks) * 100

        # Log scores
        logger.info(
            f"Overall Score: {passed_checks}/{total_checks} ({pass_percentage:.1f}%)"
        )
        logger.info(f"Criteria Score: {sum(criteria_results)}/{len(criteria_results)}")
        logger.info(f"Pitfalls Score: {sum(pitfall_results)}/{len(pitfall_results)}\n")

        # Generate feedback
        logger.info("1. General Feedback:")
        logger.info("-" * 40)
        general = generate_general_feedback(thesis_text)
        if general:
            logger.info(general)
        else:
            logger.warning("General feedback generation failed.")

        logger.info("\n2. Specific Changes Needed:")
        logger.info("-" * 40)
        specific = generate_checklist(thesis_text, include_why=True)
        if specific:
            logger.info(specific)
        else:
            logger.warning("Specific checklist generation failed.")

        return {
            "general_feedback": general or "General feedback could not be generated.",
            "specific_feedback": specific
            or "Specific checklist could not be generated.",
            "score": {
                "total": pass_percentage,
                "criteria_score": sum(criteria_results),
                "pitfalls_score": sum(pitfall_results),
            },
        }

    except Exception as e:
        logger.error(f"Error analyzing thesis: {e}")
        return {
            "general_feedback": "Error during analysis.",
            "specific_feedback": "Error during analysis.",
            "score": {
                "total": 0.0,
                "criteria_score": 0,
                "pitfalls_score": 0,
            },
        }

from flask import current_app
from ..models import HC, GuidedReflection, CommonPitfall
from .agent_general_feedback import generate_general_feedback
from .agent_specific_feedback import generate_checklist, evaluate_pitfall
from .agent_evaluation import evaluate_all_criteria
from .ai_config import initialize_analysis_model, initialize_evaluation_model
from .logging_config import logger

analysis_model = initialize_analysis_model()
evaluation_model = initialize_evaluation_model()

# Cache for HC data
hc_data_cache = {}

def load_hc_data(hc_name):
    """Loads HC data from database, using cache."""
    if hc_name in hc_data_cache:
        return hc_data_cache[hc_name]

    try:
        hc = HC.query.filter_by(name=hc_name).first()
        if hc:
            # Convert to dictionary format
            hc_data = {
                "hc_name": hc.name,
                "footnote": hc.footnote,
                "general_example": hc.general_example,
                "guided_reflection": [gr.text for gr in hc.guided_reflections],
                "common_pitfalls": [cp.text for cp in hc.common_pitfalls]
            }
            hc_data_cache[hc_name] = hc_data
            return hc_data

    except Exception as e:
        logger.error(f"Error fetching HC data from database: {e}")
        return None

    logger.error(f"HC data not found for: {hc_name}")
    return None

def analyze_hc(assignment_text, hc_name, guided_reflection, common_pitfalls):
    """Analyzes assignment text based on the chosen HC."""
    logger.info(f"\n=== HC Analysis: {hc_name} ===")
    logger.info(f'Analyzing: "{assignment_text}"\n')

    hc_data = load_hc_data(hc_name)
    if not hc_data:
        logger.error(f"HC data not found for: {hc_name}")
        return {"error": f"HC '{hc_name}' not found"}

    criteria = guided_reflection
    pitfalls = common_pitfalls

    criteria_results = evaluate_all_criteria(
        assignment_text, criteria
    )

    pitfall_results = [
        evaluate_pitfall(assignment_text, pitfall) for pitfall in pitfalls
    ]

    total_checks = len(criteria_results) + len(pitfall_results)
    passed_checks = sum(criteria_results) + sum(pitfall_results)
    pass_percentage = (passed_checks / total_checks) * 100

    logger.info(
        f"Overall Score: {passed_checks}/{total_checks} ({pass_percentage:.1f}%)"
    )
    logger.info(f"Criteria Score: {sum(criteria_results)}/{len(criteria_results)}")
    logger.info(f"Pitfalls Score: {sum(pitfall_results)}/{len(pitfall_results)}\n")

    logger.info("1. General Feedback:")
    logger.info("-" * 40)
    general = generate_general_feedback(assignment_text, criteria)
    logger.info(general)

    logger.info("\n2. Specific Changes Needed:")
    logger.info("-" * 40)
    specific = generate_checklist(assignment_text, criteria, pitfalls, include_why=True)
    logger.info(specific)

    return {
        "general_feedback": general,
        "specific_feedback": specific,
        "score": {
            "total": pass_percentage,
            "criteria_score": sum(criteria_results),
            "pitfalls_score": sum(pitfall_results),
        },
    }

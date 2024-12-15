from flask import current_app
from feedback.ai.general_feedback import generate_general_feedback
from feedback.ai.specific_feedback import generate_checklist, evaluate_pitfall
from feedback.ai.evaluation import (
    evaluate_all_criteria,
)  # Assuming you adapt this for all HCs
from feedback.ai.config import initialize_analysis_model, initialize_evaluation_model
from feedback.ai.logging_config import logger
import json
import logging
import os
import requests

analysis_model = initialize_analysis_model()
evaluation_model = initialize_evaluation_model()

# Cache for HC data (avoids repeated file reads)
hc_data_cache = {}


def load_hc_data(hc_name):
    """Loads HC data from online JSON, using cache."""
    if hc_name in hc_data_cache:
        return hc_data_cache[hc_name]

    try:
        # Fetch JSON from the online source
        response = requests.get("https://jsonkeeper.com/b/CCDQ", verify=False)
        response.raise_for_status()  # Raise HTTPError for bad responses
        all_hc_data = response.json()  # Parse JSON response

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching JSON data: {e}")
        return None

    for cornerstone, hcs in all_hc_data.items():
        for hc in hcs:
            if hc["hc_name"] == hc_name:
                hc_data_cache[hc_name] = hc  # Add HC data to the cache
                return hc

    logger.error(f"HC data not found for: {hc_name}")
    return None


def analyze_hc(
    assignment_text, hc_name, guided_reflection, common_pitfalls
):  # Renamed and updated parameters
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
    )  # Update this to work for HC criteria

    pitfall_results = [
        evaluate_pitfall(assignment_text, pitfall) for pitfall in pitfalls
    ]

    total_checks = len(criteria_results) + len(pitfall_results)
    passed_checks = sum(criteria_results) + sum(pitfall_results)
    pass_percentage = (passed_checks / total_checks) * 100

    logging.info(
        f"Overall Score: {passed_checks}/{total_checks} ({pass_percentage:.1f}%)"
    )
    logging.info(f"Criteria Score: {sum(criteria_results)}/{len(criteria_results)}")
    logging.info(f"Pitfalls Score: {sum(pitfall_results)}/{len(pitfall_results)}\n")

    logging.info("1. General Feedback:")
    logging.info("-" * 40)
    general = generate_general_feedback(assignment_text, criteria)
    logging.info(general)

    logging.info("\n2. Specific Changes Needed:")
    logging.info("-" * 40)
    specific = generate_checklist(assignment_text, criteria, pitfalls, include_why=True)
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

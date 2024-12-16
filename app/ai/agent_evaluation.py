import os
import sys

# Adjust the import paths if the script is run directly
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from app.ai.ai_config import initialize_evaluation_model
    from app.ai.logging_config import get_logger
else:
    from .ai_config import initialize_evaluation_model
    from .logging_config import get_logger

import logging

# Create module-specific logger
logger = get_logger('agent_evaluation')

model = initialize_evaluation_model()

def evaluate_criterion(assignment_text, criterion):
    """
    Evaluate a thesis against a single criterion
    Returns: True for Pass, False for Fail
    """
    logger.info(f"Evaluating criterion: {criterion}")
    prompt = f"""
You are a strict evaluator. Evaluate this response against ONE criterion:
"{criterion}"

Respond with EXACTLY one word: either "PASS" or "FAIL".

Response: {assignment_text}
"""
    try:
        response = model.generate_content(prompt)
        logger.info(f"Criterion evaluation result: {response.text.strip().upper()}")
        return response.text.strip().upper() == "PASS"
    except Exception as e:
        logger.error(f"Error in criterion evaluation: {e}")
        return False

def evaluate_all_criteria(assignment_text, criteria):
    """
    Evaluate a thesis against all criteria provided
    Returns: List of boolean results (True for Pass, False for Fail)
    """
    logger.info("Evaluating all criteria.")
    results = []
    for criterion in criteria:
        result = evaluate_criterion(assignment_text, criterion)
        results.append(result)
    logger.info(f"All criteria evaluation results: {results}")
    return results

if __name__ == "__main__":
    # Example usage
    assignment_text = "This is a sample assignment text."
    criteria = ["Criterion 1", "Criterion 2"]
    print(evaluate_all_criteria(assignment_text, criteria))

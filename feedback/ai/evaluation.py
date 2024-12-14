from feedback.ai.config import initialize_evaluation_model, get_single_criterion, get_criteria
from feedback.ai.logging_config import logger  # Import the shared logger or setup
import logging

model = initialize_evaluation_model()


def evaluate_criterion(assignment_text, criterion): # Removed criterion_index
    """
    Evaluate a thesis against a single criterion
    Returns: True for Pass, False for Fail
    """

# ideally {criteria} instead of "thesis" evaluator
    prompt = f"""
You are a strict evaluator. Evaluate this response against ONE criterion:
"{criterion}"

Respond with EXACTLY one word: either "PASS" or "FAIL".

Response: {assignment_text}
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip().upper() == "PASS"
    except Exception as e:
        logger.error(f"Error in criterion evaluation: {e}")
        return False


def evaluate_all_criteria(assignment_text, criteria):  # Updated parameters
    """
    Evaluate a thesis against all criteria provided
    Returns: List of boolean results (True for Pass, False for Fail)
    """
    results = []
    for criterion in criteria:
        result = evaluate_criterion(assignment_text, criterion) # Updated this line
        results.append(result)
    return results

from pipeline_config import initialize_model, get_criteria, get_single_criterion
from logging_config import logger
from typing import List, Union


def evaluate_criterion(thesis_text: str, criterion_index: int) -> bool:
    """
    Evaluate a thesis against a single criterion.
    Returns: True for Pass, False for Fail
    """
    criterion = get_single_criterion(criterion_index)

    prompt = f"""
    You are a strict thesis evaluator. Evaluate this thesis against ONE criterion:
    "{criterion}"

    Respond with EXACTLY one word: either "PASS" or "FAIL".

    Thesis: {thesis_text}
    """
    try:
        evaluation_model = initialize_model(model_type="evaluation")  # Initialize here
        response = evaluation_model.generate_content(prompt)
        return response.text.strip().upper() == "PASS"
    except Exception as e:
        log_error("criterion evaluation", e)
        return False


def evaluate_all_criteria(thesis_text: str) -> List[bool]:
    """
    Evaluate a thesis against all criteria.
    Returns: List of booleans indicating pass/fail for each criterion.
    """
    criteria = get_criteria()
    results = []
    for index, _ in enumerate(criteria):
        try:
            result = evaluate_criterion(thesis_text, index)
            results.append(result)
        except Exception as e:
            log_error("all criteria evaluation", e)
            results.append(False)
    return results


def evaluate_pitfall(thesis_text: str, pitfalls: List[str]) -> Union[str, None]:
    """
    Evaluate a thesis against a list of pitfalls.
    Returns: The first pitfall identified or None if none are found.
    """
    for pitfall in pitfalls:
        prompt = f"""
        You are a critical evaluator. Identify if this thesis has the following pitfall:
        "{pitfall}"

        Respond with EXACTLY one word: either "YES" or "NO".

        Thesis: {thesis_text}
        """
        try:
            evaluation_model = initialize_model(
                model_type="evaluation"
            )  # Initialize here
            response = evaluation_model.generate_content(prompt)
            if response.text.strip().upper() == "YES":
                return pitfall
        except Exception as e:
            log_error("pitfall evaluation", e)
    return None


def log_error(context: str, exception: Exception) -> None:
    """
    Unified error logging function.

    Args:
        context (str): The context where the error occurred.
        exception (Exception): The exception to log.
    """
    logger.error(f"Error in {context}: {exception}")

from pipeline_config import initialize_model, get_criteria, get_pitfalls
from logging_config import logger
from typing import List, Union
from evaluation import evaluate_all_criteria, evaluate_pitfall


def initialize_analysis_model():
    """
    Initialize the analysis model once and reuse it.
    """
    try:
        analysis_model = initialize_model(model_type="analysis")
        if not analysis_model:
            raise RuntimeError("Failed to initialize the analysis model.")
        logger.info("Analysis model initialized successfully.")
        return analysis_model
    except Exception as e:
        logger.error(f"Error initializing analysis model: {e}")
        return None


# Initialize the model globally
ANALYSIS_MODEL = initialize_analysis_model()


def validate_input(thesis_text: str) -> bool:
    """
    Validate the thesis text.

    Args:
        thesis_text (str): The thesis statement.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not thesis_text.strip():
        logger.error("Thesis text is empty or invalid.")
        return False
    return True


def generate_specific_feedback_for_criterion(
    thesis_text: str, criterion: str, criterion_type: str = "criteria"
) -> Union[str, None]:
    """
    Generate specific line-by-line feedback for a criterion or pitfall.

    Args:
        thesis_text (str): The thesis statement.
        criterion (str): The criterion or pitfall to evaluate against.
        criterion_type (str): Type of the criterion ("criteria" or "pitfall").

    Returns:
        Union[str, None]: Formatted feedback string or None if generation fails.
    """
    if not validate_input(thesis_text):
        return None

    if not ANALYSIS_MODEL:
        logger.error("Analysis model is not initialized.")
        return None

    prompt = f"""
Analyze this thesis specifically against this {criterion_type}:
"{criterion}"

Provide a specific change AND explanation in this format:
- [ ] Change: <what needs to change>
  From: <specific part that needs change>
  To: <specific suggested revision>
  Why: <one-line, 75-character explanation of how this change helps pass the criterion from a FAIL to a PASS.>

The Why section should be specific to this change and criterion.
Focus on the most important change needed.
Be precise and concrete. Don't refer to criteria by numbers.

Thesis: {thesis_text}
"""
    try:
        response = ANALYSIS_MODEL.generate_content(prompt)
        if not response or not response.text:
            logger.error("No response or empty text generated.")
            return None
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating specific feedback: {e}")
        return None


def format_feedback_for_display(
    feedback_items: List[str], include_why: bool = False
) -> str:
    """
    Format feedback items for display.

    Args:
        feedback_items (List[str]): List of feedback strings.
        include_why (bool): Whether to include "Why" sections in the output.

    Returns:
        str: Formatted feedback for display.
    """
    display_items = []
    for item in feedback_items:
        lines = item.split("\n")
        if not include_why:
            # Filter out Why lines
            lines = [line for line in lines if not line.strip().startswith("Why:")]
        display_items.append("\n".join(lines))
    return "\n\n".join(display_items)


def generate_checklist(thesis_text: str, include_why: bool = False) -> str:
    """
    Generate a checklist of feedback for guided criteria and pitfalls.

    Args:
        thesis_text (str): The thesis statement.
        include_why (bool): Whether to include "Why" explanations.

    Returns:
        str: Checklist of feedback or a message indicating no changes needed.
    """
    if not validate_input(thesis_text):
        return "Invalid thesis text provided."

    feedback_items = []

    try:
        # Check guided criteria
        logger.info("Evaluating guided criteria...")
        evaluation_results = evaluate_all_criteria(thesis_text)
        criteria = get_criteria()

        for i, (criterion, passed) in enumerate(zip(criteria, evaluation_results)):
            if not passed:
                logger.info(f"Generating feedback for failed criterion #{i+1}")
                feedback = generate_specific_feedback_for_criterion(
                    thesis_text, criterion
                )
                if feedback:
                    feedback_items.append(feedback)

        # Check pitfalls
        logger.info("Evaluating common pitfalls...")
        pitfalls = get_pitfalls()
        for i, pitfall in enumerate(pitfalls):
            if not evaluate_pitfall(thesis_text, pitfall):
                logger.info(f"Generating feedback for failed pitfall #{i+1}")
                feedback = generate_specific_feedback_for_criterion(
                    thesis_text, pitfall, "pitfall"
                )
                if feedback:
                    feedback_items.append(feedback)

    except Exception as e:
        logger.error(f"Error generating checklist: {e}")
        return "An error occurred while generating the checklist."

    if not feedback_items:
        return "No specific changes needed."

    return format_feedback_for_display(feedback_items, include_why)

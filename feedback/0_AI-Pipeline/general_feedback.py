from pipeline_config import initialize_model, get_criteria
from logging_config import logger
from typing import Optional


def format_criteria(criteria_list: list) -> str:
    """
    Format the criteria list into a readable numbered paragraph.

    Args:
        criteria_list (list): The list of criteria.

    Returns:
        str: The formatted criteria as a string.
    """
    return "\n".join(
        f"{i + 1}. {criterion}" for i, criterion in enumerate(criteria_list)
    )


def validate_input(hc_text: str) -> bool:
    """
    Validate the input HC text.

    Args:
        hc_text (str): The HC statement to analyze.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not hc_text.strip():
        logger.warning("HC text is empty or contains only whitespace.")
        return False
    return True


def generate_general_feedback(hc_text: str) -> Optional[str]:
    """
    Generate high-level, constructive feedback for a given HC statement based on guided reflection criteria.

    Args:
        hc_text (str): The HC statement to analyze.

    Returns:
        Optional[str]: A paragraph of constructive feedback or None if an error occurs.
    """
    # Validate input
    if not validate_input(hc_text):
        return None

    # Fetch criteria
    criteria_list = get_criteria()
    if not criteria_list:
        logger.error("Criteria list is empty. Cannot generate feedback.")
        return None

    # Format criteria into a prompt
    formatted_criteria = format_criteria(criteria_list)
    prompt = f"""
Analyze this HC statement based on the guided reflection criteria:
{formatted_criteria}

Provide a single paragraph of constructive feedback (600 characters).

Do not show a sample improvement; that's another agent's job. Do not refer to criteria by numbers. Be direct and to the point.

Focus on giving high-level feedback that is specific yet avoids micromanagement.

HC Statement: {hc_text}
"""
    try:
        # Initialize the model
        analysis_model = initialize_model(model_type="analysis")
        if not analysis_model:
            logger.error("Analysis model is not initialized.")
            return None

        # Generate content
        response = analysis_model.generate_content(prompt)

        # Validate response
        if not response or not response.text:
            logger.error("No response text generated.")
            return None

        feedback = response.text.strip()
        if len(feedback) > 600:
            logger.warning("Generated feedback exceeds character limit.")
            return feedback[:600]  # Truncate to 600 characters

        return feedback
    except ValueError as ve:
        logger.error(f"ValueError during feedback generation: {ve}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during feedback generation: {e}")
        return None

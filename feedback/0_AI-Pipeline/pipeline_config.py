import os
from logging_config import logger  # Import the shared logger or setup
import logging
import google.generativeai as genai
from typing import List, Optional

carl_api_key = os.getenv(
    "CARL_API_KEY"
)  # Securely fetch API key from environment variables

# Thesis evaluation criteria
GUIDED_REFLECTION_CRITERIA: List[str] = [
    "Ensure your thesis is substantial, precise, relevant, arguable, concise, and sets up the forthcoming evidence.",
    "Ensure your thesis is appropriate in terms of scope.",
    "Ensure your thesis is supported by the evidence of your work.",
    "Ensure your thesis references the type of evidence you will use to support your claim.",
    "Ensure your thesis is a one to two sentence statement of your main claim.",
    "When applicable, provide a detailed justification for a thesis critique or suggest a non-trivial improvement.",
    "Revise your thesis after a complete first draft to align it with the evidence and reasoning you provided.",
]

# Common thesis pitfalls
COMMON_PITFALLS: List[str] = [
    "The thesis is too vague or open-ended.",
    "The thesis is too long or mentions too many topics.",
    "The thesis does not take a stance.",
    "The thesis states a claim without reasoning (e.g., 'A is B' without 'because of X, Y, and Z').",
    "The thesis provides a claim and reasoning but neglects to mention the importance of the claim.",
    "The central idea is strong, but the thesis is not stated clearly or is hard to find.",
    "The paper has not identified its main points, making it hard to write a precise thesis.",
    "The thesis is not revised during the writing process, so it does not match the scope or accomplishments of the work.",
]


def get_criteria() -> List[str]:
    """Fetch evaluation criteria."""
    logger.info("Fetching evaluation criteria")
    return GUIDED_REFLECTION_CRITERIA


def get_pitfalls() -> List[str]:
    """Fetch common pitfalls."""
    logger.info("Fetching common pitfalls")
    return COMMON_PITFALLS


def get_single_criterion(index: int) -> Optional[str]:
    """
    Get a specific criterion by index.
    Args:
        index (int): The index of the criterion.
    Returns:
        str: The selected criterion or None if the index is invalid.
    """
    try:
        return GUIDED_REFLECTION_CRITERIA[index]
    except IndexError:
        logger.error(f"Invalid criterion index: {index}")
        return None


def initialize_model(model_type: str = "evaluation") -> Optional[genai.GenerativeModel]:
    """
    Initialize the Generative AI model for evaluation or analysis.
    Args:
        model_type (str): Type of model to initialize, either "evaluation" or "analysis".
    Returns:
        genai.GenerativeModel: The initialized model or None if an error occurs.
    """
    try:
        logger.info(f"Configuring {model_type} model")
        api_key = os.getenv("CARL_API_KEY")
        if not api_key:
            raise ValueError("API Key is missing. Ensure CARL_API_KEY is set.")

        genai.configure(api_key=api_key)

        if model_type == "evaluation":
            config = genai.GenerationConfig(temperature=0.1, max_output_tokens=1)
        elif model_type == "analysis":
            config = genai.GenerationConfig(temperature=1.0, max_output_tokens=8000)
        else:
            raise ValueError(f"Invalid model type: {model_type}")

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", generation_config=config
        )
        logger.info(f"{model_type.capitalize()} model initialized successfully")
        return model
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        raise
    except Exception as e:
        logger.error(f"Error initializing {model_type} model: {e}")
        return None

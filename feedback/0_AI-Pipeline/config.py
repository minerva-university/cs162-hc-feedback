import os
from logging_config import logger  # Import the shared logger or setup
import logging
import google.generativeai as genai

carl_api_key = ""

# Thesis evaluation criteria
GUIDED_REFLECTION_CRITERIA = [
    "Have you ensured your thesis is substantial, precise, relevant, arguable, concise, and sets up the forthcoming evidence?",
    "Have you ensured your thesis is appropriate in terms of scope?",
    "Have you ensured your thesis is supported by the evidence of your work?",
    "Have you ensured your thesis references what type of evidence you will use to give the reader an idea of how you will support your claim?",
    "Have you ensured your thesis is a one to two sentence statement of your main claim?",
    "When applicable, have you provided a detailed justification for a thesis critique or suggested a non-trivial improvement?",
    "Have you revised your thesis when you've finished a complete first draft to tailor it to the evidence and reasoning you provided?",
]

# Common thesis pitfalls
COMMON_PITFALLS = [
    "The application's thesis is too vague or opened-ended.",
    "The application's thesis is too long or mentions too many topics.",
    "The application's thesis does not take a stance.",
    "The application's thesis states a claim with no reasoning. For example, the thesis says A is B but does not mention A is B because of X, Y, and Z.",
    "The application's thesis provides a claim and reasoning but neglects to mention the importance of the claim. For example, the thesis states A is B because of X, Y, and Z but does not include that A is B because of X, Y, and Z, which is important for D.",
    "The application has a strong central idea, but the thesis is not stated clearly or easily found within the paper.",
    "The application lives within a paper that has yet to identify its main points, which makes it hard to write a precise thesis.",
    "The thesis is not revised throughout the process of writing and researching, so it does not match the scope or accomplishments of the work.",
]


def get_criteria():
    logger.info("Fetching evaluation criteria")
    return GUIDED_REFLECTION_CRITERIA

def get_pitfalls():
    logger.info("Fetching common pitfalls")
    return COMMON_PITFALLS


def get_single_criterion(index):
    """Get a specific criterion by index"""
    return GUIDED_REFLECTION_CRITERIA[index]


def initialize_evaluation_model():
    """Initialize model optimized for Pass/Fail evaluation"""
    try:
        logger.info("Configuring evaluation model")
        api_key = carl_api_key
        logger.debug(f"API Key present: {bool(api_key)}")
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=0.1,
                max_output_tokens=1,  # Minimal tokens for Pass/Fail
            ),
        )
        logger.info("Evaluation model initialized successfully")
        return model
    except Exception as e:
        logger.error(f"Error initializing evaluation model: {e}")
        return None


def initialize_analysis_model():
    """Initialize model for detailed analysis"""
    try:
        logger.info("Configuring analysis model")
        api_key = carl_api_key
        logger.debug(f"API Key present: {bool(api_key)}")
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=1.0,
                max_output_tokens=8000,  # Higher tokens for detailed analysis
            ),
        )
        logger.info("Analysis model initialized successfully")
        return model
    except Exception as e:
        logger.error(f"Error initializing analysis model: {e}")
        return None

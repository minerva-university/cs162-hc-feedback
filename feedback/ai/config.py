import os
from feedback.ai.logging_config import logger
import logging
import google.generativeai as genai

carl_api_key = "AIzaSyAG_a2dwMt2TYxpozHuIPHD_Y_ZLFRumaA"

def get_criteria(guided_reflection=None):
    """Get criteria from passed parameter"""
    logger.info("Fetching evaluation criteria")
    return guided_reflection if guided_reflection else []

def get_pitfalls(common_pitfalls=None):
    """Get pitfalls from passed parameter"""
    logger.info("Fetching common pitfalls")
    return common_pitfalls if common_pitfalls else []


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

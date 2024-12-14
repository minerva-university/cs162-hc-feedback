import os
from feedback.ai.logging_config import logger  # Import the shared logger or setup
import logging
import google.generativeai as genai

carl_api_key = ""


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

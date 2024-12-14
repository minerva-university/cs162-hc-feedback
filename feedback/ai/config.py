import os
from dotenv import load_dotenv
from feedback.ai.logging_config import logger  # Import the shared logger or setup
import logging
import google.generativeai as genai

# Load environment variables from .env file
# Construct the path to the .env file relative to this script
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
dotenv_path = os.path.join(root_dir, '.env')
load_dotenv(dotenv_path)

genai_api_key = os.getenv('GENAI_API_KEY')
if not genai_api_key:
    raise ValueError("GENAI_API_KEY environment variable is not set")


def initialize_evaluation_model():
    """Initialize model optimized for Pass/Fail evaluation"""
    try:
        logger.info("Configuring evaluation model")
        logger.debug(f"API Key present: {bool(genai_api_key)}")
        genai.configure(api_key=genai_api_key)

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
        logger.debug(f"API Key present: {bool(genai_api_key)}")
        genai.configure(api_key=genai_api_key)

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

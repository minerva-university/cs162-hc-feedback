import os
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path
from .logging_config import get_logger  # Correct import

# Create module-specific logger
logger = get_logger('ai_config')

gemini_model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")
gemini_model = genai.GenerativeModel(gemini_model_name)

# Get the project root directory
project_root = Path(__file__).parent.parent.parent

# Load environment variables from .env file
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path)

# Get API key from environment variables with debugging
genai_api_key = os.getenv("GENAI_API_KEY")
if not genai_api_key:
    print(f"Error: Could not load GENAI_API_KEY from environment")
    print(f"Checking .env file at: {dotenv_path}")
    print(f"Current environment variables: {dict(os.environ)}")
    raise ValueError("GENAI_API_KEY environment variable is not set")


def initialize_evaluation_model():
    """Initialize and return the Google GenAI model for evaluation"""
    try:
        logger.info("Configuring evaluation model")
        logger.debug(f"API Key present: {bool(genai_api_key)}")
        genai.configure(api_key=genai_api_key)

        model = gemini_model
        logger.info("Evaluation model initialized successfully")
        return model
    except Exception as e:
        logger.error(f"Error initializing evaluation model: {e}")
        return None


def initialize_analysis_model():
    """Initialize and return the Google GenAI model for analysis"""
    try:
        logger.info("Configuring analysis model")
        logger.debug(f"API Key present: {bool(genai_api_key)}")
        genai.configure(api_key=genai_api_key)

        model = gemini_model
        logger.info("Analysis model initialized successfully")
        return model
    except Exception as e:
        logger.error(f"Error initializing analysis model: {e}")
        return None

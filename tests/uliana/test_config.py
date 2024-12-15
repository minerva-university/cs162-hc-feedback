
from config import initialize_evaluation_model, initialize_analysis_model
from logging_config import logger  # Import the shared logger or setup
import logging


def main():
    logger.info("Testing Evaluation Model...")
    eval_model = initialize_evaluation_model()
    logger.info(f"Evaluation Model initialized: {eval_model is not None}")

    logger.info("\nTesting Analysis Model...")
    analysis_model = initialize_analysis_model()
    logger.info(f"Analysis Model initialized: {analysis_model is not None}")

if __name__ == "__main__":
    main()
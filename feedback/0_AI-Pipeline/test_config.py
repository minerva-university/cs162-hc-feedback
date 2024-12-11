
from config import initialize_evaluation_model, initialize_analysis_model

def main():
    logger.debug("Testing Evaluation Model...")
    eval_model = initialize_evaluation_model()
    logger.debug(f"Evaluation Model initialized: {eval_model is not None}")

    logger.debug("\nTesting Analysis Model...")
    analysis_model = initialize_analysis_model()
    logger.debug(f"Analysis Model initialized: {analysis_model is not None}")

if __name__ == "__main__":
    main()
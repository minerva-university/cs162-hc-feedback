
from general_feedback import generate_general_feedback
from logging_config import logger  # Import the shared logger or setup
import logging

def main():
    test_theses = [
        """Investing in homeless shelters is merely a temporary relief to homelessness in San Francisco because doing so fails to address underlying causes.""",

        """Climate change is bad.""",  # intentionally weak thesis

        """The implementation of artificial intelligence in healthcare systems will revolutionize patient care through improved diagnosis accuracy, personalized treatment plans, and reduced medical errors."""
    ]

    logger.info("Testing General Feedback Generation...")
    for i, thesis in enumerate(test_theses, 1):
        logger.info(f"\nTest Thesis #{i}:")
        logger.info(f"Input: {thesis}")
        logger.info("\nFeedback:")
        feedback = generate_general_feedback(thesis)
        logger.info(feedback)
        logger.info("-" * 80)

if __name__ == "__main__":
    main()
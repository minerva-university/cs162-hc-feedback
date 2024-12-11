from evaluation import evaluate_criterion, evaluate_all_criteria
from config import get_criteria
from logging_config import logger  # Import the shared logger or setup
import logging


def main():
    test_theses = [
        """The implementation of artificial intelligence in healthcare systems
        will revolutionize patient care through improved diagnosis accuracy,
        personalized treatment plans, and reduced medical errors.""",

        """Climate change is bad.""",  # intentionally weak thesis

        """Investing in homeless shelters is merely a temporary relief to
        homelessness in San Francisco because doing so fails to address underlying
        causes such as mental health services, affordable housing policies, and job training programs.""",
    ]

    logger.info("Testing Criterion-by-Criterion Evaluation...")
    for i, thesis in enumerate(test_theses, 1):
        logger.info(f"\nTest Thesis #{i}:")
        logger.info(f"Input: {thesis}")
        logger.info("\nResults by criterion:")

        results = evaluate_all_criteria(thesis)
        criteria = get_criteria()

        for criterion, passed in zip(criteria, results):
            logger.debug(f"{'PASS' if passed else 'FAIL'}: {criterion[:100]}...")

        logger.info(f"Overall Pass Rate: {sum(results)}/{len(results)}")
        logger.info("-" * 80)


if __name__ == "__main__":
    main()

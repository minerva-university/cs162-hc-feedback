from main import analyze_thesis
from logging_config import logger  # Import the shared logger or setup
from typing import List, Tuple, Dict


def run_demo() -> None:
    """
    Run a demo to evaluate multiple thesis statements and compare their scores.
    """
    test_theses: List[Tuple[str, str]] = [
        ("Weak Thesis", "Climate change is bad."),
        (
            "Medium Thesis",
            "The implementation of artificial intelligence in healthcare "
            "will revolutionize patient care through improved diagnosis accuracy.",
        ),
        (
            "Strong Thesis",
            "Investing in homeless shelters is merely a temporary relief to "
            "homelessness in San Francisco because doing so fails to address underlying "
            "causes such as mental health services, affordable housing policies, and job "
            "training programs, which are essential for creating lasting solutions to urban homelessness.",
        ),
    ]

    results: List[Tuple[str, float]] = []

    # Analyze each thesis statement
    for name, thesis in test_theses:
        logger.info("=" * 80)
        logger.info(f"Example: {name}")
        logger.info("=" * 80)

        try:
            result: Dict = analyze_thesis(thesis)
            score = result["score"]["total"]
            results.append((name, score))
            logger.info(f"Analysis completed for {name}. Score: {score:.1f}%")
        except Exception as e:
            logger.error(f"Error analyzing thesis '{name}': {e}")
            results.append((name, 0.0))  # Assign 0.0 score in case of error

        input("\nPress Enter to continue...")

    # Final score comparison
    logger.info("=" * 80)
    logger.info("=== Final Score Comparison ===")
    logger.info("-" * 40)
    for name, score in results:
        logger.info(f"{name}: {score:.1f}%")


if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("Welcome to the Thesis Feedback Demo")
    logger.info("This demo will analyze and compare three different thesis statements.")
    input("Press Enter to begin...")
    run_demo()

from main import analyze_thesis
from logging_config import logger  # Import the shared logger or setup
import logging

def run_demo():
    test_theses = [
        ("Weak Thesis", """Climate change is bad."""),
        (
            "Medium Thesis",
            """The implementation of artificial intelligence in healthcare
        will revolutionize patient care through improved diagnosis accuracy.""",
        ),
        (
            "Strong Thesis",
            """Investing in homeless shelters is merely a temporary relief to
        homelessness in San Francisco because doing so fails to address underlying
        causes such as mental health services, affordable housing policies, and job
        training programs, which are essential for creating lasting solutions to urban homelessness.""",
        ),
    ]

    results = []
    for name, thesis in test_theses:
        logger.info(f"\n{'='*80}\nExample: {name}\n{'='*80}") # Corrected line
        result = analyze_thesis(thesis)
        results.append((name, result["score"]["total"]))
        input("\nPress Enter to continue...")

    logger.info(f"\n{'='*80}\n=== Final Score Comparison ===\n{'='*40}")  # Corrected line
    for name, score in results:
        logger.info(f"\n{'='*80}\n{name}: {score:.1f}%") # Corrected line


if __name__ == "__main__":
    logger.info(f"\n{'='*80}\nWelcome to the Thesis Feedback Demo\n{'='*80}") # Corrected line
    input("Press Enter to begin...")
    run_demo()

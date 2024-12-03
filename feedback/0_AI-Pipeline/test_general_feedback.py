
from general_feedback import generate_general_feedback

def main():
    test_theses = [
        """Investing in homeless shelters is merely a temporary relief to homelessness in San Francisco because doing so fails to address underlying causes.""",

        """Climate change is bad.""",  # intentionally weak thesis

        """The implementation of artificial intelligence in healthcare systems will revolutionize patient care through improved diagnosis accuracy, personalized treatment plans, and reduced medical errors."""
    ]

    print("Testing General Feedback Generation...")
    for i, thesis in enumerate(test_theses, 1):
        print(f"\nTest Thesis #{i}:")
        print(f"Input: {thesis}")
        print("\nFeedback:")
        feedback = generate_general_feedback(thesis)
        print(feedback)
        print("-" * 80)

if __name__ == "__main__":
    main()
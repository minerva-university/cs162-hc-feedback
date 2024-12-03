
from specific_feedback import generate_checklist

def main():
    test_theses = [
        """Climate change is bad.""",  # Should generate multiple improvement suggestions

        """The implementation of artificial intelligence in healthcare systems will revolutionize patient care."""  # Should generate suggestions about evidence
    ]

    print("Testing Specific Feedback Generation...")
    for i, thesis in enumerate(test_theses, 1):
        print(f"\nTest Thesis #{i}:")
        print(f"Input: {thesis}")
        print("\nChecklist:")
        checklist = generate_checklist(thesis)
        print(checklist)
        print("-" * 80)

if __name__ == "__main__":
    main()

from explanations import generate_explanations

def main():
    test_checklist = """
- [ ] Change: Add specific evidence
  From: Climate change is bad
  To: Climate change poses severe threats to global ecosystems, as evidenced by rising sea levels and increasing natural disasters

- [ ] Change: Include reasoning
  From: AI will revolutionize healthcare
  To: AI will revolutionize healthcare by improving diagnosis accuracy and reducing medical errors
"""

    print("Testing Explanation Generation...")
    print("\nInput Checklist:")
    print(test_checklist)
    print("\nExplanations:")
    explanations = generate_explanations(test_checklist)
    print(explanations)

if __name__ == "__main__":
    main()
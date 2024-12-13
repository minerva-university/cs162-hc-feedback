from config import (
    initialize_evaluation_model,
    initialize_analysis_model,
    get_criteria,
    get_pitfalls,
    GUIDED_REFLECTION_CRITERIA,
    COMMON_PITFALLS
)

def test_model_initialization():
    print("Testing Model Initialization...")
    eval_model = initialize_evaluation_model()
    analysis_model = initialize_analysis_model()

    print(f"Evaluation Model initialized: {eval_model is not None}")
    print(f"Analysis Model initialized: {analysis_model is not None}")

def test_criteria_configuration():
    print("\nTesting Criteria Configuration...")
    criteria = get_criteria()
    pitfalls = get_pitfalls()

    print("\nGuided Reflection Criteria:")
    for i, criterion in enumerate(criteria, 1):
        print(f"{i}. {criterion}")

    print("\nCommon Pitfalls:")
    for pitfall in pitfalls:
        print(f"- {pitfall}")

    # Verify criteria match defined constants
    assert criteria == GUIDED_REFLECTION_CRITERIA, "Criteria mismatch"
    assert pitfalls == COMMON_PITFALLS, "Pitfalls mismatch"

def main():
    test_model_initialization()
    test_criteria_configuration()

if __name__ == "__main__":
    main()
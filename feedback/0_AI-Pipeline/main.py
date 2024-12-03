from general_feedback import generate_general_feedback
from specific_feedback import generate_checklist, evaluate_pitfall
from evaluation import evaluate_all_criteria
from config import get_criteria, get_pitfalls


def analyze_thesis(thesis_text):
    """Generate both general and specific feedback for a thesis"""
    print("\n=== Thesis Analysis ===")
    print(f'Analyzing: "{thesis_text}"\n')

    # Calculate overall score
    criteria_results = evaluate_all_criteria(thesis_text)
    pitfalls = get_pitfalls()
    pitfall_results = [evaluate_pitfall(thesis_text, pitfall) for pitfall in pitfalls]

    total_checks = len(criteria_results) + len(pitfall_results)
    passed_checks = sum(criteria_results) + sum(pitfall_results)
    pass_percentage = (passed_checks / total_checks) * 100

    print(f"Overall Score: {passed_checks}/{total_checks} ({pass_percentage:.1f}%)")
    print(f"Criteria Score: {sum(criteria_results)}/{len(criteria_results)}")
    print(f"Pitfalls Score: {sum(pitfall_results)}/{len(pitfall_results)}\n")

    print("1. General Feedback:")
    print("-" * 40)
    general = generate_general_feedback(thesis_text)
    print(general)

    print("\n2. Specific Changes Needed:")
    print("-" * 40)
    specific = generate_checklist(thesis_text, include_why=True)
    print(specific)

    return {
        "general_feedback": general,
        "specific_feedback": specific,
        "score": {
            "total": pass_percentage,
            "criteria_score": sum(criteria_results),
            "pitfalls_score": sum(pitfall_results),
        },
    }

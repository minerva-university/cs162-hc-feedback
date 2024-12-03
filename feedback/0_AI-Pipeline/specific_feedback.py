from config import (
    initialize_analysis_model,
    initialize_evaluation_model,
    get_criteria,
    get_pitfalls
)
from evaluation import evaluate_all_criteria

analysis_model = initialize_analysis_model()

def generate_specific_feedback_for_criterion(thesis_text, criterion, criterion_type="criteria"):
    """Generate specific line-by-line feedback for a failed criterion"""
    prompt = f"""
Analyze this thesis specifically against this {criterion_type}:
"{criterion}"

Provide EXACTLY ONE specific change needed in this format:
- [ ] Change: <what needs to change>
  From: <specific part that needs change>
  To: <specific suggested revision>

Focus on the most important change needed to satisfy this specific {criterion_type}.
Be precise and concrete in your suggestion.

Thesis: {thesis_text}
"""
    try:
        response = analysis_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating specific feedback: {e}")
        return None

def evaluate_pitfall(thesis_text, pitfall):
    """Evaluate if a thesis avoids a specific pitfall"""
    prompt = f"""
You are a strict thesis evaluator. Determine if this thesis AVOIDS this pitfall:
"{pitfall}"

Respond with EXACTLY one word: "PASS" if the thesis avoids the pitfall, "FAIL" if it exhibits the pitfall.

Thesis: {thesis_text}
"""
    try:
        response = analysis_model.generate_content(prompt)
        return response.text.strip().upper() == "PASS"
    except Exception as e:
        print(f"Error in pitfall evaluation: {e}")
        return False

def generate_checklist(thesis_text):
    """Generate a checklist of specific changes needed based on failed criteria and pitfalls"""
    feedback_items = []

    # Check guided criteria
    print("\nEvaluating guided criteria...")
    evaluation_results = evaluate_all_criteria(thesis_text)
    criteria = get_criteria()

    for i, (criterion, passed) in enumerate(zip(criteria, evaluation_results)):
        if not passed:
            print(f"Generating feedback for failed criterion #{i+1}")
            feedback = generate_specific_feedback_for_criterion(thesis_text, criterion)
            if feedback:
                feedback_items.append(feedback)

    # Check pitfalls
    print("\nEvaluating common pitfalls...")
    pitfalls = get_pitfalls()
    for i, pitfall in enumerate(pitfalls):
        if not evaluate_pitfall(thesis_text, pitfall):
            print(f"Generating feedback for failed pitfall #{i+1}")
            feedback = generate_specific_feedback_for_criterion(thesis_text, pitfall, "pitfall")
            if feedback:
                feedback_items.append(feedback)

    return "\n\n".join(feedback_items) if feedback_items else "No specific changes needed."
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

def generate_checklist(thesis_text):
    """Generate a checklist of specific changes needed based on failed criteria"""
    # First, evaluate against all criteria
    evaluation_results = evaluate_all_criteria(thesis_text)
    criteria = get_criteria()

    # Generate specific feedback for failed criteria
    feedback_items = []
    for criterion, passed in zip(criteria, evaluation_results):
        if not passed:
            feedback = generate_specific_feedback_for_criterion(thesis_text, criterion)
            if feedback:
                feedback_items.append(feedback)

    # Also check common pitfalls
    pitfalls = get_pitfalls()
    for pitfall in pitfalls:
        feedback = generate_specific_feedback_for_criterion(thesis_text, pitfall, "pitfall")
        if feedback:
            feedback_items.append(feedback)

    # Combine all feedback items
    return "\n\n".join(feedback_items) if feedback_items else "No specific changes needed."
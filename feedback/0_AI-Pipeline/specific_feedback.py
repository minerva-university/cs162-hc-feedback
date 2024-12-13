from config import (
    initialize_analysis_model,
    initialize_evaluation_model,
    get_criteria,
    get_pitfalls
)
from evaluation import evaluate_all_criteria
from logging_config import logger  # Import the shared logger or setup
import logging

analysis_model = initialize_analysis_model()

def generate_specific_feedback_for_criterion(thesis_text, criterion, criterion_type="criteria"):
    """Generate specific line-by-line feedback with hidden explanation"""
    prompt = f"""
Analyze this thesis specifically against this {criterion_type}:
"{criterion}"

Provide a specific change AND explanation in this format:
- [ ] Change: <what needs to change>
  From: <specific part that needs change>
  To: <specific suggested revision>
  Why: <one-line, 75-character explanation of how this change helps pass the criterion from a FAIL to a PASS. Be straightforward. No need complete sentence. Skip "This revision...">

The Why section should be specific to this change and criterion.
Focus on the most important change needed.
Be precise and concrete. Don't refer to criteria by numbers.

Thesis: {thesis_text}
"""
    try:
        response = analysis_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating specific feedback: {e}")
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
        logger.error(f"Error in pitfall evaluation: {e}")
        return False

def format_feedback_for_display(feedback_items, include_why=False):
    """Format feedback items, optionally including or excluding Why sections"""
    display_items = []
    for item in feedback_items:
        lines = item.split('\n')
        if not include_why:
            # Filter out Why lines
            lines = [line for line in lines if not line.strip().startswith('Why:')]
        display_items.append('\n'.join(lines))
    return '\n\n'.join(display_items)

def generate_checklist(thesis_text, include_why=False):
    """Generate a checklist with optional Why explanations"""
    feedback_items = []

    # Check guided criteria
    logger.info("\nEvaluating guided criteria...")
    evaluation_results = evaluate_all_criteria(thesis_text)
    criteria = get_criteria()

    for i, (criterion, passed) in enumerate(zip(criteria, evaluation_results)):
        if not passed:
            logger.info(f"Generating feedback for failed criterion #{i+1}")
            feedback = generate_specific_feedback_for_criterion(thesis_text, criterion)
            if feedback:
                feedback_items.append(feedback)

    # Check pitfalls
    logger.info("\nEvaluating common pitfalls...")
    pitfalls = get_pitfalls()
    for i, pitfall in enumerate(pitfalls):
        if not evaluate_pitfall(thesis_text, pitfall):
            logger.info(f"Generating feedback for failed pitfall #{i+1}")
            feedback = generate_specific_feedback_for_criterion(thesis_text, pitfall, "pitfall")
            if feedback:
                feedback_items.append(feedback)

    if not feedback_items:
        return "No specific changes needed."

    return format_feedback_for_display(feedback_items, include_why)
from .ai_config import initialize_analysis_model
from .agent_evaluation import evaluate_all_criteria
from .logging_config import logger
import logging


analysis_model = initialize_analysis_model()


def generate_specific_feedback_for_criterion(
    assignment_text, criterion, context=None, criterion_type="criteria"
):
    """Generate specific line-by-line feedback with hidden explanation"""
    logger.info(f"Generating specific feedback for criterion: {criterion}")

    # Build context-aware prompt
    context_info = ""
    if context:
        if context.get("assignmentDescription"):
            context_info += (
                f"\nAssignment Description:\n{context['assignmentDescription']}"
            )
        if context.get("existingContext"):
            context_info += f"\nFull Assignment Context:\n{context['existingContext']}"

    prompt = f"""
Consider the following context:{context_info if context_info else ' No additional context provided.'}

Analyze specifically against this {criterion_type}:
"{criterion}"

Provide a specific change AND explanation in this format:
- [ ] Change: <what needs to change>
  From: <specific part that needs change>
  To: <specific suggested revision>
  Why: <one-line, 75-character explanation of how this change helps pass the criterion from a FAIL to a PASS. Be straightforward. No need complete sentence. Skip "This revision...">

The Why section should be specific to this change and criterion.
Focus on the most important change needed.
Be precise and concrete. Don't refer to criteria by numbers.
Consider the provided context in your analysis.

Text to analyze:
{assignment_text}
"""
    try:
        response = analysis_model.generate_content(prompt)
        logger.info(f"Generated specific feedback: {response.text.strip()}")
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating specific feedback: {e}")
        return None


def evaluate_pitfall(assignment_text, pitfall, context=None):
    """Evaluate if a thesis avoids a specific pitfall"""
    logger.info(f"Evaluating pitfall: {pitfall}")

    # Build context-aware prompt
    context_info = ""
    if context:
        if context.get("assignmentDescription"):
            context_info += (
                f"\nAssignment Description:\n{context['assignmentDescription']}"
            )
        if context.get("existingContext"):
            context_info += f"\nFull Assignment Context:\n{context['existingContext']}"

    prompt = f"""
Consider the following context:{context_info if context_info else ' No additional context provided.'}

You are a strict evaluator. Determine if this response AVOIDS this pitfall:
"{pitfall}"

Respond with EXACTLY one word: "PASS" if the response avoids the pitfall, "FAIL" if it exhibits the pitfall.
Consider the full context when making your evaluation.

Response: {assignment_text}
"""
    try:
        response = analysis_model.generate_content(prompt)
        logger.info(f"Pitfall evaluation result: {response.text.strip().upper()}")
        return response.text.strip().upper() == "PASS"
    except Exception as e:
        logger.error(f"Error in pitfall evaluation: {e}")
        return False


def format_feedback_for_display(feedback_items, include_why=False):
    """Format feedback items, optionally including or excluding Why sections"""
    logger.info("Formatting feedback for display.")
    display_items = []
    for item in feedback_items:
        lines = item.split("\n")
        if not include_why:
            # Filter out Why lines
            lines = [line for line in lines if not line.strip().startswith("Why:")]
        display_items.append("\n".join(lines))
    formatted_feedback = "\n\n".join(display_items)
    logger.info(f"Formatted feedback: {formatted_feedback}")
    return formatted_feedback


def generate_checklist(
    assignment_text, criteria, pitfalls, context=None, include_why=False
):
    """Generate a checklist with optional Why explanations"""
    logger.info("Generating checklist for assignment.")
    feedback_items = []

    # Check guided criteria
    logger.info("Evaluating guided criteria.")
    evaluation_results = evaluate_all_criteria(assignment_text, criteria)

    for i, (criterion, passed) in enumerate(zip(criteria, evaluation_results)):
        if not passed:
            logger.info(f"Generating feedback for failed criterion #{i+1}")
            feedback = generate_specific_feedback_for_criterion(
                assignment_text, criterion, context=context
            )
            if feedback:
                feedback_items.append(feedback)

    # Check pitfalls
    logger.info("Evaluating common pitfalls.")
    for i, pitfall in enumerate(pitfalls):
        if not evaluate_pitfall(assignment_text, pitfall, context=context):
            logger.info(f"Generating feedback for failed pitfall #{i+1}")
            feedback = generate_specific_feedback_for_criterion(
                assignment_text, pitfall, context=context, criterion_type="pitfall"
            )
            if feedback:
                feedback_items.append(feedback)

    if not feedback_items:
        logger.info("No specific changes needed.")
        return "No specific changes needed."

    return format_feedback_for_display(feedback_items, include_why)

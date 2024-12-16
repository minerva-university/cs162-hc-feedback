from .ai_config import initialize_analysis_model
from .logging_config import get_logger  # Correct import
import logging

# Create module-specific logger
logger = get_logger('agent_general_feedback')

model = initialize_analysis_model()


def generate_general_feedback(assignment_text, criteria, context=None):
    """Generate general feedback considering assignment context"""
    logger.info("Generating general feedback.")
    criteria_list = criteria
    numbered_criteria = "\n".join(
        f"{i+1}. {criterion}" for i, criterion in enumerate(criteria_list)
    )

    # Build context-aware prompt
    context_info = ""
    if context:
        if context.get("assignmentDescription"):
            context_info += (
                f"\nAssignment Description:\n{context['assignmentDescription']}"
            )
            logger.info("Got the assignment description info")
        if context.get("existingContext"):
            context_info += f"\nFull Assignment Context:\n{context['existingContext']}"
            logger.info("Got the context info")

    prompt = f"""
Consider the following context for your analysis:{context_info if context_info else ' No additional context provided.'}

Analyze the following text based on these guided reflection criteria:
{numbered_criteria}

Provide a single paragraph of constructive feedback (600 characters).
Consider the provided context in your analysis.
Don't show a sample improvement, that's another agent's job.
Don't refer to criteria by numbers.
Be straightforward and specific while maintaining a high-level perspective.

Text to analyze:
{assignment_text}
"""

    try:
        response = model.generate_content(prompt)
        logger.info(f"Generated general feedback: {response.text.strip()}")
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error in general feedback: {e}")
        return None

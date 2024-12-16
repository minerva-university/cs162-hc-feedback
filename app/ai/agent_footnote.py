from .ai_config import initialize_analysis_model
from .logging_config import logger
import os
from flask import current_app

model = initialize_analysis_model()


def get_score_threshold():
    """Get score threshold from environment or config with fallback"""
    try:
        # Try environment variable first
        env_threshold = os.getenv("SCORE_THRESHOLD")
        if env_threshold is not None:
            return float(env_threshold)  # Should be 0.01 for 1%

        # Fall back to app config if available
        if current_app:
            return current_app.config.get("SCORE_THRESHOLD", 0.01)  # Default to 1%

        return 0.01  # Default to 1%
    except (ValueError, TypeError) as e:
        logger.warning(f"Invalid SCORE_THRESHOLD value, using default 1%: {e}")
        return 0.01


def check_score_threshold(score):
    """Check if score meets the current threshold"""
    threshold = get_score_threshold()
    logger.info(f"Checking score {score:.3f} against threshold {threshold:.3f}")
    return score >= threshold


def generate_footnote(assignment_text, hc_name, context=None):
    """Generate a contextual footnote for the HC application."""
    logger.info(f"Generating footnote for HC: {hc_name}")

    context_info = ""
    if context:
        if context.get("assignmentDescription"):
            context_info += (
                f"\nAssignment Description:\n{context['assignmentDescription']}"
            )
        if context.get("existingContext"):
            context_info += f"\nFull Assignment Context:\n{context['existingContext']}"

    prompt = f"""
<OBJECTIVE_AND_PERSONA>
You are writing a first-person footnote explaining how you consciously applied this HC in your work.
Adopt the perspective of the student who wrote the text.
</OBJECTIVE_AND_PERSONA>

<CONTEXT>
HC: {hc_name}
{context_info}
</CONTEXT>

<INSTRUCTIONS>
Generate a concise, first-person footnote that:
1. Uses "I" statements to explain your conscious application of the HC
2. Points to specific parts of your text as evidence
3. Explains your deliberate choices in applying the HC
4. Follows academic footnote format while maintaining personal voice
5. Shows awareness of guided reflection criteria and avoiding common pitfalls

Format example:
"In this [type of work], I consciously applied [HC] by [specific method]. For example, I [specific example from text]. I deliberately [specific choice] to ensure [HC goal]. Through this approach, I demonstrated [HC aspect] while avoiding [potential pitfall]."

Text to analyze (treat this as your own writing):
{assignment_text}
"""

    try:
        response = model.generate_content(prompt)
        logger.info("Personal footnote generated successfully")
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating footnote: {e}")
        return None

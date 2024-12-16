from .ai_config import initialize_analysis_model
from .logging_config import logger
import os
from flask import current_app

model = initialize_analysis_model()

def get_score_threshold():
    """Get score threshold from environment or config with fallback"""
    try:
        # Try environment variable first
        env_threshold = os.getenv('SCORE_THRESHOLD')
        if env_threshold is not None:
            return float(env_threshold)  # Should be 0.01 for 1%

        # Fall back to app config if available
        if current_app:
            return current_app.config.get('SCORE_THRESHOLD', 0.01)  # Default to 1%

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
            context_info += f"\nAssignment Description:\n{context['assignmentDescription']}"
        if context.get("existingContext"):
            context_info += f"\nFull Assignment Context:\n{context['existingContext']}"

    prompt = f"""
<OBJECTIVE_AND_PERSONA>
You are an Analytical Footnote Generator for Minerva's HC applications.
</OBJECTIVE_AND_PERSONA>

<CONTEXT>
HC Name: {hc_name}
{context_info}
</CONTEXT>

<INSTRUCTIONS>
Generate a concise footnote that:
1. Explains how this text demonstrates the HC
2. Highlights key elements and their effectiveness
3. Provides specific examples from the text
4. Follows academic footnote format
</INSTRUCTIONS>

Text to analyze:
{assignment_text}
"""

    try:
        response = model.generate_content(prompt)
        logger.info("Footnote generated successfully")
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generating footnote: {e}")
        return None

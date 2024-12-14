from feedback.ai.config import initialize_analysis_model
from feedback.ai.logging_config import logger  # Import the shared logger or setup
import logging

model = initialize_analysis_model()


def generate_general_feedback(assignment_text, criteria):
    criteria_list = criteria
    numbered_criteria = "\n".join(
        f"{i+1}. {criterion}" for i, criterion in enumerate(criteria_list)
    )

# todo: change "thesis" into {HC}
    prompt = f"""
Analyze  based on the guided reflection criteria:
{numbered_criteria}

Provide a single paragraph of constructive feedback (600 characters).

Don't show a sample improvement, that's another agent's job. Don't refer to criteria by numbers. Straight to point.

Focus on giving high-level feedback that is still specific, but not micromanage-y.

{assignment_text}
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error in general feedback: {e}")
        return None

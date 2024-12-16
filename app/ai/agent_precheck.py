from .ai_config import initialize_analysis_model
from .logging_config import get_logger
import logging

# Create module-specific logger
logger = get_logger('agent_precheck')

model = initialize_analysis_model()

def check_input_quality(text):
    """
    Check if the input text is meaningful enough for HC feedback analysis.
    Returns: tuple (is_meaningful: bool, feedback: str)
    """
    prompt = f"""
    You are a pre-check evaluator. Determine if this text is meaningful enough for detailed HC feedback analysis.
    The text should:
    1. Be written in complete sentences
    2. Have actual academic content
    3. Be more than just placeholder text or random words
    4. Be relevant to academic work

    Respond in this exact format:
    VERDICT: <PASS or FAIL>
    FEEDBACK: <one sentence explaining why, or what needs to be fixed>

    Text to evaluate: {text}
    """
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split('\n')
        verdict = lines[0].split(':')[1].strip() == 'PASS'
        feedback = lines[1].split(':')[1].strip()
        return verdict, feedback
    except Exception as e:
        logger.error(f"Error in input quality check: {e}")
        return False, "Unable to evaluate input quality. Please try again."

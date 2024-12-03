
from config import initialize_analysis_model

model = initialize_analysis_model()

def generate_explanations(checklist):
    prompt = """
For each suggested change in this checklist, explain WHY it improves the thesis:

{checklist}

Format as:
Change #1: <explanation>
Change #2: <explanation>
etc.
"""
    try:
        response = model.generate_content(prompt.format(checklist=checklist))
        return response.text.strip()
    except Exception as e:
        print(f"Error in explanation generation: {e}")
        return None
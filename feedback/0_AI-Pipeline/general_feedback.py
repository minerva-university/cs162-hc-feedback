from config import initialize_analysis_model, get_criteria

model = initialize_analysis_model()


def generate_general_feedback(thesis_text):
    criteria_list = get_criteria()
    numbered_criteria = "\n".join(
        f"{i+1}. {criterion}" for i, criterion in enumerate(criteria_list)
    )

# todo: change "thesis" into {HC}
    prompt = f"""
Analyze this thesis statement based on the guided reflection criteria:
{numbered_criteria}

Provide a single paragraph of constructive feedback (600 characters).

Don't show a sample improvement, that's another agent's job. Don't refer to criteria by numbers. Straight to point.

Focus on giving high-level feedback that is still specific, but not micromanage-y.

Thesis: {thesis_text}
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in general feedback: {e}")
        return None

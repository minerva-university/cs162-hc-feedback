from config import initialize_analysis_model, get_pitfalls

model = initialize_analysis_model()

def generate_checklist(thesis_text):
    pitfalls = get_pitfalls()
    pitfalls_list = "\n".join(f"- {pitfall}" for pitfall in pitfalls)

    prompt = f"""
Analyze this thesis against common pitfalls and create a checklist of specific changes needed:
{pitfalls_list}

For each applicable pitfall, provide:
1. What needs to change
2. Specific text to modify
3. Suggested revision

Format as:
- [ ] Change: <what>
  From: <original>
  To: <suggestion>

Only include failed items that need changes.

Thesis: {thesis_text}
"""
    try:
        response = model.generate_content(prompt.format(thesis_text=thesis_text))
        return response.text.strip()
    except Exception as e:
        print(f"Error in checklist generation: {e}")
        return None
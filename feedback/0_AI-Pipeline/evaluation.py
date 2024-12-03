from config import initialize_evaluation_model, get_single_criterion, get_criteria

model = initialize_evaluation_model()


def evaluate_criterion(thesis_text, criterion_index):
    """
    Evaluate a thesis against a single criterion
    Returns: True for Pass, False for Fail
    """
    criterion = get_single_criterion(criterion_index)

# ideally {criteria} instead of "thesis" evaluator
    prompt = f"""
You are a strict thesis evaluator. Evaluate this thesis against ONE criterion:
"{criterion}"

Respond with EXACTLY one word: either "PASS" or "FAIL".

Thesis: {thesis_text}
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip().upper() == "PASS"
    except Exception as e:
        print(f"Error in criterion evaluation: {e}")
        return False


def evaluate_all_criteria(thesis_text):
    """
    Evaluate a thesis against all criteria
    Returns: List of boolean results (True for Pass, False for Fail)
    """
    results = []
    for i in range(len(get_criteria())):
        result = evaluate_criterion(thesis_text, i)
        results.append(result)
    return results

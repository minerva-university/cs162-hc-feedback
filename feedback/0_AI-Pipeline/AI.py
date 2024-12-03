import enum
import os
import google.generativeai as genai
from general_feedback import generate_general_feedback
from specific_feedback import generate_checklist
from explanations import generate_explanations


# Define the Pass/Fail Enum
class Evaluation(enum.Enum):
    PASS = "Pass"
    FAIL = "Fail"


def initialize_model():
    try:
        # Get API key from environment variable
        api_key = "AIzaSyBqj7l0AIxQ78bzg_LYwwsBOoIM7lWMSFY"
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")

        # Configure the API
        genai.configure(api_key=api_key)

        # Initialize the model
        return genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=genai.GenerationConfig(
                temperature=0.1,
                max_output_tokens=10000,
            ),
        )
    except Exception as e:
        print(f"Error initializing model: {e}")
        return None


# Replace the existing model initialization with the new function call
model = initialize_model()


def analyze_thesis(thesis_text, criterion):
    detailed_prompt = f"""
Please analyze the following thesis statement based on the criterion below:

Criterion: {criterion}

For each point of failure, identify the specific sentences that need to be changed, suggest how to change them (before and after), and explain why it's a good change.

Provide your response in the following format:

- **Issue Identified**: [description]
- **Before**: [original sentence]
- **After**: [suggested sentence]
- **Explanation**: [why it's a good change]

Thesis statement:

{thesis_text}
"""
    try:
        response = model.generate_content(detailed_prompt)
        analysis = response.text.strip()
        print(f"\nDetailed Analysis for Criterion: {criterion}")
        print(analysis)
        return analysis
    except Exception as e:
        print(f"Error in analysis: {e}")
        return None


def get_general_feedback(thesis_text):
    prompt = """
Analyze this thesis statement based on the guided reflection criteria:
1. Is it substantial, precise, relevant, arguable, concise, and sets up evidence?
2. Is it appropriate in scope?
3. Is it supported by evidence?
4. Does it reference types of evidence?
5. Is it a one to two sentence statement?

Provide a single paragraph of constructive feedback.

Thesis: {thesis_text}
"""
    try:
        response = model.generate_content(prompt.format(thesis_text=thesis_text))
        return response.text.strip()
    except Exception as e:
        print(f"Error in general feedback: {e}")
        return None


def get_actionable_checklist(thesis_text):
    prompt = """
Analyze this thesis against common pitfalls and create a checklist of specific changes needed:
- Too vague/open-ended
- Too long/too many topics
- No clear stance
- Claim without reasoning
- Missing importance
- Unclear statement
- Undefined main points
- Scope mismatch

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
        print(f"Error in actionable checklist: {e}")
        return None


def get_change_explanations(checklist):
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
        print(f"Error in explanations: {e}")
        return None


def flow(thesis_text):
    # Get general feedback
    print("\n=== General Feedback ===")
    feedback = generate_general_feedback(thesis_text)
    print(feedback)

    # Get actionable checklist
    print("\n=== Actionable Changes ===")
    checklist = generate_checklist(thesis_text)
    print(checklist)

    # Get explanations if needed
    if checklist and "[ ]" in checklist:
        print("\n=== Change Explanations ===")
        explanations = generate_explanations(checklist)
        print(explanations)
    else:
        print("\nNo changes needed - thesis meets all criteria!")


# Example Usage
example_thesis = """
Investing in homeless shelters is merely a temporary relief to homelessness in San Francisco because doing so fails to address underlying causes in terms of housing unaffordability, low wages, and rising inflation.
"""


def main():
    flow(example_thesis)


if __name__ == "__main__":
    main()

from flask import Blueprint, render_template, jsonify, request
from app.models import db, HCExample  # Add db import here

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Render the main page of the application."""
    return render_template("index.html")


@main.route("/api/hc-example/<hc_name>")
def get_hc_example(hc_name):
    example = HCExample.query.filter_by(hc_name=hc_name).first()
    if example:
        return jsonify(
            {"general_example": example.general_example, "footnote": example.footnote}
        )
    return jsonify({"error": "Example not found"}), 404


@main.route("/api/hc-examples")
def get_hc_examples():
    examples = HCExample.query.all()
    return jsonify(
        [
            {
                "hc_name": ex.hc_name,
                "cornerstone": ex.cornerstone,
                "general_example": ex.general_example,
                "footnote": ex.footnote,
            }
            for ex in examples
        ]
    )


@main.route("/api/feedback", methods=["POST"])
def get_feedback():
    """
    API endpoint to process feedback requests based on user input and stored HC examples.
    Evaluates alignment and provides actionable steps for improvement.
    
    Request Body:
    - hc_name (str): The name of the HC (high-context) skill or action.
    - paragraph (str): The user-provided paragraph applying the HC.
    - user_footnote (str, optional): Explanation of how the HC is applied.

    Response:
    - feedback (str): Alignment analysis and suggestions.
    - hc_details (dict): Stored general example and footnote for the HC.
    """
    # Parse input data from the request
    data = request.get_json()
    hc_name = data.get("hc_name", "")
    paragraph = data.get("paragraph", "")
    user_footnote = data.get("user_footnote", "")

    # Fetch the HC example from the database
    example = HCExample.query.filter_by(hc_name=hc_name).first()
    if not example:
        return jsonify({"error": f"HC name '{hc_name}' not found."}), 404

    # Extract stored general example and footnote
    general_example = example.general_example
    footnote = example.footnote

    # Construct the AI evaluation prompt
    prompt = (
        f"Stored HC Example:\n{general_example}\n"
        f"Stored HC Footnote:\n{footnote}\n\n"
        f"User's Paragraph:\n{paragraph}\n"
        f"User's Footnote (if any):\n{user_footnote}\n\n"
        "Evaluate the user's paragraph for alignment with the stored HC example. "
        "Provide two to five specific actionable steps for improvement. Assess the user's footnote (if provided) "
        "for clarity and alignment."
    )

    try:
        # Generate feedback using the OpenAI API -- NEEDS AN ACTUAL API KEY
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7,
        )
        feedback = response.choices[0].text.strip()

        # Prepare and return the response
        return jsonify({
            "feedback": feedback,
            "hc_details": {
                "hc_name": hc_name,
                "general_example": general_example,
                "footnote": footnote,
            },
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
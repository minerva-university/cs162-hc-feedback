from flask import Blueprint, render_template, jsonify, request
from app.models import db, HCExample  # Add db import here

main = Blueprint("main", __name__)

@main.route("/")
def index():
    """Render the main page of the application."""
    return render_template("index.html")

#feature/HFC-5/add-button-design
@main.route("/api/feedback", methods=["POST"])
@main.route("/api/feedback", methods=["POST"])
def get_feedback():
    """
    API endpoint to process feedback requests.
    Returns JSON with feedback and actionable steps.
    """
    # Mock feedback response - replace with actual implementation
    feedback = {
        "text": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
        "actionable_steps": [
            {
                "text": 'Change "you are wrong" to "this could be a possibility..."',
                "tooltip": "This promotes a more collaborative tone",
            },
            {
                "text": 'Start with "xyz" instead of "zyx..." for active voice',
                "tooltip": "Active voice is more engaging",
            },
            {
                "text": 'Instead of "xyz", use "zyx" to be more parsimonious',
                "tooltip": "Shorter statements are often clearer",
            },
        ],
    }
    return jsonify(feedback)


@main.route("/api/general_feedback", methods=["GET"])
def general_feedback():
    """
    API endpoint to provide general feedback.
    Returns JSON with general feedback text and score.
    """
    # Mock general feedback data - replace with actual implementation
    general_feedback = {
        "text": "Your application demonstrates excellent structure and clarity.",
        "score": 95,
    }
    return jsonify(general_feedback)


@main.route("/api/hc-example/<hc_name>")
def get_hc_example(hc_name):
    """
    API endpoint to fetch a specific HC example by name.
    """
    example = HCExample.query.filter_by(hc_name=hc_name).first()
    if example:
        return jsonify(
            {"general_example": example.general_example, "footnote": example.footnote}
        )
    return jsonify({"error": "Example not found"}), 404


@main.route("/api/hc-examples")
def get_hc_examples():
    """
    API endpoint to fetch all HC examples.
    """
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

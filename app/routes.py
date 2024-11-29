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
                "general_example": ex.general_example,
                "footnote": ex.footnote,
            }
            for ex in examples
        ]
    )


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

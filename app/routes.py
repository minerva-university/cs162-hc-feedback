from flask import Blueprint, render_template, jsonify, request
from .models import HCDescription

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Render the main page of the application."""
    return render_template("index.html")


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


@main.route("/api/hc_descriptions", methods=["GET"])
def get_hc_descriptions():
    """
    A route to demonstrate the database connection.
    Returns JSON with all HC descriptions.
    """
    hc_descriptions = HCDescription.query.all()
    data = [
        {
            "id": hc.id,
            "HC_name": hc.HC_name,
            "short_desc": hc.short_desc,
            "paragraph_desc": hc.paragraph_desc,
            "grade_reqs": hc.grade_reqs,
        }
        for hc in hc_descriptions
    ]
    return jsonify(data)

from flask import Blueprint, render_template, jsonify, request, current_app
from feedback.ai.main import analyze_hc  # Import your analyze_hc function

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/api/feedback", methods=["POST"])
def api_feedback():
    with current_app.app_context():
        data = request.get_json()
        assignment_text = data.get("text")
        hc_name = data.get("hc_name")  # Get the HC name from the request
        guided_reflection = data.get("guided_reflection") # get the guided reflection
        common_pitfalls = data.get("common_pitfalls") # get the common pitfalls

        if not assignment_text or not hc_name:
            return jsonify({"error": "Missing 'text' or 'hc_name' in request"}), 400
        
        feedback = analyze_hc(assignment_text, hc_name, guided_reflection, common_pitfalls) #pass the relevant info

    return jsonify(feedback)

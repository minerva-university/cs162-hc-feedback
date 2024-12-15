from flask import Blueprint, render_template, jsonify, request, current_app
from .ai.main import analyze_hc  # Import your analyze_hc function
from .models import Cornerstone, HC
from .ai.logging_config import logger

main = Blueprint("main", __name__)


@main.route("/")
def index():
    cornerstones = Cornerstone.query.all()
    return render_template("index.html", cornerstones=cornerstones)


@main.route("/api/hcs/<cornerstone>")
def get_hcs(cornerstone):
    cornerstone_obj = Cornerstone.query.filter_by(name=cornerstone).first_or_404()
    hcs = [{"name": hc.name, "footnote": hc.footnote} for hc in cornerstone_obj.hcs]
    return jsonify(hcs)


@main.route("/api/feedback", methods=["POST"])
def api_feedback():
    try:
        with current_app.app_context():
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400

            data = request.get_json()
            if data is None:
                return jsonify({"error": "Invalid JSON"}), 400

            assignment_text = data.get("text")
            hc_name = data.get("hc_name")
            guided_reflection = data.get("guided_reflection")
            common_pitfalls = data.get("common_pitfalls")

            if not all([assignment_text, hc_name, guided_reflection, common_pitfalls]):
                return jsonify({"error": "Missing required fields"}), 400

            feedback = analyze_hc(assignment_text, hc_name, guided_reflection, common_pitfalls)
            return jsonify(feedback)
    except Exception as e:
        logger.error(f"Error processing feedback request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

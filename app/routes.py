from flask import Blueprint, render_template, jsonify, request, current_app
from .ai.main import analyze_hc  # Import your analyze_hc function
from .models import Cornerstone, HC
from .ai.logging_config import logger
from .ai.agent_precheck import check_input_quality

main = Blueprint("main", __name__)


def format_cornerstone_name(name):
    """Format cornerstone name for display (e.g., 'MULTIMODAL_COMMUNICATIONS' -> 'Multimodal Communications')"""
    return name.replace("_", " ").title()


@main.route("/")
def index():
    cornerstones = Cornerstone.query.all()
    formatted_cornerstones = [
        {"name": cs.name, "display_name": format_cornerstone_name(cs.name)}
        for cs in cornerstones
    ]
    return render_template("index.html", cornerstones=formatted_cornerstones)


@main.route("/api/hcs/<cornerstone>")
def get_hcs(cornerstone):
    # Handle case-insensitive matching and normalize spaces
    cornerstone_name = cornerstone.strip().upper().replace("_", " ")
    cornerstone_obj = Cornerstone.query.filter(
        Cornerstone.name.ilike(f"%{cornerstone_name}%")
    ).first_or_404()

    hcs = [
        {"name": hc.name, "footnote": hc.footnote, "cornerstone": cornerstone_obj.name}
        for hc in cornerstone_obj.hcs
    ]
    return jsonify(hcs)


@main.route("/api/hcs")
def get_all_hcs():
    """Get all HCs grouped by cornerstone"""
    cornerstones = Cornerstone.query.all()
    data = {}
    for cornerstone in cornerstones:
        hcs = [
            {
                "hc_name": hc.name,
                "footnote": hc.footnote,
                "general_example": hc.general_example,
                "cornerstone": cornerstone.name,
                "guided_reflection": [gr.text for gr in hc.guided_reflections],
                "common_pitfalls": [cp.text for cp in hc.common_pitfalls],
            }
            for hc in cornerstone.hcs
        ]
        data[cornerstone.name] = hcs
    return jsonify(data)


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
            context = data.get("context", {})  # Get context information

            if not all([assignment_text, hc_name, guided_reflection, common_pitfalls]):
                return jsonify({"error": "Missing required fields"}), 400

            feedback = analyze_hc(
                assignment_text,
                hc_name,
                guided_reflection,
                common_pitfalls,
                context,  # Pass context to analysis
            )
            return jsonify(feedback)
    except Exception as e:
        logger.error(f"Error processing feedback request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@main.route("/api/precheck", methods=["POST"])
def api_precheck():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Missing text field"}), 400

        is_meaningful, feedback = check_input_quality(data["text"])
        return jsonify({"is_meaningful": is_meaningful, "feedback": feedback})
    except Exception as e:
        logger.error(f"Error in precheck: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

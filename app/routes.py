from flask import Blueprint, render_template, jsonify, request, current_app
from .ai.main import analyze_hc
from .models import Cornerstone, HC
from .ai.logging_config import get_logger  # Change this line
from .ai.agent_precheck import check_input_quality
from .ai.agent_footnote import generate_footnote, check_score_threshold, get_score_threshold

# Create module-specific logger
logger = get_logger('routes')  # Use this instead
from .ai.agent_footnote import generate_footnote, check_score_threshold, get_score_threshold

main = Blueprint("main", __name__)


def format_cornerstone_name(name):
    """Format cornerstone name for display (e.g., 'MULTIMODAL_COMMUNICATIONS' -> 'Multimodal Communications')"""
    return name.replace("_", " ").title()


@main.route("/")
def index():
    logger.info("Fetching all cornerstones for index page.")
    cornerstones = Cornerstone.query.all()
    formatted_cornerstones = [
        {"name": cs.name, "display_name": format_cornerstone_name(cs.name)}
        for cs in cornerstones
    ]
    logger.info(f"Formatted cornerstones: {formatted_cornerstones}")
    return render_template("index.html", cornerstones=formatted_cornerstones)


@main.route("/api/hcs/<cornerstone>")
def get_hcs(cornerstone):
    logger.info(f"Fetching HCs for cornerstone: {cornerstone}")
    # Modify the query to match exact name
    cornerstone_obj = Cornerstone.query.filter(
        Cornerstone.name == cornerstone.strip()
    ).first_or_404()
    logger.info(f"Found cornerstone: {cornerstone_obj.name}")

    hcs = [
        {"name": hc.name, "footnote": hc.footnote, "cornerstone": cornerstone_obj.name}
        for hc in cornerstone_obj.hcs
    ]
    logger.info(f"HCs for cornerstone {cornerstone_obj.name}: {hcs}")
    return jsonify(hcs)


@main.route("/api/hcs")
def get_all_hcs():
    logger.info("Fetching all HCs grouped by cornerstone.")
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
    logger.info(f"All HCs data: {data}")
    return jsonify(data)


@main.route("/api/feedback", methods=["POST"])
def api_feedback():
    try:
        with current_app.app_context():
            logger.info("Received feedback request.")
            if not request.is_json:
                logger.error("Request is not JSON.")
                return jsonify({"error": "Request must be JSON"}), 400

            data = request.get_json()
            if data is None:
                logger.error("Invalid JSON in request.")
                return jsonify({"error": "Invalid JSON"}), 400

            assignment_text = data.get("text")
            hc_name = data.get("hc_name")
            guided_reflection = data.get("guided_reflection")
            common_pitfalls = data.get("common_pitfalls")
            context = data.get("context", {})  # Get context information

            if not all([assignment_text, hc_name, guided_reflection, common_pitfalls]):
                logger.error("Missing required fields in request.")
                return jsonify({"error": "Missing required fields"}), 400

            logger.info(f"Analyzing HC: {hc_name} with context: {context}")
            feedback = analyze_hc(
                assignment_text,
                hc_name,
                guided_reflection,
                common_pitfalls,
                context,  # Pass context to analysis
            )
            logger.info(f"Feedback generated: {feedback}")
            return jsonify(feedback)

    except Exception as e:
        logger.error(f"Error processing feedback request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@main.route("/api/precheck", methods=["POST"])
def api_precheck():
    try:
        logger.info("Received precheck request.")
        if not request.is_json:
            logger.error("Request is not JSON.")
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        if not data or "text" not in data:
            logger.error("Missing text field in request.")
            return jsonify({"error": "Missing text field"}), 400

        logger.info(f"Checking input quality for text: {data['text']}")
        is_meaningful, feedback = check_input_quality(data["text"])
        logger.info(f"Input quality check result: {is_meaningful}, feedback: {feedback}")
        return jsonify({"is_meaningful": is_meaningful, "feedback": feedback})
    except Exception as e:
        logger.error(f"Error in precheck: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@main.route("/api/footnote", methods=["POST"])
def api_footnote():
    try:
        logger.info("Received footnote generation request")
        data = request.get_json()

        if not data or not all(key in data for key in ["text", "hc_name", "score"]):
            return jsonify({"error": "Missing required fields"}), 400

        score = float(data["score"])
        threshold = get_score_threshold()

        if not check_score_threshold(score):
            return jsonify({
                "error": "Score too low",
                "message": f"Score of {score:.1%} is below the required {threshold:.1%}"
            }), 403

        footnote = generate_footnote(
            data["text"],
            data["hc_name"],
            data.get("context")
        )

        if not footnote:
            return jsonify({"error": "Failed to generate footnote"}), 500

        return jsonify({"footnote": footnote})

    except Exception as e:
        logger.error(f"Error processing footnote request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@main.route("/api/threshold")
def get_threshold():
    """Get the current score threshold"""
    try:
        threshold = get_score_threshold()
        return jsonify({"threshold": threshold})
    except Exception as e:
        logger.error(f"Error getting threshold: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

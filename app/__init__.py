from flask import Flask
from .ai.ai_config import initialize_analysis_model, initialize_evaluation_model


def create_app():
    """
    Create and configure the Flask application.
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)

    # Set configuration
    app.config["SECRET_KEY"] = "dev"  # Change this in production!
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hc_feedback.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["ANALYSIS_MODEL"] = initialize_analysis_model()
    app.config["EVALUATION_MODEL"] = initialize_evaluation_model()

    # Register routes
    from app.routes import main

    app.register_blueprint(main)

    return app

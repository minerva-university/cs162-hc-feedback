from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .ai.ai_config import initialize_analysis_model, initialize_evaluation_model
from .models import db, Cornerstone  # Add Cornerstone import
from .utils.database import init_db, populate_data

def create_app():
    """
    Create and configure the Flask application.
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hc_feedback.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Other configurations
    app.config["SECRET_KEY"] = "dev"  # Change this in production!
    app.config["ANALYSIS_MODEL"] = initialize_analysis_model()
    app.config["EVALUATION_MODEL"] = initialize_evaluation_model()

    # Initialize database
    db.init_app(app)

    with app.app_context():
        # Create tables
        init_db()

        # Check if database is empty and populate if needed
        if not Cornerstone.query.first():
            populate_data()

    # Register routes
    from app.routes import main

    app.register_blueprint(main)

    return app

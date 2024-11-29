from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import db
from app.data import HC_EXAMPLES_DATA


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

    # Initialize database
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()
        initialize_database()

    # Register routes
    from app.routes import main

    app.register_blueprint(main)

    return app


def initialize_database():
    from app.models import HCExample

    # Only add initial data if table is empty
    if HCExample.query.first() is None:
        examples = [
            HCExample(
                hc_name=data["hc_name"],
                general_example=data["general_example"],
                footnote=data["footnote"],
            )
            for data in HC_EXAMPLES_DATA
        ]

        # Use chunks to avoid memory issues with large datasets
        chunk_size = 50
        for i in range(0, len(examples), chunk_size):
            chunk = examples[i: i + chunk_size]
            db.session.bulk_save_objects(chunk)
            db.session.commit()

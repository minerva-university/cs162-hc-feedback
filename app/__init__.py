from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import db

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
        initial_data = [
            HCExample(
                hc_name="thesis",
                general_example="You are struck by the number of homeless people you see on the streets of San Francisco and decide to investigate further and write an article in an undergraduate journal. While you may feel outraged by the poor social and economic support you find in the city for this population, you realize that you need to do more than express your outrage in your article. You must present a clear and specific claim about conditions contributing to this problem. As such, you end the introduction of your essay with a clear, arguable, and precise thesis based on your findings: Investing in homeless shelters is merely a temporary relief to homelessness in San Francisco because doing so fails to address underlying causes in terms of housing unaffordability, low wages, and rising inflation.",
                footnote="The thesis lays out precisely what the paper will argue, provides a clear indication of the significant reasons you'll offer in support of that argument, and explains the relevance of your argument. The statement is arguable, precise, and clear."
            ),
            # Add more examples here as needed
        ]

        db.session.bulk_save_objects(initial_data)
        db.session.commit()

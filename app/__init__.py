from flask import Flask
from .db import db
import os

def create_app():
    """
    Create and configure the Flask application.
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)

    # Set configuration
    app.config["SECRET_KEY"] = "dev"  # Change this in production!
    db_path = os.path.join(os.path.dirname(__file__), "database", "hc_data.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}" 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True  # Disable tracking to save resources

    # Initialize database
    db.init_app(app)

    # Register routes
    from app.routes import main
    app.register_blueprint(main)

    # Create the tables if they don't exist yet
    with app.app_context():
        db.create_all()

    return app

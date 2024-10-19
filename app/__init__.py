from flask import Flask


def create_app():
    """
    Create and configure the Flask application.
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)

    # Set configuration
    app.config["SECRET_KEY"] = "dev"  # Change this in production!

    # Register routes
    from app.routes import main

    app.register_blueprint(main)

    return app

import pytest
import sys
import os
import logging
from flask import Flask
from app.models import db

# Configure logging for tests
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
)
logger = logging.getLogger(__name__)

@pytest.fixture
def app():
    """Create and configure a test Flask application instance"""
    logger.info("Setting up test Flask application")
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    with app.app_context():
        db.init_app(app)
        db.create_all()
        logger.info("Database tables created")
        yield app
        db.session.remove()
        db.drop_all()
        logger.info("Database tables dropped")

@pytest.fixture
def client(app):
    """Create a test client"""
    logger.info("Creating test client")
    return app.test_client()

@pytest.fixture
def db_session(app):
    """Create a database session"""
    logger.info("Creating database session")
    with app.app_context():
        yield db.session

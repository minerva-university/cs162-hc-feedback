from flask import Blueprint, render_template, jsonify, request
from app.models import db, HCExample

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Render the main page of the application."""
    return render_template("index.html")

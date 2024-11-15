from .db import db

class HCDescription(db.Model):
    __tablename__ = 'hc_descriptions'  # Typically table names are plural

    id = db.Column(db.Integer, primary_key=True)
    HC_name = db.Column(db.String(100), nullable=False)  # Health Check name
    short_desc = db.Column(db.String(200), nullable=False)  # Short description
    paragraph_desc = db.Column(db.Text, nullable=True)  # Paragraph description (longer text)
    grade_reqs = db.Column(db.String(100), nullable=True)  # Grade requirements

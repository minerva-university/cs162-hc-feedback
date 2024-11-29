from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class HCExample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hc_name = db.Column(db.String(100), nullable=False)
    cornerstone = db.Column(db.String(100), nullable=False)
    general_example = db.Column(db.Text, nullable=False)
    footnote = db.Column(db.Text, nullable=False)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cornerstone(db.Model):
    __tablename__ = 'cornerstones'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    hcs = db.relationship('HC', backref='cornerstone', lazy=True)

class HC(db.Model):
    __tablename__ = 'hcs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    footnote = db.Column(db.Text, nullable=False)
    general_example = db.Column(db.Text, nullable=False)
    cornerstone_id = db.Column(db.Integer, db.ForeignKey('cornerstones.id'), nullable=False)
    guided_reflections = db.relationship('GuidedReflection', backref='hc', lazy=True)
    common_pitfalls = db.relationship('CommonPitfall', backref='hc', lazy=True)

class GuidedReflection(db.Model):
    __tablename__ = 'guided_reflections'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    hc_id = db.Column(db.Integer, db.ForeignKey('hcs.id'), nullable=False)

class CommonPitfall(db.Model):
    __tablename__ = 'common_pitfalls'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    hc_id = db.Column(db.Integer, db.ForeignKey('hcs.id'), nullable=False)

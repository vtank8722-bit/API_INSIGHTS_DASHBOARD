from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Insight(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    repo_name = db.Column(db.String(200), nullable=False)

    stars = db.Column(db.Integer)
    forks = db.Column(db.Integer)
    open_issues = db.Column(db.Integer)
    language = db.Column(db.String(100))

    note = db.Column(db.String(500))
    priority = db.Column(db.String(20))

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
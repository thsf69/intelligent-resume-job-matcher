from app import db
from flask_login import UserMixin
from datetime import datetime, timezone

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    resumes = db.relationship('Resume', backref='author', lazy=True)
    jobs = db.relationship('Job', backref='author', lazy=True)
    analyses = db.relationship('Analysis', backref='user', lazy=True)

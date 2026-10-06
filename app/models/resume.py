from app import db
from datetime import datetime, timezone

class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    extracted_skills = db.Column(db.Text, nullable=True) # JSON string
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    analyses = db.relationship('Analysis', backref='resume', lazy=True)

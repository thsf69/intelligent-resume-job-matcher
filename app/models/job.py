from app import db
from datetime import datetime, timezone

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=False)
    extracted_requirements = db.Column(db.Text, nullable=True) # JSON string
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    analyses = db.relationship('Analysis', backref='job', lazy=True)

from app import db
from datetime import datetime, timezone

class Analysis(db.Model):
    __tablename__ = 'analyses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    
    overall_score = db.Column(db.Float, nullable=False)
    skill_score = db.Column(db.Float, nullable=False)
    similarity_score = db.Column(db.Float, nullable=False)
    experience_score = db.Column(db.Float, nullable=False)
    education_score = db.Column(db.Float, nullable=False)
    
    matched_skills = db.Column(db.Text, nullable=True) # JSON string
    missing_skills = db.Column(db.Text, nullable=True) # JSON string
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

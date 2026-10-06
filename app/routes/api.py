from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models.resume import Resume
from app.models.job import Job
from app.models.analysis import Analysis
import json

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@api_bp.route('/resumes', methods=['GET'])
@login_required
def get_resumes():
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    return jsonify([{"id": r.id, "name": r.name} for r in resumes]), 200

@api_bp.route('/jobs', methods=['GET'])
@login_required
def get_jobs():
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    return jsonify([{"id": j.id, "title": j.title} for j in jobs]), 200

from flask import request
from app.services.matcher import calculate_match_score
from app import db

@api_bp.route('/analyze', methods=['POST'])
@login_required
def analyze():
    data = request.get_json()
    if not data or 'resume_id' not in data or 'job_id' not in data:
        return jsonify({"error": "resume_id and job_id are required"}), 400
        
    resume = Resume.query.filter_by(id=data['resume_id'], user_id=current_user.id).first()
    job = Job.query.filter_by(id=data['job_id'], user_id=current_user.id).first()
    
    if not resume or not job:
        return jsonify({"error": "Resume or Job not found"}), 404
        
    resume_skills = json.loads(resume.extracted_skills) if resume.extracted_skills else []
    job_requirements = json.loads(job.extracted_requirements) if job.extracted_requirements else []
    
    match_results = calculate_match_score(
        resume.content, 
        job.description, 
        resume_skills, 
        job_requirements
    )
    
    analysis = Analysis(
        user_id=current_user.id,
        resume_id=resume.id,
        job_id=job.id,
        overall_score=match_results['overall_score'],
        skill_score=match_results['skill_score'],
        similarity_score=match_results['similarity_score'],
        experience_score=match_results['experience_score'],
        education_score=match_results['education_score'],
        matched_skills=json.dumps(match_results['matched_skills']),
        missing_skills=json.dumps(match_results['missing_skills'])
    )
    
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify({"message": "Analysis successful", "analysis_id": analysis.id, "score": analysis.overall_score}), 201

@api_bp.route('/analysis/<int:id>', methods=['GET'])
@login_required
def get_analysis(id):
    analysis = Analysis.query.filter_by(id=id, user_id=current_user.id).first()
    if not analysis:
        return jsonify({"error": "Analysis not found"}), 404
        
    return jsonify({
        "id": analysis.id,
        "resume_id": analysis.resume_id,
        "job_id": analysis.job_id,
        "overall_score": analysis.overall_score,
        "skill_score": analysis.skill_score,
        "similarity_score": analysis.similarity_score,
        "experience_score": analysis.experience_score,
        "education_score": analysis.education_score,
        "matched_skills": json.loads(analysis.matched_skills) if analysis.matched_skills else [],
        "missing_skills": json.loads(analysis.missing_skills) if analysis.missing_skills else []
    }), 200

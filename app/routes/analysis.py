from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models.resume import Resume
from app.models.job import Job
from app.models.analysis import Analysis
from app import db
from app.services.matcher import calculate_match_score
import json

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@analysis_bp.route('/', methods=['GET'])
@login_required
def history():
    analyses = Analysis.query.filter_by(user_id=current_user.id).order_by(Analysis.created_at.desc()).all()
    return render_template('history.html', analyses=analyses)

@analysis_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_analysis():
    if request.method == 'POST':
        resume_id = request.form.get('resume_id')
        job_id = request.form.get('job_id')
        
        if not resume_id or not job_id:
            flash('Please select both a resume and a job.')
            return redirect(url_for('analysis.new_analysis'))
            
        resume = Resume.query.filter_by(id=resume_id, user_id=current_user.id).first()
        job = Job.query.filter_by(id=job_id, user_id=current_user.id).first()
        
        if not resume or not job:
            abort(404)
            
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
        
        return redirect(url_for('analysis.view_analysis', id=analysis.id))
        
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    return render_template('analysis.html', resumes=resumes, jobs=jobs)

@analysis_bp.route('/<int:id>')
@login_required
def view_analysis(id):
    analysis = Analysis.query.filter_by(id=id, user_id=current_user.id).first()
    if not analysis:
        abort(404)
        
    matched_skills = json.loads(analysis.matched_skills) if analysis.matched_skills else []
    missing_skills = json.loads(analysis.missing_skills) if analysis.missing_skills else []
    
    resume_skills = json.loads(analysis.resume.extracted_skills) if analysis.resume.extracted_skills else []
    job_reqs = json.loads(analysis.job.extracted_requirements) if analysis.job.extracted_requirements else []
    
    return render_template('analysis_result.html', 
                           analysis=analysis,
                           matched_skills=matched_skills,
                           missing_skills=missing_skills,
                           resume_skills=resume_skills,
                           job_reqs=job_reqs)

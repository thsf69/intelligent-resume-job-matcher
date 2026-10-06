from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.job import Job
from app import db
from app.services.job_parser import parse_job_description
import json

jobs_bp = Blueprint('jobs', __name__, url_prefix='/job')

@jobs_bp.route('/', methods=['GET'])
@login_required
def list_jobs():
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    return render_template('job.html', jobs=jobs)

@jobs_bp.route('/add', methods=['POST'])
@login_required
def add_job():
    title = request.form.get('title')
    company = request.form.get('company', '')
    description = request.form.get('description')
    
    if not description or not description.strip():
        flash('Job description cannot be empty.')
        return redirect(url_for('jobs.list_jobs'))
        
    if not title:
        title = "Untitled Job"

    parsed = parse_job_description(description)
    requirements = parsed.get('requirements', [])
    
    new_job = Job(
        user_id=current_user.id,
        title=title,
        company=company,
        description=description,
        extracted_requirements=json.dumps(requirements)
    )
    
    db.session.add(new_job)
    db.session.commit()
    
    flash('Job added successfully.')
    return redirect(url_for('jobs.list_jobs'))

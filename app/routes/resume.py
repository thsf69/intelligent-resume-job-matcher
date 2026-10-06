from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.resume import Resume
from app import db
from app.services.resume_parser import parse_resume
import json

resume_bp = Blueprint('resume', __name__, url_prefix='/resume')

@resume_bp.route('/', methods=['GET'])
@login_required
def list_resumes():
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    return render_template('resume.html', resumes=resumes)

@resume_bp.route('/add', methods=['POST'])
@login_required
def add_resume():
    name = request.form.get('name')
    content = ""
    
    # Handle text paste
    text_content = request.form.get('content')
    if text_content and text_content.strip():
        content = text_content.strip()
    
    # Handle file upload
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            if file.filename.endswith('.txt'):
                content = file.read().decode('utf-8')
            else:
                flash('Only .txt files are supported currently.')
                return redirect(url_for('resume.list_resumes'))
                
    if not content:
        flash('Resume content cannot be empty.')
        return redirect(url_for('resume.list_resumes'))
        
    if not name:
        name = "Untitled Resume"

    parsed = parse_resume(content)
    skills = parsed.get('skills', [])
    
    new_resume = Resume(
        user_id=current_user.id,
        name=name,
        content=content,
        extracted_skills=json.dumps(skills)
    )
    
    db.session.add(new_resume)
    db.session.commit()
    
    flash('Resume added successfully.')
    return redirect(url_for('resume.list_resumes'))

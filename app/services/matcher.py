import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def calculate_match_score(resume_text, job_text, resume_skills, job_requirements):
    # 1. Skill Match (50%)
    if not job_requirements:
        skill_score = 100.0
        matched_skills = resume_skills
        missing_skills = []
    else:
        matched_skills = [skill for skill in job_requirements if skill in resume_skills]
        missing_skills = [skill for skill in job_requirements if skill not in resume_skills]
        skill_score = (len(matched_skills) / len(job_requirements)) * 100.0

    # 2. Text Similarity (25%)
    # Clean text
    clean_resume = re.sub(r'[^a-zA-Z0-9\s]', '', resume_text.lower())
    clean_job = re.sub(r'[^a-zA-Z0-9\s]', '', job_text.lower())
    
    if clean_job.strip() and clean_resume.strip():
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([clean_job, clean_resume])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            similarity_score = similarity * 100.0
        except ValueError:
            similarity_score = 0.0
    else:
        similarity_score = 0.0

    # 3. Experience Relevance (15%) - Mock logic based on keywords
    exp_keywords = ['years', 'experience', 'senior', 'junior', 'lead', 'manager', 'role']
    exp_matches = sum(1 for kw in exp_keywords if kw in clean_resume and kw in clean_job)
    experience_score = min(100.0, exp_matches * 20.0)
    if experience_score == 0 and 'experience' in clean_resume:
        experience_score = 50.0

    # 4. Education Relevance (10%) - Mock logic based on keywords
    edu_keywords = ['degree', 'bachelor', 'master', 'phd', 'university', 'college', 'cs', 'computer science']
    edu_matches = sum(1 for kw in edu_keywords if kw in clean_resume and kw in clean_job)
    education_score = min(100.0, edu_matches * 30.0)
    if education_score == 0 and ('degree' in clean_resume or 'university' in clean_resume):
        education_score = 50.0

    # Calculate overall
    overall_score = (skill_score * 0.50) + (similarity_score * 0.25) + (experience_score * 0.15) + (education_score * 0.10)

    return {
        "overall_score": round(overall_score, 1),
        "skill_score": round(skill_score, 1),
        "similarity_score": round(similarity_score, 1),
        "experience_score": round(experience_score, 1),
        "education_score": round(education_score, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }

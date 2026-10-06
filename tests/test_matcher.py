from app.services.matcher import calculate_match_score

def test_calculate_match_score():
    resume_skills = ["Python", "Flask", "SQL", "Git", "Java"]
    job_reqs = ["Python", "Flask", "SQL", "Git", "Docker", "AWS"]
    
    resume_text = "Experienced software engineer with 5 years in Python, Flask, SQL, and Git. I have a degree in Computer Science."
    job_text = "Looking for a senior developer with experience in Python, Flask, SQL, Git, Docker, and AWS. Must have a bachelor degree."
    
    result = calculate_match_score(resume_text, job_text, resume_skills, job_reqs)
    
    assert "overall_score" in result
    assert result["skill_score"] == round((4 / 6) * 100.0, 1)
    assert "Docker" in result["missing_skills"]
    assert "AWS" in result["missing_skills"]
    assert "Python" in result["matched_skills"]
    assert result["experience_score"] > 0
    assert result["education_score"] > 0
    assert result["similarity_score"] > 0

def test_empty_requirements():
    result = calculate_match_score("resume", "job", ["Python"], [])
    assert result["skill_score"] == 100.0
    assert len(result["missing_skills"]) == 0

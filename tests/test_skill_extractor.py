from app.services.skill_extractor import extract_skills_from_text, normalize_skill

def test_extract_skills():
    text = "I am a Python developer with 5 years of Flask and SQL experience. Also C++."
    skills = extract_skills_from_text(text)
    assert "Python" in skills
    assert "Flask" in skills
    assert "SQL" in skills
    assert "C++" in skills
    assert "Java" not in skills

def test_case_insensitivity():
    text = "python, flask, sql"
    skills = extract_skills_from_text(text)
    assert "Python" in skills
    assert "Flask" in skills
    assert "SQL" in skills

def test_normalize_skill():
    assert normalize_skill("python") == "Python"
    assert normalize_skill("  FLASK  ") == "Flask"
    assert normalize_skill("UnknownSkill") == "Unknownskill"

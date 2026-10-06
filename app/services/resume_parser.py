from .skill_extractor import extract_skills_from_text

def parse_resume(text):
    skills = extract_skills_from_text(text)
    
    # In a real app we might extract sections.
    # For now, we will just return extracted skills as a list.
    return {
        "skills": skills
    }

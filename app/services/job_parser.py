from .skill_extractor import extract_skills_from_text

def parse_job_description(text):
    requirements = extract_skills_from_text(text)
    
    return {
        "requirements": requirements
    }

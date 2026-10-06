import re
import json

SKILL_DICTIONARY = {
    "Programming": ["Python", "Java", "JavaScript", "C", "C++", "C#", "SQL", "Ruby", "PHP", "Go", "Swift", "TypeScript", "R"],
    "Web": ["HTML", "CSS", "JavaScript", "Flask", "Django", "REST API", "React", "Angular", "Vue", "Node.js", "Express"],
    "Databases": ["MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis", "Oracle", "SQL Server", "Cassandra", "DynamoDB"],
    "Data": ["Pandas", "NumPy", "Excel", "Power BI", "Tableau", "Hadoop", "Spark", "Kafka"],
    "Machine Learning": ["Machine Learning", "NLP", "Scikit-learn", "TensorFlow", "PyTorch", "Keras", "Deep Learning"],
    "Cloud / DevOps": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Git", "GitHub", "GitLab", "Linux", "CI/CD", "Jenkins", "Terraform"]
}

# Flatten the dictionary for quick lookups and normalization
NORMALIZED_SKILLS = {}
for category, skills in SKILL_DICTIONARY.items():
    for skill in skills:
        NORMALIZED_SKILLS[skill.lower()] = skill

def normalize_skill(skill):
    skill_lower = skill.lower().strip()
    return NORMALIZED_SKILLS.get(skill_lower, skill.strip().title())

def extract_skills_from_text(text):
    if not text:
        return []
    
    found_skills = set()
    text_lower = text.lower()
    
    # We pad the text with spaces to match word boundaries easily, 
    # but re.finditer with \b is better.
    for category, skills in SKILL_DICTIONARY.items():
        for skill in skills:
            # Escape regex characters in skill (like C++)
            escaped_skill = re.escape(skill.lower())
            
            # Use word boundaries if it's alphanumeric, otherwise just normal find
            if escaped_skill.isalnum():
                pattern = r'\b' + escaped_skill + r'\b'
            elif '+' in escaped_skill or '#' in escaped_skill:
                # Handle C++, C#
                pattern = escaped_skill + r'(?!\w)'
            else:
                pattern = r'\b' + escaped_skill + r'\b'
                
            if re.search(pattern, text_lower):
                found_skills.add(skill)
                
    # Additional naive check for things not exactly in dict but might be interesting?
    # Keeping it to the dictionary for reliability as requested.
    return sorted(list(found_skills))


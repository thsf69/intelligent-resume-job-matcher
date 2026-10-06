# Intelligent Resume & Job Matching Platform

## Project Overview
This platform is an intelligent web-based tool designed to analyze candidate resumes against job descriptions. It extracts technical skills, educational requirements, and experience keywords using NLP techniques, computing a deterministic match score.

## Features
- **User Authentication**: Secure registration and login with session management.
- **Resume & Job Parsing**: Extracts technical skills from text using a robust categorization dictionary.
- **Intelligent Matching**: Computes a detailed score based on skill overlap, text similarity (TF-IDF/Cosine Similarity), experience relevance, and education matches.
- **Match Insights**: Highlights matched skills, missing requirements, and provides actionable recommendations.
- **History Tracking**: Saves previous analyses securely for each user.
- **REST API**: Provides JSON endpoints for core resources.

## Architecture
- **Backend**: Python 3, Flask, Flask-Login
- **Database**: SQLite, Flask-SQLAlchemy (ORM)
- **Data / NLP**: Regular Expressions, scikit-learn (TF-IDF Vectorizer, Cosine Similarity)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Testing**: pytest

## Scoring Methodology
The matching algorithm calculates an overall score (0-100) based on four weighted components:
1. **Skill Match (50%)**: Direct overlap of extracted resume skills against job requirements.
2. **Text Similarity (25%)**: Cosine similarity between TF-IDF vectorized representations of the resume and job description.
3. **Experience Relevance (15%)**: Keyword-based heuristics identifying years of experience and seniority.
4. **Education Relevance (10%)**: Keyword-based heuristics for degrees and academic fields.

## Installation & Running Locally

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application (this will automatically create the database)
python run.py
```
Access the application at `http://127.0.0.1:5000`

## Testing
Run the comprehensive test suite:
```bash
pytest
```

## Security Considerations
- Passwords hashed securely via Werkzeug's `scrypt`.
- Route-level authorization ensures users can only access their own data.
- ID-based lookups are validated against `current_user.id` to prevent IDOR vulnerabilities.
- Cross-Site Request Forgery (CSRF) protections can be enabled easily.

## Interview Explanation (30 seconds)
"I built a full-stack Flask application that automates the resume screening process. It uses regex and a custom dictionary to extract technical skills, then leverages scikit-learn for TF-IDF cosine similarity to score the resume against the job description. The data is securely stored in a SQLite database using SQLAlchemy, with user authentication handled via Flask-Login. It's fully tested with pytest and deployed using standard web technologies."

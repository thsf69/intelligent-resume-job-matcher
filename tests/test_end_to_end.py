from app.models.analysis import Analysis
from app import db
import json

def test_full_workflow(client, app):
    # 1. Register user & Login (done by fixture and login helper)
    client.post('/login', data=dict(
        email='test@example.com',
        password='password'
    ), follow_redirects=True)
    
    # 2. Add Resume
    client.post('/resume/add', data=dict(
        name='Fullstack Developer Resume',
        content='I am an experienced developer skilled in Python, Flask, JavaScript, and HTML. I have 3 years of experience building web apps.'
    ), follow_redirects=True)
    
    # 3. Add Job
    client.post('/job/add', data=dict(
        title='Python Web Dev',
        company='Tech Startup',
        description='We are looking for a developer with experience in Python, Flask, React, and SQL. 3 years experience required.'
    ), follow_redirects=True)
    
    # 4. Run Analysis
    response = client.post('/analysis/new', data=dict(
        resume_id=1,
        job_id=1
    ), follow_redirects=True)
    
    assert response.status_code == 200
    
    # 5. Verify results are visible
    assert b'Match Analysis' in response.data
    assert b'Python' in response.data
    assert b'Flask' in response.data
    assert b'React' in response.data
    
    # Verify in DB
    with app.app_context():
        analysis = Analysis.query.first()
        assert analysis is not None
        assert analysis.overall_score > 0
        
        matched = json.loads(analysis.matched_skills)
        missing = json.loads(analysis.missing_skills)
        
        assert 'Python' in matched
        assert 'Flask' in matched
        assert 'React' in missing
        assert 'SQL' in missing

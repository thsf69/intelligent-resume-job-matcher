import json
from app.models.resume import Resume
from app.models.job import Job
from app import db

def login(client):
    return client.post('/login', data=dict(
        email='test@example.com',
        password='password'
    ), follow_redirects=True)

def login_other(client):
    client.get('/logout')
    return client.post('/login', data=dict(
        email='other@example.com',
        password='password'
    ), follow_redirects=True)

def test_add_resume(client, app):
    login(client)
    response = client.post('/resume/add', data=dict(
        name='My Resume',
        content='I know Python and Java.'
    ), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'My Resume' in response.data
    
    with app.app_context():
        resume = Resume.query.first()
        assert resume is not None
        assert resume.name == 'My Resume'
        skills = json.loads(resume.extracted_skills)
        assert 'Python' in skills
        assert 'Java' in skills

def test_add_job(client, app):
    login(client)
    response = client.post('/job/add', data=dict(
        title='Backend Dev',
        company='Google',
        description='Need Python and SQL.'
    ), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Backend Dev' in response.data
    
    with app.app_context():
        job = Job.query.first()
        assert job is not None
        reqs = json.loads(job.extracted_requirements)
        assert 'Python' in reqs
        assert 'SQL' in reqs

def test_api_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    
def test_unauthorized_access(client, app):
    # Create a resume as test user
    login(client)
    client.post('/resume/add', data=dict(name='Test Resume', content='Python'))
    client.post('/job/add', data=dict(title='Test Job', description='Python'))
    client.post('/analysis/new', data=dict(resume_id=1, job_id=1))
    client.get('/logout')
    
    # Login as other user
    login_other(client)
    
    # Try to view analysis 1
    response = client.get('/analysis/1')
    assert response.status_code == 404 # Should be blocked

def test_api_endpoints(client, app):
    login(client)
    
    # Setup test data
    client.post('/resume/add', data=dict(name='Test Resume', content='Python'))
    client.post('/job/add', data=dict(title='Test Job', description='Python'))
    
    # Test POST /api/analyze
    response = client.post('/api/analyze', json={'resume_id': 1, 'job_id': 1})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'analysis_id' in data
    
    analysis_id = data['analysis_id']
    
    # Test GET /api/analysis/<id>
    response = client.get(f'/api/analysis/{analysis_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['overall_score'] > 0
    assert 'Python' in data['matched_skills']
    
    # Test unauthorized access to API
    login_other(client)
    response = client.get(f'/api/analysis/{analysis_id}')
    assert response.status_code == 404
    
    # Test invalid payload
    login(client)
    response = client.post('/api/analyze', json={'resume_id': 999, 'job_id': 999})
    assert response.status_code == 404

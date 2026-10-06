def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_successful_login(client):
    response = client.post('/login', data=dict(
        email='test@example.com',
        password='password'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data

def test_invalid_login(client):
    response = client.post('/login', data=dict(
        email='test@example.com',
        password='wrongpassword'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Please check your login details and try again.' in response.data

def test_logout(client):
    client.post('/login', data=dict(email='test@example.com', password='password'))
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

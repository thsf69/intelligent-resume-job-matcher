import pytest
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        
        # Create a test user
        user = User(
            name="Test User",
            email="test@example.com",
            password_hash=generate_password_hash("password", method='scrypt')
        )
        db.session.add(user)
        
        user2 = User(
            name="Other User",
            email="other@example.com",
            password_hash=generate_password_hash("password", method='scrypt')
        )
        db.session.add(user2)
        
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

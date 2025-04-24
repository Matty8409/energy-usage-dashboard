import pytest
from app.app import server as app  # Use the existing server instance
from app.database import db

@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.drop_all()  # Clear the database
        db.create_all()  # Create tables
        # Add a test user to the database
        from app.models import User
        from werkzeug.security import generate_password_hash
        test_user = User(username="testuser", password_hash=generate_password_hash("testpassword"))
        db.session.add(test_user)
        db.session.commit()

    with app.test_client() as client:
        yield client

def test_login_success(client):
    print(app.url_map)
    response = client.post('/login', json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json['message'] == "Login successful"  # Ensure the response contains the expected message

def test_login_failure(client):
    response = client.post('/login', json={"username": "wronguser", "password": "wrongpassword"})
    assert response.status_code == 401  # Ensure the status code is 401 for invalid credentials
    assert response.json['error'] == "Invalid username or password"  # Ensure the response contains the expected error
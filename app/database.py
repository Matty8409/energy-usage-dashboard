from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # Import User here to avoid circular import
        from app.models import User
        # Add a default test user if it doesn't already exist
        if not User.query.filter_by(username="testuser").first():
            test_user = User(username="testuser", password_hash=generate_password_hash("testpassword"))
            db.session.add(test_user)
            db.session.commit()
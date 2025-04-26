from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        # Import your User model here to avoid circular import issues
        from app.models import User  # Assuming Base is included in User model

        db.create_all()  # This should be enough to create tables for defined models

        # Initialize the database engine
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])  # Use your app's database URI

        # Check if the 'user' table already exists
        inspector = inspect(engine)
        if 'user' not in inspector.get_table_names():
            # Create the table if it does not exist
            db.create_all()

        # Add a default test user if it doesn't already exist
        if not User.query.filter_by(username="testuser").first():
            test_user = User(username="testuser", password_hash=generate_password_hash("testpassword"))
            db.session.add(test_user)
            db.session.commit()

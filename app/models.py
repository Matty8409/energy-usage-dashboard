from app.database import db
# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=False, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
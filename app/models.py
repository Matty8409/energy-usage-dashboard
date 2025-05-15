# app/models.py
from app.database import db
# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=False, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)

class SavedCollection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), nullable=False)
    energy_type = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    input = db.Column(db.String(255), nullable=True)
    datetime = db.Column(db.String(255), nullable=False)
    values = db.Column(db.JSON, nullable=False)  # Store the data as JSON

# app/auth.py
from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from app.models import User

# Login a user
def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return {'error': 'Invalid username or password'}, 401  # Return a dictionary with a 401 status code

    session['user_id'] = user.id
    return {'message': 'Login successful'}, 200  # Return a dictionary with a 200 status code

# Logout a user
def logout_user():
    session.pop('user_id', None)
    return {'message': 'Logout successful'}, 200
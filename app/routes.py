from flask import Flask, request, jsonify
from app.auth import register_user, login_user, logout_user

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    return jsonify(register_user(data['username'], data['password']))

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    return jsonify(login_user(data['username'], data['password']))

@app.route('/logout', methods=['POST'])
def logout():
    return jsonify(logout_user())
from flask import request, jsonify
from app.auth import register_user, login_user, logout_user

# Use the `server` object dynamically to avoid circular imports
def get_server():
    from app.app import server
    return server

def register_routes():
    server = get_server()

    @server.route('/register', methods=['POST'])
    def register():
        data = request.json
        return jsonify(register_user(data['username'], data['password']))

    @server.route('/login', methods=['POST'])
    def login():
        print("Login route accessed")
        data = request.json
        response, status_code = login_user(data['username'], data['password'])
        return jsonify(response), status_code  # Return the response and status code

    @server.route('/logout', methods=['POST'])
    def logout():
        return jsonify(logout_user())
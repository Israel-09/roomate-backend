#!/usr/bin/env python3
"""
main app
"""
from flask import Flask, request, jsonify, abort
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

auth = Auth()

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorised(error) -> str:
    """
    unauthorised handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def handle_forbidden(error) -> str:
    """
    forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """check if enpoint requires authentication"""
    excluded_paths = ['/api/v1/status/',
                        '/api/v1/unauthorized/', '/api/v1/forbidden/',
                        '/api/v1/auth_session/login/']

    if auth.require_auth(request.path, excluded_paths) is False:
        current_user = auth.current_user(request)
        if current_user is None:
            abort(403)
        request.current_user = current_user
            
if __name__ == '__main__':
    HOST = getenv('API_HOST', '0.0.0.0')
    PORT = getenv('API_PORT', 5000)
    app.run(debug=True, host=HOST, port=PORT)
#!/usr/bin/env python3
"""
main app
"""
from flask import Flask, jsonify
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)



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

            
if __name__ == '__main__':
    HOST = getenv('API_HOST', '0.0.0.0')
    PORT = getenv('API_PORT', 5000)
    app.run(debug=True, host=HOST, port=PORT)
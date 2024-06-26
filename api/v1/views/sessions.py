#!/usr/bin/env python3
"""
sessions view
"""
from flask import jsonify, request, abort, redirect, url_for, make_response
from api.v1.views import app_views
from api.v1.auth.auth import Auth


AUTH = Auth()


@app_views.route('/', strict_slashes=False)
def home():
    """
    home path
    """
    return jsonify({"message": "Bienvenue"})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    create new user
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if email is None or password is None:
        return jsonify({"message": "Bad request"}), 400
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app_views.route('/sessions', methods=['OPTIONS', 'POST'], strict_slashes=False)
def login():
    """implement login

    Return:
        json: login message
    """
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print(email, password)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged-in"})
        resp.set_cookie("session_id", session_id)
        return resp
    abort(401)


@app_views.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    implement logout
    """
    from sqlalchemy.orm.exc import NoResultFound

    session_id = request.cookies.get('session_id')
    print(session_id)
    user = AUTH.get_user_from_session_id(session_id=session_id)
    print(user)
    if user is not None:
        AUTH.destroy_session(user.id)
        return jsonify({"message": "successfully logged-out"})
    abort(403)


@app_views.route('/profile', strict_slashes=False)
def profile():
    """
    returns user email
    """
    session_id = request.cookies.get('session_id')
    print(session_id)
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        return jsonify({"email": user.email, "first_name":user.profile.first_name})
    abort(403)


@app_views.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_token():
    """get password reset token"""
    data = request.get_json()
    print(data)
    email = data.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app_views.route('/reset_password', methods=['PUT'], strict_slashes=False)
def reset_password():
    """reset password"""
    data = request.get_json()
    reset_token = data.get('reset_token')
    new_password = data.get('new_password')
    email = data.get('email')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)

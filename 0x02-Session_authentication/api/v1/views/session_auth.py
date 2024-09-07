#!/usr/bin/env python3
"""module for view of session auth"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from api.v1.app import auth
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login() -> str:
    """post email and password from request"""
    email = request.form.get('email')
    password = request.form.get('password')

    # validate email and password prescence
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # retrieve the User instance based on email
    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # validate password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # import auth and create session for user
    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    # return dict representation of User
    user_json = user.to_json()

    # create a response and set the session id in the cookie
    response = make_response(jsonify(user_json))
    session_name = getenv("SESSION_NAME", "_my_session_id")
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def auth_session_logout() -> str:
    """DELETE /auth_session/logout: handle session logout"""
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({})

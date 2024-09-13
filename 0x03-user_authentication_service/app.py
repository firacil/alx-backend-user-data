#!/usr/bin/env python3
"""Basic flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def basic():
    """basic form json payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
    """_summary_
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # register user if user does not exist
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"})


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login() -> str:
    """login for user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not (AUTH.valid_login(email, password)):
        abort(401)
    else:
        # create new session
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": "<user email>", "message": "logged in"})
        resp.set_cookie('session_id', session_id)

    return resp


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """_summary_
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """_summary_
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=[POST])
def get_reset_password_token() -> str:
    """_summary_
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

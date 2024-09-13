#!/usr/bin/env python3
"""Basic flask app"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

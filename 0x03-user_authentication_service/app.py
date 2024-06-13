#!/usr/bin/env python3
"""
Task 6: Basic Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth


auth = Auth()
app = Flask(__name__)


@app.route("/")
def index():
    """
    return a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    end-point to register a user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        auth.register_user(email, password)
        return jsonify(
                       {"email": "{}".format(email),
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

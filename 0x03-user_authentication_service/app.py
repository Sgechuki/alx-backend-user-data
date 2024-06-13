#!/usr/bin/env python3
"""
Task 6: Basic Flask app
"""
from flask import Flask, jsonify, request, make_response, abort
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


@app.route("/sessions", methods=["POST"])
def login():
    """
    If the login information is incorrect
    use flask.abort to respond with a 401 HTTP status
    Otherwise, create a new session for the user,
    store it the session ID as a cookie with key "session_id"
    on the response and return a JSON payload
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if auth.valid_login(email, password):
        ssn_id = auth.create_session(email)
        resp = make_response(
                             jsonify(
                                     {"email": "{}".format(email),
                                      "message": "logged in"}))
        resp.set_cookie('session_id', ssn_id)
        return resp
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

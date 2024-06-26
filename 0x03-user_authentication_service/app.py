#!/usr/bin/env python3
"""
Task 6: Basic Flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


AUTH = Auth()
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
        AUTH.register_user(email, password)
        return jsonify(
                       {"email": "{}".format(email),
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
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
    if AUTH.valid_login(email, password):
        ssn_id = AUTH.create_session(email)
        resp = jsonify({"email": "{}".format(email), "message": "logged in"})
        resp.set_cookie('session_id', ssn_id)
        return resp
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    destroy the session and redirect the user to GET /
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """
    request is expected to contain a session_id cookie
    Use it to find the user. If the user exist, respond with a 200
    If the session ID is invalid or the user does not exist
    respond with a 403 HTTP status
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": "{}".format(user.email)}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """
    If the email is not registered, respond with a 403 status code
    Otherwise, generate a token and respond with a 200
    HTTP status and the following JSON payload
    """
    email = request.form.get("email")
    try:
        tkn = AUTH.get_reset_password_token(email)
        if tkn:
            return jsonify({"email": "{}".format(email),
                            "reset_token": "{}".format(tkn)}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

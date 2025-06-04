#!/usr/bin/env python3
'''basic Flask app'''
from flask import Flask, jsonify, request, abort, make_response
from flask import redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def basic() -> None:
    '''return hello message'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    '''user registation end-point'''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """session login"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password) is False:
        abort(401)
    session_id = AUTH.create_session(email)
    res = make_response(jsonify({"email": email, "message": "logged in"}))
    res.set_cookie("session_id", session_id)
    return res


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """session logout"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('basic'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """route to get user profile"""
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Get reset password token"""
    email = request.form.get('email')
    if not email:
        abort(403)
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

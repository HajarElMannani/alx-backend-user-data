#!/usr/bin/env python3
""" Module of session authenticaton  views
"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_session():
    '''session authentication'''
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not user or user == []:
        return jsonify({"error": "no user found for this email"}), 404
    if user[0].is_valid_password(password) is False:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    resp = make_response(jsonify(user[0].to_json()))
    resp.set_cookie(getenv('SESSION_NAME'), session_id)
    return resp


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    '''session logout'''
    from api.v1.app import auth
    destroyed = auth.destroy_session(request)
    if destroyed is False:
        abort(404)
    return jsonify({}), 200

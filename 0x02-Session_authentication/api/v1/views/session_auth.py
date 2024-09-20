#!/usr/bin/env python3
"""
Module for Session Authentication Views
"""
from flask import (
    request,
    jsonify,
    abort
)
from flask.typing import ResponseReturnValue
from os import getenv
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> ResponseReturnValue:
    """
    Login in user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({'error': 'email missing'}), 400

    if not password:
        return jsonify({'error': 'password missing'}), 400

    try:
        user = User.search({'email': email})
        if len(user) >= 1:
            if user[0].is_valid_password(password):
                from api.v1.app import auth
                session_id = auth.create_session(user[0].id)
                resp = jsonify(user[0].to_json())
                resp.set_cookie(getenv('SESSION_NAME'), session_id)

                return resp

            return jsonify({
                'error': 'wrong password'
            }), 401

        return jsonify({
            'error': 'no user found for this email'
        }), 404
    except Exception:
        return jsonify({
            'error': 'no user found for this email'
        }), 404


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False
)
def logout() -> ResponseReturnValue:
    """
    Log out user
    """
    from api.v1.app import auth

    status = auth.destroy_session(request)
    if not status:
        abort(404)

    return jsonify({}), 200

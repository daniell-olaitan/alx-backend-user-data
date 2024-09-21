#!/usr/bin/env python3
"""
Application module
"""
from auth import Auth
from flask import (
    Flask,
    jsonify,
    request,
    abort,
    redirect,
    url_for
)

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index() -> str:
    """
    Get the index
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    Register users
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)

        return jsonify({
            'email': user.email,
            'message': 'user created'
        })
    except ValueError:
        return jsonify({
            'message': 'email already registered'
        }), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    Create a new session and log a user in
    """
    try:
        email = request.form['email']
        password = request.form['password']

        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            resp = jsonify({'email': email, 'message': 'logged in'})
            resp.set_cookie('session_id', session_id)

            return resp
        abort(401)
    except Exception:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """
    Log out a given user and delete the user session
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        redirect(url_for('/'))

    abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """
    Get the user profile
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({'email': user.email})

    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """
    Generate reset token for the user
    """
    try:
        email = request.form.get('email')
        token = AUTH.get_reset_password_token(email)

        return jsonify(
            {'email': email, 'reset_token': token}
        )
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """
    Update password
    """
    try:
        email = request.form['email']
        reset_token = request.form['reset_token']
        new_password = request.form['new_password']

        AUTH.update_password(reset_token, new_password)
        return jsonify({
            'email': email,
            'message': "Password updated"
        })
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

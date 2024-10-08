#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = getenv('AUTH_TYPE')
if auth == 'auth':
    auth = Auth()
elif auth == 'basic_auth':
    auth = BasicAuth()
elif auth == 'session_auth':
    auth = SessionAuth()
elif auth == 'session_exp_auth':
    auth = SessionExpAuth()
elif auth == 'session_db_auth':
    auth = SessionDBAuth()


@app.before_request
def validate_user():
    """
    Validate users before handling requests
    """
    excluded_paths = [
        '/api/v1/stat*',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]

    if ((auth is not None) and
            auth.require_auth(request.path, excluded_paths)):
        if (auth.authorization_header(request) is None and
                auth.session_cookie(request) is None):
            abort(401)

        current_user = auth.current_user(request)
        if current_user is None:
            abort(403)

        request.current_user = current_user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Authorization error
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """Forbidden error
    """
    return jsonify({'error': 'Forbidden'}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)

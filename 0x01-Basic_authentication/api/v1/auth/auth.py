#!/usr/bin/env python3
"""
Provide authentication implementation
"""
from flask import request
import typing as t
from werkzeug.wrappers import Request

UserType = t.TypeVar('User')


class Auth:
    """
    Base class for basic user authentication
    """
    def require_auth(self, path: str, excluded_paths: t.List[str]) -> bool:
        """
        Check if path requires authentication
        """
        if (path is None) or (not excluded_paths):
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                excluded_path = excluded_path[:-1]

            if excluded_path in path:
                return False

        return True

    def authorization_header(self, request: Request = None) -> str:
        """
        Get the authorization header from the request
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request: Request = None) -> UserType:
        """
        Get the current authenticated user
        """
        return None

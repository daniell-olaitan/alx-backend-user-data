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
        Check if path is to be excluded
        """
        if (path is None) or (not excluded_paths):
            return True

        if not path.endswith('/'):
            path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request: Request = None) -> str:
        """
        Validate requests
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request: Request = None) -> UserType:
        """
        Template for upcoming tasks
        """
        return None

#!/usr/bin/env python3
"""
Provide authentication implementation
"""
from flask import request
import typing as t
from werkzeug.wrappers import Request


class Auth:
    """
    Base class for basic user authentication
    """
    def require_auth(self, path: str, excluded_paths: t.List[str]) -> bool:
        """
        Template for upcoming tasks
        """
        return False

    def authorization_header(self, request: Request = None) -> str:
        """
        Template for upcoming tasks
        """
        return None

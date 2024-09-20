#!/usr/bin/env python3
"""
Implement session authentication class
"""
from api.v1.auth.auth import Auth
from werkzeug.wrappers import Request
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    Implement Session Authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a new session
        """
        if user_id is None or type(user_id) is not str:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id.update({session_id: user_id})

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Get user id from a session
        """
        if session_id is None or type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request: Request = None) -> User:
        """
        Get the current authenticated user
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request: Request = None) -> bool:
        """
        Log a user out and delete user session
        """
        session_id = self.session_cookie(request)
        if request is None or session_id is None:
            return False

        if self.user_id_for_session_id(session_id) is None:
            return False

        del self.user_id_by_session_id[session_id]

        return True

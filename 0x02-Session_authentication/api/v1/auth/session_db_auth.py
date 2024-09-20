#!/usr/bin/env python3
"""
Module for Persistent Session Authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from werkzeug.wrappers import Request
from datetime import (
    datetime,
    timedelta
)


class SessionDBAuth(SessionExpAuth):
    """
    Implement persistent session authentication
    """
    def create_session(self, user_id: str = None) -> str:
        """
        Create a user session
        """
        session_id = super().create_session(user_id)
        user_session = UserSession(
            user_id=user_id,
            session_id=session_id
        )

        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id: str = None):
        """
        Get the id of the current user
        """
        if session_id is None:
            return None

        try:
            sessions = UserSession.search({'session_id': session_id})
            if len(sessions) >= 1:
                user_session = sessions[0]
                if self.session_duration <= 0:
                    return user_session.user_id

                if user_session.created_at is None:
                    return None

                expire_time = (user_session.created_at
                               + timedelta(seconds=self.session_duration))

                if expire_time < datetime.now():
                    return None

                return user_session.user_id

            return None
        except Exception:
            return None

    def destroy_session(self, request: Request = None) -> str:
        """
        Destroy a session
        """
        session_id = self.session_cookie(request)
        if request is None or session_id is None:
            return False

        try:
            sessions = UserSession.search({'session_id': session_id})
            if len(sessions) >= 1:
                sessions[0].remove()

                return True

            return False
        except Exception:
            return False

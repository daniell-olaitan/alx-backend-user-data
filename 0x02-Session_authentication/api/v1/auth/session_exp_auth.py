#!/usr/bin/env python3
"""
Module for Expirable Session Authentication
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import (
    datetime,
    timedelta
)


class SessionExpAuth(SessionAuth):
    """
    Implement Expirable session authentication
    """
    def __init__(self) -> None:
        """
        Initialization method
        """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except TypeError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """
        Create session for user
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id.update({
            session_id: {
                'user_id': user_id,
                'created_at': datetime.now()
            }
        })

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Get user id for a given session
        """
        if session_id is None:
            return None

        user_session = self.user_id_by_session_id.get(session_id)
        if user_session is None:
            return None

        if self.session_duration <= 0:
            return user_session.get('user_id')

        if user_session.get('created_at') is None:
            return None

        elapsed_time = (user_session.get('created_at')
                        + timedelta(seconds=self.session_duration))

        if elapsed_time < datetime.now():
            return None

        return user_session.get('user_id')

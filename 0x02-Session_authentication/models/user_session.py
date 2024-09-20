#!/usr/bin/env python3
"""
Module for for session model
"""
from models.base import Base


class UserSession(Base):
    """
    Implement persistent session
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialization method
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

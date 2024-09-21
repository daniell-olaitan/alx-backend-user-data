#!/usr/bin/env python3
"""
Module for Authentication
"""
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import typing as t


def _hash_password(password: str) -> bytes:
    """
    Hash a given password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate UUID string
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Create and register a new user
        """
        try:
            user = self._db.find_user_by(email=email)

            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(
                email=email,
                hashed_password=hashed_password
            )

            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True

            return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """
        Create a new user session
        """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()

            return user.session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> t.Optional[User]:
        """
        Get a user using the given session id
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)

            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session id of the user whose id is gievn
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)

            return reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update user password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
            )

            self._db.update_user(
                user.id,
                hashed_password=hashed_pwd,
                reset_token=None
            )
        except Exception:
            raise ValueError

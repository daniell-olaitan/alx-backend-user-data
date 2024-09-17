#!/usr/bin/env python3
"""
Implement a function that perform password encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a given password
    """
    password = password.encode('utf-8')

    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Verify the validity of a password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

#!/usr/bin/env python3
"""
End-to-end integration test for the project
"""
import requests
URL = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """
    Test register_user
    """
    payload = {
        'email': email,
        'password': password
    }

    resp = requests.post(f"{URL}/users", data=payload)
    assert resp.status_code == 200
    assert resp.json() == {
        'email': email,
        'message': 'user created'
    }


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test log in with wrong password
    """
    payload = {
        'email': email,
        'password': password
    }

    resp = requests.post(f"{URL}/sessions", data=payload)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Test Log in with correct credentials
    """
    payload = {
        'email': email,
        'password': password
    }

    resp = requests.post(f"{URL}/sessions", data=payload)
    assert resp.status_code == 200
    assert resp.json() == {'email': email, 'message': 'logged in'}

    return resp.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Test profile without cookie
    """
    resp = requests.get(f"{URL}/profile")
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Test profile with cookies
    """
    resp = requests.get(
        f"{URL}/profile",
        cookies={'session_id': session_id}
    )

    assert resp.status_code == 200
    assert resp.json() == {'email': "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    """
    Test Log out
    """
    resp = requests.delete(
        f"{URL}/sessions",
        cookies={'session_id': session_id}
    )

    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Test password reset token generation
    """
    resp = requests.post(f"{URL}/reset_password", data={'email': email})
    assert resp.status_code == 200
    assert resp.json().get('email') == email

    return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test password update
    """
    payload = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }

    resp = requests.put(f"{URL}/reset_password", data=payload)
    assert resp.status_code == 200
    assert resp.json() == {
            'email': email,
            'message': "Password updated"
        }


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == '__main__':
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

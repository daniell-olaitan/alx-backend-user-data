#!/usr/bin/env python3
"""
Implement Basic authentication class
"""
from api.v1.auth.auth import (
   Auth,
   UserType
)
import base64
import binascii
import typing as t
from models.user import User
from werkzeug.wrappers import Request


class BasicAuth(Auth):
    """
    Implement basic authentication
    """
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """
        Extract the base64 auth token from the request header
        """
        if ((authorization_header is None) or
                not isinstance(authorization_header, str)):
            return None

        auth_string = authorization_header.split(' ')
        if len(auth_string) == 2:
            if auth_string[0] == 'Basic':
                return auth_string[1]

        return None

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """
        Decode the base64 auth token from the request header
        """
        if ((base64_authorization_header is None) or
                not isinstance(base64_authorization_header, str)):
            return None

        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            auth_bytes = base64.b64decode(base64_bytes)

            return auth_bytes.decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> t.Tuple[str, str]:
        """
        Extract user credentials from request authorization header
        """
        if ((decoded_base64_authorization_header is None) or
                not isinstance(decoded_base64_authorization_header, str)):
            return None, None

        idx = decoded_base64_authorization_header.find(':')
        if idx == -1:
            return None, None

        credentials = (
            decoded_base64_authorization_header[:idx],
            decoded_base64_authorization_header[idx + 1:]
        )

        return credentials

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> UserType:
        """
        Fetch the user with the given credentials
        """
        if ((user_email is None) or
            (user_pwd is None) or
            not isinstance(user_email, str) or
                not isinstance(user_pwd, str)):
            return None

        users = User.search({'email': user_email})
        if len(users) > 0:
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user

        return None

    def current_user(self, request: Request = None) -> UserType:
        """
        Get the current authenticated user
        """
        auth_header = self.authorization_header(request)
        base64_auth = self.extract_base64_authorization_header(auth_header)
        auth = self.decode_base64_authorization_header(base64_auth)
        credentials = self.extract_user_credentials(auth)

        return self.user_object_from_credentials(*credentials)

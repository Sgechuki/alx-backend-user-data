#!/usr/bin/env python3
"""
Task 3: Auth class
"""
from flask import request
from api.v1.auth.auth import Auth
from typing import List, TypeVar
import base64
from models.user import User


class BasicAuth(Auth):
    """
    inherits from Auth
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        elif not isinstance(authorization_header, str):
            return None
        elif not authorization_header.startswith("Basic "):
            return None
        else:
            return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64
        string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        elif not isinstance(base64_authorization_header,
                            str):
            return None
        else:
            try:
                a = base64_authorization_header.encode('utf-8')
                b = base64.b64decode(a)
                c = b.decode('utf-8')
            except Exception:
                return None
            return c

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password
        from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        elif not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        elif ":" not in decoded_base64_authorization_header:
            return (None, None)
        else:
            return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password
        """
        if user_email is None or user_pwd is None:
            return None
        elif not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        else:
            try:
                user = User.search({'email': user_email})
            except Exception:
                return None
            if len(user) == 0:
                return None
            elif not user[0].is_valid_password(user_pwd):
                return None
            else:
                return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """
        retrieves the User instance for a request
        """
        ath = self.authorization_header(request)
        hd = self.extract_base64_authorization_header(ath)
        hd_dcd = self.decode_base64_authorization_header(hd)
        user_crd = self.extract_user_credentials(hd_dcd)
        usr = self.user_object_from_credentials(user_crd[0], user_crd[1])
        return usr

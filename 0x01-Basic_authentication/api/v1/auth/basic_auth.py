#!/usr/bin/env python3
"""
Task 3: Auth class
"""
from flask import request
from api.v1.auth.auth import Auth
from typing import List, TypeVar


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

#!/usr/bin/env python3
"""
Task 3: Auth class
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """
    class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns false
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        else:
            for p in excluded_paths:
                if path.rstrip("/") == p.rstrip("/"):
                    return False
            return True

    def authorization_header(self, request=None) -> str:
        """
        Return None
        """
        if request is None:
            return None
        else:
            return request.headers.get("authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return None
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request
        """
        if request is None:
            return None
        return request.cookies.get(os.getenv("SESSION_NAME"))

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
    pass

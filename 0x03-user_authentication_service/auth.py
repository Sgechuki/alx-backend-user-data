#!/usr/bin/env python3
"""
Task 4: Hash password
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    hashes password
    """
    b = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(b, salt)
    return hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            pass
        hashed = _hash_password(password)
        user = self._db.add_user(email, hashed)
        return user

    def valid_login(self, email: str, password: str):
        """
        check the password
        """
        try:
            user = self._db.find_user_by(email=email)
            b = password.encode('utf-8')
            valid = bcrypt.checkpw(b, user.hashed_password)
        except NoResultFound:
            return False
        return valid

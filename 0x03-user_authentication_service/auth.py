#!/usr/bin/env python3
"""
Task 4: Hash password
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    hashes password
    """
    b = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(b, salt)
    return hash


def _generate_uuid() -> str:
    """
    return a string representation of a new UUID
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        check the password
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                b = password.encode('utf-8')
                valid = bcrypt.checkpw(b, user.hashed_password)
                return valid
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        find the user corresponding to the email
        generate a new UUID and store it in the database
        as the user’s session_id, then return the session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                ssn_id = _generate_uuid()
                self._db.update_user(user.id, session_id=ssn_id)
                return ssn_id
        except NoResultFound:
            pass
        return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        takes a single session_id string argument
        and returns the corresponding User or None
        """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                if user:
                    return user
            except NoResultFound:
                pass
        return None

    def destroy_session(self, user_id: int) -> None:
        """
        updates the corresponding user’s session ID to None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Find the user corresponding to the email
        If the user does not exist, raise a ValueError exception
        If it exists, generate a UUID and
        update the user’s reset_token database field
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset_tkn = _generate_uuid()
                self._db.update_user(user.id, reset_token=reset_tkn)
                return reset_tkn
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Used to update password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                hashed_pwd = _hash_password(password)
                self._db.update_user(user.id,
                                     hashed_password=hashed_pwd,
                                     reset_token=None)

        except ValueError:
            raise ValueError()
        return None

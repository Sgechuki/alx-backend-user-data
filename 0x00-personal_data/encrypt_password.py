#!/usr/bin/env python3
"""
Task 5: Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    returns a salted, hashed password
    which is a byte string
    """
    b = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(b, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validate that the provided password
    matches the hashed password
    """
    b = password.encode('utf-8')
    return bcrypt.checkpw(b, hashed_password)

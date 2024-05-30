#!/usr/bin/env python3
"""
Task 0: Regex-ing
"""
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    returns the log message obfuscated
    """
    for item in fields:
        message = re.sub(f'{item}=.*?{separator}',
                         f'{item}={redaction}{separator}',
                         message)
    return message

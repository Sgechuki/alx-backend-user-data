#!/usr/bin/env python3
"""
Task 0: Regex-ing
"""
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    returns the log message obfuscated
    """
    details = message.split(separator)[:-1]
    obf = []
    for detail in details:
        key, value = detail.split('=')
        if key in fields:
            text = key + "=" + redaction + separator
        else:
            text = detail + separator
        obf.append(text)
    return "".join(obf)

#!/usr/bin/env python3
"""module to handle authorization"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """takes password(string) and returns
        hashed_password
    """
    # first we have to encode string into bytes
    pwd_byte = password.encode('utf-8')

    # hash the encoded string
    hashed_pwd = bcrypt.hashpw(pwd_byte, bcrypt.gensalt())

    return hashed_pwd

#!/usr/bin/env python3
"""module to handle authorization"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """takes password(string) and returns
        hashed_password
    """
    # first we have to encode string into bytes
    pwd_byte = password.encode('utf-8')

    # hash the encoded string
    hashed_pwd = bcrypt.hashpw(pwd_byte, bcrypt.gensalt())

    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user to the db"""
        try:
            # find the user with the given email
            self._db.find_user_by(email=email)
        except NoResultFound:
            # if there is no user by passed email
            return self._db.add_user(email, _hash_password(password))

        else:
            # if user already exists in db
            raise ValueError(f"User {email} already exists")

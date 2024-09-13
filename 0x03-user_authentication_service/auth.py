#!/usr/bin/env python3
"""module to handle authorization"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
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


def _generate_uuid() -> str:
    """return a string repr"""
    id = uuid4()
    return str(id)


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

    def valid_login(self, email: str, password: str) -> bool:
        """validate the user"""
        try:
            # to find the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # but if the user does'nt exist
            return False

        # if user exist check if password is correct
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """_summary_"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            user.session_id = _generate_uuid()
            return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """find user by session id"""
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: int) -> None:
        """destroy session, update the user session to None"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        else:
            user.session_id = None
            return None

    def get_reset_password_token(self, email: str) -> str:
        """_summary_"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            user.reset_token = _generate_uuid()
            return user.reset_token

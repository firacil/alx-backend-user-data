#!/usr/bin/env python3
"""module for sessionauth"""
import uuid
from models.user import User
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """class SessionAuth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates session id for a user_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on session ID"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        # retrieve session id from the cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        # retrieve user id based on session id
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        # retrieve the user instance from db
        return User.get(user_id)

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True

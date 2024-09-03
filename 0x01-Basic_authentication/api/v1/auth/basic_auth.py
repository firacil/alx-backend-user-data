#!/usr/bin/env python3
"""class for basic auth"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """class basic auth inherits from auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 of Authorization header
        for Basic Authentication
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """returns the decoded value of base64string
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # attempt to decode the base64 string
            byte_str = base64.b64decode(base64_authorization_header)
            my_str = byte_str.decode('utf-8')
        except(TypeError, ValueError):
            # if decodeing fails, return None
            return None

        return my_str

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """returns the user email and password from
        Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        uname, pwd = decoded_base64_authorization_header.split(':', 1)

        return uname, pwd

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """returns the User instance based on his email and
        password
        """
        if not isinstance(user_email, str) or user_email is None:
            return None
        if not isinstance(user_pwd, str) or user_pwd is None:
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the
        User instance for a request
        """
        if request is None:
            return None

        # get the authorization header from the request
        auth_header = self.authorization_header(request)

        if auth_header is None:
            return None

        # extract base64 part from the authorization header
        base64_auth = self.extract_base64_authorization_header(auth_header)

        if base64_auth is None:
            return None

        # decode base64 authrization header
        decoded = self.decode_base64_authorization_header(base64_auth)

        if decoded is None:
            return None

        # extract credentials
        uemail, upwd = self.extract_user_credentials(decoded)
        if uemail is None or upwd is None:
            return None

        # get user object from credentials
        user = self.user_object_from_credentials(uemail, upwd)

        return user

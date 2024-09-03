#!/usr/bin/env python3
"""class for basic auth"""
import base64
from api.v1.auth.auth import Auth


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

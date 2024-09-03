#!/usr/bin/env python3
"""class for basic auth"""
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

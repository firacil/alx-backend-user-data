#!/usr/bin/env python3
"""class to manage api auth
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class to manage api authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return False"""
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == "":
            return True

        if path.endswith('/'):
            if path in excluded_paths:
                return False
            return True
        else:
            path = path + '/'
            if path in excluded_paths:
                return False
            return True

    def authorization_header(self, request=None) -> str:
        """returns None
        request will be flask request object
        """
        if request is None:
            return None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            return auth_header
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None
        request will be flask request object
        """
        return None

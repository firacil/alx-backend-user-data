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
        return False

    def authorization_header(self, request=None) -> str:
        """returns None
        request will be flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None
        request will be flask request object
        """
        return None

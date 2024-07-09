#!/usr/bin/env python3
"""
A module to apply authorization logic.
"""

from typing import List, TypeVar

from flask import request

User = TypeVar("User")


class Auth:
    """[TODO:description]"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False if path is in the list of excluded paths"""
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Add trailing slash for comparison
        if not path.endswith("/"):
            path += "/"

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """The Method is returning None for now"""
        return None

    def current_user(self, request=None) -> User:
        """The Method is returning None for now"""
        return None

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
        """The Method is returning False for now"""
        return False

    def authorization_header(self, request=None) -> str:
        """The Method is returning None for now"""
        return None

    def current_user(self, request=None) -> User:
        """The Method is returning None for now"""
        return None

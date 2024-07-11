#!/usr/bin/env python3
"""
This module applies session authentication logic.
"""
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    A class used to manage session-based user authentication.

    Attributes
    ----------
    user_id_by_session_id : dict
        A dictionary that maps session IDs (str) to user IDs (str).
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a new session for a user."""
        if user_id is None or not isinstance(user_id, str):
            return None

        gen_id = uuid4()
        self.user_id_by_session_id[str(gen_id)] = user_id
        return str(gen_id)

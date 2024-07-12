#!/usr/bin/env python3
"""
SessionDBAuth handles session authentication with a database.
"""

from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """A class used to handle session authentication with a database."""

    def create_session(self, user_id=None):
        """Creates a new session for a user and saves it in the database."""
        session_id = super().create_session(user_id)
        if session_id:
            UserSession(user_id=user_id, session_id=session_id).save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user ID associated with a session ID."""
        if session_id:
            user_id = super().user_id_for_session_id(session_id)
            return user_id
        return None

    def destroy_session(self, request=None):
        """Destroys a session based on the session ID from a request cookie."""
        if request:
            session_id = self.session_cookie(request)
            super().destroy_session(request)
            user_session = UserSession.search({"session_id": session_id})
            if user_session and user_session is not []:
                user_session[0].remove()
                return True
        return False

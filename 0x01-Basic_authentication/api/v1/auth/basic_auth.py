#!/usr/bin/env python3
"""
Implementation of Basic Authentication
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class inherits from Auth"""

    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """Extract the Base64 Authorization Header"""
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None

        return authorization_header.split(" ")[1]

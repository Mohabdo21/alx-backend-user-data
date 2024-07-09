#!/usr/bin/env python3
""" Module of Index views
"""
from flask import Response, abort, jsonify
from flask.typing import ResponseReturnValue

from api.v1.views import app_views


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status() -> Response:
    """GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats/", strict_slashes=False)
def stats() -> Response:
    """GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User

    stats = {}
    stats["users"] = User.count()
    return jsonify(stats)


@app_views.route("/unauthorized", strict_slashes=False)
def unauthorized() -> ResponseReturnValue:
    """GET /api/v1/unauthorized
    Return:
        - Unaithorized Error.
    """
    abort(401)

"""Python Flask API Auth0 integration example
"""

from tasteofnostalgia import APP
from os import environ as env

from dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify
from flask_cors import cross_origin
from authlib.integrations.flask_oauth2 import ResourceProtector
from .validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "dev-ukcv1nsl77121wun.us.auth0.com",
    "https://dev-ukcv1nsl77121wun.us.auth0.com/api/v2/"
)
require_auth.register_token_validator(validator)

@APP.route("/api/public")
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
def public():
    """No access token required."""
    response = (
        "Hello from a public endpoint! You don't need to be"
        " authenticated to see this."
    )
    return jsonify(message=response)


@APP.route("/api/private")
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
@require_auth(None)
def private():
    """A valid access token is required."""
    response = (
        "Hello from a private endpoint! You need to be"
        " authenticated to see this."
    )
    return jsonify(message=response)


@APP.route("/api/private-scoped")
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
@require_auth("read:messages")
def private_scoped():
    """A valid access token and scope are required."""
    response = (
        "Hello from a private endpoint! You need to be"
        " authenticated and have a scope of read:messages to see"
        " this."
    )
    return jsonify(message=response)
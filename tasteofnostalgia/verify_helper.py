from jose import jwt
from functools import wraps
from flask import Flask, request, jsonify, _request_ctx_stack

from six.moves.urllib.request import urlopen
import json
from typing import Dict

from tasteofnostalgia import AUTH0_DOMAIN, API_IDENTIFIER, ALGORITHMS
from flask_cors import cross_origin

class AuthError(Exception):
    """
    An AuthError is raised whenever the authentication failed.
    """
    def __init__(self, error: Dict[str, str], status_code: int):
        super().__init__()
        self.error = error
        self.status_code = status_code

def get_token_auth_header() -> str:
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                             "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    if len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    if len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "Authorization header must be"
                             " Bearer token"}, 401)

    token = parts[1]
    return token

def requires_auth(func):
    """Determines if the access token is valid
    """
    
    @wraps(func)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError as jwt_error:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Invalid header. "
                                "Use an RS256 signed JWT Access Token"}, 401) from jwt_error
        if unverified_header["alg"] == "HS256":
            raise AuthError({"code": "invalid_header",
                             "description":
                                 "Invalid header. "
                                 "Use an RS256 signed JWT Access Token"}, 401)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_IDENTIFIER,
                    issuer="https://" + AUTH0_DOMAIN + "/"
                )
            except jwt.ExpiredSignatureError as expired_sign_error:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401) from expired_sign_error
            except jwt.JWTClaimsError as jwt_claims_error:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    " please check the audience and issuer"}, 401) from jwt_claims_error
            except Exception as exc:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401) from exc

            _request_ctx_stack.top.current_user = payload
            return func(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 401)

    return decorated

# Function to validate and decode the JWT
def get_user_id_from_token(token):
    try:
        # Decode the token using Auth0 public key
        decoded_token = jwt.decode(
            token,
            auth0_public_key(),
            algorithms=ALGORITHMS,
            audience=API_IDENTIFIER,
            issuer=f'https://{AUTH0_DOMAIN}/'
        )

        # Extract user ID from the decoded token
        user_id = decoded_token.get('sub')
        return user_id
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    # except jwt.InvalidTokenError:
        # return None  # Token is invalid

# Function to fetch Auth0 public key
def auth0_public_key():
    # Fetch Auth0 public key from jwks endpoint
    # You may need to implement this based on Auth0 documentation
    # Example: https://auth0.com/docs/quickstart/backend/python/01-authorization
    # Return the public key associated with the Auth0 API identifier
    # Ensure you cache the public key for better performance
    # ...
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    return jwks

# Your API endpoint requiring authentication

# @APP.route('/secure-endpoint', methods=['GET'])
# @cross_origin(headers=["Access-Control-Allow-Origin", "*"])
def get_user_id():
    # Get the Authorization header from the request
    authorization_header = request.headers.get('Authorization')

    if not authorization_header:
        return jsonify({"message": "Authorization header is missing"}), 401

    # Extract the token from the header
    token = authorization_header.split()[1]

    # Get the user ID from the token
    user_id = get_user_id_from_token(token)

    return user_id
    # if user_id:
    #     return jsonify({"user_id": user_id, "message": "Access granted"})
    # else:
    #     return jsonify({"message": "Invalid or expired token"}), 401
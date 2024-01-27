from jose import jwt
from flask import Flask, request, jsonify

from six.moves.urllib.request import urlopen
import json

from tasteofnostalgia import APP
from flask_cors import cross_origin

# Auth0 configuration
AUTH0_DOMAIN="dev-ukcv1nsl77121wun.us.auth0.com"
API_IDENTIFIER="https://dev-ukcv1nsl77121wun.us.auth0.com/api/v2/"
ALGORITHMS = ["RS256"]  # The algorithm used to sign the token

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

@APP.route('/secure-endpoint', methods=['GET'])
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
def secure_endpoint():
    # Get the Authorization header from the request
    authorization_header = request.headers.get('Authorization')

    if not authorization_header:
        return jsonify({"message": "Authorization header is missing"}), 401

    # Extract the token from the header
    token = authorization_header.split()[1]

    # Get the user ID from the token
    user_id = get_user_id_from_token(token)

    if user_id:
        return jsonify({"user_id": user_id, "message": "Access granted"})
    else:
        return jsonify({"message": "Invalid or expired token"}), 401

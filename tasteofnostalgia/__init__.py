from functools import wraps
import json
from os import environ as env
from typing import Dict

from six.moves.urllib.request import urlopen

from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify, _request_ctx_stack, Response
from flask_cors import cross_origin
from jose import jwt

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
API_IDENTIFIER = env.get("API_IDENTIFIER")
ALGORITHMS = ["RS256"]
APP = Flask(__name__)

if not AUTH0_DOMAIN or not API_IDENTIFIER:
    print("WARNING: AUTH0_DOMAIN or API_IDENTIFIER not specified in .env")

from tasteofnostalgia import routes, server, verify#, auth0
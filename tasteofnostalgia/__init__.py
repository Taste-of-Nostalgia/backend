from functools import wraps
import json, certifi
from os import environ as env
from typing import Dict

from six.moves.urllib.request import urlopen

from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify, _request_ctx_stack, Response
from flask_cors import cross_origin
from jose import jwt

from pymongo import MongoClient

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
API_IDENTIFIER = env.get("API_IDENTIFIER")
ALGORITHMS = ["RS256"]
APP = Flask(__name__)

client = MongoClient("mongodb+srv://onlineuser:$k25DsumFLfXEtF@discord-bot-online-judg.7gm4i.mongodb.net/", tlsCAFile=certifi.where())['taste-of-nostalgia']
db = client['taste-of-nostalgia']
users = client['users']
food_collection = client['food']

from tasteofnostalgia import form, server, verify